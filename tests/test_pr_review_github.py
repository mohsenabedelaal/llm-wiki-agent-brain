"""Tests for finding filters and GitHub review payload shape."""

from __future__ import annotations

from pr_review.github_post import build_review_payload, filter_findings, finding_to_review_comment
from pr_review.types import CommentAnchor, Finding, ReviewResult


def _anchors() -> set[CommentAnchor]:
    return {
        CommentAnchor("wiki_agent/agent.py", 18, "RIGHT"),
        CommentAnchor("wiki_agent/agent.py", 19, "RIGHT"),
        CommentAnchor("pr_review/diff.py", 4, "LEFT"),
    }


def test_drops_comments_not_in_diff() -> None:
    findings = [
        Finding(
            path="wiki_agent/agent.py",
            line=18,
            side="RIGHT",
            severity="should-fix",
            body="Pin the model.",
            doc_path="docs/tech/google-adk/agents.md",
        ),
        Finding(
            path="wiki_agent/agent.py",
            line=99,
            side="RIGHT",
            severity="nit",
            body="Not in the hunk.",
            doc_path="docs/tech/google-adk/agents.md",
        ),
    ]
    kept, dropped = filter_findings(findings, _anchors())
    assert len(kept) == 1
    assert kept[0].line == 18
    assert len(dropped) == 1
    assert dropped[0].line == 99


def test_file_level_comment_kept_for_changed_path() -> None:
    findings = [
        Finding(
            path="wiki_agent/agent.py",
            line=None,
            severity="should-fix",
            body="Missing tool sandbox note.",
            doc_path="docs/tech/google-adk/tools.md",
        )
    ]
    kept, dropped = filter_findings(findings, _anchors())
    assert dropped == []
    assert kept[0].is_file_level
    payload = finding_to_review_comment(kept[0])
    assert payload["subject_type"] == "file"
    assert "line" not in payload


def test_review_payload_requests_changes_on_blocker() -> None:
    review = ReviewResult(
        summary="One blocker versus ADK tool docs.",
        findings=[
            Finding(
                path="wiki_agent/agent.py",
                line=18,
                side="RIGHT",
                severity="blocker",
                body="Tools must return JSON-serializable dicts.",
                doc_path="docs/tech/google-adk/tools.md",
                section="Function tools",
            )
        ],
    )
    payload = build_review_payload("abc123", review)
    assert payload["commit_id"] == "abc123"
    assert payload["event"] == "REQUEST_CHANGES"
    assert payload["comments"][0]["path"] == "wiki_agent/agent.py"
    assert payload["comments"][0]["line"] == 18
    assert payload["comments"][0]["side"] == "RIGHT"
    assert "blocker" in payload["comments"][0]["body"]
    assert "docs/tech/google-adk/tools.md" in payload["comments"][0]["body"]


def test_review_payload_comments_when_no_blockers() -> None:
    review = ReviewResult(
        summary="Nits only.",
        findings=[
            Finding(
                path="wiki_agent/agent.py",
                line=19,
                side="RIGHT",
                severity="nit",
                body="Consider a shorter description.",
                doc_path="docs/tech/google-adk/agents.md",
            )
        ],
    )
    payload = build_review_payload("def456", review)
    assert payload["event"] == "COMMENT"
    assert len(payload["comments"]) == 1

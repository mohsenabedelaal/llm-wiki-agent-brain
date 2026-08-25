"""Tests for docs/tech loading, Gemini JSON parse, and CLI dry-run."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pr_review import __main__ as cli_mod
from pr_review.docs_loader import _display_docs_root, load_tech_docs
from pr_review.gemini_review import parse_model_json
from pr_review.types import Finding, ReviewResult

REPO_DOCS = Path("docs") / "tech"


def test_load_tech_docs_prefers_adk_when_agent_files_change() -> None:
    docs_root = cli_mod.resolve_docs_root(REPO_DOCS)
    docs = load_tech_docs(
        docs_root,
        changed_paths=["wiki_agent/agent.py", "wiki_agent/tools/vault.py"],
        diff_text="from google.adk.agents import Agent",
    )
    assert docs
    assert any("google-adk" in d.rel_path for d in docs)
    assert all(not Path(d.rel_path).is_absolute() for d in docs)
    assert all(":" not in d.rel_path.split("/")[0] for d in docs)  # no drive letter
    top = docs[0]
    assert top.source_id == "google-adk"
    assert top.score > 0


def test_resolve_docs_root_prefers_cwd_relative(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    docs = tmp_path / "docs" / "tech"
    docs.mkdir(parents=True)
    (docs / "manifest.yaml").write_text("sources: []\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    resolved = cli_mod.resolve_docs_root(Path("docs") / "tech")
    assert resolved == docs.resolve()
    assert _display_docs_root(resolved) == "docs/tech"


def test_parse_model_json_strips_fence_and_caps_findings() -> None:
    findings = [
        {
            "path": "wiki_agent/agent.py",
            "line": 18,
            "side": "RIGHT",
            "severity": "should-fix",
            "body": "Expose root_agent.",
            "doc_path": "docs/tech/google-adk/agents.md",
            "section": "Agents",
        }
        for _ in range(25)
    ]
    fenced = "```json\n" + json.dumps({"summary": "Too many nits.", "findings": findings}) + "\n```"
    result = parse_model_json(fenced)
    assert result.summary == "Too many nits."
    assert len(result.findings) == 20
    assert result.findings[0].section == "Agents"


def test_dry_run_prints_json_without_posting(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from pr_review import __main__ as cli

    monkeypatch.setattr(
        cli,
        "fetch_pull_request",
        lambda *a, **k: {
            "title": "Add review",
            "body": "n/a",
            "draft": False,
            "head": {"sha": "deadbeef"},
        },
    )
    monkeypatch.setattr(
        cli,
        "fetch_pull_files",
        lambda *a, **k: [
            {
                "filename": "wiki_agent/agent.py",
                "status": "modified",
                "patch": "@@ -1,1 +1,1 @@\n-old\n+new\n",
            }
        ],
    )
    monkeypatch.setattr(
        cli,
        "generate_review",
        lambda **k: ReviewResult(
            summary="One nit versus ADK docs.",
            findings=[
                Finding(
                    path="wiki_agent/agent.py",
                    line=1,
                    side="RIGHT",
                    severity="nit",
                    body="Keep root_agent public.",
                    doc_path="docs/tech/google-adk/agents.md",
                )
            ],
        ),
    )

    posted: list[object] = []
    monkeypatch.setattr(cli, "submit_review", lambda *a, **k: posted.append(a) or {})

    rc = cli.run(["--pr", "7", "--repo", "acme/llm-wiki-agent-brain", "--dry-run"])
    assert rc == 0
    assert posted == []
    payload = json.loads(capsys.readouterr().out)
    assert payload["commit_id"] == "deadbeef"
    assert payload["event"] == "COMMENT"
    assert payload["comments"][0]["line"] == 1
    assert payload["comments"][0]["path"] == "wiki_agent/agent.py"

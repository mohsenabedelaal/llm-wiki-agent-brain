"""Tests for docs loading, Gemini JSON parse, context helpers, and CLI dry-run."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pr_review import __main__ as cli_mod
from pr_review.context import format_pr_file_context, load_project_conventions
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


def test_load_tech_docs_missing_dir_returns_empty(tmp_path: Path) -> None:
    assert load_tech_docs(tmp_path / "missing", changed_paths=[]) == []


def test_resolve_docs_root_prefers_cwd_relative(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
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
            "category": "api-docs",
            "body": "Expose root_agent.",
            "doc_path": "docs/tech/google-adk/agents.md",
            "section": "Agents",
        }
        for _ in range(25)
    ]
    fenced = (
        "```json\n"
        + json.dumps({"summary": "Too many nits.", "findings": findings})
        + "\n```"
    )
    result = parse_model_json(fenced)
    assert result.summary == "Too many nits."
    assert len(result.findings) == 20
    assert result.findings[0].section == "Agents"
    assert result.findings[0].category == "api-docs"


def test_parse_model_json_allows_null_doc_path() -> None:
    payload = {
        "summary": "Regression risk.",
        "findings": [
            {
                "path": "src/api.py",
                "line": 10,
                "side": "RIGHT",
                "severity": "blocker",
                "category": "regression",
                "body": "Return type changed without updating callers.",
                "doc_path": None,
            }
        ],
    }
    result = parse_model_json(json.dumps(payload))
    assert result.findings[0].doc_path is None
    assert result.findings[0].category == "regression"


def test_conventions_and_changed_files_are_relative(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "CONTRIBUTING.md").write_text("# Contributing\nUse tests.\n", encoding="utf-8")
    src = tmp_path / "src"
    src.mkdir()
    (src / "main.py").write_text("print('hi')\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    conventions = load_project_conventions(tmp_path)
    assert "CONTRIBUTING.md" in conventions
    assert "Use tests" in conventions
    files = format_pr_file_context(
        [{"filename": "src/main.py", "status": "modified", "additions": 1, "deletions": 0}],
        tmp_path,
    )
    assert "### src/main.py" in files
    assert "print('hi')" in files
    assert "`src/main.py`" in files


def test_format_pr_file_context_includes_before_after(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("new = 2\n", encoding="utf-8")

    def fetch(path: str, ref: str) -> str | None:
        if path == "app.py" and ref == "base":
            return "old = 1\n"
        return None

    block = format_pr_file_context(
        [{"filename": "app.py", "status": "modified", "additions": 1, "deletions": 1}],
        tmp_path,
        base_sha="base",
        head_sha="head",
        fetch_at_ref=fetch,
    )
    assert "Before (base)" in block
    assert "old = 1" in block
    assert "After (head)" in block
    assert "new = 2" in block
    assert "`app.py`" in block


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
            "base": {"sha": "cafebabe"},
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
                    category="conventions",
                    body="Keep root_agent public.",
                    doc_path="docs/tech/google-adk/agents.md",
                )
            ],
        ),
    )

    posted: list[object] = []
    monkeypatch.setattr(cli, "submit_review", lambda *a, **k: posted.append(a) or {})
    monkeypatch.setattr(cli, "fetch_file_at_ref", lambda *a, **k: None)

    rc = cli.run(["--pr", "7", "--repo", "acme/llm-wiki-agent-brain", "--dry-run"])
    assert rc == 0
    assert posted == []
    payload = json.loads(capsys.readouterr().out)
    assert payload["commit_id"] == "deadbeef"
    assert payload["event"] == "COMMENT"
    assert payload["comments"][0]["line"] == 1
    assert payload["comments"][0]["path"] == "wiki_agent/agent.py"

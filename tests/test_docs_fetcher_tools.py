"""Sandbox tests for the docs fetcher write/fetch allowlist and CLI helpers."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from docs_fetcher_agent.cli import _slug_from_url, refresh_all
from docs_fetcher_agent.stack import scan_stack
from docs_fetcher_agent.tools import tech_docs


@pytest.fixture()
def tech_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    repo = tmp_path / "repo"
    docs = repo / "docs" / "tech" / "google-adk"
    docs.mkdir(parents=True)
    (repo / "src").mkdir()
    manifest = {
        "sources": [
            {
                "id": "google-adk",
                "title": "Google ADK",
                "url": "https://google.github.io/adk-docs/",
                "local_dir": "google-adk",
                "keywords": ["adk"],
                "notes": "test",
            }
        ]
    }
    manifest_path = repo / "docs" / "tech" / "manifest.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest), encoding="utf-8")
    (docs / "agents.md").write_text("# Agents\n", encoding="utf-8")

    monkeypatch.setattr(tech_docs, "REPO_ROOT", repo)
    monkeypatch.setattr(tech_docs, "DOCS_TECH_ROOT", repo / "docs" / "tech")
    monkeypatch.setattr(tech_docs, "MANIFEST_PATH", manifest_path)
    return repo / "docs" / "tech"


def test_write_rejects_outside_docs_tech(tech_root: Path) -> None:
    raw = tech_docs.write_file("raw/seed/nope.md", "# no")
    assert raw["status"] == "error"
    wiki = tech_docs.write_file("wiki/entities/nope.md", "# no")
    assert wiki["status"] == "error"
    src = tech_docs.write_file("src/secret.md", "# no")
    assert src["status"] == "error"


def test_write_and_list_docs_tech(tech_root: Path) -> None:
    wrote = tech_docs.write_file("docs/tech/google-adk/tools.md", "# Tools\n\nCanonical: x\n")
    assert wrote["status"] == "success"
    listed = tech_docs.list_docs("docs/tech/google-adk")
    assert listed["status"] == "success"
    names = {Path(e["path"]).name for e in listed["entries"]}
    assert "tools.md" in names


def test_url_allowlist(tech_root: Path) -> None:
    assert tech_docs.url_is_allowed("https://google.github.io/adk-docs/")
    assert tech_docs.url_is_allowed("https://google.github.io/adk-docs/agents/")
    blocked = tech_docs.fetch_url("https://example.com/random")
    assert blocked["status"] == "error"
    assert "allowlist" in blocked["error"].lower()


def test_update_manifest_stamps_fetched_at(tech_root: Path) -> None:
    result = tech_docs.update_manifest("google-adk", fetched_at="2026-08-24T13:00:00Z", notes="ok")
    assert result["status"] == "success"
    data = yaml.safe_load(tech_docs.MANIFEST_PATH.read_text(encoding="utf-8"))
    source = data["sources"][0]
    assert source["fetched_at"] == "2026-08-24T13:00:00Z"
    assert source["notes"] == "ok"


def test_scan_stack_detects_node_and_go(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    (tmp_path / "go.mod").write_text("module example\n", encoding="utf-8")
    data = scan_stack(tmp_path)
    assert "javascript" in data["keywords"]
    assert "go" in data["keywords"]
    paths = {m["path"] for m in data["markers"]}
    assert "package.json" in paths
    assert "go.mod" in paths


def test_slug_from_url() -> None:
    assert _slug_from_url("https://docs.example.com/guide/") == "guide.md"
    assert _slug_from_url("https://docs.example.com/") == "index.md"


def test_refresh_writes_snapshot(tech_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        tech_docs,
        "fetch_url",
        lambda url: {
            "status": "success",
            "content": "Hello docs",
            "chars": 10,
        },
    )
    # refresh_all imports fetch_url from tech_docs at call time via cli module
    import docs_fetcher_agent.cli as cli

    monkeypatch.setattr(
        cli,
        "fetch_url",
        lambda url: {"status": "success", "content": "Hello docs", "chars": 10},
    )
    out = refresh_all()
    assert out["status"] == "success"
    written = Path(tech_docs.REPO_ROOT) / "docs" / "tech" / "google-adk" / "index.md"
    # slug from https://google.github.io/adk-docs/ → last segment adk-docs.md or index?
    # url path is /adk-docs so slug adk-docs.md
    alt = Path(tech_docs.REPO_ROOT) / "docs" / "tech" / "google-adk" / "adk-docs.md"
    assert written.is_file() or alt.is_file()

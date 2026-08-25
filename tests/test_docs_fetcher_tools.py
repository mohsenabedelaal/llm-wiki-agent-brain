"""Sandbox tests for the docs_fetcher_agent write/fetch allowlist."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from docs_fetcher_agent.tools import tech_docs


@pytest.fixture()
def tech_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    repo = tmp_path / "repo"
    docs = repo / "docs" / "tech" / "google-adk"
    docs.mkdir(parents=True)
    (repo / "raw").mkdir()
    (repo / "wiki").mkdir()
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
    monkeypatch.setattr(tech_docs, "RAW_ROOT", repo / "raw")
    monkeypatch.setattr(tech_docs, "WIKI_ROOT", repo / "wiki")
    return repo / "docs" / "tech"


def test_write_rejects_raw_and_wiki(tech_root: Path) -> None:
    raw = tech_docs.write_file("raw/seed/nope.md", "# no")
    assert raw["status"] == "error"
    wiki = tech_docs.write_file("wiki/entities/nope.md", "# no")
    assert wiki["status"] == "error"


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

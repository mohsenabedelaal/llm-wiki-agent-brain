"""Tests for path-safe vault tools and PDF extraction."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.build_sample_pdf import write_sample_manual
from wiki_agent.tools import vault


@pytest.fixture()
def sample_pdf(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a tiny text PDF under a fake repo raw/manuals and re-root vault helpers."""
    repo = tmp_path / "repo"
    raw_manuals = repo / "raw" / "manuals"
    wiki = repo / "wiki"
    raw_manuals.mkdir(parents=True)
    wiki.mkdir(parents=True)
    (wiki / "index.md").write_text("# Index\n", encoding="utf-8")
    (wiki / "log.md").write_text("# Log\n", encoding="utf-8")
    (wiki / "hot.md").write_text("# Hot\n", encoding="utf-8")

    pdf_path = write_sample_manual(raw_manuals / "sample-ac-manual.pdf")

    monkeypatch.setattr(vault, "REPO_ROOT", repo)
    monkeypatch.setattr(vault, "RAW_ROOT", repo / "raw")
    monkeypatch.setattr(vault, "WIKI_ROOT", wiki)
    monkeypatch.setattr(vault, "INDEX_PATH", wiki / "index.md")
    monkeypatch.setattr(vault, "LOG_PATH", wiki / "log.md")
    monkeypatch.setattr(vault, "HOT_PATH", wiki / "hot.md")
    return pdf_path


def test_list_vault_top_level(sample_pdf: Path) -> None:
    result = vault.list_vault("")
    assert result["status"] == "success"
    names = {e["path"] for e in result["entries"]}
    assert "raw" in names
    assert "wiki" in names


def test_write_rejects_raw(sample_pdf: Path) -> None:
    result = vault.write_file("raw/seed/hack.md", "nope")
    assert result["status"] == "error"
    assert "forbidden" in result["error"].lower() or "immutable" in result["error"].lower()


def test_write_rejects_escape(sample_pdf: Path) -> None:
    result = vault.write_file("../outside.md", "nope")
    assert result["status"] == "error"


def test_write_and_read_wiki(sample_pdf: Path) -> None:
    content = "---\ntype: entity\ntitle: AHU-3\n---\n\n# AHU-3\n\n**Summary**: Test.\n"
    wrote = vault.write_file("wiki/entities/ahu-3.md", content)
    assert wrote["status"] == "success"
    read = vault.read_file("wiki/entities/ahu-3.md")
    assert read["status"] == "success"
    assert "AHU-3" in read["content"]


def test_append_log_and_update_hot(sample_pdf: Path) -> None:
    log = vault.append_log("## 2026-07-29 — test\n\n- hello\n")
    assert log["status"] == "success"
    hot = vault.update_hot("# Hot\n\nFresh cache.\n")
    assert hot["status"] == "success"
    assert "Fresh cache" in vault.read_file("wiki/hot.md")["content"]


def test_read_pdf_extracts_specs(sample_pdf: Path) -> None:
    result = vault.read_pdf("raw/manuals/sample-ac-manual.pdf")
    assert result["status"] == "success"
    assert result["pages_total"] >= 1
    assert "16.5 kW" in result["content"]
    assert "AHU-3" in result["content"]


def test_read_pdf_rejects_non_pdf(sample_pdf: Path) -> None:
    vault.write_file("wiki/notes.md", "x")
    result = vault.read_pdf("wiki/notes.md")
    assert result["status"] == "error"


def test_agent_exports_root_agent() -> None:
    from wiki_agent.agent import root_agent

    assert root_agent.name == "wiki_agent"
    assert root_agent.tools

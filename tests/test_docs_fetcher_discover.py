"""Tests for inferring docs sources from project dependency files."""

from __future__ import annotations

from pathlib import Path

from docs_fetcher_agent.discover import (
    collect_direct_dependencies,
    parse_go_mod,
    parse_package_json,
    parse_requirements_txt,
    propose_sources,
    resolve_docs_url,
)
from docs_fetcher_agent.tools import tech_docs


def test_parse_requirements_skips_flags() -> None:
    text = """
# comment
google-adk>=1.0.0
pypdf>=5.0.0
-e ./local
git+https://example.com/x.git
"""
    names = parse_requirements_txt(text)
    assert names == ["google-adk", "pypdf"]


def test_parse_package_json_deps() -> None:
    names = parse_package_json(
        '{"dependencies": {"react": "18.0.0"}, "devDependencies": {"vitest": "1.0.0"}}'
    )
    assert names == ["react", "vitest"]


def test_parse_go_mod_skips_indirect() -> None:
    text = """
module example.com/app

require (
    github.com/gin-gonic/gin v1.9.0
    github.com/foo/bar v1.0.0 // indirect
)
"""
    assert parse_go_mod(text) == ["github.com/gin-gonic/gin"]


def test_collect_from_requirements(tmp_path: Path) -> None:
    (tmp_path / "requirements.txt").write_text("pytest>=8\n", encoding="utf-8")
    deps = collect_direct_dependencies(tmp_path)
    assert any(d["name"] == "pytest" and d["ecosystem"] == "python" for d in deps)


def test_resolve_uses_well_known_without_network() -> None:
    assert resolve_docs_url("python", "pytest", fetch_json=lambda url: None)
    assert "docs.pytest.org" in (resolve_docs_url("python", "pytest") or "")


def test_propose_uses_pypi_project_urls(tmp_path: Path) -> None:
    (tmp_path / "requirements.txt").write_text("obscure-lib==1.0\n", encoding="utf-8")

    def fake_json(url: str) -> dict | None:
        if "obscure-lib" in url:
            return {
                "info": {
                    "project_urls": {"Documentation": "https://obscure.readthedocs.io/en/stable/"}
                }
            }
        return None

    proposals = propose_sources(tmp_path, fetch_json=fake_json)
    assert len(proposals) == 1
    assert proposals[0]["url"] == "https://obscure.readthedocs.io/en/stable/"
    assert proposals[0]["id"].startswith("python-")


def test_merge_does_not_overwrite_existing(tmp_path: Path, monkeypatch) -> None:
    docs = tmp_path / "docs" / "tech"
    docs.mkdir(parents=True)
    manifest = docs / "manifest.yaml"
    manifest.write_text(
        "sources:\n- id: python-pytest\n  url: https://docs.pytest.org/en/stable/\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(tech_docs, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(tech_docs, "DOCS_TECH_ROOT", docs)
    monkeypatch.setattr(tech_docs, "MANIFEST_PATH", manifest)
    result = tech_docs.merge_manifest_sources(
        [
            {
                "id": "python-pytest",
                "title": "pytest",
                "url": "https://docs.pytest.org/en/stable/",
                "local_dir": "python-pytest",
                "keywords": ["pytest"],
            },
            {
                "id": "python-httpx",
                "title": "httpx",
                "url": "https://www.python-httpx.org/",
                "local_dir": "python-httpx",
                "keywords": ["httpx"],
            },
        ]
    )
    assert result["status"] == "success"
    assert "python-httpx" in result["added"]
    assert "python-pytest" in result["skipped_existing"]

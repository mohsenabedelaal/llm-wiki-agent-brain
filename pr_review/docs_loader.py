"""Load docs/tech markdown and budget it against changed PR files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_DOCS_BUDGET = 40_000


@dataclass
class TechDoc:
    rel_path: str
    source_id: str
    title: str
    url: str
    content: str
    score: int = 0


def _display_docs_root(docs_root: Path) -> str:
    """Return a portable relative display path for citations (never drive-absolute)."""
    resolved = docs_root.resolve()
    for base in (Path.cwd().resolve(),):
        try:
            return resolved.relative_to(base).as_posix()
        except ValueError:
            continue
    # Fall back to the last path segments (e.g. docs/tech) rather than C:\...
    parts = resolved.parts
    if len(parts) >= 2 and parts[-2].lower() == "docs":
        return f"{parts[-2]}/{parts[-1]}"
    return parts[-1]


def load_manifest(docs_root: Path) -> dict[str, Any]:
    path = docs_root / "manifest.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"Missing manifest under {docs_root.as_posix()}/manifest.yaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict) or not data.get("sources"):
        raise ValueError("manifest.yaml must contain a sources list")
    return data


def _keywords_for(source: dict[str, Any]) -> list[str]:
    raw = source.get("keywords") or []
    return [str(k).lower() for k in raw]


def _score_source(source: dict[str, Any], changed_paths: list[str], diff_text: str) -> int:
    haystack = " ".join(changed_paths).lower() + "\n" + diff_text.lower()
    score = 0
    source_id = str(source.get("id") or "").lower()
    local_dir = str(source.get("local_dir") or "").lower()
    if source_id and source_id in haystack:
        score += 8
    if local_dir and local_dir in haystack:
        score += 4
    for kw in _keywords_for(source):
        if kw and kw.lower() in haystack:
            score += 3
    return score


def load_tech_docs(
    docs_root: Path,
    changed_paths: list[str],
    diff_text: str = "",
    budget_chars: int = DEFAULT_DOCS_BUDGET,
) -> list[TechDoc]:
    """Return scored, budgeted markdown docs. Higher-scoring stacks first."""
    manifest = load_manifest(docs_root)
    docs: list[TechDoc] = []
    for source in manifest["sources"]:
        local_dir = str(source.get("local_dir") or source.get("id") or "")
        folder = docs_root / local_dir
        if not folder.is_dir():
            continue
        score = _score_source(source, changed_paths, diff_text)
        docs_prefix = _display_docs_root(docs_root)
        for md in sorted(folder.rglob("*.md")):
            rel = md.relative_to(docs_root).as_posix()
            docs.append(
                TechDoc(
                    rel_path=f"{docs_prefix}/{rel}",
                    source_id=str(source.get("id") or local_dir),
                    title=str(source.get("title") or local_dir),
                    url=str(source.get("url") or ""),
                    content=md.read_text(encoding="utf-8", errors="replace"),
                    score=score,
                )
            )
    docs.sort(key=lambda d: (-d.score, d.rel_path))
    return _budget(docs, budget_chars)


def _budget(docs: list[TechDoc], budget_chars: int) -> list[TechDoc]:
    out: list[TechDoc] = []
    used = 0
    for doc in docs:
        if used >= budget_chars:
            break
        remaining = budget_chars - used
        content = doc.content
        if len(content) > remaining:
            content = content[:remaining] + "\n\n[truncated]\n"
        out.append(
            TechDoc(
                rel_path=doc.rel_path,
                source_id=doc.source_id,
                title=doc.title,
                url=doc.url,
                content=content,
                score=doc.score,
            )
        )
        used += len(content)
    return out


def format_docs_for_prompt(docs: list[TechDoc]) -> str:
    if not docs:
        return "(no tech docs loaded — review against general senior-engineer practice only, and say so.)"
    parts: list[str] = []
    for doc in docs:
        parts.append(
            f"### {doc.rel_path}  (source: {doc.source_id}, {doc.url})\n\n{doc.content.strip()}\n"
        )
    return "\n".join(parts)

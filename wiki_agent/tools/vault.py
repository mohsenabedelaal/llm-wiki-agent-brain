"""Path-safe vault I/O tools rooted at the repository root.

Rules:
- All paths must resolve under the repo root.
- Writes are allowed only under wiki/.
- raw/ is read-only.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pypdf import PdfReader

# repo root = parents[2] from wiki_agent/tools/vault.py
REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = REPO_ROOT / "raw"
WIKI_ROOT = REPO_ROOT / "wiki"
INDEX_PATH = WIKI_ROOT / "index.md"
LOG_PATH = WIKI_ROOT / "log.md"
HOT_PATH = WIKI_ROOT / "hot.md"

MAX_READ_CHARS = 200_000
MAX_PDF_PAGES = 80


def _ok(**payload: Any) -> dict[str, Any]:
    return {"status": "success", **payload}


def _err(message: str, **payload: Any) -> dict[str, Any]:
    return {"status": "error", "error": message, **payload}


def _resolve(path: str) -> Path:
    """Resolve a vault-relative path and ensure it stays under REPO_ROOT."""
    clean = path.replace("\\", "/").lstrip("/")
    candidate = (REPO_ROOT / clean).resolve()
    try:
        candidate.relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"Path escapes vault root: {path}") from exc
    return candidate


def _rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def list_vault(path: str = "") -> dict[str, Any]:
    """List files and directories under raw/ or wiki/ (or repo-relative path).

    Args:
        path: Relative path from vault root. Empty lists top-level raw/ and wiki/.
    """
    try:
        if not path or path in (".", "/"):
            entries = []
            for name in ("raw", "wiki"):
                p = REPO_ROOT / name
                if p.exists():
                    entries.append(
                        {
                            "path": name,
                            "type": "dir",
                            "children": sorted(
                                c.name for c in p.iterdir() if not c.name.startswith(".")
                            ),
                        }
                    )
            return _ok(entries=entries)

        target = _resolve(path)
        if not target.exists():
            return _err(f"Path not found: {path}")
        if target.is_file():
            return _ok(
                entries=[
                    {
                        "path": _rel(target),
                        "type": "file",
                        "size_bytes": target.stat().st_size,
                    }
                ]
            )

        entries = []
        for child in sorted(target.iterdir(), key=lambda p: p.name.lower()):
            if child.name.startswith(".") and child.name != ".gitkeep":
                continue
            if child.name == ".gitkeep":
                continue
            entries.append(
                {
                    "path": _rel(child),
                    "type": "dir" if child.is_dir() else "file",
                    "size_bytes": child.stat().st_size if child.is_file() else None,
                }
            )
        return _ok(path=_rel(target), entries=entries)
    except ValueError as exc:
        return _err(str(exc))
    except OSError as exc:
        return _err(f"OS error: {exc}")


def read_file(path: str) -> dict[str, Any]:
    """Read a text/markdown file under the vault (raw/ or wiki/).

    Args:
        path: Relative path to a text file (e.g. raw/seed/foo.md or wiki/index.md).
    """
    try:
        target = _resolve(path)
        if not target.exists():
            return _err(f"File not found: {path}")
        if not target.is_file():
            return _err(f"Not a file: {path}")
        if target.suffix.lower() == ".pdf":
            return _err(
                "Use read_pdf for PDF files.",
                path=_rel(target),
            )
        text = target.read_text(encoding="utf-8", errors="replace")
        truncated = False
        if len(text) > MAX_READ_CHARS:
            text = text[:MAX_READ_CHARS]
            truncated = True
        return _ok(path=_rel(target), content=text, truncated=truncated, chars=len(text))
    except ValueError as exc:
        return _err(str(exc))
    except OSError as exc:
        return _err(f"OS error: {exc}")


def read_pdf(path: str, max_pages: int = MAX_PDF_PAGES) -> dict[str, Any]:
    """Extract text from a PDF under raw/ (manuals or reports).

    Args:
        path: Relative path to a PDF (e.g. raw/manuals/ahu-om.pdf).
        max_pages: Maximum pages to extract (default 80).
    """
    try:
        target = _resolve(path)
        if not target.exists():
            return _err(f"File not found: {path}")
        if not target.is_file():
            return _err(f"Not a file: {path}")
        if target.suffix.lower() != ".pdf":
            return _err("read_pdf only accepts .pdf files. Use read_file for markdown.")
        if not _is_under(target, RAW_ROOT) and not _is_under(target, WIKI_ROOT):
            return _err("PDF must be under raw/ or wiki/.")

        reader = PdfReader(str(target))
        total_pages = len(reader.pages)
        limit = max(1, min(int(max_pages), MAX_PDF_PAGES, total_pages))
        pages: list[str] = []
        empty_pages = 0
        for i in range(limit):
            page_text = reader.pages[i].extract_text() or ""
            if not page_text.strip():
                empty_pages += 1
            pages.append(f"--- page {i + 1} ---\n{page_text}")
        content = "\n\n".join(pages)
        truncated = total_pages > limit
        if len(content) > MAX_READ_CHARS:
            content = content[:MAX_READ_CHARS]
            truncated = True

        caveats: list[str] = []
        if empty_pages:
            caveats.append(
                f"{empty_pages} of {limit} extracted pages had little/no text "
                "(possible scanned PDF; no OCR in v1)."
            )
        if truncated:
            caveats.append("Content truncated by page or character limit.")

        return _ok(
            path=_rel(target),
            content=content,
            pages_extracted=limit,
            pages_total=total_pages,
            truncated=truncated,
            chars=len(content),
            caveats=caveats,
        )
    except ValueError as exc:
        return _err(str(exc))
    except Exception as exc:  # noqa: BLE001 — surface PDF parse errors to the agent
        return _err(f"PDF read failed: {exc}")


def write_file(path: str, content: str) -> dict[str, Any]:
    """Create or overwrite a markdown file under wiki/ only.

    Args:
        path: Relative path under wiki/ (e.g. wiki/entities/ahu-3.md).
        content: Full file contents to write.
    """
    try:
        target = _resolve(path)
        if target.suffix.lower() not in {".md", ".txt", ""}:
            return _err("Only write .md (or .txt) under wiki/ in v1.")
            return _err("Only write .md (or .txt) under wiki/ in v1.")

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        return _ok(path=_rel(target), bytes_written=len(content.encode("utf-8")))
    except ValueError as exc:
        return _err(str(exc))
    except OSError as exc:
        return _err(f"OS error: {exc}")


def append_log(entry: str) -> dict[str, Any]:
    """Append a dated operation entry to wiki/log.md (newest at bottom).

    Args:
        entry: Markdown section to append (include heading if desired).
    """
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        existing = ""
        if LOG_PATH.exists():
            existing = LOG_PATH.read_text(encoding="utf-8")
        block = entry.strip()
        if not block:
            return _err("Log entry is empty.")
        if existing and not existing.endswith("\n"):
            existing += "\n"
        if existing and not existing.endswith("\n\n"):
            existing += "\n"
        LOG_PATH.write_text(existing + block + "\n", encoding="utf-8", newline="\n")
        return _ok(path=_rel(LOG_PATH))
    except OSError as exc:
        return _err(f"OS error: {exc}")


def update_hot(content: str) -> dict[str, Any]:
    """Overwrite wiki/hot.md with a fresh ~500-word recent-context cache.

    Args:
        content: Full replacement content for hot.md.
    """
    try:
        if not content.strip():
            return _err("hot.md content is empty.")
        HOT_PATH.parent.mkdir(parents=True, exist_ok=True)
        HOT_PATH.write_text(content, encoding="utf-8", newline="\n")
        return _ok(path=_rel(HOT_PATH), chars=len(content))
    except OSError as exc:
        return _err(f"OS error: {exc}")


def read_index() -> dict[str, Any]:
    """Read wiki/index.md (master catalog)."""
    return read_file("wiki/index.md")

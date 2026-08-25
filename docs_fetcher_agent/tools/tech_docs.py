"""Path-safe docs/tech I/O and allowlisted HTTP fetch for the docs fetcher agent."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_TECH_ROOT = REPO_ROOT / "docs" / "tech"
MANIFEST_PATH = DOCS_TECH_ROOT / "manifest.yaml"

MAX_READ_CHARS = 200_000
MAX_FETCH_BYTES = 2_000_000
FETCH_TIMEOUT_S = 30
USER_AGENT = "pr-docs-fetcher/1.0"


def _ok(**payload: Any) -> dict[str, Any]:
    return {"status": "success", **payload}


def _err(message: str, **payload: Any) -> dict[str, Any]:
    return {"status": "error", "error": message, **payload}


def _resolve(path: str) -> Path:
    clean = path.replace("\\", "/").lstrip("/")
    candidate = (REPO_ROOT / clean).resolve()
    try:
        candidate.relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"Path escapes repository root: {path}") from exc
    return candidate


def _rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def list_docs(path: str = "docs/tech") -> dict[str, Any]:
    """List files under docs/tech (or a subfolder).

    Args:
        path: Relative path from repo root. Defaults to docs/tech.
    """
    try:
        target = _resolve(path or "docs/tech")
        if not _is_under(target, DOCS_TECH_ROOT) and target.resolve() != DOCS_TECH_ROOT.resolve():
            return _err("list_docs is limited to docs/tech/.")
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
            if child.name.startswith("."):
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
    """Read a text file under the repo (typically docs/tech).

    Args:
        path: Relative path to a text file.
    """
    try:
        target = _resolve(path)
        if not target.exists():
            return _err(f"File not found: {path}")
        if not target.is_file():
            return _err(f"Not a file: {path}")
        if target.suffix.lower() == ".pdf":
            return _err("PDF is not supported by the docs fetcher. Use markdown/HTML snapshots.")
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


def read_manifest() -> dict[str, Any]:
    """Read docs/tech/manifest.yaml and return parsed sources plus raw text."""
    return read_file("docs/tech/manifest.yaml")


def _manifest_sources() -> list[dict[str, Any]]:
    data = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8")) or {}
    sources = data.get("sources") or []
    if not isinstance(sources, list):
        return []
    return [s for s in sources if isinstance(s, dict)]


def _allowed_url_prefixes() -> list[str]:
    prefixes: list[str] = []
    for source in _manifest_sources():
        url = str(source.get("url") or "").strip()
        if url:
            prefixes.append(url.rstrip("/"))
    return prefixes


def url_is_allowed(url: str, prefixes: list[str] | None = None) -> bool:
    """True when url is a listed manifest URL or a subpath of one."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    normalized = url.strip().rstrip("/")
    allowed = prefixes if prefixes is not None else _allowed_url_prefixes()
    for prefix in allowed:
        p = prefix.rstrip("/")
        if normalized == p or normalized.startswith(p + "/"):
            return True
        # Allow same-host docs trees when the manifest URL is the site root.
        p_parsed = urlparse(p)
        if (
            parsed.netloc == p_parsed.netloc
            and parsed.scheme == p_parsed.scheme
            and (not p_parsed.path or p_parsed.path == "/")
        ):
            return True
    return False


class _HTMLTextExtractor(HTMLParser):
    SKIP = {"script", "style", "nav", "footer", "noscript", "svg", "iframe"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.SKIP:
            self._skip += 1
            return
        if self._skip:
            return
        if tag in {"p", "div", "tr", "li", "br", "h1", "h2", "h3", "h4", "pre", "code"}:
            self._parts.append("\n")
        if tag in {"h1", "h2", "h3", "h4"}:
            hashes = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### "}[tag]
            self._parts.append(hashes)

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP and self._skip:
            self._skip -= 1
            return
        if tag in {"p", "div", "h1", "h2", "h3", "h4", "li", "pre"}:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self._parts.append(data)

    def text(self) -> str:
        joined = "".join(self._parts)
        joined = re.sub(r"[ \t]+", " ", joined)
        joined = re.sub(r"\n{3,}", "\n\n", joined)
        return joined.strip()


def html_to_text(html: str) -> str:
    parser = _HTMLTextExtractor()
    parser.feed(html)
    parser.close()
    return parser.text()


def fetch_url(url: str) -> dict[str, Any]:
    """HTTP GET an official-docs URL from the manifest allowlist.

    Args:
        url: Absolute http(s) URL that equals or is a subpath of a manifest url.
    """
    try:
        if not url_is_allowed(url):
            return _err(
                "URL is not on the manifest allowlist. "
                "Add it to docs/tech/manifest.yaml first.",
                url=url,
            )
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,text/plain,*/*"})
        with urlopen(req, timeout=FETCH_TIMEOUT_S) as resp:
            raw = resp.read(MAX_FETCH_BYTES + 1)
            content_type = resp.headers.get("Content-Type", "")
            final_url = resp.geturl()
        if len(raw) > MAX_FETCH_BYTES:
            return _err("Response exceeded size limit.", url=url)
        text = raw.decode("utf-8", errors="replace")
        if "html" in content_type.lower() or text.lstrip()[:15].lower().startswith("<!doctype html") or "<html" in text[:200].lower():
            extracted = html_to_text(text)
            kind = "html"
        else:
            extracted = text
            kind = "text"
        truncated = len(extracted) > MAX_READ_CHARS
        if truncated:
            extracted = extracted[:MAX_READ_CHARS]
        return _ok(
            url=url,
            final_url=final_url,
            kind=kind,
            content=extracted,
            truncated=truncated,
            chars=len(extracted),
        )
    except HTTPError as exc:
        return _err(f"HTTP {exc.code} fetching {url}")
    except URLError as exc:
        return _err(f"Network error: {exc.reason}")
    except Exception as exc:  # noqa: BLE001
        return _err(f"Fetch failed: {exc}")


def write_file(path: str, content: str) -> dict[str, Any]:
    """Create or overwrite a markdown file under docs/tech/ only.

    Args:
        path: Relative path under docs/tech/ (e.g. docs/tech/google-adk/agents.md).
        content: Full file contents to write.
    """
    try:
        target = _resolve(path)
        if not _is_under(target, DOCS_TECH_ROOT):
            return _err("Writes are only allowed under docs/tech/.")
        if target.suffix.lower() not in {".md", ".txt", ".yaml", ".yml"}:
            return _err("Only write .md, .txt, or .yaml under docs/tech/.")
        if not content.strip():
            return _err("Refusing to write an empty file.")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        return _ok(path=_rel(target), bytes_written=len(content.encode("utf-8")))
    except ValueError as exc:
        return _err(str(exc))
    except OSError as exc:
        return _err(f"OS error: {exc}")


def update_manifest(source_id: str, fetched_at: str = "", notes: str = "") -> dict[str, Any]:
    """Stamp fetched_at (UTC ISO-8601) and optional notes on a manifest source.

    Args:
        source_id: The `id` field of the source in manifest.yaml.
        fetched_at: Timestamp; defaults to now UTC if empty.
        notes: Short refresh note written onto that source.
    """
    try:
        if not MANIFEST_PATH.is_file():
            return _err("manifest.yaml not found")
        stamp = fetched_at.strip() or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8")) or {}
        sources = data.get("sources") or []
        matched = False
        for source in sources:
            if not isinstance(source, dict):
                continue
            if str(source.get("id")) == source_id:
                source["fetched_at"] = stamp
                if notes.strip():
                    source["notes"] = notes.strip()
                matched = True
                break
        if not matched:
            return _err(f"Unknown source id: {source_id}")
        header = (
            "# Official tech-doc corpus used by the PR review Action.\n"
            "# Entries may be added by hand or via `python -m docs_fetcher_agent --sync-manifest`\n"
            "# (from project dependency files). The fetcher may only GET these URLs / subpaths.\n\n"
        )
        MANIFEST_PATH.write_text(
            header + yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
            newline="\n",
        )
        return _ok(path=_rel(MANIFEST_PATH), source_id=source_id, fetched_at=stamp)
    except OSError as exc:
        return _err(f"OS error: {exc}")


def merge_manifest_sources(new_sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Add proposed sources that are not already in the manifest (match by id or url)."""
    try:
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        data: dict[str, Any] = {"sources": []}
        if MANIFEST_PATH.is_file():
            loaded = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8")) or {}
            if isinstance(loaded, dict):
                data = loaded
                data.setdefault("sources", [])
        sources = [s for s in (data.get("sources") or []) if isinstance(s, dict)]
        existing_ids = {str(s.get("id")) for s in sources}
        existing_urls = {str(s.get("url") or "").rstrip("/") for s in sources}
        added: list[str] = []
        skipped: list[str] = []
        for source in new_sources:
            sid = str(source.get("id") or "")
            url = str(source.get("url") or "").rstrip("/")
            if not sid or not url:
                continue
            if sid in existing_ids or url in existing_urls:
                skipped.append(sid)
                continue
            sources.append(source)
            existing_ids.add(sid)
            existing_urls.add(url)
            added.append(sid)
        data["sources"] = sources
        header = (
            "# Official tech-doc corpus used by the PR review Action.\n"
            "# Entries may be added by hand or via `python -m docs_fetcher_agent --sync-manifest`\n"
            "# (from project dependency files). The fetcher may only GET these URLs / subpaths.\n\n"
        )
        MANIFEST_PATH.write_text(
            header + yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
            newline="\n",
        )
        return _ok(
            path=_rel(MANIFEST_PATH),
            added=added,
            skipped_existing=skipped,
            total=len(sources),
        )
    except OSError as exc:
        return _err(f"OS error: {exc}")


def propose_from_project() -> dict[str, Any]:
    """Read host dependency files and propose manifest entries (no web search)."""
    from ..discover import propose_sources

    proposals = propose_sources(REPO_ROOT)
    return _ok(count=len(proposals), sources=proposals)


def sync_manifest_from_project() -> dict[str, Any]:
    """Merge proposed sources from dependency files into docs/tech/manifest.yaml."""
    from ..discover import propose_sources

    proposals = propose_sources(REPO_ROOT)
    merged = merge_manifest_sources(proposals)
    if merged.get("status") != "success":
        return merged
    return _ok(
        proposed=len(proposals),
        added=merged.get("added"),
        skipped_existing=merged.get("skipped_existing"),
        total=merged.get("total"),
        path=merged.get("path"),
    )


def inspect_stack() -> dict[str, Any]:
    """Detect the host repo's languages/tools from lockfiles (package.json, go.mod, …)."""
    from ..stack import scan_stack

    data = scan_stack(REPO_ROOT)
    return _ok(**data)

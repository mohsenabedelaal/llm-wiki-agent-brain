"""CLI: refresh docs/tech from the manifest (no ADK required)."""

from __future__ import annotations

import argparse
import json
import re
from urllib.parse import urlparse

from .stack import scan_stack
from .tools.tech_docs import (
    REPO_ROOT,
    fetch_url,
    propose_from_project,
    sync_manifest_from_project,
    update_manifest,
    write_file,
    _manifest_sources,
)


def _slug_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    name = (path.split("/")[-1] if path else "") or "index"
    name = re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-") or "index"
    if not name.lower().endswith(".md"):
        name = name + ".md"
    return name.lower()


def _markdown_snapshot(title: str, url: str, body: str) -> str:
    heading = title.strip() or "Official docs"
    return f"# {heading}\n\nCanonical: {url}\n\n{body.strip()}\n"


def refresh_all() -> dict:
    sources = _manifest_sources()
    results: list[dict] = []
    if not sources:
        return {"status": "error", "error": "No sources in docs/tech/manifest.yaml"}
    for source in sources:
        source_id = str(source.get("id") or "")
        url = str(source.get("url") or "").strip()
        local_dir = str(source.get("local_dir") or source_id)
        title = str(source.get("title") or source_id)
        if not source_id or not url or not local_dir:
            results.append({"id": source_id, "status": "error", "error": "incomplete source"})
            continue
        fetched = fetch_url(url)
        if fetched.get("status") != "success":
            results.append({"id": source_id, "url": url, **fetched})
            continue
        slug = _slug_from_url(url)
        rel = f"docs/tech/{local_dir}/{slug}"
        content = _markdown_snapshot(title, url, str(fetched.get("content") or ""))
        wrote = write_file(rel, content)
        if wrote.get("status") != "success":
            results.append({"id": source_id, **wrote})
            continue
        stamp = update_manifest(source_id, notes=f"CLI refresh of {url}")
        results.append(
            {
                "id": source_id,
                "status": "success",
                "path": wrote.get("path"),
                "chars": fetched.get("chars"),
                "fetched_at": stamp.get("fetched_at"),
            }
        )
    ok = all(r.get("status") == "success" for r in results)
    return {"status": "success" if ok else "partial", "results": results}


def inspect_stack() -> dict:
    data = scan_stack(REPO_ROOT)
    return {"status": "success", **data}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch official docs listed in docs/tech/manifest.yaml (portable; no ADK)."
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Fetch every manifest URL and write markdown under docs/tech/",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Print detected stack markers/keywords for this repo",
    )
    parser.add_argument(
        "--propose",
        action="store_true",
        help="List docs/tech sources inferred from dependency files (no web search)",
    )
    parser.add_argument(
        "--sync-manifest",
        action="store_true",
        help="Merge inferred sources into docs/tech/manifest.yaml (does not fetch pages)",
    )
    args = parser.parse_args(argv)
    if args.scan:
        print(json.dumps(inspect_stack(), indent=2))
        return 0
    if args.propose:
        print(json.dumps(propose_from_project(), indent=2))
        return 0
    if args.sync_manifest:
        print(json.dumps(sync_manifest_from_project(), indent=2))
        return 0
    if args.refresh:
        payload = refresh_all()
        print(json.dumps(payload, indent=2))
        return 0 if payload.get("status") == "success" else 1
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

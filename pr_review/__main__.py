"""CLI: review a GitHub PR against docs/tech and post inline comments."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .diff import commentable_from_files, format_diff_for_prompt
from .docs_loader import format_docs_for_prompt, load_tech_docs
from .gemini_review import generate_review
from .github_post import (
    build_review_payload,
    fetch_pull_files,
    fetch_pull_request,
    filter_findings,
    repo_slug,
    submit_review,
)
from .types import ReviewResult

# Package parent = repository root when this package lives at <repo>/pr_review/
_PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCS = Path("docs") / "tech"


def resolve_docs_root(docs: Path) -> Path:
    """Resolve a docs corpus path without baking in machine-specific absolutes.

    Relative paths are tried against the process cwd first (GitHub Actions /
    any clone), then against this package's parent directory.
    """
    if docs.is_absolute():
        return docs
    cwd_candidate = (Path.cwd() / docs).resolve()
    if cwd_candidate.is_dir():
        return cwd_candidate
    package_candidate = (_PACKAGE_ROOT / docs).resolve()
    if package_candidate.is_dir():
        return package_candidate
    return cwd_candidate


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Docs-grounded GitHub PR review (inline comments)."
    )
    p.add_argument("--pr", type=int, required=True, help="Pull request number")
    p.add_argument(
        "--docs",
        type=Path,
        default=DEFAULT_DOCS,
        help="Path to tech-doc corpus (default: docs/tech, relative to cwd)",
    )
    p.add_argument("--repo", default=None, help="owner/name (default: GITHUB_REPOSITORY)")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the review JSON; do not post to GitHub",
    )
    return p


def run(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    owner, repo = repo_slug(args.repo)
    pr = fetch_pull_request(owner, repo, args.pr)
    if pr.get("draft"):
        print("Skipping draft pull request.", file=sys.stderr)
        return 0

    files = fetch_pull_files(owner, repo, args.pr)
    anchors = commentable_from_files(files)
    diff_block = format_diff_for_prompt(files)
    changed_paths = [f.get("filename") or "" for f in files]
    docs_root = resolve_docs_root(Path(args.docs))
    docs = load_tech_docs(docs_root, changed_paths, diff_block)
    docs_block = format_docs_for_prompt(docs)

    head = (pr.get("head") or {}).get("sha")
    if not head:
        raise SystemExit("PR payload missing head.sha")

    result: ReviewResult = generate_review(
        title=pr.get("title") or "",
        body=pr.get("body") or "",
        diff_block=diff_block,
        docs_block=docs_block,
        anchors=anchors,
    )
    kept, dropped = filter_findings(result.findings, anchors)
    result.findings = kept
    result.dropped = dropped
    payload = build_review_payload(head, result)

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    posted = submit_review(owner, repo, args.pr, payload)
    html = posted.get("html_url") or posted.get("id")
    print(f"Posted review {html} ({payload['event']}, {len(payload['comments'])} comments)")
    return 0


def main() -> None:
    try:
        raise SystemExit(run())
    except KeyboardInterrupt:
        raise SystemExit(130) from None


if __name__ == "__main__":
    main()

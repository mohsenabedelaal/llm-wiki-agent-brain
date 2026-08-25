"""Optional portable project context for PR review (any repository)."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

# Common convention files — loaded only if present. No project-specific names required.
CONVENTION_CANDIDATES = (
    "CONTRIBUTING.md",
    "AGENTS.md",
    "CLAUDE.md",
    ".cursorrules",
    ".github/CONTRIBUTING.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
)

TEXT_SUFFIXES = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".kts",
    ".cs",
    ".fs",
    ".rb",
    ".php",
    ".swift",
    ".scala",
    ".md",
    ".yml",
    ".yaml",
    ".toml",
    ".json",
    ".txt",
    ".sh",
    ".ps1",
    ".sql",
    ".graphql",
    ".css",
    ".scss",
    ".html",
    ".vue",
    ".svelte",
    ".cpp",
    ".cc",
    ".cxx",
    ".h",
    ".hpp",
    ".m",
    ".mm",
    ".dart",
    ".tf",
    ".ex",
    ".exs",
    ".erl",
    ".hs",
    ".lua",
    ".r",
    ".jl",
    ".zig",
    ".proto",
    ".xml",
    ".gradle",
    ".cmake",
    ".sol",
}

MAX_FILE_CHARS = 60_000
MAX_CHANGED_FILES_CHARS = 240_000
MAX_CONVENTIONS_CHARS = 20_000
MAX_FILES_WITH_BODIES = 40

FetchAtRef = Callable[[str, str], str | None]


def load_project_conventions(repo_root: Path | None = None) -> str:
    """Load any present portable convention files (relative paths only in the prompt)."""
    root = repo_root or Path.cwd()
    parts: list[str] = []
    used = 0
    for rel in CONVENTION_CANDIDATES:
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) > MAX_CONVENTIONS_CHARS - used:
            text = text[: max(0, MAX_CONVENTIONS_CHARS - used)] + "\n\n[truncated]\n"
        block = f"### {rel}\n\n{text.strip()}\n"
        if used + len(block) > MAX_CONVENTIONS_CHARS:
            break
        parts.append(block)
        used += len(block)
    if not parts:
        return (
            "(no CONTRIBUTING/AGENTS/CLAUDE/.cursorrules found — review against "
            "general senior-engineer practice and any tech docs provided.)"
        )
    return "\n".join(parts)


def _is_text_path(path: str) -> bool:
    name = Path(path).name
    suffix = Path(path).suffix.lower()
    return suffix in TEXT_SUFFIXES or name in {"Dockerfile", "Makefile", "Jenkinsfile"}


def _clip(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n[truncated]\n"


def _read_local(root: Path, path: str) -> str | None:
    local = root / path
    if not local.is_file():
        return None
    try:
        raw = local.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw[:1024]:
        return None
    return raw.decode("utf-8", errors="replace")


def format_change_index(files: list[dict]) -> str:
    """Always include a complete changed-file index, even if bodies are budgeted out."""
    if not files:
        return "(no files in this pull request)"
    lines = []
    for item in files:
        path = (item.get("filename") or "").replace("\\", "/")
        status = item.get("status") or "modified"
        prev = item.get("previous_filename")
        stats = f"+{item.get('additions', 0)}/-{item.get('deletions', 0)}"
        line = f"- `{path}` ({status}, {stats}"
        if prev:
            line += f", renamed from `{prev}`"
        line += ")"
        lines.append(line)
    return "\n".join(lines)


def format_pr_file_context(
    files: list[dict],
    repo_root: Path | None = None,
    *,
    base_sha: str | None = None,
    head_sha: str | None = None,
    fetch_at_ref: FetchAtRef | None = None,
) -> str:
    """Before/after contents of changed files, plus a full path index.

    New (head) bodies come from the checkout. Old (base) bodies come from
    GitHub at `base_sha` when `fetch_at_ref` is provided.
    """
    root = repo_root or Path.cwd()
    index = format_change_index(files)
    parts: list[str] = [f"## Changed files ({len(files)})\n\n{index}\n"]
    used = len(parts[0])
    bodies = 0

    for item in files:
        if bodies >= MAX_FILES_WITH_BODIES or used >= MAX_CHANGED_FILES_CHARS:
            remaining = len(files) - bodies
            parts.append(
                f"\n[{remaining} additional file(s) listed in the index above; "
                "bodies omitted to stay within budget. Use the Diff section.]\n"
            )
            break

        path = (item.get("filename") or "").replace("\\", "/")
        if not path:
            continue
        status = item.get("status") or "modified"
        prev = (item.get("previous_filename") or "").replace("\\", "/")
        old_path = prev or path

        if not _is_text_path(path) and not (old_path and _is_text_path(old_path)):
            block = f"### {path} ({status})\n\n(binary or non-text — see diff if present)\n"
            parts.append(block)
            used += len(block)
            bodies += 1
            continue

        new_text: str | None = None
        if status != "removed":
            new_text = _read_local(root, path)
            if new_text is None and fetch_at_ref and head_sha:
                new_text = fetch_at_ref(path, head_sha)

        old_text: str | None = None
        if status != "added" and fetch_at_ref and base_sha:
            old_text = fetch_at_ref(old_path, base_sha)

        remaining_budget = MAX_CHANGED_FILES_CHARS - used
        per_file = min(MAX_FILE_CHARS, max(4_000, remaining_budget // 2))

        chunk = [f"### {path} ({status})"]
        if prev:
            chunk.append(f"Renamed from `{prev}`.")
        if status != "added":
            if old_text is None:
                chunk.append("#### Before (base)\n\n(unavailable)\n")
            else:
                chunk.append(f"#### Before (base)\n\n```\n{_clip(old_text, per_file)}\n```\n")
        if status != "removed":
            if new_text is None:
                chunk.append("#### After (head)\n\n(unavailable)\n")
            else:
                chunk.append(f"#### After (head)\n\n```\n{_clip(new_text, per_file)}\n```\n")

        block = "\n".join(chunk) + "\n"
        if used + len(block) > MAX_CHANGED_FILES_CHARS:
            parts.append(
                "\n[remaining file bodies omitted to stay within budget; see Diff]\n"
            )
            break
        parts.append(block)
        used += len(block)
        bodies += 1

    return "\n".join(parts)


def load_changed_file_contents(
    files: list[dict],
    repo_root: Path | None = None,
) -> str:
    """Head-side changed file bodies from the checkout (no GitHub base fetch)."""
    return format_pr_file_context(files, repo_root)

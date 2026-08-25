"""Parse GitHub pull-request file patches into commentable (path, line, side) anchors."""

from __future__ import annotations

import re
from typing import Iterable

from .types import CommentAnchor

HUNK_RE = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")
GIT_HEADER_RE = re.compile(r"^diff --git a/(.+) b/(.+)$")


def commentable_from_files(files: Iterable[dict]) -> set[CommentAnchor]:
    """Build the set of GitHub-commentable anchors from the PR files API payload."""
    anchors: set[CommentAnchor] = set()
    for item in files:
        path = (item.get("filename") or "").replace("\\", "/")
        patch = item.get("patch") or ""
        if not path or not patch:
            continue
        anchors.update(commentable_from_patch(path, patch))
    return anchors


def commentable_from_patch(path: str, patch: str) -> set[CommentAnchor]:
    """Parse a unified-diff patch for one file.

    Added lines (`+`) are RIGHT at the new line number.
    Deleted lines (`-`) are LEFT at the old line number.
    Context lines (` `) are RIGHT at the new line number (GitHub allows this).
    """
    anchors: set[CommentAnchor] = set()
    old_line = 0
    new_line = 0
    in_hunk = False

    for raw in patch.splitlines():
        hunk = HUNK_RE.match(raw)
        if hunk:
            old_line = int(hunk.group(1))
            new_line = int(hunk.group(2))
            in_hunk = True
            continue
        if not in_hunk:
            continue
        if raw.startswith("\\"):
            continue
        if raw.startswith("+"):
            anchors.add(CommentAnchor(path=path, line=new_line, side="RIGHT"))
            new_line += 1
        elif raw.startswith("-"):
            anchors.add(CommentAnchor(path=path, line=old_line, side="LEFT"))
            old_line += 1
        elif raw.startswith(" "):
            anchors.add(CommentAnchor(path=path, line=new_line, side="RIGHT"))
            old_line += 1
            new_line += 1
        else:
            # File headers inside a patch should not appear once a hunk started.
            continue
    return anchors


def commentable_from_unified_diff(diff_text: str) -> set[CommentAnchor]:
    """Parse a multi-file unified diff (optional helper for tests / local files)."""
    anchors: set[CommentAnchor] = set()
    current_path = ""
    chunk: list[str] = []

    def flush() -> None:
        nonlocal chunk, current_path
        if current_path and chunk:
            anchors.update(commentable_from_patch(current_path, "\n".join(chunk)))
        chunk = []

    for raw in diff_text.splitlines():
        header = GIT_HEADER_RE.match(raw)
        if header:
            flush()
            current_path = header.group(2)
            chunk = [raw]
            continue
        if raw.startswith("+++ "):
            plus_path = raw[4:].strip()
            if plus_path.startswith("b/"):
                current_path = plus_path[2:]
            elif plus_path != "/dev/null":
                current_path = plus_path
        chunk.append(raw)
    flush()
    return anchors


def format_diff_for_prompt(files: Iterable[dict], max_chars: int = 60_000) -> str:
    """Render PR file patches as a single prompt block, truncated if needed."""
    parts: list[str] = []
    used = 0
    for item in files:
        path = item.get("filename") or ""
        status = item.get("status") or ""
        patch = item.get("patch")
        header = f"### {path} ({status})"
        if not patch:
            block = header + "\n(no textual patch — binary or too large)\n"
        else:
            block = header + "\n```diff\n" + patch + "\n```\n"
        if used + len(block) > max_chars:
            parts.append("\n[diff truncated to stay within the token budget]\n")
            break
        parts.append(block)
        used += len(block)
    return "\n".join(parts)

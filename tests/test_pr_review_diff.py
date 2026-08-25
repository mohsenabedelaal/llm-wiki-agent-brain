"""Tests for unified-diff → GitHub commentable (path, line, side) mapping."""

from __future__ import annotations

from pr_review.diff import commentable_from_files, commentable_from_patch
from pr_review.types import CommentAnchor


def test_added_lines_are_right_side() -> None:
    patch = "@@ -0,0 +1,3 @@\n+alpha\n+beta\n+gamma\n"
    anchors = commentable_from_patch("pr_review/diff.py", patch)
    assert CommentAnchor("pr_review/diff.py", 1, "RIGHT") in anchors
    assert CommentAnchor("pr_review/diff.py", 2, "RIGHT") in anchors
    assert CommentAnchor("pr_review/diff.py", 3, "RIGHT") in anchors
    assert not any(a.side == "LEFT" for a in anchors)


def test_deleted_lines_are_left_side() -> None:
    patch = "@@ -10,2 +10,0 @@\n-old one\n-old two\n"
    anchors = commentable_from_patch("gone.py", patch)
    assert CommentAnchor("gone.py", 10, "LEFT") in anchors
    assert CommentAnchor("gone.py", 11, "LEFT") in anchors


def test_mixed_hunk_maps_add_delete_and_context() -> None:
    patch = (
        "@@ -10,4 +10,5 @@ def foo():\n"
        "     x = 1\n"
        "-    y = 2\n"
        "+    y = 3\n"
        "+    z = 4\n"
        "     return x\n"
    )
    anchors = commentable_from_patch("mod.py", patch)
    assert CommentAnchor("mod.py", 10, "RIGHT") in anchors  # context
    assert CommentAnchor("mod.py", 11, "LEFT") in anchors  # deleted y=2
    assert CommentAnchor("mod.py", 11, "RIGHT") in anchors  # added y=3
    assert CommentAnchor("mod.py", 12, "RIGHT") in anchors  # added z=4
    assert CommentAnchor("mod.py", 13, "RIGHT") in anchors  # context return


def test_no_newline_marker_is_ignored() -> None:
    patch = "@@ -1,1 +1,1 @@\n-old\n+new\n\\ No newline at end of file\n"
    anchors = commentable_from_patch("a.txt", patch)
    assert CommentAnchor("a.txt", 1, "RIGHT") in anchors
    assert CommentAnchor("a.txt", 1, "LEFT") in anchors
    assert len(anchors) == 2


def test_commentable_from_files_skips_binary_without_patch() -> None:
    files = [
        {"filename": "raw/manuals/S24AWN.pdf", "status": "modified"},
        {
            "filename": "wiki_agent/agent.py",
            "status": "modified",
            "patch": "@@ -1,1 +1,1 @@\n-old\n+new\n",
        },
    ]
    anchors = commentable_from_files(files)
    assert CommentAnchor("wiki_agent/agent.py", 1, "RIGHT") in anchors
    assert all(a.path != "raw/manuals/S24AWN.pdf" for a in anchors)

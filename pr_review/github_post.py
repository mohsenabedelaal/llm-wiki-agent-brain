"""GitHub REST client: fetch a PR and post an inline review."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from .types import CommentAnchor, Finding, ReviewResult

API_VERSION = "2022-11-28"
USER_AGENT = "llm-wiki-agent-brain-pr-review"


class GitHubError(RuntimeError):
    pass


def _token() -> str:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise GitHubError("GITHUB_TOKEN is not set")
    return token


def _api(method: str, url: str, body: dict[str, Any] | None = None) -> Any:
    data = None
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {_token()}",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": USER_AGENT,
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise GitHubError(f"GitHub {method} {url} failed ({exc.code}): {detail}") from exc


def repo_slug(explicit: str | None = None) -> tuple[str, str]:
    slug = explicit or os.environ.get("GITHUB_REPOSITORY") or ""
    if "/" not in slug:
        raise GitHubError("Set --repo owner/name or GITHUB_REPOSITORY")
    owner, name = slug.split("/", 1)
    return owner, name


def fetch_pull_request(owner: str, repo: str, number: int) -> dict[str, Any]:
    return _api("GET", f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}")


def fetch_pull_files(owner: str, repo: str, number: int) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    page = 1
    while True:
        qs = urllib.parse.urlencode({"per_page": 100, "page": page})
        batch = _api(
            "GET",
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}/files?{qs}",
        )
        if not isinstance(batch, list) or not batch:
            break
        files.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return files


def filter_findings(
    findings: list[Finding],
    anchors: set[CommentAnchor],
) -> tuple[list[Finding], list[Finding]]:
    """Keep file-level notes and inline comments whose (path, line, side) is in the diff."""
    kept: list[Finding] = []
    dropped: list[Finding] = []
    allowed_paths = {a.path for a in anchors}
    for finding in findings:
        if finding.is_file_level:
            if finding.path in allowed_paths or not anchors:
                kept.append(finding)
            else:
                dropped.append(finding)
            continue
        side = finding.side if finding.side in {"LEFT", "RIGHT"} else "RIGHT"
        anchor = CommentAnchor(path=finding.path, line=int(finding.line or 0), side=side)
        if anchor in anchors:
            kept.append(finding)
        else:
            dropped.append(finding)
    return kept, dropped


def finding_to_review_comment(finding: Finding) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "path": finding.path,
        "body": finding.comment_body(),
    }
    if finding.is_file_level:
        payload["subject_type"] = "file"
        return payload
    payload["line"] = int(finding.line or 0)
    payload["side"] = finding.side if finding.side in {"LEFT", "RIGHT"} else "RIGHT"
    return payload


def build_review_payload(
    commit_id: str,
    review: ReviewResult,
) -> dict[str, Any]:
    comments = [finding_to_review_comment(f) for f in review.findings]
    summary = review.summary.strip()
    if review.dropped:
        summary += (
            f"\n\n_{len(review.dropped)} finding(s) omitted because the line "
            "was not in the PR diff._"
        )
    return {
        "commit_id": commit_id,
        "body": summary,
        "event": review.event,
        "comments": comments,
    }


def submit_review(
    owner: str,
    repo: str,
    number: int,
    payload: dict[str, Any],
) -> dict[str, Any]:
    return _api(
        "POST",
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}/reviews",
        payload,
    )

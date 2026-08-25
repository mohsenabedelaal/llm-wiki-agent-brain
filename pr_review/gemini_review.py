"""Ask Gemini for a senior-engineer, docs-grounded PR review as JSON."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from .types import MAX_FINDINGS, SEVERITY_RANK, Finding, ReviewResult

MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")

REVIEW_SCHEMA: dict[str, Any] = {
    "type": "OBJECT",
    "properties": {
        "summary": {
            "type": "STRING",
            "description": "Markdown PR-level summary. 2-8 sentences. No auto-approve language.",
        },
        "findings": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "path": {"type": "STRING"},
                    "line": {"type": "INTEGER", "nullable": True},
                    "side": {"type": "STRING", "enum": ["LEFT", "RIGHT"]},
                    "severity": {
                        "type": "STRING",
                        "enum": ["blocker", "should-fix", "nit"],
                    },
                    "body": {"type": "STRING"},
                    "doc_path": {"type": "STRING"},
                    "section": {"type": "STRING", "nullable": True},
                },
                "required": ["path", "severity", "body", "doc_path"],
            },
        },
    },
    "required": ["summary", "findings"],
}

SYSTEM_PROMPT = """You are a senior software engineer reviewing a GitHub pull request.

Review against the provided official tech docs first. Prefer:
1. Correctness and API misuse versus those docs
2. Security (path traversal, leaked secrets, unbounded network/file IO)
3. Behavioral regressions
4. Missing tests for new behavior

Ignore pure style nits unless they hide a real bug. Cap findings at 20, highest severity first.
Never rubber-stamp or approve. If the diff is clean versus the docs, say so in the summary
and return an empty findings array.

Each finding MUST:
- Anchor to a changed file. Use `line` + `side` (`RIGHT` for additions/context, `LEFT` for deletions)
  from the COMMENTABLE ANCHORS list. If no single line fits, omit `line` (file-level).
- Cite `doc_path` of the tech-doc file you used (and `section` when possible).
- Write `body` as a senior review comment: what is wrong, why (doc rule), and a concrete fix.

Do not comment on files that are not in the diff.
"""


def _parse_findings(raw: list[dict[str, Any]]) -> list[Finding]:
    findings: list[Finding] = []
    for item in raw:
        path = str(item.get("path") or "").replace("\\", "/")
        if not path:
            continue
        severity = str(item.get("severity") or "should-fix")
        if severity not in SEVERITY_RANK:
            severity = "should-fix"
        line_val = item.get("line")
        line: int | None
        try:
            line = int(line_val) if line_val is not None and str(line_val) != "" else None
        except (TypeError, ValueError):
            line = None
        side = str(item.get("side") or "RIGHT").upper()
        if side not in {"LEFT", "RIGHT"}:
            side = "RIGHT"
        findings.append(
            Finding(
                path=path,
                line=line,
                side=side,
                severity=severity,
                body=str(item.get("body") or "").strip(),
                doc_path=str(item.get("doc_path") or "").strip() or "(unspecified)",
                section=(str(item["section"]) if item.get("section") else None),
            )
        )
    findings.sort(key=lambda f: (SEVERITY_RANK.get(f.severity, 9), f.path, f.line or 0))
    return findings[:MAX_FINDINGS]


def parse_model_json(text: str) -> ReviewResult:
    payload = json.loads(_extract_json(text))
    findings = _parse_findings(list(payload.get("findings") or []))
    summary = str(payload.get("summary") or "").strip() or "Review completed."
    return ReviewResult(summary=summary, findings=findings)


def _extract_json(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped


def build_user_prompt(
    *,
    title: str,
    body: str,
    diff_block: str,
    docs_block: str,
    anchors_block: str,
) -> str:
    return (
        f"## Pull request\n\n**Title:** {title}\n\n{body or '(no description)'}\n\n"
        f"## Official tech docs\n\n{docs_block}\n\n"
        f"## Diff\n\n{diff_block}\n\n"
        f"## COMMENTABLE ANCHORS\n\nOnly use these (path, line, side) pairs:\n{anchors_block}\n"
    )


def format_anchors(anchors: set, limit: int = 400) -> str:
    rows = sorted(f"{a.path}:{a.line}:{a.side}" for a in anchors)
    if len(rows) > limit:
        rows = rows[:limit] + [f"... ({len(anchors) - limit} more omitted)"]
    return "\n".join(rows) if rows else "(none — file-level comments only)"


def generate_review(
    *,
    title: str,
    body: str,
    diff_block: str,
    docs_block: str,
    anchors: set,
    api_key: str | None = None,
) -> ReviewResult:
    key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_API_KEY is not set")

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=key)
    prompt = build_user_prompt(
        title=title,
        body=body or "",
        diff_block=diff_block,
        docs_block=docs_block,
        anchors_block=format_anchors(anchors),
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=REVIEW_SCHEMA,
            temperature=0.2,
        ),
    )
    text = getattr(response, "text", None) or ""
    if not text.strip():
        raise RuntimeError("Gemini returned empty review JSON")
    return parse_model_json(text)

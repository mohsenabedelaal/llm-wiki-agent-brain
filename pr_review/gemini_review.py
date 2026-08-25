"""Ask Gemini for a senior-engineer PR review as JSON (portable across repos)."""

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
                    "category": {
                        "type": "STRING",
                        "enum": [
                            "correctness",
                            "regression",
                            "security",
                            "api-docs",
                            "tests",
                            "maintainability",
                            "conventions",
                            "performance",
                        ],
                    },
                    "body": {"type": "STRING"},
                    "doc_path": {
                        "type": "STRING",
                        "nullable": True,
                        "description": "Tech-doc or convention file path when applicable; omit or null otherwise.",
                    },
                    "section": {"type": "STRING", "nullable": True},
                },
                "required": ["path", "severity", "category", "body"],
            },
        },
    },
    "required": ["summary", "findings"],
}

SYSTEM_PROMPT = """You are a lead / senior software engineer reviewing a GitHub pull request
for an arbitrary repository. This workflow is portable — do not assume any specific product
domain. Judge from: the PR description, the diff, full changed-file contents when provided,
optional official tech docs, and optional project convention files.

Review priorities (highest first):
1. Correctness bugs and logic errors visible in the change
2. Behavioral regressions / broken contracts with surrounding code you can see
3. Security (injection, path traversal, secret leakage, authz gaps, unsafe deserialization,
   unbounded network/file IO)
4. API misuse versus provided official tech docs (when docs are present)
5. Missing or weak tests for new/changed behavior
6. Maintainability and bad practices (dead code, misleading names, swallowed errors,
   god functions, brittle coupling) — only when actionable
7. Project conventions when CONTRIBUTING/AGENTS/CLAUDE/.cursorrules (or similar) are provided
8. Clear performance foot-guns in hot paths

Rules:
- Prefer fewer high-signal findings over style nits. Ignore pure formatting/import-order nits
  unless they hide a real bug.
- Cap findings at 20, highest severity first.
- Never rubber-stamp or approve. If the change looks solid, say so in the summary and return
  an empty findings array.
- You may raise findings that are NOT grounded in tech docs. Use category accordingly.
- Cite `doc_path` only when a provided tech doc or convention file actually supports the claim.
  Otherwise leave `doc_path` null — do not invent citations.
- Anchor each finding to a changed file. Use `line` + `side` from COMMENTABLE ANCHORS
  (`RIGHT` for additions/context, `LEFT` for deletions). If no single line fits, omit `line`
  (file-level).
- Write `body` like a lead review comment: what is wrong, why it matters, and a concrete fix.
- Do not comment on files that are not in the diff.
- Use the Diff plus Before/After file bodies as the source of truth for what changed.
  The After (head) body is the new file; Before (base) is the previous version.
  Do not invent surrounding callers you cannot see.
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
        doc_raw = item.get("doc_path")
        doc_path = str(doc_raw).strip() if doc_raw else None
        if doc_path in {"", "null", "none", "(unspecified)"}:
            doc_path = None
        category = str(item.get("category") or "correctness").strip() or "correctness"
        findings.append(
            Finding(
                path=path,
                line=line,
                side=side,
                severity=severity,
                category=category,
                body=str(item.get("body") or "").strip(),
                doc_path=doc_path,
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
    conventions_block: str,
    files_block: str,
    anchors_block: str,
) -> str:
    return (
        f"## Pull request\n\n**Title:** {title}\n\n{body or '(no description)'}\n\n"
        f"## Project conventions (if any)\n\n{conventions_block}\n\n"
        f"## Official tech docs (if any)\n\n{docs_block}\n\n"
        f"## Changed files (index + before/after bodies)\n\n{files_block}\n\n"
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
    conventions_block: str,
    files_block: str,
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
        conventions_block=conventions_block,
        files_block=files_block,
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

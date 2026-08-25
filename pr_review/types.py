"""PR review types shared across modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Severity = Literal["blocker", "should-fix", "nit"]
Side = Literal["LEFT", "RIGHT"]

SEVERITY_RANK = {"blocker": 0, "should-fix": 1, "nit": 2}
MAX_FINDINGS = 20


@dataclass(frozen=True)
class CommentAnchor:
    path: str
    line: int
    side: str


@dataclass
class Finding:
    path: str
    body: str
    severity: str
    doc_path: str
    line: int | None = None
    side: str = "RIGHT"
    section: str | None = None

    @property
    def is_file_level(self) -> bool:
        return self.line is None

    def comment_body(self) -> str:
        cite = f"`{self.doc_path}`"
        if self.section:
            cite += f" ({self.section})"
        return f"**{self.severity}** — {self.body.strip()}\n\nGrounded in {cite}."


@dataclass
class ReviewResult:
    summary: str
    findings: list[Finding] = field(default_factory=list)
    dropped: list[Finding] = field(default_factory=list)

    @property
    def event(self) -> str:
        if any(f.severity == "blocker" for f in self.findings):
            return "REQUEST_CHANGES"
        return "COMMENT"

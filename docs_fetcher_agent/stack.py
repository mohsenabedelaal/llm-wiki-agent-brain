"""Detect common project stacks from repo-relative lockfiles / manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

# Marker file (repo-relative) -> keywords useful for docs/tech matching.
STACK_MARKERS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("package.json", ("javascript", "typescript", "node", "npm")),
    ("pnpm-lock.yaml", ("javascript", "typescript", "node", "pnpm")),
    ("yarn.lock", ("javascript", "typescript", "node", "yarn")),
    ("go.mod", ("go", "golang")),
    ("Cargo.toml", ("rust", "cargo")),
    ("pyproject.toml", ("python", "pip", "poetry")),
    ("requirements.txt", ("python", "pip")),
    ("Pipfile", ("python", "pipenv")),
    ("pom.xml", ("java", "maven")),
    ("build.gradle", ("java", "kotlin", "gradle")),
    ("build.gradle.kts", ("kotlin", "gradle")),
    ("Gemfile", ("ruby", "bundler")),
    ("composer.json", ("php", "composer")),
    ("pubspec.yaml", ("dart", "flutter")),
    ("Package.swift", ("swift", "spm")),
    ("*.csproj", ("csharp", "dotnet")),  # handled via glob in scan
    ("CMakeLists.txt", ("cpp", "cmake")),
    ("mix.exs", ("elixir", "mix")),
    ("go.sum", ("go",)),
)


def scan_stack(repo_root: Path) -> dict[str, Any]:
    """Return detected markers and flattened keywords. No network."""
    found: list[dict[str, Any]] = []
    keywords: list[str] = []
    root = repo_root.resolve()

    csprojs = list(root.glob("*.csproj")) + list(root.glob("src/*/*.csproj"))
    if csprojs:
        rels = [p.relative_to(root).as_posix() for p in csprojs[:8]]
        found.append({"path": rels[0], "keywords": ["csharp", "dotnet"]})
        keywords.extend(["csharp", "dotnet"])

    for marker, kws in STACK_MARKERS:
        if marker.startswith("*"):
            continue
        path = root / marker
        if path.is_file():
            found.append({"path": marker, "keywords": list(kws)})
            keywords.extend(kws)

    # Unique, stable order
    seen: set[str] = set()
    unique_kw: list[str] = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_kw.append(kw)

    return {"markers": found, "keywords": unique_kw}

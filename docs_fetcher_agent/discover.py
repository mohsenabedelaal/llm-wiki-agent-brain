"""Propose docs/tech manifest entries from the host project's dependency files.

No web search. Direct dependencies only. Doc URLs come from:
1. a small well-known map
2. package-registry metadata (PyPI / npm)
3. conventional hosts (pkg.go.dev, docs.rs)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

WELL_KNOWN: dict[tuple[str, str], str] = {
    ("python", "google-adk"): "https://google.github.io/adk-docs/",
    ("python", "pytest"): "https://docs.pytest.org/en/stable/",
    ("python", "pypdf"): "https://pypdf.readthedocs.io/en/stable/",
    ("python", "google-genai"): "https://ai.google.dev/gemini-api/docs",
    ("python", "python-dotenv"): "https://saurabh-kumar.com/python-dotenv/",
    ("python", "pyyaml"): "https://yaml.readthedocs.io/en/latest/",
    ("javascript", "react"): "https://react.dev/",
    ("javascript", "next"): "https://nextjs.org/docs",
    ("javascript", "vue"): "https://vuejs.org/guide/introduction.html",
    ("go", "github.com/gin-gonic/gin"): "https://pkg.go.dev/github.com/gin-gonic/gin",
}

MAX_DIRECT_DEPS = 40
REG_TIMEOUT_S = 20
USER_AGENT = "pr-docs-fetcher/1.0"

_REQ_NAME = re.compile(r"^\s*([A-Za-z0-9_.-]+)")


JsonFetch = Callable[[str], dict[str, Any] | None]


def _slug(ecosystem: str, name: str) -> str:
    raw = f"{ecosystem}-{name}".lower()
    return re.sub(r"[^a-z0-9]+", "-", raw).strip("-") or "pkg"


def parse_requirements_txt(text: str) -> list[str]:
    names: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("-"):
            continue
        if stripped.startswith(("git+", "http://", "https://", "file:")):
            continue
        match = _REQ_NAME.match(stripped)
        if match:
            names.append(match.group(1))
    return names


def parse_package_json(text: str) -> list[str]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    names: list[str] = []
    for key in ("dependencies", "devDependencies"):
        block = data.get(key) or {}
        if isinstance(block, dict):
            names.extend(str(n) for n in block.keys())
    return names


def parse_go_mod(text: str) -> list[str]:
    names: list[str] = []
    in_block = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("require ("):
            in_block = True
            continue
        if in_block:
            if line == ")":
                in_block = False
                continue
            if "// indirect" in line:
                continue
            parts = line.split()
            if parts and not parts[0].startswith("//"):
                names.append(parts[0])
            continue
        if line.startswith("require ") and "(" not in line:
            parts = line.split()
            if len(parts) >= 2 and "// indirect" not in line:
                names.append(parts[1])
    return names


def parse_cargo_toml_dep_names(text: str) -> list[str]:
    """Minimal TOML scan of [dependencies] / [dev-dependencies] keys."""
    names: list[str] = []
    section = ""
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            continue
        if section not in {"dependencies", "dev-dependencies"}:
            continue
        if not line or line.startswith("#"):
            continue
        key = line.split("=", 1)[0].strip().strip('"')
        if key:
            names.append(key)
    return names


def parse_pyproject_dep_names(text: str) -> list[str]:
    names: list[str] = []
    try:
        import tomllib
    except ImportError:  # pragma: no cover
        tomllib = None  # type: ignore
    if tomllib:
        try:
            data = tomllib.loads(text)
        except Exception:  # noqa: BLE001
            data = {}
        project_deps = (data.get("project") or {}).get("dependencies") or []
        for item in project_deps:
            match = _REQ_NAME.match(str(item))
            if match:
                names.append(match.group(1))
        poetry = ((data.get("tool") or {}).get("poetry") or {}).get("dependencies") or {}
        if isinstance(poetry, dict):
            names.extend(k for k in poetry.keys() if k.lower() != "python")
        return names
    return names


def collect_direct_dependencies(repo_root: Path) -> list[dict[str, str]]:
    """Return [{ecosystem, name, from_file}, ...] unique, capped."""
    found: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add(ecosystem: str, name: str, from_file: str) -> None:
        key = (ecosystem, name.lower())
        if key in seen or len(found) >= MAX_DIRECT_DEPS:
            return
        seen.add(key)
        found.append({"ecosystem": ecosystem, "name": name, "from_file": from_file})

    req = repo_root / "requirements.txt"
    if req.is_file():
        for name in parse_requirements_txt(req.read_text(encoding="utf-8", errors="replace")):
            add("python", name, "requirements.txt")

    pyproject = repo_root / "pyproject.toml"
    if pyproject.is_file():
        for name in parse_pyproject_dep_names(
            pyproject.read_text(encoding="utf-8", errors="replace")
        ):
            add("python", name, "pyproject.toml")

    pkg = repo_root / "package.json"
    if pkg.is_file():
        for name in parse_package_json(pkg.read_text(encoding="utf-8", errors="replace")):
            add("javascript", name, "package.json")

    gomod = repo_root / "go.mod"
    if gomod.is_file():
        for name in parse_go_mod(gomod.read_text(encoding="utf-8", errors="replace")):
            add("go", name, "go.mod")

    cargo = repo_root / "Cargo.toml"
    if cargo.is_file():
        for name in parse_cargo_toml_dep_names(
            cargo.read_text(encoding="utf-8", errors="replace")
        ):
            add("rust", name, "Cargo.toml")

    return found


def _http_json(url: str) -> dict[str, Any] | None:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urlopen(req, timeout=REG_TIMEOUT_S) as resp:
            raw = resp.read(1_000_000)
        return json.loads(raw.decode("utf-8", errors="replace"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None


def _pick_project_url(urls: dict[str, Any]) -> str | None:
    preferred = (
        "Documentation",
        "Docs",
        "Document",
        "Home",
        "Homepage",
        "Changelog",
    )
    lower_map = {str(k).lower(): str(v).strip() for k, v in urls.items() if v}
    for key in preferred:
        val = lower_map.get(key.lower())
        if val and val.startswith("http"):
            return val
    for val in lower_map.values():
        if val.startswith("http") and ("readthedocs" in val or "github.io" in val):
            return val
    homepage = lower_map.get("homepage") or lower_map.get("home")
    if homepage and homepage.startswith("http"):
        return homepage
    return None


def resolve_docs_url(
    ecosystem: str,
    name: str,
    fetch_json: JsonFetch | None = None,
) -> str | None:
    known = WELL_KNOWN.get((ecosystem, name.lower()))
    if known:
        return known
    getter = fetch_json or _http_json
    if ecosystem == "python":
        payload = getter(f"https://pypi.org/pypi/{quote(name)}/json")
        if isinstance(payload, dict):
            info = payload.get("info") or {}
            urls = info.get("project_urls") or {}
            if isinstance(urls, dict):
                picked = _pick_project_url(urls)
                if picked:
                    return picked
            home = str(info.get("home_page") or "").strip()
            if home.startswith("http"):
                return home
        return f"https://pypi.org/project/{name}/"
    if ecosystem == "javascript":
        payload = getter(f"https://registry.npmjs.org/{quote(name, safe='@/')}")
        if isinstance(payload, dict):
            home = str(payload.get("homepage") or "").strip()
            if home.startswith("http"):
                return home
            repo = payload.get("repository")
            if isinstance(repo, dict):
                url = str(repo.get("url") or "").strip()
                url = url.replace("git+", "").replace("git://", "https://")
                if url.startswith("http"):
                    return url
        return f"https://www.npmjs.com/package/{name}"
    if ecosystem == "go":
        return f"https://pkg.go.dev/{name}"
    if ecosystem == "rust":
        crate = name.split("/")[-1]
        return f"https://docs.rs/{crate}"
    return None


def propose_sources(
    repo_root: Path,
    fetch_json: JsonFetch | None = None,
) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for dep in collect_direct_dependencies(repo_root):
        url = resolve_docs_url(dep["ecosystem"], dep["name"], fetch_json=fetch_json)
        if not url:
            continue
        source_id = _slug(dep["ecosystem"], dep["name"])
        proposals.append(
            {
                "id": source_id,
                "title": dep["name"],
                "url": url,
                "local_dir": source_id,
                "keywords": [dep["name"], dep["ecosystem"]],
                "notes": f"Proposed from {dep['from_file']}",
            }
        )
    return proposals

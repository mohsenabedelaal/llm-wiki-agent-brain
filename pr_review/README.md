# Portable PR review kit

Copy these folders into **any** GitHub repo (Python, Node, Go, Rust, Java, …). The host project does not need to be Python except that CI installs a small Python package to run the reviewer.

Two pieces, meant to work together:

| Piece | Role |
|-------|------|
| `docs_fetcher_agent` | Fills `docs/tech/` from official doc URLs in a manifest |
| `pr_review` | On each PR: lead-style review of **the actual change** (diff + before/after files), grounded in `docs/tech/` when present |

The reviewer never assumes this wiki vault, HVAC, or ADK. It reviews whatever is in the PR.

## Drop-in layout (repo-relative)

```
your-repo/
├── pr_review/                          # required for CI review
│   ├── requirements.txt
│   └── …
├── docs_fetcher_agent/                 # optional; keeps docs/tech fresh
├── docs/tech/
│   ├── manifest.yaml                   # stack → official URL + local folder
│   └── <id>/*.md                       # snapshots the reviewer reads
└── .github/workflows/pr-docs-review.yml
```

## 1. Docs fetcher → `docs/tech/`

**Source of packages:** the host project's own config (`requirements.txt`, `pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`). Direct dependencies only.

**Source of doc URLs:** not Google. A well-known map, then PyPI/npm metadata, then `pkg.go.dev` / `docs.rs`. Results are **merged into** `docs/tech/manifest.yaml`, which remains the allowlist for page fetches.

```bash
python -m docs_fetcher_agent --propose         # preview inferred sources
python -m docs_fetcher_agent --sync-manifest   # write/merge manifest.yaml
python -m docs_fetcher_agent --refresh         # download those official pages
```

You can still edit the manifest by hand (add, pin, or delete). Existing entries are not overwritten on sync.

Fetcher extra deps: `pip install -r docs_fetcher_agent/requirements.txt`

**Optional interactive agent** (needs Google ADK + `GOOGLE_API_KEY`):

```bash
adk run docs_fetcher_agent
# Refresh all sources in docs/tech/manifest.yaml
```

Writes **only** under `docs/tech/`. Commit the snapshots so PR review is reproducible.

## 2. PR reviewer (GitHub Action)

Repo secret: `GOOGLE_API_KEY`.

The workflow checks out the PR, installs `pr_review/requirements.txt`, and runs:

```bash
python -m pr_review --pr "$PR_NUMBER" --docs docs/tech
```

If `docs/tech/` is missing, the review still runs (lead-engineer judgment + any `CONTRIBUTING.md` / `AGENTS.md` / `CLAUDE.md` / `.cursorrules`).

Local dry-run from the **repository root**:

```bash
python -m pr_review --pr 12 --docs docs/tech --dry-run
```

## Hand-in-hand loop

1. `python -m docs_fetcher_agent --sync-manifest` (or maintain `manifest.yaml` by hand).
2. `--refresh` (or the ADK agent) writes markdown snapshots.
3. Commit `docs/tech/`.
4. Open a PR → Action reviews the **full change** (file index, before/after, diff) against those docs plus general engineering practice.

Do not hard-code machine paths. Keep everything repo-relative.

# Official tech docs (PR review corpus)

This tree is the **source of truth for docs-grounded PR review**. It is separate from `raw/` (building-ops manuals) and `wiki/` (Obsidian knowledge). Do not mix HVAC sources here.

The GitHub Action in `.github/workflows/pr-docs-review.yml` reads these files, reviews the PR diff against them, and posts **inline** GitHub review comments on specific lines/files.

## Layout

| Path | Role |
|------|------|
| `manifest.yaml` | Stack → canonical URL + local folder + keywords |
| `<id>/*.md` | Markdown snapshots of official docs |

Current stacks (from `requirements.txt` / this repo): Google ADK, Gemini API, pypdf, pytest.

## Add docs manually

1. Add or edit an entry in `manifest.yaml` (`id`, `url`, `local_dir`, `keywords`).
2. Put markdown under `docs/tech/<local_dir>/`. Start the file with the canonical URL.
3. Keep excerpts faithful to the official page. Do not invent APIs.

## Refresh docs with the fetcher agent

The `docs_fetcher_agent` ADK agent fetches **only** URLs listed in `manifest.yaml` (or subpaths of those URLs) and writes markdown under `docs/tech/`.

```powershell
Copy-Item docs_fetcher_agent\.env.example docs_fetcher_agent\.env
# set GOOGLE_API_KEY
adk web --no-reload
# select docs_fetcher_agent, then:
# Fetch and refresh all sources in docs/tech/manifest.yaml
```

CLI: `adk run docs_fetcher_agent`

The fetcher never writes under `raw/` or `wiki/`.

## GitHub Action setup

Repo secret:

- `GOOGLE_API_KEY` — Gemini key used by `python -m pr_review`

`GITHUB_TOKEN` is provided by Actions (`pull-requests: write`).

Draft PRs are skipped. Reviews use `REQUEST_CHANGES` when any finding is a **blocker**, otherwise `COMMENT`. The bot never auto-approves.

## Local dry-run

Needs `GOOGLE_API_KEY` and `GITHUB_TOKEN` (a PAT with `repo` or `pull_requests: read` is enough for dry-run fetch).

Run from the **repository root** (paths below are relative):

```powershell
$env:GOOGLE_API_KEY = "..."
$env:GITHUB_TOKEN = "..."
python -m pr_review --pr 12 --docs docs/tech --dry-run
```

`--dry-run` prints the review JSON and does not post.

## Reuse in another repository

Copy these pieces (keep relative layout):

| Path | Role |
|------|------|
| `pr_review/` | Review CLI package |
| `docs/tech/` | Official doc snapshots + `manifest.yaml` |
| `.github/workflows/pr-docs-review.yml` | PR trigger |

In the other repo, run Actions from the checkout root with `--docs docs/tech` (already the default). Do not hard-code machine paths. Set the `GOOGLE_API_KEY` secret in that repo.

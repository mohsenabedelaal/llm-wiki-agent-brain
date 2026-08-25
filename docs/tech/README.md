# Official tech docs (optional corpus for portable PR review)

This tree is an **optional** plug-in for `pr_review`. The reviewer always runs as a
lead/senior engineer on the PR's real code changes. When `docs/tech/` is present, API
findings can also cite official docs.

Put **framework/library** docs here for *this* repository's stack. Do not mix product-domain
wikis into this tree.

See [`pr_review/README.md`](../../pr_review/README.md) for copy-paste into any project.

## Layout

| Path | Role |
|------|------|
| `manifest.yaml` | Stack → canonical URL + local folder + keywords |
| `<id>/*.md` | Markdown snapshots of official docs |

## Add or refresh

From the repository root:

```bash
python -m docs_fetcher_agent --propose
python -m docs_fetcher_agent --sync-manifest
python -m docs_fetcher_agent --refresh
```

`--sync-manifest` reads **direct** dependencies from project config files and looks up doc URLs via package registries (not web search). You can still edit `manifest.yaml` by hand. Page fetches are allowlisted to those URLs.

## GitHub Action

Repo secret `GOOGLE_API_KEY`. Workflow: `.github/workflows/pr-docs-review.yml`.
Draft PRs are skipped. `REQUEST_CHANGES` only when a finding is a **blocker**.

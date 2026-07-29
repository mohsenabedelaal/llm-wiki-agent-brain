# WIKI.md — Vault Conventions (ADK)

Condensed schema for the DistrictNex LLM Wiki. Agent runtime: Google ADK + Gemini. Inspired by Karpathy LLM Wiki / claude-obsidian behavior.

## Architecture

```
vault/
├── raw/                    # immutable sources — never write here
│   ├── manuals/            # equipment O&M / vendor PDFs
│   ├── reports/            # commissioning, TAB, fault PDFs
│   └── seed/               # markdown demo sources
├── wiki/                   # agent-generated knowledge
│   ├── index.md
│   ├── log.md
│   ├── hot.md
│   ├── sources/
│   ├── entities/
│   ├── concepts/
│   └── sessions/
├── AGENTS.md
├── WIKI.md
└── wiki_agent/             # Google ADK package
```

## Rules

- `raw/` is read-only. Never modify source files.
- `wiki/` is writable. Create, update, rename freely (prefer update over duplicate).
- Filenames: `lowercase-with-hyphens.md`.
- Wikilinks: `[[page-name]]` (match filename stem).
- Atomic notes: one concept/entity per page.
- Cite facts: `(source: filename.ext)`.
- Flag contradictions on **both** affected pages.

## Frontmatter (every page)

```yaml
---
type: source|entity|concept|session|meta
title: "Human Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
status: seed|developing|mature|evergreen
related: []
sources: []
---
```

## Page body

1. `# Title`
2. **Summary** — 1–2 sentences
3. Main content with `[[wikilinks]]` and `(source: …)` citations
4. Exact numeric specs / tables with **original units** when present
5. **Related pages**

## Catalog triad

| File | Role |
|------|------|
| `wiki/index.md` | Master catalog of all pages |
| `wiki/log.md` | Append-only ops log (newest at **bottom**) |
| `wiki/hot.md` | ~500-word recent-context cache (overwrite each update) |

## PDF / manual ingest

Accepted raw inputs: `.pdf`, `.md` (later `.txt` / images).

Extraction priority:

1. Equipment / entities
2. Exact numeric specs with units
3. Tables and schedules
4. Mode logic / sequences
5. Cross-source contradictions

When extracting from PDFs:

- Record document type, filename, and extraction caveats on the source page.
- Normalize important table rows into markdown tables or bullet specs on entity/concept pages.
- If parsing drops structure or units, say so — do not invent values.
- Local text extraction only (no cloud OCR in v1).

## Operations

### Ingest

1. List/read the source (`read_file` for `.md`, `read_pdf` for `.pdf`).
2. Create/update `wiki/sources/<slug>.md`.
3. Create/update entities and concepts; preserve exact specs.
4. Update `index.md`, append `log.md`, refresh `hot.md`.
5. Report pages created/updated.

### Query

1. Read `hot.md` → `index.md` → relevant pages only.
2. Answer from wiki only; cite pages.
3. If missing, say so; offer to save answer to `wiki/sessions/`.

### Lint

Check orphans, dead wikilinks, missing citations/units, contradictions, index drift. Report; do not auto-delete without asking.

### Save

File Q&A as `wiki/sessions/<slug>.md`; update index/log/hot.

# LLM Wiki Schema — DistrictNex / Picacity

You maintain this vault as an LLM Wiki for DistrictNex / Picacity building-operations knowledge (HVAC, electrical, sequences, KPI definitions, fault libraries).

This project uses **Google ADK + Gemini** as the agent runtime. Obsidian is the knowledge UI. ADK Web is for development/debug chat only.

Read and follow `WIKI.md` for full conventions. Summary:

1. `raw/` is **read-only**. Never modify files there (including PDFs under `raw/manuals/` and `raw/reports/`).
2. `wiki/` is your workspace. Create, update, and heavily interlink markdown using Obsidian `[[wiki-links]]`.
3. Page names: lowercase with hyphens. Prefer updating existing pages over duplicates — check `wiki/index.md` first.
4. Every page: YAML frontmatter + **Summary**, content with citations, then **Related pages**.
5. Every factual claim cites `(source: filename)`. Contradictions must be called out explicitly.
6. After every ingest or meaningful change: update `wiki/index.md`, append `wiki/log.md`, refresh `wiki/hot.md`.
7. On questions: read `wiki/hot.md` → `wiki/index.md` → relevant pages. Cite wiki pages. Offer to file valuable answers back.
8. Extract **tables and numeric specs carefully** into entity pages with exact values and units — these drive Overwatch alert baselines.
9. **PDF-first**: most real sources are manuals/reports as PDF. Use `read_pdf` for those; preserve units; never invent missing values.

## Common commands (via ADK Web / `adk run`)

- **Ingest**: "Ingest `raw/seed/<file>` and update the wiki."
- **Ingest PDF**: "Ingest `raw/manuals/<file>.pdf` without discussion."
- **Ingest without discussion**: "Ingest `raw/<path>` without discussion."
- **Query**: ask any building-ops question; answer from the wiki only.
- **Lint**: "Lint the wiki."
- **Save answer**: "Save that answer as a wiki page."

## Source layout

| Path | Purpose |
|------|---------|
| `raw/seed/` | Demo markdown sources (DAEP HVAC/electrical) |
| `raw/manuals/` | Vendor O&M / equipment PDFs |
| `raw/reports/` | Commissioning, TAB, fault-report PDFs |

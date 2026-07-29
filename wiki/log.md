# Log

Append-only operation log. Newest entries at the bottom.

---

## 2026-07-29 — vault scaffolded

- Created greenfield Google ADK LLM Wiki layout on `main`.
- Seeded five DAEP markdown sources under `raw/seed/`.
- Reserved `raw/manuals/` and `raw/reports/` for PDF ingest.

## 2026-07-29 — offline demo ingest (vault tools)

**Sources ingested**:
- `raw/seed/*.md` (five DAEP documents)
- `raw/manuals/sample-ahu-om-excerpt.pdf` (PDF fixture; verified 16.5 kW extraction)

**Created / updated**: sources, entities (ahu-3, lp-3, f-34), concepts, session answer, index/hot/log.

**Note**: Live Gemini ingest via ADK requires `wiki_agent/.env` with `GOOGLE_API_KEY`. See `scripts/adk_demo.py`.

## 2026-07-29 — seed markdown & PDF ingest completed

**Sources ingested**:
- `raw/seed/daep-ahu-commissioning-report-2019.md`
- `raw/seed/daep-ahu-om-manual-excerpt.md`
- `raw/seed/daep-ahu-sequence-of-operation.md`
- `raw/seed/daep-electrical-panel-schedule.md`
- `raw/seed/hvac-fault-library-fan-power-high.md`
- `raw/manuals/sample-ahu-om-excerpt.pdf` (PDF fixture; verified 16.5 kW baseline extraction)

**Pages created / updated**:
- `wiki/sources/daep-ahu-om-manual-excerpt.md`
- `wiki/sources/daep-ahu-commissioning-report-2019.md`
- `wiki/sources/daep-ahu-sequence-of-operation.md`
- `wiki/sources/daep-electrical-panel-schedule.md`
- `wiki/sources/hvac-fault-library-fan-power-high.md`
- `wiki/sources/sample-ahu-om-excerpt-pdf.md`
- `wiki/entities/ahu-3.md`
- `wiki/entities/lp-3.md`
- `wiki/entities/f-34.md`
- `wiki/concepts/standard-fan-power-baseline.md`
- `wiki/concepts/ahu-cooling-mode.md`
- `wiki/concepts/fan-pwr-high.md`
- `wiki/concepts/filter-differential-pressure.md`
- `wiki/index.md`
- `wiki/hot.md`
- `wiki/log.md`

## 2026-07-29 — ingest raw/manuals/S24AWN.pdf

**Sources ingested**:
- `raw/manuals/S24AWN.pdf` (LG Room Air Conditioner Owner's Manual, P/No. 3828A24010C)

**Pages created / updated**:
- `wiki/sources/lg-s24awn-manual.md`
- `wiki/entities/lg-s24awn.md`
- `wiki/concepts/split-ac-operating-modes.md`
- `wiki/index.md`
- `wiki/hot.md`
- `wiki/log.md`

## 2026-07-29 — ingest raw/manuals/Schneider MCCB.pdf

**Sources ingested**:
- `raw/manuals/Schneider MCCB.pdf` (Schneider Electric Compact NSX DC & Masterpact NW DC Catalogue, 2012)

**Pages created / updated**:
- `wiki/sources/schneider-mccb-dc-catalogue.md`
- `wiki/entities/compact-nsx-dc.md`
- `wiki/entities/masterpact-nw-dc.md`
- `wiki/concepts/dc-circuit-breaker-pole-configurations.md`
- `wiki/index.md`
- `wiki/hot.md`
- `wiki/log.md`

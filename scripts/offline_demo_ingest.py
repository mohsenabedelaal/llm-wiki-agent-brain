"""Offline demo: ingest seed markdown + sample PDF into wiki via vault tools.

Used when GOOGLE_API_KEY is not set. Live agent path: scripts/adk_demo.py
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from wiki_agent.tools import vault

TODAY = date.today().isoformat()


def page(path: str, body: str) -> None:
    result = vault.write_file(path, body.strip() + "\n")
    if result["status"] != "success":
        raise RuntimeError(f"Failed writing {path}: {result}")


def main() -> None:
    # Verify PDF tool works on sample manual
    pdf = vault.read_pdf("raw/manuals/sample-ahu-om-excerpt.pdf")
    if pdf["status"] != "success":
        raise RuntimeError(pdf)
    if "16.5 kW" not in pdf["content"]:
        raise RuntimeError("PDF fixture missing expected 16.5 kW text")

    page(
        "wiki/sources/daep-ahu-om-manual-excerpt.md",
        f"""---
type: source
title: "DAEP AHU O&M Manual Excerpt"
created: {TODAY}
updated: {TODAY}
tags: [hvac, om, baseline]
status: mature
related: ["[[ahu-3]]", "[[standard-fan-power-baseline]]"]
sources: ["daep-ahu-om-manual-excerpt.md"]
---

# DAEP AHU O&M Manual Excerpt

**Summary**: O&M R2 (2024) design schedule and fan-power baselines for AHU-1–AHU-4; monitoring source of truth for Overwatch.

## Key claims

- Design fan power baseline = expected average at design airflow, clean filters, **75°F** OA cooling mode. (source: daep-ahu-om-manual-excerpt.md)
- [[AHU-3]] design fan power baseline = **16.5 kW**; design airflow **14,000 CFM**; motor **30 HP**. (source: daep-ahu-om-manual-excerpt.md)
- Exception: power **>20%** above baseline for **>30 minutes** with airflow within **±5%** design. (source: daep-ahu-om-manual-excerpt.md)
- At 75°F OA, mechanical cooling is expected and does **not** explain high fan power. (source: daep-ahu-om-manual-excerpt.md)

## Related pages

- [[ahu-3]]
- [[standard-fan-power-baseline]]
- [[fan-pwr-high]]
""",
    )

    page(
        "wiki/sources/daep-ahu-sequence-of-operation.md",
        f"""---
type: source
title: "DAEP AHU Sequence of Operation"
created: {TODAY}
updated: {TODAY}
tags: [hvac, sequence]
status: mature
related: ["[[ahu-cooling-mode]]", "[[ahu-3]]", "[[f-34]]"]
sources: ["daep-ahu-sequence-of-operation.md"]
---

# DAEP AHU Sequence of Operation

**Summary**: Mode selection by OA dry-bulb; at ≥70°F cooling mode applies for all AHUs including AHU-3.

## Mode table

| Outdoor air dry-bulb | Mode |
|----------------------|------|
| OA ≥ 70°F | Cooling |
| 55°F ≤ OA < 70°F | Economizer / mixed air |
| OA < 55°F | Heating |

(source: daep-ahu-sequence-of-operation.md)

## Related pages

- [[ahu-cooling-mode]]
- [[ahu-3]]
- [[f-34]]
""",
    )

    page(
        "wiki/sources/daep-electrical-panel-schedule.md",
        f"""---
type: source
title: "DAEP Electrical Panel Schedule LP-3"
created: {TODAY}
updated: {TODAY}
tags: [electrical, panel]
status: mature
related: ["[[lp-3]]", "[[ahu-3]]", "[[f-34]]"]
sources: ["daep-electrical-panel-schedule.md"]
---

# DAEP Electrical Panel Schedule LP-3

**Summary**: Floor 3 panel LP-3 circuit excerpt; AHU-3 fan VFD on Circuit 7.

## Related pages

- [[lp-3]]
- [[ahu-3]]
- [[f-34]]
""",
    )

    page(
        "wiki/sources/daep-ahu-commissioning-report-2019.md",
        f"""---
type: source
title: "DAEP AHU Commissioning Report 2019"
created: {TODAY}
updated: {TODAY}
tags: [commissioning, contradiction]
status: mature
related: ["[[ahu-3]]", "[[standard-fan-power-baseline]]"]
sources: ["daep-ahu-commissioning-report-2019.md"]
---

# DAEP AHU Commissioning Report 2019

**Summary**: As-built CX snapshots. AHU-3 measured **15.8 kW** — not the Overwatch monitoring baseline.

> [!contradiction]
> CX 15.8 kW (2019) vs O&M design baseline 16.5 kW (2024). Prefer **16.5 kW** for monitoring. (sources: daep-ahu-commissioning-report-2019.md, daep-ahu-om-manual-excerpt.md)

## Related pages

- [[ahu-3]]
- [[standard-fan-power-baseline]]
""",
    )

    page(
        "wiki/sources/hvac-fault-library-fan-power-high.md",
        f"""---
type: source
title: "HVAC Fault Library FAN-PWR-HIGH"
created: {TODAY}
updated: {TODAY}
tags: [fault, fan]
status: mature
related: ["[[fan-pwr-high]]", "[[filter-differential-pressure]]"]
sources: ["hvac-fault-library-fan-power-high.md"]
---

# HVAC Fault Library FAN-PWR-HIGH

**Summary**: Ordered cause list and DAEP AHU-3 checks for supply fan power >20% above baseline.

## Related pages

- [[fan-pwr-high]]
- [[filter-differential-pressure]]
- [[ahu-3]]
""",
    )

    page(
        "wiki/sources/sample-ahu-om-excerpt-pdf.md",
        f"""---
type: source
title: "Sample AHU O&M Excerpt PDF"
created: {TODAY}
updated: {TODAY}
tags: [pdf, manual, hvac]
status: seed
related: ["[[ahu-3]]", "[[standard-fan-power-baseline]]"]
sources: ["sample-ahu-om-excerpt.pdf"]
---

# Sample AHU O&M Excerpt PDF

**Summary**: Synthetic PDF fixture under `raw/manuals/` validating PDF text extraction into the wiki.

**Document type**: equipment O&M excerpt (PDF)  
**Filename**: `sample-ahu-om-excerpt.pdf`  
**Extraction**: local pypdf text extraction (no OCR)

## Extracted specs

| Field | Value |
|-------|-------|
| Equipment | AHU-3 / Trane CSAA-40 |
| Design supply airflow | 14,000 CFM |
| Fan motor | 30 HP |
| Design fan power baseline | **16.5 kW** at 75°F OA |
| Design SAT | 55°F |
| Cooling coil | 52 tons |
| Filter | MERV 14; replace ΔP > 1.5 in. w.g. |
| Minimum OA | 2,800 CFM |

(source: sample-ahu-om-excerpt.pdf)

## Related pages

- [[ahu-3]]
- [[standard-fan-power-baseline]]
""",
    )

    page(
        "wiki/entities/ahu-3.md",
        f"""---
type: entity
title: "AHU-3"
created: {TODAY}
updated: {TODAY}
tags: [ahu, hvac, entity]
status: mature
related: ["[[lp-3]]", "[[f-34]]", "[[standard-fan-power-baseline]]", "[[ahu-cooling-mode]]", "[[fan-pwr-high]]"]
sources: ["daep-ahu-om-manual-excerpt.md", "daep-ahu-commissioning-report-2019.md", "daep-electrical-panel-schedule.md", "sample-ahu-om-excerpt.pdf"]
---

# AHU-3

**Summary**: Third-floor AHU (Trane CSAA-40). Highest design airflow/fan power on the DAEP schedule; Circuit 7 on [[lp-3]].

## Design data (O&M Table 2)

| Field | Value |
|-------|-------|
| Floor | 3 |
| Supply airflow (design) | 14,000 CFM |
| Fan motor | 30 HP |
| Design fan power baseline | **16.5 kW** |
| Design SAT | 55°F |
| Cooling coil | 52 tons |
| Filter MERV | 14 |
| Minimum OA | 2,800 CFM |

(source: daep-ahu-om-manual-excerpt.md; also sample-ahu-om-excerpt.pdf)

## Electrical feed

- Fan VFD: [[lp-3]] **Circuit 7** (60A, 3-pole)
- Controls: Circuit 9
- Fire damper [[f-34]]: Circuit 13

(source: daep-electrical-panel-schedule.md)

## Commissioning vs design baseline

Commissioning (2019) measured **15.8 kW** at ~13,850 CFM. O&M R2 monitoring baseline is **16.5 kW**.

> [!contradiction]
> Do not use 15.8 kW as the Overwatch baseline. Prefer 16.5 kW. (sources: daep-ahu-commissioning-report-2019.md, daep-ahu-om-manual-excerpt.md)

## Related pages

- [[standard-fan-power-baseline]]
- [[ahu-cooling-mode]]
- [[fan-pwr-high]]
- [[f-34]]
- [[lp-3]]
""",
    )

    page(
        "wiki/entities/lp-3.md",
        f"""---
type: entity
title: "LP-3"
created: {TODAY}
updated: {TODAY}
tags: [electrical, panel]
status: mature
related: ["[[ahu-3]]", "[[f-34]]"]
sources: ["daep-electrical-panel-schedule.md"]
---

# LP-3

**Summary**: Floor 3 lighting/power panel (480Y/277V) feeding AHU-3 fan VFD (Circuit 7), controls (9), and F-34 (13).

## Selected circuits

| Circuit | Breaker | Load |
|---------|---------|------|
| 7 | 60A / 3P | [[ahu-3]] supply fan VFD — **primary power KPI feed** |
| 9 | 30A / 3P | AHU-3 controls (not fan power) |
| 13 | 20A / 1P | [[f-34]] actuator / status |

(source: daep-electrical-panel-schedule.md)

## Related pages

- [[ahu-3]]
- [[f-34]]
- [[fan-pwr-high]]
""",
    )

    page(
        "wiki/entities/f-34.md",
        f"""---
type: entity
title: "F-34"
created: {TODAY}
updated: {TODAY}
tags: [damper, safety]
status: mature
related: ["[[ahu-3]]", "[[lp-3]]", "[[fan-pwr-high]]"]
sources: ["daep-ahu-sequence-of-operation.md", "daep-electrical-panel-schedule.md", "hvac-fault-library-fan-power-high.md"]
---

# F-34

**Summary**: Fire/smoke damper on AHU-3 third-floor supply trunk. Must prove open before fan enable; check during FAN-PWR-HIGH investigations.

## Related pages

- [[ahu-3]]
- [[lp-3]]
- [[fan-pwr-high]]
""",
    )

    page(
        "wiki/concepts/standard-fan-power-baseline.md",
        f"""---
type: concept
title: "Standard fan power baseline"
created: {TODAY}
updated: {TODAY}
tags: [kpi, baseline]
status: mature
related: ["[[ahu-3]]", "[[fan-pwr-high]]"]
sources: ["daep-ahu-om-manual-excerpt.md", "daep-ahu-commissioning-report-2019.md"]
---

# Standard fan power baseline

**Summary**: Design expected supply-fan electrical power at design airflow and defined OA conditions; Overwatch comparison point for FAN-PWR-HIGH.

## Definition

Expected average power at design airflow with clean filters and OA at **75°F** dry-bulb (cooling). (source: daep-ahu-om-manual-excerpt.md)

## DAEP baselines (O&M R2)

| Unit | Design fan power baseline (kW) |
|------|--------------------------------|
| AHU-1 | 14.2 |
| AHU-2 | 13.8 |
| [[ahu-3]] | **16.5** |
| AHU-4 | 12.0 |

(source: daep-ahu-om-manual-excerpt.md)

## Exception threshold

Power **>20%** above baseline for **>30 minutes**, airflow within **±5%** design → [[fan-pwr-high]]. For AHU-3 ≈ **19.8 kW**.

## Not commissioning snapshots

2019 CX measured AHU-3 at **15.8 kW** — as-built day-one data, not the monitoring baseline. (source: daep-ahu-commissioning-report-2019.md)

## Related pages

- [[ahu-3]]
- [[fan-pwr-high]]
- [[ahu-cooling-mode]]
""",
    )

    page(
        "wiki/concepts/ahu-cooling-mode.md",
        f"""---
type: concept
title: "AHU cooling mode"
created: {TODAY}
updated: {TODAY}
tags: [sequence, cooling]
status: mature
related: ["[[ahu-3]]", "[[standard-fan-power-baseline]]"]
sources: ["daep-ahu-sequence-of-operation.md"]
---

# AHU cooling mode

**Summary**: OA ≥ 70°F → chilled-water coil active, economizer locked out. At 75°F OA, cooling mode is expected.

## Diagnostic implication

At **75°F outdoor air**, elevated fan power **cannot** be explained by wrong mode. (source: daep-ahu-sequence-of-operation.md)

## Related pages

- [[ahu-3]]
- [[standard-fan-power-baseline]]
- [[f-34]]
""",
    )

    page(
        "wiki/concepts/fan-pwr-high.md",
        f"""---
type: concept
title: "FAN-PWR-HIGH"
created: {TODAY}
updated: {TODAY}
tags: [fault, fan]
status: mature
related: ["[[standard-fan-power-baseline]]", "[[filter-differential-pressure]]", "[[ahu-3]]"]
sources: ["hvac-fault-library-fan-power-high.md"]
---

# FAN-PWR-HIGH

**Summary**: Supply fan power >20% above standard baseline for >30 minutes while airflow near design.

## Likely causes (priority)

1. Loaded filters ([[filter-differential-pressure]])
2. Cooling-coil fouling
3. Motor bearing wear
4. Damper / duct restriction (include [[f-34]])
5. VFD / control issue

(source: hvac-fault-library-fan-power-high.md)

## DAEP [[ahu-3]] checks

1. Confirm [[ahu-cooling-mode]] at 75°F OA (expected — not itself a fault).
2. Compare to **16.5 kW** baseline, not 15.8 kW CX snapshot.
3. Verify [[f-34]] open.
4. Confirm KPI on [[lp-3]] Circuit 7.

## Related pages

- [[standard-fan-power-baseline]]
- [[ahu-3]]
- [[filter-differential-pressure]]
""",
    )

    page(
        "wiki/concepts/filter-differential-pressure.md",
        f"""---
type: concept
title: "Filter differential pressure"
created: {TODAY}
updated: {TODAY}
tags: [maintenance, filters]
status: mature
related: ["[[fan-pwr-high]]", "[[ahu-3]]"]
sources: ["daep-ahu-om-manual-excerpt.md", "hvac-fault-library-fan-power-high.md"]
---

# Filter differential pressure

**Summary**: First check for elevated AHU fan power. Replace filters if ΔP exceeds 1.5 in. w.g.

- Loaded filters are the top-ranked cause of [[fan-pwr-high]]. (source: hvac-fault-library-fan-power-high.md)
- Replace when ΔP **> 1.5 in. w.g.** (source: daep-ahu-om-manual-excerpt.md)

## Related pages

- [[fan-pwr-high]]
- [[ahu-3]]
""",
    )

    page(
        "wiki/sessions/ahu-3-high-power-at-75f.md",
        f"""---
type: session
title: "AHU-3 high power at 75°F OA"
created: {TODAY}
updated: {TODAY}
tags: [demo, session]
status: developing
related: ["[[ahu-3]]", "[[fan-pwr-high]]", "[[ahu-cooling-mode]]"]
sources: ["daep-ahu-om-manual-excerpt.md", "daep-ahu-sequence-of-operation.md", "daep-ahu-commissioning-report-2019.md", "hvac-fault-library-fan-power-high.md"]
---

# AHU-3 high power at 75°F OA

**Summary**: Demo Q&A — 75°F OA cooling mode is expected and does not explain ~20% high fan power; investigate as FAN-PWR-HIGH against 16.5 kW baseline.

## Question

Why is [[ahu-3]] using 20% more power than its baseline at 75°F outdoor air?

## Answer

**75°F OA does not explain the excess power.** [[ahu-cooling-mode]] applies (OA ≥ 70°F).

- Monitoring baseline = **16.5 kW** ([[standard-fan-power-baseline]]); ~20% exception ≈ **19.8 kW** → [[fan-pwr-high]].
- Likely causes (order): [[filter-differential-pressure]], coil fouling, bearings, [[f-34]], VFD/controls.
- Confirm KPI on [[lp-3]] Circuit 7 (not Circuit 9).

### Contradiction

O&M **16.5 kW** vs commissioning **15.8 kW** — do not use 15.8 kW as Overwatch baseline.

## Related pages

- [[ahu-3]]
- [[standard-fan-power-baseline]]
- [[ahu-cooling-mode]]
- [[fan-pwr-high]]
""",
    )

    page(
        "wiki/index.md",
        f"""# Index

Master catalog of this wiki. The agent updates this after every ingest.

**Purpose**: DistrictNex / Picacity building-ops knowledge (HVAC + electrical) for LLM Wiki + Google ADK demo.

**Last catalog refresh**: {TODAY}

## Sources

- [[daep-ahu-om-manual-excerpt]] — AHU O&M R2 design schedule + baselines
- [[daep-ahu-sequence-of-operation]] — Mode selection and cooling sequence
- [[daep-electrical-panel-schedule]] — Panel LP-3 circuit schedule excerpt
- [[daep-ahu-commissioning-report-2019]] — As-built CX values (contradicts O&M baseline)
- [[hvac-fault-library-fan-power-high]] — FAN-PWR-HIGH fault procedure
- [[sample-ahu-om-excerpt-pdf]] — Synthetic PDF manual fixture (PDF ingest path)

## Entities

- [[ahu-3]] — Floor 3 AHU; 16.5 kW design baseline; Circuit 7 feed
- [[lp-3]] — Floor 3 electrical panel
- [[f-34]] — AHU-3 supply trunk fire/smoke damper

## Concepts

- [[standard-fan-power-baseline]] — Design monitoring baselines + 20% rule
- [[ahu-cooling-mode]] — OA ≥70°F → mechanical cooling
- [[fan-pwr-high]] — Fault definition and ordered checks
- [[filter-differential-pressure]] — First mechanical check for high fan power

## Sessions / answers

- [[ahu-3-high-power-at-75f]] — Demo Q&A: 20% above baseline at 75°F OA
""",
    )

    vault.append_log(
        f"""## {TODAY} — offline demo ingest (vault tools)

**Sources ingested**:
- `raw/seed/*.md` (five DAEP documents)
- `raw/manuals/sample-ahu-om-excerpt.pdf` (PDF fixture; verified 16.5 kW extraction)

**Created / updated**: sources, entities (ahu-3, lp-3, f-34), concepts, session answer, index/hot/log.

**Note**: Live Gemini ingest via ADK requires `wiki_agent/.env` with `GOOGLE_API_KEY`. See `scripts/adk_demo.py`.
"""
    )

    vault.update_hot(
        f"""# Hot cache

**Status**: Demo wiki populated ({TODAY}). PDF ingest path verified on sample-ahu-om-excerpt.pdf.

**Core facts for AHU-3 @ 75°F OA**:
- [[ahu-3]] monitoring baseline = **16.5 kW** (O&M). CX 15.8 kW is **not** the baseline.
- [[ahu-cooling-mode]] at 75°F OA is expected — not explanatory of high power.
- Exception ≈ **19.8 kW** sustained near design airflow → [[fan-pwr-high]].
- Checks: [[filter-differential-pressure]], coil, bearings, [[f-34]], KPI on [[lp-3]] Circuit 7.

**Next**: Set `GOOGLE_API_KEY` in `wiki_agent/.env`, then `adk web --no-reload` or `python scripts/adk_demo.py`.
"""
    )

    print("Offline demo ingest complete.")
    print("PDF chars extracted:", pdf["chars"])
    listing = vault.list_vault("wiki")
    print("wiki entries:", [e["path"] for e in listing.get("entries", [])])


if __name__ == "__main__":
    main()

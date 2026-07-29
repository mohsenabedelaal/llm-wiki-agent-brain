---
type: session
title: "AHU-3 high power at 75°F OA"
created: 2026-07-29
updated: 2026-07-29
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

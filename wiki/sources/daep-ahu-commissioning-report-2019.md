---
type: source
title: "DAEP AHU Commissioning Report 2019"
created: 2026-07-29
updated: 2026-07-29
tags: [commissioning, contradiction, hvac]
status: mature
related: ["[[ahu-3]]", "[[standard-fan-power-baseline]]"]
sources: ["daep-ahu-commissioning-report-2019.md"]
---

# DAEP AHU Commissioning Report 2019

**Summary**: As-built commissioning snapshots (Doc ID: DAEP-CX-AHU-2019, Date: 2019-08-22). Recorded as-tested fan power at 78°F OAT during substantial completion.

## Measured fan power at design airflow (2019-08-22, 78°F OAT)

| Unit | Measured supply CFM | Measured fan power (kW) | OAT during test (°F) | CX Notes |
|------|---------------------|-------------------------|----------------------|----------|
| AHU-1 | 11,900 | 13.9 | 78 | Within 3% of design |
| AHU-2 | 11,400 | 13.5 | 78 | Within 3% of design |
| [[ahu-3]] | 13,850 | **15.8** | 78 | ~4% below 2024 O&M baseline (16.5 kW) |
| AHU-4 | 9,950 | 11.7 | 78 | Within 3% of design |

(source: daep-ahu-commissioning-report-2019.md)

## Explicit contradiction notice

> [!contradiction]
> **AHU-3 Fan Power Baseline Contradiction**:
> - Commissioning Report (2019): **15.8 kW** measured at 13,850 CFM. (source: daep-ahu-commissioning-report-2019.md)
> - O&M Manual R2 (2024): **16.5 kW** design fan power baseline. (source: daep-ahu-om-manual-excerpt.md)
> 
> **Resolution**: Commissioning is day-one snapshot. Overwatch monitoring baselines must use the 2024 O&M design baseline (**16.5 kW**). Citing 15.8 kW as the baseline is a documentation error.

## Safety & interlocks tested

- Fire/smoke damper [[f-34]] proved open during functional testing. Fan enable interlocked with F-34 status. (source: daep-ahu-commissioning-report-2019.md)

## Related pages

- [[ahu-3]]
- [[standard-fan-power-baseline]]
- [[f-34]]

---
type: concept
title: "Standard fan power baseline"
created: 2026-07-29
updated: 2026-07-29
tags: [kpi, baseline, concept]
status: mature
related: ["[[ahu-3]]", "[[fan-pwr-high]]", "[[ahu-cooling-mode]]"]
sources: ["daep-ahu-om-manual-excerpt.md", "daep-ahu-commissioning-report-2019.md", "sample-ahu-om-excerpt.pdf"]
---

# Standard fan power baseline

**Summary**: Expected average supply fan electrical power (kW) at design airflow with clean filters and outdoor air at 75°F dry-bulb in cooling mode. Serves as the primary monitoring baseline for Overwatch fault detection.

## DAEP Design Fan Power Baselines (O&M Table 2)

| Unit | Design Airflow (CFM) | Fan Motor (HP) | Design Fan Power Baseline (kW) |
|------|----------------------|----------------|--------------------------------|
| AHU-1 | 12,000 | 25 | 14.2 |
| AHU-2 | 11,500 | 25 | 13.8 |
| [[ahu-3]] | **14,000** | **30** | **16.5** |
| AHU-4 | 10,000 | 20 | 12.0 |

(sources: daep-ahu-om-manual-excerpt.md, sample-ahu-om-excerpt.pdf)

## Threshold for exception (+20% Rule)

An exception is triggered when fan power exceeds the baseline by **> 20%** for **> 30 minutes** while supply airflow is within **±5%** of design CFM.

- For **[[ahu-3]]**: 16.5 kW × 1.20 = **19.8 kW** threshold. (sources: daep-ahu-om-manual-excerpt.md, hvac-fault-library-fan-power-high.md)

## CX vs O&M contradiction

> [!contradiction]
> - 2019 CX Report measured AHU-3 fan power at **15.8 kW** (13,850 CFM, 78°F OAT). (source: daep-ahu-commissioning-report-2019.md)
> - 2024 O&M R2 defines the monitoring baseline as **16.5 kW**. (source: daep-ahu-om-manual-excerpt.md)
> 
> **Resolution**: Always use **16.5 kW** for AHU-3 monitoring.

## Related pages

- [[ahu-3]]
- [[fan-pwr-high]]
- [[ahu-cooling-mode]]

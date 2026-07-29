---
type: source
title: "DAEP AHU O&M Manual Excerpt"
created: 2026-07-29
updated: 2026-07-29
tags: [hvac, om, baseline]
status: mature
related: ["[[ahu-3]]", "[[standard-fan-power-baseline]]", "[[fan-pwr-high]]"]
sources: ["daep-ahu-om-manual-excerpt.md"]
---

# DAEP AHU O&M Manual Excerpt

**Summary**: O&M R2 (2024-09-12, Doc ID: DAEP-HVAC-OM-AHU-2024-R2) design schedule and fan-power baselines for AHU-1 through AHU-4; monitoring source of truth for Overwatch.

## Unit schedule (design baselines)

| Unit | Floor | Supply airflow (CFM) | Fan motor (HP) | Design fan power baseline (kW) | Design SAT (°F) | Cooling coil (tons) | Filter MERV |
|------|-------|----------------------|----------------|--------------------------------|-----------------|---------------------|-------------|
| AHU-1 | 1 | 12,000 | 25 | 14.2 | 55 | 45 | 13 |
| AHU-2 | 2 | 11,500 | 25 | 13.8 | 55 | 42 | 13 |
| [[ahu-3]] | 3 | 14,000 | 30 | **16.5** | 55 | 52 | 14 |
| AHU-4 | 4 | 10,000 | 20 | 12.0 | 55 | 38 | 13 |

(source: daep-ahu-om-manual-excerpt.md)

## Key claims & operating envelopes

- **Baseline condition**: Expected average fan power draw at design airflow with clean filters and outdoor air at **75°F** dry-bulb in cooling mode. (source: daep-ahu-om-manual-excerpt.md)
- **Cooling envelope**: OA ≥ 70°F DB → Mechanical cooling mode, expected power near 100% design baseline. (source: daep-ahu-om-manual-excerpt.md)
- **Economizer envelope**: 55–70°F DB → Mixed air / free cooling, power typically 85–95% baseline. (source: daep-ahu-om-manual-excerpt.md)
- **Heating envelope**: < 55°F DB → Heating + min OA, power typically 70–90% cooling baseline. (source: daep-ahu-om-manual-excerpt.md)
- **Exception threshold**: Sustained power **>20% above** baseline for **>30 minutes** while supply airflow is within **±5%** of design CFM. (source: daep-ahu-om-manual-excerpt.md)
- **AHU-3 nameplate**: Trane CSAA-40, Serial TX-DAEP-AHU3-2019, 30 HP direct-drive VFD fan, 2-row chilled water coil, minimum OA = 2,800 CFM. (source: daep-ahu-om-manual-excerpt.md)

## Related pages

- [[ahu-3]]
- [[standard-fan-power-baseline]]
- [[fan-pwr-high]]

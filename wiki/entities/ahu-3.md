---
type: entity
title: "AHU-3"
created: 2026-07-29
updated: 2026-07-29
tags: [ahu, hvac, entity]
status: mature
related: ["[[lp-3]]", "[[f-34]]", "[[standard-fan-power-baseline]]", "[[ahu-cooling-mode]]", "[[fan-pwr-high]]"]
sources: ["daep-ahu-om-manual-excerpt.md", "daep-ahu-commissioning-report-2019.md", "daep-electrical-panel-schedule.md", "daep-ahu-sequence-of-operation.md", "sample-ahu-om-excerpt.pdf"]
---

# AHU-3

**Summary**: Floor 3 Air Handling Unit (Trane CSAA-40). Serves floor 3 open office and meeting rooms with 14,000 CFM design airflow and 30 HP fan motor. Primary electrical feed is Circuit 7 on [[lp-3]].

## Design equipment schedule

| Parameter | Value | Source |
|-----------|-------|--------|
| Floor | 3 | O&M Table 2 |
| Manufacturer & Model | Trane CSAA-40 | O&M Sec 3 |
| Serial Number | TX-DAEP-AHU3-2019 | O&M Sec 3 |
| Design Supply Airflow | 14,000 CFM | O&M Table 2 / PDF |
| Fan Motor | 30 HP (direct-drive VFD) | O&M Table 2 / PDF |
| **Design Fan Power Baseline** | **16.5 kW** (at 75°F OA) | O&M Table 2 / PDF |
| Design Supply Air Temp (SAT) | 55°F | O&M Table 2 / PDF |
| Cooling Coil Capacity | 52 tons (2-row chilled water) | O&M Table 2 / PDF |
| Filter Rating | MERV 14 | O&M Table 2 / PDF |
| Minimum Outdoor Air | 2,800 CFM | O&M Sec 3 / PDF |

(sources: daep-ahu-om-manual-excerpt.md, sample-ahu-om-excerpt.pdf)

## Electrical feeds & interlocks

- **Fan Power Feed**: [[lp-3]] **Circuit 7** (60A, 3-pole, 480V) — bound to fan power KPI. (source: daep-electrical-panel-schedule.md)
- **Control Power Feed**: [[lp-3]] Circuit 9 (30A, 3-pole). (source: daep-electrical-panel-schedule.md)
- **Fire/Smoke Damper Feed**: [[lp-3]] Circuit 13 (20A, 1-pole) feeding actuator for [[f-34]] on 3rd floor supply trunk. (source: daep-electrical-panel-schedule.md)

## Sequence of operation & mode rules

- At **OA ≥ 70°F** (e.g. 75°F OA): [[ahu-cooling-mode\|Mechanical Cooling Mode]] (chilled water active, economizer locked out, SAT setpoint 55°F, static setpoint 1.2 in. w.g.). (source: daep-ahu-sequence-of-operation.md)
- High power threshold: Power **> 20% above baseline** (≈ **19.8 kW**) for **>30 minutes** at design CFM triggers [[fan-pwr-high]]. (sources: daep-ahu-om-manual-excerpt.md, hvac-fault-library-fan-power-high.md)

## Commissioning vs O&M baseline contradiction

> [!contradiction]
> - **2019 CX Report**: Recorded measured power of **15.8 kW** at 13,850 CFM and 78°F OAT. (source: daep-ahu-commissioning-report-2019.md)
> - **2024 O&M Manual R2**: Sets standard design fan power baseline to **16.5 kW**. (source: daep-ahu-om-manual-excerpt.md)
> 
> **Rule**: Use **16.5 kW** as the Overwatch monitoring baseline. Commissioning 15.8 kW is an as-built snapshot only.

## Related pages

- [[lp-3]]
- [[f-34]]
- [[standard-fan-power-baseline]]
- [[ahu-cooling-mode]]
- [[fan-pwr-high]]

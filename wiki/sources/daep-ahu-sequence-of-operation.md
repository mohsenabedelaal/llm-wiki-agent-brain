---
type: source
title: "DAEP AHU Sequence of Operation"
created: 2026-07-29
updated: 2026-07-29
tags: [hvac, sequence, controls]
status: mature
related: ["[[ahu-cooling-mode]]", "[[ahu-3]]", "[[f-34]]", "[[standard-fan-power-baseline]]"]
sources: ["daep-ahu-sequence-of-operation.md"]
---

# DAEP AHU Sequence of Operation

**Summary**: BAS sequence of operation (Doc ID: DAEP-HVAC-SOO-AHU-2023, Rev: 2023-11-02) covering mode selection, cooling sequence, and safety interlocks for AHU-1 through AHU-4.

## Mode selection by outdoor air dry-bulb

| Outdoor air dry-bulb | Mode | Description |
|----------------------|------|-------------|
| OA ≥ 70°F | [[ahu-cooling-mode\|Cooling]] | Chilled-water coil active; economizer locked out |
| 55°F ≤ OA < 70°F | Economizer / mixed air | Free cooling preferred when OA enthalpy allows |
| OA < 55°F | Heating | Hot-water reheat as needed; OA at minimum (2,800 CFM for [[ahu-3]]) |

(source: daep-ahu-sequence-of-operation.md)

## Cooling mode sequence details ([[ahu-3]])

1. Occupancy schedule ON → unit start command.
2. Supply fan ramps via VFD to maintain duct static pressure setpoint = **1.2 in. w.g.**
3. Outdoor air damper opens to minimum OA (**2,800 CFM**).
4. Chilled-water valve modulates to maintain supply air temperature setpoint (**SAT = 55°F**).
5. "SAT not met" alarm raised if SAT cannot be met within 15 minutes.
6. Return air temperature (RAT) monitored for zone load.

(source: daep-ahu-sequence-of-operation.md)

## Power vs airflow diagnostics

- **Airflow ≈ design, Power ≫ baseline**: Investigate mechanical / filter / coil / damper issues.
- **Airflow ≫ design, Power ≫ baseline**: Investigate static pressure setpoint, zone dampers, VFD max limit.
- **Airflow ≪ design, Power high**: Investigate sensor calibration, drive mechanicals.

(source: daep-ahu-sequence-of-operation.md)

## Safety interlocks

- **Freeze protection**: Mixed air < 38°F → trip to heating / emergency OA close.
- **Smoke detector**: Fan stop, OA dampers close, alarm to fire panel.
- **Fire/smoke dampers**: Damper [[f-34]] (AHU-3 supply trunk) must prove open before fan enable.

(source: daep-ahu-sequence-of-operation.md)

## Related pages

- [[ahu-cooling-mode]]
- [[ahu-3]]
- [[f-34]]
- [[standard-fan-power-baseline]]

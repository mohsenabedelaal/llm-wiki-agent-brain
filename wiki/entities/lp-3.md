---
type: entity
title: "LP-3"
created: 2026-07-29
updated: 2026-07-29
tags: [electrical, panel, entity]
status: mature
related: ["[[ahu-3]]", "[[f-34]]", "[[fan-pwr-high]]"]
sources: ["daep-electrical-panel-schedule.md"]
---

# LP-3

**Summary**: Lighting and Power Panel LP-3 located on Floor 3 (480Y/277V, 3-phase, 4-wire, 400A main breaker). Serves Floor 3 lighting, receptacles, pump P-3, and [[ahu-3]].

## Selected circuit schedule

| Circuit | Breaker | Poles | Load description | Fed equipment | Notes |
|---------|---------|-------|------------------|---------------|-------|
| 1 | 20A | 1 | Lighting — open office west | Branch panel | Non-HVAC |
| 3 | 20A | 1 | Lighting — open office east | Branch panel | Non-HVAC |
| 5 | 30A | 2 | Receptacles — meeting rooms | — | Non-HVAC |
| 7 | **60A** | **3** | **[[ahu-3]] supply fan VFD** | **AHU-3 fan motor (30 HP)** | **Primary fan power KPI feed** |
| 9 | 30A | 3 | [[ahu-3]] controls & actuators | Control panel | Control power only |
| 11 | 40A | 3 | Chilled water pump P-3 | Pump P-3 | Plant side |
| 13 | 20A | 1 | Fire damper [[f-34]] actuator | Damper F-34 | Must remain energized |
| 15 | 100A | 3 | Spare / future | — | Reserved |
| 17 | 50A | 3 | Elevator machine room HVAC | DX unit | Not AHU-3 |

(source: daep-electrical-panel-schedule.md)

## Diagnostic notes

- Fan power monitoring KPIs for [[ahu-3]] must be mapped to **Circuit 7**.
- Circuit 13 de-energization prevents damper [[f-34]] from proving open and trips the fan enable interlock.

## Related pages

- [[ahu-3]]
- [[f-34]]
- [[fan-pwr-high]]

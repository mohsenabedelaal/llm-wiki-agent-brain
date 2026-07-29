---
type: source
title: "DAEP Electrical Panel Schedule LP-3"
created: 2026-07-29
updated: 2026-07-29
tags: [electrical, panel, schedule]
status: mature
related: ["[[lp-3]]", "[[ahu-3]]", "[[f-34]]"]
sources: ["daep-electrical-panel-schedule.md"]
---

# DAEP Electrical Panel Schedule LP-3

**Summary**: Floor 3 panel LP-3 schedule excerpt (Doc ID: DAEP-ELEC-PNL-LP3-2022, Rev: 2022-06-18). Voltage: 480Y/277V, 3-phase, 4-wire, 400A main breaker.

## Circuit schedule (excerpt)

| Circuit | Breaker (A) | Poles | Load description | Fed equipment | Notes |
|---------|-------------|-------|------------------|---------------|-------|
| 1 | 20 | 1 | Lighting — open office west | Lighting panel branch | Non-HVAC |
| 3 | 20 | 1 | Lighting — open office east | Lighting panel branch | Non-HVAC |
| 5 | 30 | 2 | Receptacles — meeting rooms | — | Non-HVAC |
| 7 | 60 | 3 | [[ahu-3]] supply fan VFD | AHU-3 fan motor (30 HP) | **Primary AHU-3 fan power feed** |
| 9 | 30 | 3 | [[ahu-3]] controls & damper actuators | AHU-3 control panel | Control power only |
| 11 | 40 | 3 | Chilled water pump P-3 (floor) | Pump P-3 | Plant side |
| 13 | 20 | 1 | Fire damper [[f-34]] actuator / status | Damper F-34 | Must remain energized |
| 15 | 100 | 3 | Spare / future | — | Reserved |
| 17 | 50 | 3 | Elevator machine room HVAC | Small DX unit | Not AHU-3 |

(source: daep-electrical-panel-schedule.md)

## Key Overwatch monitoring notes

- **AHU-3 Fan Power KPI**: Bound to **Circuit 7** (60A/3P feeder for 30 HP motor), not Circuit 9 (controls). (source: daep-electrical-panel-schedule.md)
- **Interlock dependencies**: Circuit 13 loss prevents damper [[f-34]] from proving open and blocks fan enable. (source: daep-electrical-panel-schedule.md)

## Related pages

- [[lp-3]]
- [[ahu-3]]
- [[f-34]]

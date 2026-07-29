---
type: source
title: "HVAC Fault Library FAN-PWR-HIGH"
created: 2026-07-29
updated: 2026-07-29
tags: [fault, library, fan]
status: mature
related: ["[[fan-pwr-high]]", "[[filter-differential-pressure]]", "[[ahu-3]]", "[[standard-fan-power-baseline]]"]
sources: ["hvac-fault-library-fan-power-high.md"]
---

# HVAC Fault Library FAN-PWR-HIGH

**Summary**: Fault diagnostic procedure and library entry (Doc ID: PICACITY-FAULT-LIB-FAN-PWR-2024, Rev: 2024-03-01) for high supply fan power.

## Fault definition

Supply fan electrical power exceeds standard baseline by **>20%** for **>30 minutes** while supply airflow is within **±5%** of design CFM. (source: hvac-fault-library-fan-power-high.md)

## Ranked root causes

| Priority | Cause | Evidence to gather | Typical fix |
|----------|-------|--------------------|-------------|
| 1 | [[filter-differential-pressure\|Loaded filters]] | Filter ΔP > 1.5 in. w.g. | Replace filters |
| 2 | Cooling-coil fouling | High approach / unable to hold SAT at moderate load | Clean coil |
| 3 | Motor bearing wear | Vibration, noise, elevated motor current | Service bearings / replace motor |
| 4 | Damper / duct restriction | High static pressure, airflow restriction | Clear obstruction; verify [[f-34]] open |
| 5 | VFD / control issue | Setpoint drift, VFD hunting | Tune controls |

(source: hvac-fault-library-fan-power-high.md)

## Specific DAEP AHU-3 checks

1. Confirm [[ahu-cooling-mode]] (expected at 75°F OA).
2. Compare power against **16.5 kW** design baseline (not 15.8 kW commissioning snapshot).
3. Verify fire damper [[f-34]] fully open.
4. Confirm KPI is mapped to [[lp-3]] Circuit 7.

(source: hvac-fault-library-fan-power-high.md)

## Related pages

- [[fan-pwr-high]]
- [[filter-differential-pressure]]
- [[ahu-3]]
- [[f-34]]
- [[lp-3]]

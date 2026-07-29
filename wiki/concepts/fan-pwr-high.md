---
type: concept
title: "FAN-PWR-HIGH"
created: 2026-07-29
updated: 2026-07-29
tags: [fault, fan, concept]
status: mature
related: ["[[standard-fan-power-baseline]]", "[[filter-differential-pressure]]", "[[ahu-3]]", "[[f-34]]", "[[lp-3]]"]
sources: ["hvac-fault-library-fan-power-high.md", "daep-ahu-om-manual-excerpt.md"]
---

# FAN-PWR-HIGH

**Summary**: Fault condition where supply fan power exceeds the standard baseline by **> 20%** for **> 30 minutes** while supply airflow is within **±5%** of design CFM.

## Operational definition for [[ahu-3]]

- **Design baseline**: 16.5 kW at 14,000 CFM (source: daep-ahu-om-manual-excerpt.md)
- **Fault threshold (+20%)**: **19.8 kW** sustained for >30 minutes (source: hvac-fault-library-fan-power-high.md)

## Ranked troubleshooting workflow

1. **Check [[filter-differential-pressure\|Filter ΔP]]**: First check. If filter ΔP > 1.5 in. w.g., replace filters.
2. **Inspect Cooling Coil**: Check for coil fouling / high approach temperature.
3. **Inspect Fan Motor / Bearings**: Check for mechanical friction, vibration, noise, or elevated current.
4. **Inspect Dampers & Duct**: Verify fire/smoke damper [[f-34]] on 3rd floor supply trunk is fully open.
5. **Verify VFD & Controls**: Check static pressure setpoint and VFD output.

(source: hvac-fault-library-fan-power-high.md)

## DAEP verification checklist

- Confirm KPI monitoring is mapped to [[lp-3]] Circuit 7 (60A 3P VFD feed).
- Confirm outdoor air mode (at 75°F OA, [[ahu-cooling-mode\|cooling mode]] is normal).
- Confirm baseline used is 16.5 kW (O&M), not 15.8 kW (commissioning snapshot).

(sources: hvac-fault-library-fan-power-high.md, daep-electrical-panel-schedule.md)

## Related pages

- [[standard-fan-power-baseline]]
- [[ahu-3]]
- [[filter-differential-pressure]]
- [[f-34]]
- [[lp-3]]

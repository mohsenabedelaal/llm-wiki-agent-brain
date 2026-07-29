# HVAC Fault Library — Fan Power High (excerpt)

**Document ID**: PICACITY-FAULT-LIB-FAN-PWR-2024  
**Scope**: Generic + DAEP-relevant checks  
**Revision**: 2024-03-01  

---

## Fault: FAN-PWR-HIGH — Supply fan power above baseline

### Definition

Supply fan electrical power exceeds the asset’s **standard power baseline** by more than **20%** for longer than **30 minutes**, while reported supply airflow is within **±5%** of design CFM.

### Likely causes (ordered)

| Priority | Cause | Evidence to gather | Typical fix |
|----------|-------|--------------------|-------------|
| 1 | Loaded filters | Filter ΔP > 1.5 in. w.g. | Replace filters |
| 2 | Cooling-coil fouling | High approach / inability to hold SAT at moderate load | Coil clean |
| 3 | Motor bearing wear | Vibration, noise, elevated motor amps | Bearing service / motor replace |
| 4 | Damper / duct restriction | Static high, airflow hard to maintain | Clear obstruction; verify FSD position |
| 5 | VFD / control issue | Setpoint drift, hunting | Controls tune |

### DAEP AHU-3 specific checks

When investigating AHU-3:

1. Confirm outdoor air mode via sequence — at 75°F OA, expect **cooling mode** (not a fault by itself).
2. Compare live power to **16.5 kW** design baseline from O&M Table 2 (not the 2019 commissioning 15.8 kW snapshot).
3. Verify fire damper **F-34** fully open (electrical Circuit 13 status / BAS prove).
4. Confirm power KPI is bound to **Panel LP-3 Circuit 7** (fan VFD), not Circuit 9 (controls).

### Do not

- Do not raise a critical electrical work order solely from high fan power without HVAC mechanical checks.
- Do not “fix” by raising the baseline in software without engineering approval.

---
type: concept
title: "Split Air Conditioner Operating Modes"
created: 2026-07-29
updated: 2026-07-29
tags: [concept, hvac, controls, operating-modes, lg]
status: mature
related: ["[[lg-s24awn]]", "[[lg-s24awn-manual]]"]
sources: ["lg-s24awn-manual.md", "S24AWN.pdf"]
---

# Split Air Conditioner Operating Modes

**Summary**: Functional description of operational modes, control logic, and protection routines in residential and light commercial split air conditioning systems, derived from [[lg-s24awn-manual]].

## Operational Modes Summary

1. **Cooling Mode**: Operates compressor and fan to reduce room temperature (setpoint range 18°C–30°C).
2. **Heating Mode**: Heat pump reverse-cycle operation (setpoint range 16°C–30°C).
3. **Auto Changeover / Auto Operation**: Automatically selects cooling or heating to hold room temperature within ±2°C of setpoint.
4. **Healthy Dehumidification**: Optimizes fan speed and cooling algorithm based on room temperature to remove humidity without manual temperature control.
5. **Jet Cool / Jet Heat**: Forces maximum cooling (18°C setpoint, 30 min) or heating (30°C setpoint, 60 min) at super high fan speed for rapid conditioning.
6. **Energy-Saving Cooling Mode**: Adjusts target room temperature over time based on human body thermal adaptation logic.
7. **CHAOS Air Mode**: Varies fan speed according to natural airflow algorithms to prevent direct cold draft discomfort.

(source: lg-s24awn-manual.md)

## Internal Maintenance & Purification Logic

- **Auto Clean**: Following shutdown from cooling or dehumidification, the indoor fan runs internally for ~30 minutes with louvers closed to dry moisture on the evaporator coil, inhibiting microbial growth.
- **NEO PLASMA Purification**: High-voltage electrostatic air purification charging airborne particles and contaminants. Requires 10-second discharge wait time after opening inlet grille before servicing.

(source: lg-s24awn-manual.md)

## Protection Logic & Safeguards

- **Hot Start**: Delays indoor fan operation during heating startup to avoid blowing unheated cold air into occupied spaces.
- **Defrost Cycle**: Pauses heating for a short duration to clear ice buildup on the outdoor heat exchanger coil.
- **Compressor Restart Delay**: Enforces a 3-minute delay before restarting compressor after power interruption.
- **Auto Restart**: Preserves mode setpoints in non-volatile memory and resumes prior operation automatically upon power recovery.

(source: lg-s24awn-manual.md)

## Related pages

- [[lg-s24awn]]
- [[lg-s24awn-manual]]

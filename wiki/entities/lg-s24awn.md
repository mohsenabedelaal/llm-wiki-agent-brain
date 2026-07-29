---
type: entity
title: "LG S24AWN Air Conditioner"
created: 2026-07-29
updated: 2026-07-29
tags: [entity, lg, air-conditioner, split-ac, hvac]
status: mature
related: ["[[lg-s24awn-manual]]", "[[split-ac-operating-modes]]"]
sources: ["lg-s24awn-manual.md", "S24AWN.pdf"]
---

# LG S24AWN Air Conditioner

**Summary**: LG Room Air Conditioner unit family (including S24AWN model, Art Cool, Art Cool Deluxe, and Standard Split models). Supports inverter/non-inverter and heat pump / cooling-only configurations.

## Equipment Specifications

| Parameter | Non-Inverter Spec | Inverter Spec | Source |
|-----------|-------------------|---------------|--------|
| Cooling Outdoor Temp Range | 21°C to 43°C (70°F to 109°F) | -10°C to 43°C (14°F to 109°F) | lg-s24awn-manual.md |
| Heating Outdoor Temp Range | 1°C to 24°C (34°F to 75°F) | -10°C to 24°C (14°F to 24°C) | lg-s24awn-manual.md |
| Cooling Indoor Temp Range | 21°C to 32°C (70°F to 90°F) | 18°C to 32°C (64°F to 90°F) | lg-s24awn-manual.md |
| Heating Indoor Temp Range | 20°C to 27°C (68°F to 81°F) | 18°C to 30°C (86°F) | lg-s24awn-manual.md |
| Setpoint Cooling Range | 18°C to 30°C | 18°C to 30°C | lg-s24awn-manual.md |
| Setpoint Heating Range | 16°C to 30°C | 16°C to 30°C | lg-s24awn-manual.md |
| Power Cord / Extension Rating | Dedicated Circuit / 15 A, 125 V (3-wire grounded) | Dedicated Circuit / 15 A, 125 V (3-wire grounded) | lg-s24awn-manual.md |

(sources: lg-s24awn-manual.md, S24AWN.pdf)

## Forced Operation Schedule (Manual ON/OFF Button)

When remote controller is unavailable, pressing manual ON/OFF button operates unit according to indoor temperature:

| Model | Room Temperature | Operating Mode | Fan Speed | Target Setpoint |
|-------|------------------|----------------|-----------|-----------------|
| Heat Pump Model | Room Temp ≥ 24°C | Cooling | High | 22°C |
| Heat Pump Model | 21°C ≤ Room Temp < 24°C | Cooling | High | 22°C |
| Heat Pump Model | Room Temp < 21°C | Heating | High | 24°C |
| Cooling-Only Model | Room Temp ≥ 24°C | Cooling | High | 22°C |
| Cooling-Only Model | 21°C ≤ Room Temp < 24°C | Cooling | High | 22°C |
| Cooling-Only Model | Room Temp < 21°C | Healthy Dehumidification | High | 23°C |

(sources: lg-s24awn-manual.md, S24AWN.pdf)

## Diagnostic & Service Standards

- **Thermistor Fault**: LED blinks 1 time per 3 seconds indicates room or pipe thermistor open/short circuit. (source: S24AWN.pdf)
- **High-Voltage Hazard**: High-voltage step-up capacitor and plasma filter require 10-second wait after opening grille before touching plasma unit. (source: S24AWN.pdf)
- **Air Filter Maintenance**: Clean every 2 weeks. (source: S24AWN.pdf)
- **Plasma Filter Maintenance**: Clean every 3 months. (source: S24AWN.pdf)

## Related pages

- [[lg-s24awn-manual]]
- [[split-ac-operating-modes]]

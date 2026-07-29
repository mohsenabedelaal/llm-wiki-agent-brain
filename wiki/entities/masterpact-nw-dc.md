---
type: entity
title: "Masterpact NW DC Power Circuit Breakers"
created: 2026-07-29
updated: 2026-07-29
tags: [entity, schneider, acb, electrical, dc-breaker]
status: mature
related: ["[[schneider-mccb-dc-catalogue]]", "[[compact-nsx-dc]]", "[[dc-circuit-breaker-pole-configurations]]"]
sources: ["schneider-mccb-dc-catalogue.md", "Schneider MCCB.pdf"]
---

# Masterpact NW DC Power Circuit Breakers

**Summary**: Air Circuit Breaker (ACB) / power circuit breaker range manufactured by Schneider Electric for heavy-duty low-voltage DC power distribution (1000 A to 4000 A, 24 V to 900 V DC).

## Model Schedule & Coupling Versions

| Model | Rated Current (In) | Coupling Version | Case Configuration | Operating Voltage (Ue) |
|-------|--------------------|------------------|--------------------|------------------------|
| NW10 DC | 1000 A | Version C | 3-pole case (2 poles in series) | 24 V to 500 V DC |
| NW10 DC | 1000 A | Version D | 3-pole case (3 poles in series) | 24 V to 900 V DC |
| NW10 DC | 1000 A | Version E | 4-pole case (4 poles in series) | 24 V to 900 V DC |
| NW20 DC | 2000 A | Version C, D, E | 3P / 4P | 24 V to 900 V DC |
| NW40 DC | 4000 A | Version C, D, E | 3P / 4P | 24 V to 900 V DC |

(sources: schneider-mccb-dc-catalogue.md, Schneider MCCB.pdf)

## Breaking Performance Levels (Icu for L/R = 15 ms)

| Performance Level | 500 V DC | 750 V DC | 900 V DC |
|-------------------|----------|----------|----------|
| N Level | 35 kA | — | — |
| H Level | 85 kA | 50 kA | 35 kA |

(sources: schneider-mccb-dc-catalogue.md, Schneider MCCB.pdf)

## Physical Dimensions & Weight

- **Drawout 3P**: 439 x 441 x 494 mm (Weight: 90 to 116 kg)
- **Drawout 4P**: 439 x 556 x 494 mm (Weight: 125 to 146 kg)
- **Fixed 3P**: 352 x 422 x 427 mm (Weight: 60 to 86 kg)
- **Fixed 4P**: 352 x 537 x 427 mm (Weight: 85 to 106 kg)

(sources: schneider-mccb-dc-catalogue.md, Schneider MCCB.pdf)

## Control Unit & Sensors

- **Micrologic 1.0 DC**: Interchangeable control unit with adjustable magnetic pick-up settings (A, B, C, D, E).
- **Sensor Versions**:
  - 1250 / 2500 A sensor (NW10 DC)
  - 2500 / 5400 A sensor (NW10 DC, NW20 DC)
  - 5000 / 11000 A sensor (NW40 DC)

(sources: schneider-mccb-dc-catalogue.md, Schneider MCCB.pdf)

## Related pages

- [[schneider-mccb-dc-catalogue]]
- [[compact-nsx-dc]]
- [[dc-circuit-breaker-pole-configurations]]

---
type: entity
title: "Compact NSX DC Circuit Breakers"
created: 2026-07-29
updated: 2026-07-29
tags: [entity, schneider, mccb, electrical, dc-breaker]
status: mature
related: ["[[schneider-mccb-dc-catalogue]]", "[[masterpact-nw-dc]]", "[[dc-circuit-breaker-pole-configurations]]"]
sources: ["schneider-mccb-dc-catalogue.md", "Schneider MCCB.pdf"]
---

# Compact NSX DC Circuit Breakers

**Summary**: Molded Case Circuit Breaker (MCCB) range manufactured by Schneider Electric for low-voltage DC power distribution (16 A to 630 A, 24 V to 750 V DC).

## Frame Schedule & Specifications

| Model | Rating (In) | Poles | Pitch | Dimensions (H x W x D) | Weight (Fixed 3P/4P) |
|-------|-------------|-------|-------|------------------------|----------------------|
| NSX100 DC | 16 A – 100 A | 1P, 2P, 3P, 4P | 35 mm | 161 x 105 x 86 mm (3P) | 1.6 to 1.9 kg |
| NSX160 DC | 125 A – 160 A | 1P, 2P, 3P, 4P | 35 mm | 161 x 105 x 86 mm (3P) | 1.6 to 1.9 kg |
| NSX250 DC | 200 A – 250 A | 3P, 4P | 35 mm | 161 x 105 x 86 mm (3P) | 2.2 kg |
| NSX400 DC | 400 A | 3P, 4P | 45 mm | 255 x 140 x 110 mm (3P) | 6.0 kg |
| NSX630 DC | 550 A / 630 A | 3P, 4P | 45 mm | 255 x 140 x 110 mm (3P) | 6.0 kg |

(sources: schneider-mccb-dc-catalogue.md, Schneider MCCB.pdf)

## Breaking Performance Levels (Icu at L/R = 15 ms)

| Performance Level | 1P (≤ 250 V) | 2P (≤ 500 V) | 3P / 4P (≤ 750 V) |
|-------------------|--------------|--------------|-------------------|
| F | 36 kA | 36 kA | 36 kA |
| N | 50 kA | — | — |
| M | 85 kA | 85 kA | — |
| S | — | 100 kA | 100 kA |

(sources: schneider-mccb-dc-catalogue.md, Schneider MCCB.pdf)

## Trip Unit Capabilities

- **TM-D / TM-DC / TM-G**: Thermal-magnetic trip units up to 250 A.
  - TM-D: Fixed thermal, fixed magnetic (1P/2P built-in, 3P/4P interchangeable).
  - TM-DC: Adjustable thermal (0.7 to 1.0 x In), adjustable magnetic (5 to 10 x In).
  - TM-G: Fixed thermal, low fixed magnetic pick-up for long cable protection.
- **MP1, MP2, MP3**: Built-in magnetic trip units for NSX400 DC and NSX630 DC.
  - MP1: Pick-up 800 to 1600 A
  - MP2: Pick-up 1250 to 2500 A
  - MP3: Pick-up 2000 to 4000 A

(sources: schneider-mccb-dc-catalogue.md, Schneider MCCB.pdf)

## Related pages

- [[schneider-mccb-dc-catalogue]]
- [[masterpact-nw-dc]]
- [[dc-circuit-breaker-pole-configurations]]

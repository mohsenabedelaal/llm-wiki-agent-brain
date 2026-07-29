---
type: concept
title: "DC Circuit Breaker Pole Configurations"
created: 2026-07-29
updated: 2026-07-29
tags: [concept, electrical, dc-breaker, circuit-breaker, power-distribution]
status: mature
related: ["[[schneider-mccb-dc-catalogue]]", "[[compact-nsx-dc]]", "[[masterpact-nw-dc]]"]
sources: ["schneider-mccb-dc-catalogue.md", "Schneider MCCB.pdf"]
---

# DC Circuit Breaker Pole Configurations

**Summary**: Engineering rules for connecting circuit breaker poles in series or parallel within direct-current (DC) power networks, based on system voltage, current demand, grounding topology, and time constant ($L/R$).

## Series vs. Parallel Pole Connections

1. **Series Pole Connection (Voltage Division)**:
   - Connects 2, 3, or 4 poles in series to divide total system voltage ($U_e$) across individual poles.
   - Example: A 750 V DC system using a 3-pole breaker subjects each pole to 250 V DC ($750\text{ V} / 3 = 250\text{ V}$).
   - Optimizes breaking capacity at elevated DC voltages without exceeding single-pole dielectric limits.

2. **Parallel Pole Connection (Current Division)**:
   - Connects poles in parallel to share total load current across internal current paths.
   - Example: A [[compact-nsx-dc\|Compact NSX630 DC]] 3P unit in parallel increases continuous current rating from 630 A to **1500 A** at 250 V DC.
   - Mixed configurations ($2 \times 2\text{P}$ parallel-series) combine voltage division and current expansion.

(sources: schneider-mccb-dc-catalogue.md, Schneider MCCB.pdf)

## Grounding Topologies & Pole Requirements

- **Earthed System (One Polarity Earthed)**:
  - Requires all protection poles on the ungrounded (active) polarity.
  - Breaking capacity requirement: $I_{cu} \ge I_{sc\text{ max}}$ at full system voltage $U_e$.
- **Mid-Point Earthed System**:
  - Distributes poles equally between positive and negative polarities.
  - Breaking capacity requirement: $I_{cu} \ge I_{sc\text{ max}}$ at $U_e / 2$ per polarity.
- **Isolated System (IT DC Network)**:
  - Requires equal pole distribution across both polarities. Insulation monitoring device (IMD) detects first earth fault.
  - Second double fault requires full breaking capacity $I_{cu} \ge I_{sc\text{ max}}$ at $U_e$ on both polarities.

(sources: schneider-mccb-dc-catalogue.md, Schneider MCCB.pdf)

## System Time Constants ($L/R$) & Short-Circuit Dynamics

DC short-circuit current rises exponentially according to loop resistance $R$ and inductance $L$:

$$i(t) = I_{sc} \left(1 - e^{-t / \tau}\right) \quad \text{where } \tau = \frac{L}{R}$$

- **Standard Time Constants**:
  - $L/R = 5\text{ ms}$: Fast short-circuit (e.g., battery discharge, telecom PABX, UPS DC buses).
  - $L/R = 15\text{ ms}$: Standardized reference value per **IEC 60947-2**.
  - $L/R = 30\text{ ms}$: Slow short-circuit (e.g., heavy industrial DC generators).
- Steady-state fault current is established after $t = 3\tau$ ($e^{-3} \approx 0.05$).

(sources: schneider-mccb-dc-catalogue.md, Schneider MCCB.pdf)

## Related pages

- [[schneider-mccb-dc-catalogue]]
- [[compact-nsx-dc]]
- [[masterpact-nw-dc]]

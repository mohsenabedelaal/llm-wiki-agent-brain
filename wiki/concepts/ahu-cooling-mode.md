---
type: concept
title: "AHU cooling mode"
created: 2026-07-29
updated: 2026-07-29
tags: [sequence, cooling, concept]
status: mature
related: ["[[ahu-3]]", "[[standard-fan-power-baseline]]", "[[fan-pwr-high]]"]
sources: ["daep-ahu-sequence-of-operation.md", "daep-ahu-om-manual-excerpt.md"]
---

# AHU cooling mode

**Summary**: Mode active when outdoor air dry-bulb temperature is **≥ 70°F**. Chilled-water coil modulates to maintain 55°F supply air temperature (SAT), and economizer is locked out.

## Operating parameters

- **Trigger condition**: Outdoor air dry-bulb temperature (OAT) ≥ 70°F (e.g., 75°F OA).
- **Control action**: Modulate chilled water valve to maintain SAT setpoint = 55°F; maintain minimum OA (2,800 CFM for [[ahu-3]]); maintain duct static pressure setpoint = 1.2 in. w.g.
- **Expected Fan Power**: ~100% of standard fan power baseline at design CFM.

(sources: daep-ahu-sequence-of-operation.md, daep-ahu-om-manual-excerpt.md)

## Diagnostic implication

At **75°F outdoor air**, [[ahu-3]] is expected to operate in cooling mode. High fan power at 75°F OA **cannot** be attributed to operating in the wrong mode.

## Related pages

- [[ahu-3]]
- [[standard-fan-power-baseline]]
- [[fan-pwr-high]]

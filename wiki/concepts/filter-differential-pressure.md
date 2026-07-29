---
type: concept
title: "Filter differential pressure"
created: 2026-07-29
updated: 2026-07-29
tags: [maintenance, filter, concept]
status: mature
related: ["[[fan-pwr-high]]", "[[ahu-3]]"]
sources: ["daep-ahu-om-manual-excerpt.md", "hvac-fault-library-fan-power-high.md", "sample-ahu-om-excerpt.pdf"]
---

# Filter differential pressure

**Summary**: Differential pressure (ΔP) across filter rack. High filter ΔP increases fan static loading, leading to elevated fan power draw. First mechanical check during [[fan-pwr-high]] investigations.

## Baseline & threshold limits

- **[[ahu-3]] Filter Spec**: MERV 14 filters. (source: daep-ahu-om-manual-excerpt.md)
- **Replacement Threshold**: Replace filter rack when differential pressure exceeds **1.5 in. w.g.** (sources: daep-ahu-om-manual-excerpt.md, sample-ahu-om-excerpt.pdf)
- **Fault Diagnostic Rank**: Priority #1 check for high fan power exceptions. (source: hvac-fault-library-fan-power-high.md)

## Related pages

- [[fan-pwr-high]]
- [[ahu-3]]
- [[standard-fan-power-baseline]]

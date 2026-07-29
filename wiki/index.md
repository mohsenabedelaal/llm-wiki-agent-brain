# Index

Master catalog of this wiki. The agent updates this after every ingest.

**Purpose**: DistrictNex / Picacity building-ops knowledge (HVAC + electrical) for LLM Wiki + Google ADK demo.

**Last catalog refresh**: 2026-07-29

## Sources

- [[daep-ahu-om-manual-excerpt]] — AHU O&M R2 design schedule + baselines (AHU-1 through AHU-4)
- [[daep-ahu-sequence-of-operation]] — Mode selection and cooling sequence
- [[daep-electrical-panel-schedule]] — Panel LP-3 circuit schedule excerpt (Circuits 1–17)
- [[daep-ahu-commissioning-report-2019]] — As-built CX values (15.8 kW snapshot vs 16.5 kW design baseline)
- [[hvac-fault-library-fan-power-high]] — FAN-PWR-HIGH fault procedure and ranked cause list
- [[sample-ahu-om-excerpt-pdf]] — Synthetic PDF manual fixture (PDF ingest path for AHU-3)
- [[lg-s24awn-manual]] — LG Room Air Conditioner owner's manual (P/No. 3828A24010C) for S24AWN and split models
- [[schneider-mccb-dc-catalogue]] — Schneider Electric Compact NSX DC & Masterpact NW DC Catalogue (16 A to 4000 A DC)

## Entities

- [[ahu-3]] — Floor 3 AHU (Trane CSAA-40); 16.5 kW design baseline; Circuit 7 feed
- [[lp-3]] — Floor 3 electrical panel (480Y/277V, 400A main breaker)
- [[f-34]] — AHU-3 supply trunk fire/smoke damper (Circuit 13 interlock)
- [[lg-s24awn]] — LG Room Air Conditioner unit family specs and forced operation schedule
- [[compact-nsx-dc]] — Compact NSX DC MCCB family (16 A to 630 A, 24 V to 750 V DC)
- [[masterpact-nw-dc]] — Masterpact NW DC ACB family (1000 A to 4000 A, 24 V to 900 V DC)

## Concepts

- [[standard-fan-power-baseline]] — Design monitoring baselines + 20% rule
- [[ahu-cooling-mode]] — Outdoor air ≥ 70°F → mechanical cooling mode
- [[fan-pwr-high]] — Fault definition (>20% over baseline for >30 min) and ordered troubleshooting checks
- [[filter-differential-pressure]] — First mechanical check for high fan power (replace if ΔP > 1.5 in. w.g.)
- [[split-ac-operating-modes]] — Split system operating modes, auto clean, plasma purification, and safeguards
- [[dc-circuit-breaker-pole-configurations]] — Series vs parallel pole configurations, grounding topologies, and L/R time constants

## Sessions / answers

- [[ahu-3-high-power-at-75f]] — Demo Q&A: 20% above baseline at 75°F OA

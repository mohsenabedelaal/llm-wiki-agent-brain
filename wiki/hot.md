# Hot Cache

**Status**: Ingest completed for `raw/manuals/Schneider MCCB.pdf`, `raw/manuals/S24AWN.pdf`, and prior DAEP seed files / fixtures.

## Ingested Sources Summary

1. **Schneider Electric DC Circuit Breaker Catalogue** (`Schneider MCCB.pdf` / `schneider-mccb-dc-catalogue.md`):
   - Catalogue covering direct-current power circuit breakers and switch-disconnectors from 16 A to 4000 A (24 V to 900 V DC).
   - [[compact-nsx-dc]]: MCCB range (16 A to 630 A, 24 V to 750 V DC). Performance levels F (36 kA), N (50 kA), M (85 kA), S (100 kA). Trip units: TM-D/TM-DC/TM-G (up to 250 A) and MP1/MP2/MP3 (400 A & 630 A).
   - [[masterpact-nw-dc]]: Heavy-duty power breaker range (1000 A to 4000 A, 24 V to 900 V DC). Models NW10 DC, NW20 DC, NW40 DC. Coupling versions C, D, E. Breaking capacity N (35 kA) and H (85 kA). Micrologic 1.0 DC control unit.
   - [[dc-circuit-breaker-pole-configurations]]: Series connection divides voltage per pole (up to 750 V/900 V DC); parallel connection divides current (e.g. NSX630 3P in parallel handles up to 1500 A). System time constants: L/R = 5 ms (fast/batteries), 15 ms (standard IEC 60947-2), 30 ms (slow).

2. **LG Room Air Conditioner Manual** (`S24AWN.pdf` / `lg-s24awn-manual.md`):
   - Manual P/No. 3828A24010C covering LG [[lg-s24awn]] room air conditioners (Standard Split, Art Cool, Art Cool Wide, Art Cool Deluxe).
   - Operating limits: Non-Inverter (Cooling 21°C–32°C indoor / 21°C–43°C outdoor) vs Inverter (Cooling 18°C–32°C indoor / -10°C–43°C outdoor).
   - Key modes: Jet Cool/Heat, Healthy Dehumidification, Auto Clean (30-min coil drying post shutdown), NEO PLASMA purification (10s safety delay).

3. **DAEP AHU O&M & CX Baseline** (`daep-ahu-om-manual-excerpt.md`, `daep-ahu-commissioning-report-2019.md`):
   - [[ahu-3]]: 14,000 CFM, 30 HP fan motor, **16.5 kW** design fan power baseline at 75°F OA, 55°F SAT, MERV 14 filter (replace if ΔP > 1.5 in. w.g.).
   - Fault threshold: Sustained fan power **>20% above baseline** (≈ **19.8 kW**) for **>30 minutes** triggers [[fan-pwr-high]].
   - Contradiction: 2019 CX snapshot recorded 15.8 kW; Overwatch baseline is 16.5 kW (O&M Table 2).

4. **DAEP Electrical Panel Schedule** (`daep-electrical-panel-schedule.md`):
   - Panel [[lp-3]] (480Y/277V, 400A main breaker).
   - Circuit 7: 60A/3P feeder for AHU-3 supply fan VFD (**primary power KPI feed**). Circuit 13: 20A/1P for damper [[f-34]].

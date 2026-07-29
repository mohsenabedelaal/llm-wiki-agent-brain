# DAEP Building — AHU O&M Manual Excerpt

**Document ID**: DAEP-HVAC-OM-AHU-2024-R2  
**Building**: DAEP Building  
**Revision**: R2 — 2024-09-12  
**Scope**: Air Handling Units AHU-1 through AHU-4  
**Audience**: Facility engineers, Overwatch agent knowledge ingest

---

## 1. Purpose

This excerpt covers design data, operating baselines, and maintenance notes for the air handling units serving the DAEP Building office floors. Values in Table 2 are **design / standard baselines** used for performance monitoring. Do not confuse design baselines with measured live values from the BMS.

## 2. Unit schedule (design)

| Unit | Floor | Supply airflow (CFM) | Fan motor (HP) | Design fan power baseline (kW) | Design SAT (°F) | Cooling coil capacity (tons) | Filter MERV |
|------|-------|----------------------|----------------|--------------------------------|-----------------|------------------------------|-------------|
| AHU-1 | 1     | 12,000               | 25             | 14.2                           | 55              | 45                           | 13          |
| AHU-2 | 2     | 11,500               | 25             | 13.8                           | 55              | 42                           | 13          |
| AHU-3 | 3     | 14,000               | 30             | 16.5                           | 55              | 52                           | 14          |
| AHU-4 | 4     | 10,000               | 20             | 12.0                           | 55              | 38                           | 13          |

**Notes on Table 2:**

- Design fan power baseline is the expected average power draw at design airflow with clean filters and outdoor air at 75°F dry-bulb (cooling mode). (source: this document)
- AHU-3 serves the densest floor (open office + meeting rooms) and has the highest design airflow and fan power baseline.
- A sustained reading **>20% above** the design fan power baseline for more than 30 minutes, while supply airflow is within ±5% of design CFM, is a performance exception requiring investigation.

## 3. AHU-3 nameplate and components

- Manufacturer: Trane  
- Model: CSAA-40  
- Serial: TX-DAEP-AHU3-2019  
- Supply fan: direct-drive, VFD-controlled  
- Cooling coil: chilled water, two-row  
- Heating: hot water reheat (perimeter zones only)  
- Outdoor air damper: modulating, minimum OA = 2,800 CFM  

## 4. Operating envelopes

| Condition | Outdoor air | Expected mode | Fan power relative to baseline |
|-----------|-------------|---------------|--------------------------------|
| Cooling   | ≥ 70°F DB   | Mechanical cooling | Near 100% of design baseline at design CFM |
| Economizer | 55–70°F DB | Mixed air / free cooling | Often 85–95% of baseline |
| Heating   | < 55°F DB   | Heating + min OA | Typically 70–90% of cooling baseline |

At outdoor air **75°F**, AHU-3 is correctly expected to be in **mechanical cooling mode**. That outdoor condition alone does **not** explain elevated fan power.

## 5. Common causes of elevated fan power (AHU)

1. Dirty or loaded filters (check differential pressure; replace if ΔP > 1.5 in. w.g.)
2. Cooling-coil fouling (reduced heat transfer → fan works harder to meet SAT)
3. Fan motor bearing wear / mechanical friction
4. Incorrect VFD setpoint or stuck damper forcing higher static
5. Supply duct obstruction or closed fire/smoke damper

Recommended first checks when AHU-3 power is ~20% above baseline at 75°F OA:

1. Filter ΔP vs clean baseline  
2. Fan motor bearing resistance / vibration  
3. Cooling-coil fouling inspection  
4. Verify fire damper F-34 on the third-floor supply trunk is fully open  

## 6. Related documents

- Sequence of Operation: `daep-ahu-sequence-of-operation.md`
- Commissioning report: `daep-ahu-commissioning-report-2019.md` (note: may contain as-built values that differ slightly from design Table 2)
- Electrical feed: Panel LP-3 circuits listed in `daep-electrical-panel-schedule.md`

# DAEP Building — AHU Sequence of Operation

**Document ID**: DAEP-HVAC-SOO-AHU-2023  
**Building**: DAEP Building  
**Revision**: 2023-11-02  
**Applies to**: AHU-1 … AHU-4  

---

## 1. Overview

Each AHU is controlled by the building automation system (BAS). Modes are selected by outdoor air dry-bulb temperature and zone demand.

## 2. Mode selection

| Outdoor air dry-bulb | Mode | Description |
|----------------------|------|-------------|
| OA ≥ 70°F            | Cooling | Chilled-water coil active; economizer locked out |
| 55°F ≤ OA < 70°F     | Economizer / mixed air | Free cooling preferred when OA enthalpy allows |
| OA < 55°F            | Heating | Hot-water reheat as needed; OA at minimum |

**Implication for diagnostics:** At **75°F outdoor air**, the applicable sequence for every AHU including [[AHU-3]] is **Cooling mode**. Elevated fan power at this condition cannot be attributed to “wrong mode.”

## 3. Cooling mode sequence (AHU-3 detail)

1. Occupancy schedule ON → unit start command.
2. Supply fan ramps via VFD to maintain duct static pressure setpoint (1.2 in. w.g.).
3. Outdoor air damper opens to at least minimum OA (2,800 CFM for AHU-3).
4. Chilled-water valve modulates to maintain **supply air temperature (SAT) setpoint = 55°F**.
5. If SAT cannot be met within 15 minutes, BAS raises a “SAT not met” alarm.
6. Return air temperature (RAT) is monitored for zone load indication; high RAT with met SAT usually indicates high zone load, not fan fault.

## 4. Power vs airflow relationship

In cooling mode at design CFM, fan power should track near the **design fan power baseline** from the O&M unit schedule.

- If **airflow ≈ design** and **power ≫ baseline** → investigate mechanical / filter / coil / damper issues.
- If **airflow ≫ design** and **power ≫ baseline** → investigate static pressure setpoint, zone damper demand, or VFD max limit.
- If **airflow ≪ design** and **power high** → unusual; check sensor calibration and belt/drive (if applicable).

## 5. Safety interlocks

- Freeze protection: if mixed air < 38°F, trip to heating / emergency OA close.
- Smoke detector trip: fan stop, OA dampers close, alarm to fire panel.
- Fire/smoke dampers (including **F-34** on AHU-3 supply trunk): must prove open before fan enable.

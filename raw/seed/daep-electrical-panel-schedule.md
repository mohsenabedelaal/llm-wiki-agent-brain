# DAEP Building — Electrical Panel Schedule (excerpt)

**Document ID**: DAEP-ELEC-PNL-LP3-2022  
**Building**: DAEP Building  
**Panel**: LP-3 (Lighting / Power — Floor 3)  
**Revision**: 2022-06-18  
**Voltage**: 480Y/277V, 3φ, 4W  
**Main breaker**: 400A  

---

## 1. Purpose

Circuit schedule for Panel LP-3. Used to identify which breakers feed HVAC and miscellaneous loads on Floor 3, and which monitored current points map to Overwatch KPIs.

## 2. Circuit schedule (selected rows)

| Circuit | Breaker (A) | Poles | Load description | Fed equipment | Notes |
|---------|-------------|-------|------------------|---------------|-------|
| 1       | 20          | 1     | Lighting — open office west | Lighting panel branch | Non-HVAC |
| 3       | 20          | 1     | Lighting — open office east | Lighting panel branch | Non-HVAC |
| 5       | 30          | 2     | Receptacles — meeting rooms | — | Non-HVAC |
| 7       | 60          | 3     | AHU-3 supply fan VFD | AHU-3 fan motor | **Primary AHU-3 power feed** |
| 9       | 30          | 3     | AHU-3 controls & damper actuators | AHU-3 control panel | Control power only |
| 11      | 40          | 3     | Chilled water pump P-3 (floor) | Pump P-3 | Related plant-side |
| 13      | 20          | 1     | Fire damper F-34 actuator / status | Damper F-34 | Must remain energized |
| 15      | 100         | 3     | Spare / future | — | Reserved |
| 17      | 50          | 3     | Elevator machine room HVAC | Small DX unit | Not AHU-3 |

## 3. Monitoring notes for Overwatch

- **Chilled Water Pump / AHU fan power KPIs** for Floor 3 should be tied primarily to **Circuit 7** (AHU-3 supply fan VFD), not Circuit 9 (controls).
- A trip or brownout on Circuit 7 will stop AHU-3 airflow; Circuit 13 loss can prevent F-34 from proving open and block fan enable via interlock.
- Design fan motor for AHU-3 is **30 HP**; Circuit 7 is **60A / 3-pole**, which is the correct feeder sizing per the electrical design narrative in this schedule.

## 4. Breaker trip troubleshooting (brief)

1. Confirm load description before resetting.
2. Measure motor current on Circuit 7 if AHU-3 fan trips repeatedly — compare to nameplate FLA.
3. Do not upsize breakers without engineering review.
4. If Circuit 7 current is high while AHU-3 is above power baseline, coordinate with HVAC investigation (filters, bearings, coil fouling) before assuming an electrical-only fault.

# DAEP Building — AHU Commissioning Report (excerpt)

**Document ID**: DAEP-CX-AHU-2019  
**Building**: DAEP Building  
**Date**: 2019-08-22  
**Status**: As-built / commissioning  

---

## 1. Purpose

As-measured values at substantial completion. **These are commissioning snapshots, not the current design baselines in the 2024 O&M manual.** Where they disagree, prefer the later O&M design table for Overwatch baseline monitoring unless engineering has issued a formal baseline update.

## 2. Measured fan power at design airflow (commissioning day)

| Unit | Measured supply CFM | Measured fan power (kW) | OAT during test (°F) | Notes |
|------|---------------------|-------------------------|----------------------|-------|
| AHU-1 | 11,900              | 13.9                    | 78                   | Within 3% of design |
| AHU-2 | 11,400              | 13.5                    | 78                   | Within 3% of design |
| AHU-3 | 13,850              | **15.8**                | 78                   | ~4% below 2024 O&M design baseline of 16.5 kW |
| AHU-4 | 9,950               | 11.7                    | 78                   | Within 3% of design |

## 3. Explicit contradiction note (for wiki lint practice)

- O&M Manual R2 (2024) lists AHU-3 **design fan power baseline = 16.5 kW**.
- This commissioning report (2019) recorded **15.8 kW** at near-design CFM.

Both can be true: commissioning is as-measured on day one; the O&M table is the **standard monitoring baseline**. Overwatch agents should use **16.5 kW** as the comparison baseline unless a later engineering change order updates it.

If an agent cites 15.8 kW as “the baseline,” that is a documentation error.

## 4. AHU-3 damper prove

Fire/smoke damper **F-34** proved open during functional testing. Interlock verified: fan would not enable with F-34 closed.

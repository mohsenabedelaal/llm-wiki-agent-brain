---
type: source
title: "Schneider Electric Compact NSX DC & Masterpact NW DC Catalogue"
created: 2026-07-29
updated: 2026-07-29
tags: [pdf, manual, schneider, mccb, acb, electrical, dc-breaker]
status: mature
related: ["[[compact-nsx-dc]]", "[[masterpact-nw-dc]]", "[[dc-circuit-breaker-pole-configurations]]"]
sources: ["Schneider MCCB.pdf"]
---

# Schneider Electric Compact NSX DC & Masterpact NW DC Catalogue (2012)

**Summary**: Technical catalogue covering Schneider Electric direct-current (DC) power circuit breakers and switch-disconnectors from 16 A to 4000 A, operating across 24 V to 900 V DC networks.

**Document Details**:
- Filename: `raw/manuals/Schneider MCCB.pdf`
- Pages extracted: 80 / 180 (pypdf extraction truncated at page 80)
- Manufacturer: Schneider Electric
- Key Standards: IEC 60947-1, IEC 60947-2, IEC 60947-3, IEC 60664-1, EN 60947-1, EN 60947-2

## System Overview & Current Ratings

| Range | Current Rating (In) | Voltage Range (Ue) | Pole Options | Breaking Capacity (Icu) |
|-------|--------------------|--------------------|--------------|-------------------------|
| Compact NSX DC | 16 A to 630 A | 24 V to 750 V DC | 1P, 2P, 3P, 4P | 36 kA (F), 50 kA (N), 85 kA (M), 100 kA (S) |
| Masterpact NW DC | 1000 A to 4000 A | 24 V to 900 V DC | 3P (Ver C/D), 4P (Ver E) | 35 kA (N), 85 kA (H) |

(source: Schneider MCCB.pdf)

## Environmental & Operating Specs

- **Ambient Temperature**: -25°C to +70°C operating; storage -50°C to +85°C (NSX), -40°C to +85°C (NW without trip unit). Derating applies above +40°C.
- **Altitude Derating**: Nominal performance up to 2000 m. At 3000 m (0.96 In), 4000 m (0.93 In), 5000 m (0.90 In).
- **Atmospheric Protection**: Dry cold IEC 60068-2-1 (-55°C), dry heat IEC 60068-2-2 (+85°C), damp heat IEC 60068-2-30 (95% RH at +55°C), salt mist IEC 60068-2-52 level 2.
- **Pollution Degree**: Pollution degree 3 (Compact NSX), pollution degree 4 (Masterpact NW).

(source: Schneider MCCB.pdf)

## Control Units & Trip Mechanisms

- **Compact NSX DC**:
  - TM-D / TM-DC / TM-G: Thermal-magnetic trip units (up to 250 A).
  - MP1, MP2, MP3: Built-in magnetic trip units for NSX400 DC and NSX630 DC (adjustable pick-up 800–1600 A, 1250–2500 A, 2000–4000 A).
- **Masterpact NW DC**:
  - Micrologic 1.0 DC control unit with adjustable magnetic pick-up settings (A, B, C, D, E).

(source: Schneider MCCB.pdf)

## Communication & Auxiliary Options

- **Protocols**: Modbus RS485 (RTU) via BSCM module and IFM interface; EGX100/EGX300 Ethernet Gateways for TCP/IP web supervision.
- **Auxiliary Contacts**: OF (ON/OFF), SD (trip), SDE (fault-trip), CE/CD/CT (connected/disconnected/test position carriage switches).
- **Shunt/Undervoltage Releases**: MX shunt release (<30 VA pick-up, <50 ms response), MN undervoltage release (0.35–0.7 Un trip threshold), MNR with time-delay unit (up to 200 ms immunity for transient dips).

(source: Schneider MCCB.pdf)

## Related pages

- [[compact-nsx-dc]]
- [[masterpact-nw-dc]]
- [[dc-circuit-breaker-pole-configurations]]

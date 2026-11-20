# Project Instructions: Alpha Innotec Luxtronik Heat Pump Optimization

## User Profile & Communication
- **Name**: Bas
- Address the user as Bas when appropriate.
- **Language**:
  - Converse with Bas in Dutch (Nederlands).
  - All source code, code comments, technical specifications, and documentation MUST always be written in English.

---

## System Profile & Hardware Specification
- **Heat Pump Model**: Alpha Innotec WZS 81H/K (Brine/Water Ground-Source Compact Heat Pump with integrated hydraulic tower & DHW cylinder)
- **Controller**: Luxtronik 2.0 (Interface: Java Webinterface / socket port 8889 / 8888)
- **MAC Address**: `40:ec:f8:00:b5:99`
- **Serial Number**: `220131-144` (HA entity prefix: `220131_0144`)
- **Expansion Boards**:
  - Comfort Board (A6): Installed (passive cooling & mixed heating circuits)
  - Ventilation Board (A7): Installed
- **Room Controller**: RFV-DK (visual LCD room temperature display; rotary dial modifies parallel offset ±0.2 K)
- **3-Phase Power Monitoring**: Shelly 3EM / Pro 3EM (`sensor.energymonitor_warmtepomp_*`)
- **Reference Indoor Temperature**: `sensor.temperatuur_woonkamer_temperature`
- **Home Assistant Integration**: `BenPru/luxtronik` (custom component communicating via TCP socket)

---

## Core Objectives
1. **Prevent Winter Living Room Overheating**: Eliminate excessive room temperatures (24°C+) during cold weather by fine-tuning the stooklijn (heating curve) parameters (End point currently 35.0°C, Parallel shift 24.0°C).
2. **Optimize Electrical Efficiency & COP**: Reduce total electrical consumption (kWh) and optimize the seasonal Coefficient of Performance (COP).
3. **Deep Diagnostic Telemetry**: Maintain high-precision 48h/7d telemetry dashboards (hydraulic flow, ground loop inlet/outlet, compressor runtimes, electrical power).
4. **Intelligent Dynamic Control**: Safely adjust Luxtronik heating offsets and hysterese settings via Home Assistant automations without triggering short-cycling.

---

## Safety & Operational Guardrails
- **Compressor Anti-Cycling**: Never rapidly cycle the compressor. Luxtronik 2.0 enforces a strict limit of max 3 starts per hour; respect minimum hysteresis (≥ 1.5 K).
- **Gradual Stooklijn Tuning**: Never alter the heating curve end point by more than 1.0–1.5 K at a time. Allow 48–72 hours of thermal settling before making further adjustments.
- **Entity ID Integrity**: NEVER rename existing Home Assistant entity IDs or friendly names without explicit user approval.
- **Heating System Constraints**: Low-temperature underfloor heating requires design return temperatures ≤ 30°C.
- **OPNsense Safety**: OPNsense access remains strictly **READ-ONLY**.

---

## Project Structure & Documentation Map
- `.agents/skills/alpha-innotec-luxtronik/SKILL.md`: Detailed parameter registers, Luxtronik control logic, and integration guides.
- `docs/hardware-specs.md`: Technical data, capacity tables, and electrical ratings for WZS 81H/K.
- `docs/entity-mapping.md`: Full catalog of Luxtronik sensors, numbers, switches, and Shelly energy entities.
- `docs/stooklijn-optimization-guide.md`: Mathematical heating curve formulas, hysterese logic, and step-by-step optimization protocol.
- `docs/manuals/`: Manufacturer PDF manuals and commissioning guides.
- `dashboards/`: Lovelace dashboard definitions (Heat Pump Flow Card, Plotly Graphs, Bubble Card controls).
- `automations/`: Home Assistant YAML automations for dynamic stooklijn compensation and COP tracking.

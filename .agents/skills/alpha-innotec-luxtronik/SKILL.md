---
name: alpha-innotec-luxtronik
description: Technical specification, parameter definitions, and Home Assistant control guide for the Alpha Innotec WZS 81H/K heat pump with Luxtronik 2.0 controller. Use when diagnosing, monitoring, or optimizing heating curves, room temperature overshooting, domestic hot water (DHW), and smart grid/energy integration.
---

# Alpha Innotec WZS 81H/K & Luxtronik 2.0 Heat Pump Guide

This skill provides system architecture details, hardware specifications, Luxtronik 2.0 controller parameters, and Home Assistant integration guidelines (`BenPru/luxtronik`) for the Alpha Innotec WZS 81H/K ground-source (brine/water) heat pump installation.

---

## 🏷️ 1. Hardware & Installation Profile

* **Heat Pump Model:** Alpha Innotec WZS 81H/K (Brine/Water Compact Heat Pump with integrated hydraulic tower)
* **Serial Number:** `220131-144` (Home Assistant entity prefix: `220131_0144`)
* **MAC Address:** `40:ec:f8:00:b5:99`
* **Expansion Boards:**
  * **Comfort Board (A6):** Installed (`yes`)
  * **Ventilation Board (A7):** Installed (`yes`)
* **Room Unit:** RFV-DK Room Controller with heating curve adjustment knob and status display.
* **Energy Monitor:** Shelly 3EM / Pro 3EM (`sensor.energymonitor_warmtepomp_*`).
* **Home Assistant Integration:** Custom integration [`BenPru/luxtronik`](https://github.com/BenPru/luxtronik) (communicating over TCP port 8888 / socket interface).
* **Reference Documentation:**
  * [LoxWiki Java Webinterface & Luxtronik 2.0 Parameters](https://loxwiki.atlassian.net/wiki/spaces/LOX/pages/1533935933/Java+Webinterface)
  * Alpha Innotec Luxtronik 2.0 Operating Manual (Part 2 - Qualified Technician)
  * RFV-DK Room Controller Manual (83019100aNL)
  * Nathan Group Resident Instruction ("Bewonersinstructie")
  * [Hydraulic Architecture & Flow Card Design Rules](file:///home/agy/workspace/warmtepomp/docs/hydraulic-architecture.md)

---

## ⚙️ 2. Luxtronik 2.0 Control Architecture & Logic

### Weather-Compensated Heating Curve (Stooklijn)
The Luxtronik 2.0 controller regulates heating based on the **calculated return setpoint** ($T_{\text{RL, target}}$) as a function of outdoor temperature ($T_A$):
1. **Heating Curve End Point (Endpunkt / Heizkurve):** Target return temperature at design outdoor temperature (typically $-20^\circ\text{C}$).
2. **Parallel Shift / Offset (Fußpunkt / Parallelverschiebung):** Shifts the entire heating curve up or down by $\pm K$.
3. **Heating Hysteresis (`Hysteresis HR`):** Default $2.0\,\text{K}$. The compressor starts when $T_{\text{RL}} \le T_{\text{RL, target}} - \text{Hysteresis}$ and stops when $T_{\text{RL}} \ge T_{\text{RL, target}} + \text{Hysteresis}$.
4. **Compressor Cycle Limits:** The controller strictly enforces a maximum of 3 compressor starts per hour to prevent short-cycling.

### RFV-DK Room Unit Characteristics
* **Informational Display:** The room temperature displayed on the RFV-DK LCD is **purely informational** and does not act as a traditional modulating room thermostat unless active room influence is programmed.
* **Rotary Dial:** The dial physically adjusts the parallel shift (offset) in $\pm 0.2\,\text{K}$ increments.

### Pump & Energy Optimization
* **Pump Optimization (`Pump opt.`):** When enabled (`Yes`), heating circulation pumps (`HUP`) turn off when there is no heat demand for $> 3\text{h}$, then cycle for 5 minutes every 30 minutes. If $T_A > T_{\text{RL, target}}$, pumps are stopped continuously.
* **DHW Heating (Domestic Hot Water):** DHW has top priority over space heating and cooling.

---

## 🌡️ 3. Winter Overheating Diagnosis (24°C+ Living Room)

When the living room reaches excessive temperatures (24°C+) during cold winter periods, the primary causes are:
1. **Excessive Heating Curve Slope / End Point:** If the curve is set higher than the building's thermal envelope requires, the system continuously injects excess heat into the thermal screed mass.
2. **Lack of Ambient / Solar Compensation:** A purely weather-dependent system does not throttle when passive solar gain (large windows) or internal heat loads (appliances, cooking, occupants) heat up the room.
3. **Hydraulic Imbalance:** High flow rate through the living room floor circuits compared to secondary rooms.

### Solutions & Remediation:
* **Base Curve Tuning:** Lower the heating curve end point (e.g., from $35.0^\circ\text{C}$ to $26\text{--}28^\circ\text{C}$ at $-20^\circ\text{C}$) and decrease the base offset (from $24.0^\circ\text{C}$ to $20\text{--}21^\circ\text{C}$).
* **Dynamic HA Room Compensation:** Use Home Assistant automations to dynamically lower `heating_target_correction` (or temporarily set heating mode to Standby/Off) when the living room exceeds the desired target (e.g., $21.5^\circ\text{C}$).

---

## 🏠 4. Home Assistant Integration (`BenPru/luxtronik`)

The integration exposes entity IDs prefixed by the heat pump serial number `220131_0144`.

### Key Entity Mapping
| Purpose | Entity ID / Type | Description |
| :--- | :--- | :--- |
| **Flow Temp** | `sensor.luxtronik_220131_0144_flow_in_temperature` | Supply temperature to heating system |
| **Return Temp** | `sensor.luxtronik_220131_0144_flow_out_temperature` | Actual return temperature from heating system |
| **Return Target** | `sensor.luxtronik_220131_0144_flow_out_temperature_target` | Target return temperature ($T_{\text{RL, target}}$) |
| **Outdoor Temp** | `sensor.luxtronik_220131_0144_outdoor_temperature` | External temperature sensor ($T_A$) |
| **DHW Temp** | `sensor.luxtronik_220131_0144_dhw_temperature` | Hot water storage tank temperature |
| **DHW Target** | `number.luxtronik_220131_0144_dhw_target_temperature` | DHW setpoint |
| **Source In** | `sensor.luxtronik_220131_0144_heat_source_input_temperature` | Brine inlet temperature from ground loop |
| **Source Out** | `sensor.luxtronik_220131_0144_heat_source_output_temperature`| Brine outlet temperature back to ground loop |
| **Heating Mode** | `select.luxtronik_220131_0144_mode` / `climate` | Operation mode (`Auto`, `Party`, `Off`, etc.) |
| **End Point** | `number.luxtronik_220131_0144_heating_curve_end_temperature` | Stooklijn end point at -20°C |
| **Parallel Shift** | `number.luxtronik_220131_0144_heating_curve_parallel_shift_temperature` | Stooklijn foot point / base offset |
| **Compressor** | `binary_sensor.luxtronik_220131_0144_compressor` | Compressor running state |
| **Circ. Pump** | `binary_sensor.luxtronik_220131_0144_circulation_pump_heating`| Heating circuit pump status (`HUP`) |
| **DHW Pump** | `binary_sensor.luxtronik_220131_0144_dhw_charging_pump` | DHW charging pump (`BUP`) |
| **Aux Heater** | `binary_sensor.luxtronik_220131_0144_additional_heat_generator` | Electric immersion heater (`ZWE`) |
| **Shelly Power** | `sensor.energymonitor_warmtepomp_total_active_power` | Total 3-phase electrical power (W) |
| **Shelly Energy** | `sensor.energymonitor_warmtepomp_total_active_energy` | Cumulated electrical energy (kWh) |
| **Living Room** | `sensor.temperatuur_woonkamer_temperature` | Actual room temperature |

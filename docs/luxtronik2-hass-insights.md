# Luxtronik2-HASS Repository Analysis & Architecture Insights

This document captures the technical analysis, comparative evaluation, and architectural takeaways from the repository [`notDIRK/luxtronik2-hass`](https://github.com/notDIRK/luxtronik2-hass) for our Alpha Innotec WZS 81H/K heat pump setup.

---

## 1. Executive Summary & Context

The `notDIRK/luxtronik2-hass` repository is a custom Home Assistant integration tailored for Luxtronik 2.0 heat pump controllers (Alpha Innotec, Novelan, Buderus, Nibe, Roth, Elco, Wolf) communicating directly over TCP socket port 8889.

### Key Finding on Integration Selection
The author explicitly notes in their internal evaluation (`docs/COMPETITIVE-FEATURES.md`):
> *"BenPru/luxtronik — the reference implementation. If you look at only one repo, look at this one."*

Our system is already configured with [`BenPru/luxtronik`](https://github.com/BenPru/luxtronik), which remains the superior foundational integration for our installation. We will **not** replace our active integration. However, `notDIRK/luxtronik2-hass` introduces several high-value, opinionated control concepts and safety mechanisms that we can adopt into our Home Assistant automations, scripts, and dashboards.

---

## 2. Architectural Comparison: `BenPru/luxtronik` vs. `notDIRK/luxtronik2-hass`

| Dimension | `BenPru/luxtronik` (Current Setup) | `notDIRK/luxtronik2-hass` | Strategic Decision |
| :--- | :--- | :--- | :--- |
| **Device Structure** | Multi-device hierarchy (Heatpump, Heating, Cooling, DHW) | Flat entity structure (~31 entities) | **Keep BenPru**: Logical separation matches physical subsystems |
| **Heating Entity** | Native `climate.heating` (thermostat cards, presets, offsets) | `select` (mode) + `number` (setpoint) | **Keep BenPru**: Standard Home Assistant climate cards & automations |
| **DHW Entity** | Native `water_heater` with Automatic, Party, Holiday, Off | `select` + `number` | **Keep BenPru**: Standard water heater cards and service calls |
| **Cooling (A6 Board)**| Full cooling device support & approval binary sensor | None (cooling is completely unhandled) | **Keep BenPru**: Critical for our Comfort Board A6 passive cooling |
| **Discovery** | Auto-discovery (`zeroconf` / DHCP) + manual fallback | Manual IP entry only | **Keep BenPru** |
| **Packaged Features** | Leaves advanced routines as DIY automations | Packaged Bath Boost, Solar Boost, and Night Pause | **Adopt logic**: Replicate as native HA automations & scripts |
| **Parameter Backup** | Relies on manual exports or python scripts | Built-in button entity dumping all registers to JSON | **Adopt logic**: Create automated backup utility |

---

## 3. High-Value Concepts & Architectural Patterns to Adopt

### 3.1. Bath Boost ("Badebooster") with Dynamic ETA & Progress Tracking
Rather than just raising the domestic hot water (DHW) setpoint manually, `notDIRK` provides a complete state-managed charging session:

* **Trigger & Control Mechanism**:
  * Switches Luxtronik hot water mode to **Party mode** (`PARAM_HOT_WATER_MODE = 2` / `ID_Einst_BWS_akt = 2`).
  * Raises the DHW setpoint to a target temperature (e.g., 55.0 °C to 60.0 °C).
  * Writes both parameters atomically over the socket connection.
* **Real-time Telemetry & Dynamic ETA**:
  * Computes progress percentage:
    $$\text{Progress (\%)} = \frac{T_{\text{current}} - T_{\text{start}}}{T_{\text{target}} - T_{\text{start}}} \times 100$$
  * Dynamically calculates heating rate ($^\circ\text{C}/\text{hour}$) based on successive sensor updates from calculation index 17 (`ID_WEB_Temperatur_TBW`).
  * Computes estimated remaining minutes until target temperature:
    $$\text{ETA (min)} = \max\left(1, \frac{T_{\text{target}} - T_{\text{current}}}{\text{Heat Rate}} \times 60\right)$$
* **Automatic Deactivation & Recovery**:
  * Automatically reverts DHW mode to *Automatic* and restores the baseline setpoint once $T_{\text{current}} \ge T_{\text{target}}$.
  * **Crash/Reboot Safe**: On integration startup, inspects controller registers. If the controller is still left in Party mode with the boost setpoint, it cleans up and restores normal setpoints, preventing infinite high-temperature grid draw.
* **UI**: Paired with a compact **Mushroom Template Card** displaying running status, target, live progress, and countdown.

---

### 3.2. Automated One-Click Parameter Backup (`button.luxtronik_backup`)
Luxtronik 2.0 has hundreds of internal parameters and calculation registers. Modifying heating curves and hysteresis risks configuration drift.

* **Mechanism**:
  * Instantiates a fresh `luxtronik.Luxtronik` socket client using Python's `__new__` pattern (bypassing auto-read overhead).
  * Acquires an asyncio lock to ensure serial TCP socket access (preventing collision with cyclic polling).
  * Dumps all parameters into `{ha_config}/luxtronik2_backups/YYYY-MM-DD_HH-MM-SS.json` containing:
    ```json
    {
      "timestamp": "2026-10-11T12:00:00Z",
      "host": "192.168.x.x",
      "parameters": {
        "1": { "name": "ID_Einst_WK_akt", "type": "Temperature", "raw_value": 240, "display_value": "24.0" },
        "74": { "name": "ID_Einst_BWS_Hyst_akt", "type": "Hysteresis", "raw_value": 20, "display_value": "2.0" }
      }
    }
    ```
  * Fires a persistent notification and updates `sensor.luxtronik_last_backup`.
* **Value for Our Project**:
  * Gives us a full rollback snapshot before and after stooklijn adjustments (such as lowering end point or adjusting parallel shifts).

---

### 3.3. Solar Boost (PV Surplus) with Anti-Cycling Safeguards
The Smart Energy manager in `notDIRK` implements robust anti-cycling heuristics for PV surplus heating:

1. **Debounce Timer (300 s)**:
   * Requires continuous grid export exceeding the threshold (e.g., feed-in $> 1500\text{ W}$) for at least 5 minutes before engaging boost.
   * Prevents rapid compressor start/stop cycles during transient cloud cover.
2. **Minimum Runtime Protection**:
   * Once boost is initiated, it enforces a minimum run window (e.g., 30–45 minutes) regardless of minor solar dips.
   * Protects compressor longevity and adheres to the Luxtronik $\le 3\text{ starts/hour}$ guardrail.
3. **Hysteresis & Achievable Maximums**:
   * Reads DHW hysteresis directly from controller parameter 74 (`ID_Einst_BWS_Hyst_akt`).
   * Avoids setting target temperatures higher than the heat pump's thermodynamic ceiling without immersion heaters ($T_{\text{DHW}} \le 58\text{--}60^\circ\text{C}$). Target temperatures set too high cause perpetual restarts below threshold or unwanted auxiliary heater ($ZWE$) triggering.

---

### 3.4. Heat Quantity Meters (WMZ) Integration & Long-Term COP Tracking
The integration exposes the Luxtronik internal thermal calculation registers directly into Home Assistant's Energy Dashboard:

* `calc 151` (`ID_WEB_WMZ_Heizung`): Cumulative thermal energy delivered for space heating (kWh).
* `calc 152` (`ID_WEB_WMZ_Brauchwasser`): Cumulative thermal energy delivered for domestic hot water (kWh).
* `calc 154` (`ID_WEB_WMZ_Seit`): Cumulative total thermal energy since commissioning (kWh).
* Entities configured with `device_class: energy` and `state_class: total_increasing`.
* Enables continuous Seasonal Coefficient of Performance (SCOP) calculations when divided by Shelly 3EM active energy import.

---

### 3.5. Formatting & Dashboard Telemetry
* **Status Duration Formatter**: Luxtronik exposes operating status duration as an integer in seconds. Using a simple Jinja template sensor formats this cleanly:
  ```jinja2
  template:
    - sensor:
        - name: "Luxtronik Status Duration Formatted"
          unique_id: luxtronik_status_duration_formatted
          icon: mdi:timer-sand
          state: >
            {% set s = states('sensor.luxtronik_220131_0144_status_duration') | int(0) %}
            {{ s // 3600 }}h {{ (s % 3600) // 60 }}min
  ```
* **Grid Lockout (EVU) Representation**: Explicit conditional UI card mapping EVU contact state (`True` = Free / Contact Closed, `False` = Grid Locked / Contact Open).

---

## 4. Implementation Blueprint for Our Setup

We will incorporate these features without altering our core integration:

1. **Bath Boost Script & Automation**:
   * Script to call `water_heater.set_operation_mode` (party) and set target temperature to 58.0 °C.
   * Automation to monitor `sensor.luxtronik_220131_0144_dhw_temperature` and restore automatic mode upon reaching setpoint.
   * Add the Mushroom Template Card to `dashboards/warmtepomp-dashboard.yaml`.
2. **Luxtronik Parameter Snapshot Utility**:
   * Implement a standalone Python script in our repository / HA python_scripts / shell_command that reads socket 8889 and archives the JSON register state.
3. **Solar DHW Surplus Automation**:
   * Build a Home Assistant automation utilizing Shelly 3EM export power with the 5-minute debounce and minimum runtime protection described above.
4. **Status Duration Template**:
   * Add the formatted duration template to the Lovelace dashboard.

---

## 5. References & Links
* Repository: [notDIRK/luxtronik2-hass (GitHub)](https://github.com/notDIRK/luxtronik2-hass)
* Reference integration: [BenPru/luxtronik (GitHub)](https://github.com/BenPru/luxtronik)
* Python Luxtronik binary client: [Bouni/python-luxtronik (GitHub)](https://github.com/Bouni/python-luxtronik)

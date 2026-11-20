# Entity Mapping & Registry Reference

This document catalogs all Home Assistant entities for the Alpha Innotec WZS 81H/K heat pump (integration: `BenPru/luxtronik`, serial `220131-144`), the Shelly 3-phase energy monitor, and reference room sensors.

---

## 1. Luxtronik Temperature Sensors
| Entity ID | Friendly Name | Unit | Description |
| :--- | :--- | :--- | :--- |
| `sensor.luxtronik_220131_0144_flow_in_temperature` | Flow Temperature | °C | Supply temperature to heating system ($T_{\text{VL}}$) |
| `sensor.luxtronik_220131_0144_flow_out_temperature` | Return Temperature | °C | Actual return water temperature ($T_{\text{RL}}$) |
| `sensor.luxtronik_220131_0144_flow_out_temperature_target` | Return Target Temperature | °C | Target return temperature computed by stooklijn ($T_{\text{RL, target}}$) |
| `sensor.luxtronik_220131_0144_outdoor_temperature` | Outdoor Temperature | °C | External ambient temperature sensor ($T_A$) |
| `sensor.luxtronik_220131_0144_dhw_temperature` | DHW Temperature | °C | Domestic hot water cylinder temperature |
| `sensor.luxtronik_220131_0144_heat_source_input_temperature` | Heat Source Input Temp | °C | Brine temperature coming from ground loop |
| `sensor.luxtronik_220131_0144_heat_source_output_temperature` | Heat Source Output Temp | °C | Brine return temperature returning to ground loop |

---

## 2. Luxtronik Control Numbers & Modes
| Entity ID | Type | Current Live Value (Nov 2026) | Description |
| :--- | :--- | :--- | :--- |
| `number.luxtronik_220131_0144_heating_curve_end_temperature` | `number` | `35.0 °C` | Stooklijn end point (return setpoint at -20°C outdoor) |
| `number.luxtronik_220131_0144_heating_curve_parallel_shift_temperature` | `number` | `22.0 °C` | Stooklijn base offset / foot point (shift across all outdoor temps) |
| `number.luxtronik_220131_0144_heating_target_correction` | `number` | `-3.5 °C` | Heating target correction (modified by RFV-DK rotary dial / HA) |
| `number.luxtronik_220131_0144_dhw_target_temperature` | `number` | `58.0 °C` | Domestic hot water target setpoint |
| `number.luxtronik_220131_0144_dhw_hysteresis` | `number` | `7.0 K` | DHW start threshold ($T_{\text{DHW}} \le \text{Target} - \text{Hysteresis}$) |
| `number.luxtronik_220131_0144_cooling_threshold_temperature` | `number` | `24.0 °C` | Outdoor temperature threshold to engage passive cooling |
| `sensor.luxtronik_220131_0144_status` | `sensor` | `heating` / `hot_water` / `no_request` / `cooling` | Active operational state of the heat pump (`ID_WEB_WP_BZ_akt`) |
| `update.luxtronik_220131_0144_firmware` | `update` | `V1.88.3` (`V1.90.0` skipped) | Controller firmware version (`V1.90.0` has a critical write-reboot bug on port 8889) |

---

## 3. Luxtronik Relays, Pumps & Binary Sensors
| Entity ID | Name | Role |
| :--- | :--- | :--- |
| `binary_sensor.luxtronik_220131_0144_compressor` | Compressor 1 | `on` when compressor is active |
| `binary_sensor.luxtronik_220131_0144_circulation_pump_heating` | HUP | Heating circulation pump |
| `binary_sensor.luxtronik_220131_0144_additional_circulation_pump` | ZUP | Auxiliary / floor heating circulation pump |
| `binary_sensor.luxtronik_220131_0144_dhw_charging_pump` | BUP | DHW diverter valve / cylinder charging pump |
| `binary_sensor.luxtronik_220131_0144_additional_heat_generator` | ZWE | Auxiliary electric immersion heater (6 kW) |
| `binary_sensor.luxtronik_220131_0144_evu_unlocked` | EVU Unlocked | Grid utility lock release (`on` = allowed to run) |

---

## 4. Operational Statistics & Diagnostics
| Entity ID | Description |
| :--- | :--- |
| `sensor.luxtronik_220131_0144_compressor1_impulses` | Total compressor start cycles |
| `sensor.luxtronik_220131_0144_compressor1_operation_hours` | Total compressor running hours |
| `sensor.luxtronik_220131_0144_operation_hours_heating` | Cumulative hours spent in space heating mode |
| `sensor.luxtronik_220131_0144_dhw_operation_hours` | Cumulative hours spent in DHW mode |
| `sensor.luxtronik_220131_0144_additional_heat_generator_operation_hours` | Cumulative hours of 6kW electric immersion heater |
| `sensor.luxtronik_220131_0144_error_reason` | Most recent Luxtronik fault / alarm code |

---

## 5. Electrical Monitoring (Shelly 3-Phase) & Environment
| Entity ID | Description |
| :--- | :--- |
| `sensor.energymonitor_warmtepomp_total_active_power` | Total active electrical power draw (W) |
| `sensor.energymonitor_warmtepomp_phase_a_active_power` | Phase A active power (W) |
| `sensor.energymonitor_warmtepomp_phase_b_active_power` | Phase B active power (W) |
| `sensor.energymonitor_warmtepomp_phase_c_active_power` | Phase C active power (W) |
| `sensor.energymonitor_warmtepomp_total_active_energy` | Total energy consumption (kWh) |
| `sensor.temperatuur_woonkamer_temperature` | Actual living room temperature (°C) |

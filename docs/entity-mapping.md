# Entity Mapping & Registry Reference

This document catalogs all Home Assistant entities for the Alpha Innotec WZS 81H/K heat pump (integration: `BenPru/luxtronik`, serial `220131-144`), the Shelly 3-phase energy monitor, per-mode energy utility meters, OpenEnergyMonitor diagnostic template sensors, and reference room sensors.

---

## 1. Luxtronik Temperature Sensors
| Entity ID | Friendly Name | Unit | Description |
| :--- | :--- | :--- | :--- |
| `sensor.luxtronik_220131_0144_flow_in_temperature` | Flow Temperature | °C | Supply temperature to heating system ($T_{\text{VL}}$) |
| `sensor.luxtronik_220131_0144_flow_out_temperature` | Return Temperature | °C | Actual return water temperature ($T_{\text{RL}}$) |
| `sensor.luxtronik_220131_0144_flow_out_temperature_target` | Return Target Temperature | °C | Target return temperature computed by stooklijn ($T_{\text{RL, target}}$) |
| `sensor.luxtronik_220131_0144_outdoor_temperature` | Outdoor Temperature | °C | External ambient temperature sensor ($T_A$) |
| `sensor.luxtronik_220131_0144_outdoor_temperature_average` | Avg. Outdoor Temperature | °C | Filtered/averaged outdoor temperature |
| `sensor.luxtronik_220131_0144_dhw_temperature` | DHW Temperature | °C | Domestic hot water cylinder temperature |
| `sensor.luxtronik_220131_0144_heat_source_input_temperature` | Heat Source Input Temp | °C | Brine temperature coming from ground loop |
| `sensor.luxtronik_220131_0144_heat_source_output_temperature` | Heat Source Output Temp | °C | Brine return temperature returning to ground loop |
| `sensor.luxtronik_220131_0144_hot_gas_temperature` | Hot Gas Temperature | °C | Compressor discharge hot gas temperature |

---

## 2. Luxtronik Control Numbers & Modes
| Entity ID | Type | Current Live Value (Nov 2026) | Description |
| :--- | :--- | :--- | :--- |
| `number.luxtronik_220131_0144_heating_curve_end_temperature` | `number` | `35.0 °C` | Stooklijn end point (return setpoint at -20°C outdoor) |
| `number.luxtronik_220131_0144_heating_curve_parallel_shift_temperature` | `number` | `22.0 °C` | Stooklijn base offset / foot point (shift across all outdoor temps) |
| `number.luxtronik_220131_0144_heating_target_correction` | `number` | `-3.5 °C` | Heating target correction (modified by RFV-DK rotary dial / HA) |
| `number.luxtronik_220131_0144_heating_hysteresis` | `number` | `2.0 K` | Space heating return temperature hysteresis |
| `number.luxtronik_220131_0144_dhw_target_temperature` | `number` | `58.0 °C` | Domestic hot water target setpoint |
| `number.luxtronik_220131_0144_dhw_hysteresis` | `number` | `7.0 K` | DHW start threshold ($T_{\text{DHW}} \le \text{Target} - \text{Hysteresis}$) |
| `number.luxtronik_220131_0144_cooling_threshold_temperature` | `number` | `20.0 °C` | Outdoor temperature threshold to engage passive cooling |
| `sensor.luxtronik_220131_0144_status` | `sensor` | `heating` / `hot_water` / `no_request` / `cooling` | Active operational state of the heat pump (`ID_WEB_WP_BZ_akt`) |
| `update.luxtronik_220131_0144_firmware` | `update` | `V1.88.3` (`V1.90.0` skipped) | Controller firmware version (`V1.90.0` has a critical write-reboot bug on port 8889) |

---

## 3. Luxtronik Relays, Pumps & Binary Sensors
| Entity ID | Name | Role |
| :--- | :--- | :--- |
| `binary_sensor.luxtronik_220131_0144_compressor` | Compressor 1 | `on` when compressor is active |
| `binary_sensor.luxtronik_220131_0144_circulation_pump_heating` | HUP | Heating circulation pump |
| `binary_sensor.luxtronik_220131_0144_additional_circulation_pump` | ZUP | Auxiliary / floor heating circulation pump |
| `binary_sensor.luxtronik_220131_0144_dhw_recirculation_pump` | BUP (`0038 ID_WEB_BUPout`) | DHW diverter valve / cylinder charging pump (active during `hot_water` cycles) |
| `binary_sensor.luxtronik_220131_0144_dhw_charging_pump` | ZIP (`0046 ID_WEB_ZIPout`) | External DHW ring-main circulation pump (not physically installed; permanently `off`) |
| `binary_sensor.luxtronik_220131_0144_additional_heat_generator` | ZWE | Auxiliary electric immersion heater (6 kW) |
| `binary_sensor.luxtronik_220131_0144_approval_cooling` | Cool Approval | Passive cooling approval state |
| `binary_sensor.luxtronik_220131_0144_evu_unlocked` | EVU Unlocked | Grid utility lock release (`on` = allowed to run) |

---

## 4. Operational Statistics & Diagnostics
| Entity ID | Description |
| :--- | :--- |
| `sensor.luxtronik_220131_0144_compressor1_impulses` | Total compressor start cycles |
| `sensor.luxtronik_220131_0144_compressor1_operation_hours` | Total compressor running hours |
| `sensor.luxtronik_220131_0144_operation_hours_heating` | Cumulative hours spent in space heating mode |
| `sensor.luxtronik_220131_0144_dhw_operation_hours` | Cumulative hours spent in DHW mode |
| `sensor.luxtronik_220131_0144_operation_hours_cooling` | Cumulative hours spent in passive cooling mode |
| `sensor.luxtronik_220131_0144_additional_heat_generator_operation_hours` | Cumulative hours of 6kW electric immersion heater |
| `sensor.luxtronik_220131_0144_error_reason` | Most recent Luxtronik fault / alarm code |

---

## 5. Electrical Monitoring (Shelly 3-Phase) & Environment
| Entity ID | Unit | Description |
| :--- | :--- | :--- |
| `sensor.energymonitor_warmtepomp_total_active_power` | kW | Total active electrical power draw |
| `sensor.energymonitor_warmtepomp_phase_a_active_power` | W | Phase A active power |
| `sensor.energymonitor_warmtepomp_phase_b_active_power` | W | Phase B active power |
| `sensor.energymonitor_warmtepomp_phase_c_active_power` | W | Phase C active power |
| `sensor.energymonitor_warmtepomp_total_active_energy` | kWh | Total cumulative electrical energy consumption |
| `sensor.warmtepomp_totaal_energie_dagelijks` | kWh | Daily total electrical energy (`utilitymeter.yaml`, `cycle: daily`) |
| `sensor.temperatuur_woonkamer_temperature` | °C | Actual living room temperature |

---

## 6. Per-Mode Energy Tracking (`utility_meter`, 6 Tariffs)
| Entity ID | Tariff / Type | Unit | Description |
| :--- | :--- | :--- | :--- |
| `select.warmtepomp_energie` | `select` | — | Active tariff selector controlled by `automation.warmtepomp_energiemodus_schakelaar` |
| `sensor.warmtepomp_energie_heating` | `heating` | kWh | Cumulative electrical energy consumed in Space Heating mode |
| `sensor.warmtepomp_energie_hot_water` | `hot_water` | kWh | Cumulative electrical energy consumed in DHW Boiler Charging mode |
| `sensor.warmtepomp_energie_cooling` | `cooling` | kWh | Cumulative electrical energy consumed in Passive Cooling mode |
| `sensor.warmtepomp_energie_aux_heater` | `aux_heater` | kWh | Cumulative electrical energy consumed while 6 kW Auxiliary Heater (`ZWE`) is active |
| `sensor.warmtepomp_energie_circulation` | `circulation` | kWh | Cumulative electrical energy consumed by circulation pumps (`HUP`/`ZUP`/`BUP`) when compressor is off |
| `sensor.warmtepomp_energie_standby` | `standby` | kWh | Cumulative electrical energy consumed in pure controller idle standby |

---

## 7. OpenEnergyMonitor Diagnostic Template Sensors (Steady-State LTS Hygiene — Issue #4)
| Entity ID | Entry ID | Unit | Formula / Steady-State Gating Logic |
| :--- | :--- | :--- | :--- |
| `sensor.warmtepomp_geschatte_cop` | `01M7XA0ZVAEZ4WFX6HEM9JW1S0` | COP | Combined steady-state Practical Carnot COP ($0.50 \times \frac{T_{\text{VL}} + 273.15}{(T_{\text{VL}} - T_{\text{brine, out}}) + 4.0}$) when compressor is running (`status_time >= 180`, $\Delta T_{\text{cond}} \ge 1.5\text{ K}$, $\Delta T_{\text{brine}} \ge 1.0\text{ K}$, plus $T_{\text{VL}} < 45^\circ\text{C}$ in `heating` or $T_{\text{VL}} \ge T_{\text{DHW}}$ in `hot_water`; `1.0` if ZWE only; `none` during startup/transition/idle) |
| `sensor.warmtepomp_cop_verwarmen` | `01M7Z02H76733XD16C95QSJ5G1` | COP | Mode-specific steady-state Carnot COP **only** during `status == 'heating'` (`status_time >= 180`, $T_{\text{VL}} < 45^\circ\text{C}$, $\Delta T_{\text{cond}} \ge 1.5\text{ K}$, $\Delta T_{\text{brine}} \ge 1.0\text{ K}$, `ZWE == 'off'`), else `none` |
| `sensor.warmtepomp_cop_tapwater` | `01M7Z02JYGG02C9WMYJ50YT27W` | COP | Mode-specific steady-state Carnot COP **only** during `status == 'hot_water'` (`status_time >= 180`, $T_{\text{VL}} \ge T_{\text{DHW}}$, $\Delta T_{\text{cond}} \ge 1.5\text{ K}$, $\Delta T_{\text{brine}} \ge 1.0\text{ K}$, `ZWE == 'off'`), else `none` |
| `sensor.warmtepomp_condensor_delta_t` | `01M7XA0T9ZVCF13G20MMEH0JQ7` | K | Active steady-state condenser temperature spread ($T_{\text{VL}} - T_{\text{RL}}$) gated on `steady_heat or steady_dhw` (`status_time >= 180`, $\Delta T_{\text{cond}} \ge 1.5\text{ K}$, and $T_{\text{VL}} \ge T_{\text{DHW}}$ during `hot_water` to exclude `-10.7 K` 3-way valve transitions), else `none` |
| `sensor.warmtepomp_bodembron_delta_t` | `01M7XA0WD13C8JG4SN2KKZSPBC` | K | Active steady-state ground loop brine spread ($T_{\text{brine, in}} - T_{\text{brine, out}}$) gated on `compressor == 'on'`, `status_time >= 180`, and $\Delta T_{\text{brine}} \ge 1.0\text{ K}$, else `none` |
| `sensor.warmtepomp_actieve_aanvoertemperatuur_verwarmen` | `01M7Z02MCSRAKN471339CMPKF2` | °C | Active steady-state heating supply temperature ($T_{\text{VL}}$) **only** during steady-state `heating`, else `none` |
| `sensor.warmtepomp_actieve_bodembron_inlaattemperatuur` | `01M7Z02PEQXW1Q7JVJF4DM7F4M` | °C | Active steady-state ground loop brine inlet temperature ($T_{\text{brine, in}}$) when compressor is running (`status_time >= 180`, $\Delta T_{\text{brine}} \ge 1.0\text{ K}$), else `none` |
| `sensor.warmtepomp_actieve_bodembron_uitlaattemperatuur` | `01M7Z02RB474KT0AJ6CKAA2VSP` | °C | Active steady-state ground loop brine outlet temperature ($T_{\text{brine, out}}$) when compressor is running (`status_time >= 180`, $\Delta T_{\text{brine}} \ge 1.0\text{ K}$), else `none` |
| `sensor.warmtepomp_graaddagen_hdd18` | `01M7XA0Y140PXRAPFWZXR4X93T` | °C | Instantaneous Heating Degree Days weight ($\max(0, 18.0 - T_{\text{outdoor}})$) |
| `sensor.warmtepomp_gemiddelde_compressor_runduur` | `01M7XA113WZFPJPZCBXDJA6A8E` | min | Cumulative average compressor run duration per start ($\frac{\text{Hours} \times 60}{\text{Starts}}$) |

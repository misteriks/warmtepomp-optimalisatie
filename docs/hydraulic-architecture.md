# Hydraulic Architecture & Thermodynamics: Alpha Innotec WZS 81H/K

Engineering and schematic reference for the **Alpha Innotec WZS 81H/K** ground-source heat pump (Luxtronik 2.0 controller).

---

## 1. Physical Hydraulic Overview

The Alpha Innotec WZS 81H/K compact tower contains an integrated 178-liter DHW cylinder, plate condenser, plate evaporator, auxiliary electric immersion heater (ZWE 6kW), and an internal 3-way diverter valve.

```
                              [ 🚿 SANITARY DHW CONSUMERS (Shower/Taps) ]
                                                  ^
                                                  | (Potable Hot Water 50-55°C)
                          +-------------------------------------------------------+
                          |      INTEGRATED DHW CYLINDER (178L Enamelled Tank)    |
                          |  +-------------------------------------------------+  |
                          |  |        Internal Heating Coil (Laadspiraal)      |  |
                          |  +------------------------^------------------------+  |
                          +---------------------------|---------------------------+
                                                      |
                                          (DHW Supply | (DHW Return from coil
                                              60-65°C)|  55-60°C)
                                                      |   |
                                              [3-Way Diverter Valve]
                                                 /              \
                                         [DHW Position]     [Heating Position]
                                               ^                  \
                                               |                   \ (Heating Supply 25-35°C)
                                               |                    v
  [ CONDENSER (Platenwarmtewisselaar) ]--------+           [ 🏠 UNDERFLOOR HEATING ]
  - Outlet: Flow In  (Aanvoer: 61.5°C / 28°C)                        |
  - Inlet:  Flow Out (Retour:  58.4°C / 23°C)<-----------------------+ (Heating Return 20-30°C)
           ^
           | (High-pressure R410A refrigerant gas)
  [ COMPRESSOR ] + [ ZWE 6kW AUX HEATER ]
           ^
           | (Low-pressure R410A evaporating)
  [ EVAPORATOR (Verdamper) ]
  - Inlet:  Heat Source In  (Bron In:  10-12°C from ground loop)
  - Outlet: Heat Source Out (Bron Uit:  6-8°C back to ground loop)
           ^                                |
           | (Warmed Brine)                 | (Chilled Brine)
  [ VERZAMELAAR (Warm Manifold) ]   [ VERDELER (Cold Manifold) ]
           ^                                |
           +==========[ BOREHOLE LOOPS ]====+
```

---

## 2. Operating Modes & Hydraulic State Matrix

| System State | 3-Way Valve Position | Primary Supply / Return Temp | Boiler Coil Flow | Floor Heating Flow | Geothermal Brine Flow |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Warm Tapwater (DHW)** | Diverted **UP** to Boiler | High ($60\text{--}65^\circ\text{C}$ / $55\text{--}60^\circ\text{C}$) | **Active** | **Zero / Idle** | **Active** (Compressor running) |
| **CV Verwarmen (Heating)**| Diverted **RIGHT** to Floor | Low ($25\text{--}35^\circ\text{C}$ / $20\text{--}30^\circ\text{C}$) | **Zero / Idle** | **Active** | **Active** (Compressor running) |
| **Passieve Koeling (/K)** | Diverted **RIGHT** to Floor | Low ($18\text{--}20^\circ\text{C}$) | **Zero / Idle** | **Active** | **Active** (Passive HX, Compressor OFF)|
| **Standby / Circulatie** | Last known position | Ambient room temp | **Zero / Idle** | **Periodic** (Pump opt) | **Zero / Idle** |

---

## 3. UI/UX Mapping Guidelines for Lovelace Dashboards

1. **Aanvoer & Retour Sensor Placement**:
   - `sensor.luxtronik_220131_0144_flow_in_temperature` (Aanvoer) is located on the primary condenser outlet.
   - `sensor.luxtronik_220131_0144_flow_out_temperature` (Retour) is located on the primary condenser inlet.
   - **Crucial Rule**: Never show Aanvoer/Retour sitting exclusively on the floor heating circuit, because during DHW mode those high temperatures ($60^\circ\text{C}+$) circulate exclusively through the boiler coil.
2. **Dual-Manifold Ground Circuit**:
   - Always illustrate geothermal loops using side-by-side distribution manifolds (Cold distributor on the left, Warm collector on the right) with zero overlapping pipe runs.

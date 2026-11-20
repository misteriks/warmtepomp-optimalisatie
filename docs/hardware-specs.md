# Hardware Specifications: Alpha Innotec WZS 81H/K

## 1. System Overview
The **Alpha Innotec WZS 81H/K** is a compact, ground-source (brine/water) heat pump with an integrated domestic hot water (DHW) storage cylinder and hydraulic tower.

- **Manufacturer**: Alpha Innotec (NIBE Group / Nathan Group NL)
- **Model**: WZS 81H/K
- **Serial Number**: `220131-144`
- **MAC Address**: `40:ec:f8:00:b5:99`
- **Controller**: Luxtronik 2.0 (Microprocessor control with graphical display and web interface)

---

## 2. Technical Ratings & Capacity
- **Heating Capacity (B0/W35 EN 14511)**: ~7.8 – 8.2 kW
- **COP (B0/W35)**: ~4.6 – 4.8
- **Refrigerant**: R410A
- **Auxiliary Electric Heater (ZWE)**: 6.0 kW (3-stage immersion heater)
- **Integrated DHW Storage Tank**: 175–180 Liters (enameled steel with sacrificial anode)
- **Passive Cooling**: Integrated natural cooling heat exchanger module (`/K` version)

---

## 3. Controller & Expansion Boards
- **Luxtronik 2.0 Mainboard**:
  - Network interface (Ethernet RJ45) on port `8889` (Java Webinterface) and `8888` (RAW ASCII / socket protocol)
  - LIN-bus connection to room controllers
- **Comfort Board (A6)**:
  - Installed (`yes`)
  - Controls auxiliary mixing circuits (MK1/MK2) and passive cooling diverter valves
- **Ventilation Board (A7)**:
  - Installed (`yes`)
  - Interfaced for controlled residential ventilation
- **Room Terminal**:
  - **RFV-DK**: Room controller with LCD display and rotary dial (±0.2 K parallel offset adjustment)

---

## 4. Hydraulic Architecture
1. **Primary Circuit (Ground Source / Brine)**:
   - Closed-loop vertical geothermal boreholes / ground collectors
   - Monitored via Source In (`sensor.luxtronik_220131_0144_heat_source_input_temperature`) and Source Out (`sensor.luxtronik_220131_0144_heat_source_output_temperature`)
2. **Secondary Circuit (Heating / Floor Heating)**:
   - Low-temperature underfloor heating across living spaces
   - Regulated by return temperature setpoint ($T_{\text{RL, target}}$)
   - Heating circulation pump (`HUP`)
3. **DHW Circuit**:
   - Internal 3-way diverter valve / DHW charging pump (`BUP`)
   - Prioritized over space heating

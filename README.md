# Alpha Innotec WZS 81H/K Heat Pump Optimization Project

Dedicated workspace for telemetry, diagnostic dashboards, mathematical modeling, and energy optimization for the **Alpha Innotec WZS 81H/K** ground-source heat pump (Luxtronik 2.0 controller).

---

## 📌 System Profile
- **Heat Pump Model**: Alpha Innotec WZS 81H/K (Brine/Water)
- **Controller**: Luxtronik 2.0 (Web/Socket Interface, Firmware `V1.88.3-9717` — *do not upgrade to `V1.90.0` due to port 8889 write crash bug*)
- **Serial Number**: `220131-144` (HA entity prefix: `220131_0144`)
- **MAC Address**: `40:ec:f8:00:b5:99`
- **Installed Expansion Boards**: Comfort Board (A6), Ventilation Board (A7)
- **Room Terminal**: RFV-DK
- **3-Phase Energy Monitoring**: Shelly 3EM / Pro 3EM (`sensor.energymonitor_warmtepomp_*`)
- **Reference Indoor Temp**: `sensor.temperatuur_woonkamer_temperature`

---

## 🎯 Primary Goals
1. **Per-Mode Energy & Power Telemetry**: Track electrical consumption (`kWh` and `W`) separately across operational states (`Heating`, `DHW / Hot Water`, `Passive Cooling`, `Auxiliary Heater ZWE`, and `Standby / Circulation Pumps`).
2. **Prevent Winter Living Room Overheating**: Solve overshooting ($24^\circ\text{C}+$) by optimizing the weather-compensated stooklijn parameters (End point currently $35.0^\circ\text{C}$, Shift $22.0^\circ\text{C}$, Manual Offset $-3.5^\circ\text{C}$).
3. **Optimize Electrical Consumption & COP**: Lower total kWh (including DHW target/hysteresis tuning) and improve seasonal COP.
4. **Structured Experiment Tracking**: Log every parameter change, baseline snapshot, and 48–72h thermal evaluation in GitHub Issues.

---

## 📂 Project Structure
```
/home/agy/workspace/warmtepomp/
├── .agents/
│   ├── AGENTS.md                               # Project rules, guardrails & system profile
│   └── skills/
│       └── alpha-innotec-luxtronik/
│           └── SKILL.md                        # Luxtronik skill & register map
├── docs/
│   ├── hardware-specs.md                       # WZS 81H/K specifications & hydraulics
│   ├── hydraulic-architecture.md               # Hydraulic schematic & 3-way valve state matrix
│   ├── entity-mapping.md                       # Catalog of Home Assistant entities
│   ├── stooklijn-optimization-guide.md         # Stooklijn math & tuning protocol
│   ├── luxtronik2-hass-insights.md             # Architectural insights & automation blueprints
│   └── manuals/                                # Original PDF manuals & wiring diagrams
├── dashboards/
│   └── warmtepomp-dashboard.yaml               # Diagnostic dashboard (Flow Card + Plotly)
├── automations/
│   └── dynamic_stooklijn_compensation.yaml     # HA room temperature feedback automation
├── scripts/
│   └── cop_calculator.py                       # Analytical scripts for COP & curve simulation
└── README.md                                   # Project overview & documentation
```

---

## 🎨 Related Repository: Luxtronik Flow Card
The custom Lovelace flow card (`custom:luxtronik-flow-card`) is maintained in its own dedicated repository:
- **Repository**: [`misteriks/ha-luxtronik-flow-card`](https://github.com/misteriks/ha-luxtronik-flow-card)

# Stooklijn (Heating Curve) Optimization Guide

## 1. Mathematical Foundation of the Luxtronik Heating Curve

The Luxtronik 2.0 controller calculates the target return temperature ($T_{\text{RL, target}}$) using outdoor temperature ($T_A$), the heating curve end point ($T_{\text{end}}$), parallel shift ($T_{\text{shift}}$), and dynamic correction ($\Delta T_{\text{corr}}$):

$$T_{\text{RL, target}} = T_{\text{shift}} + \left(\frac{T_{\text{end}} - T_{\text{shift}}}{-20^\circ\text{C} - 20^\circ\text{C}}\right) \cdot (T_A - 20^\circ\text{C}) + \Delta T_{\text{corr}}$$

Simplified for standard $+20^\circ\text{C}$ reference outdoor temperature:

$$T_{\text{RL, target}} = T_{\text{shift}} + \left(\frac{T_{\text{end}} - T_{\text{shift}}}{-40}\right) \cdot (T_A - 20) + \Delta T_{\text{corr}}$$

### Current Configuration vs Recommended Low-Temperature Target
| Parameter | Current Setting | Recommended Target (Underfloor Heating) | Rationale |
| :--- | :--- | :--- | :--- |
| **End Point ($T_{\text{end}}$ @ $-20^\circ\text{C}$)** | **35.0 °C** | **27.0 – 29.0 °C** | 35°C is sized for radiators or uninsulated buildings. For modern underfloor heating, return temps above 30°C cause severe room overheating. |
| **Parallel Shift ($T_{\text{shift}}$ @ $+20^\circ\text{C}$)** | **24.0 °C** | **20.5 – 21.5 °C** | 24°C base return temperature forces heating even when mild outdoor temps ($12\text{--}18^\circ\text{C}$) are present. |
| **Heating Hysteresis** | **2.0 K** | **1.5 – 2.0 K** | Prevents rapid cycling while ensuring long, steady compressor runs. |

---

## 2. Root Cause Analysis of Winter Overheating (24°C+)

1. **High Stooklijn Slope ($T_{\text{end}} = 35^\circ\text{C}$)**:
   When outdoor temperatures drop below $0^\circ\text{C}$, the target return temperature climbs towards $30\text{--}32^\circ\text{C}$. In an underfloor heating system, this saturates the screed floor with excessive thermal energy, pushing indoor air temperatures to $24^\circ\text{C}+$.
2. **Pure Weather-Compensated Blindness**:
   Without room feedback, when sunlight strikes the living room windows or internal heat gains occur, the heat pump continues to inject heat at the rate commanded by the outdoor temperature sensor.

---

## 3. Step-by-Step Optimization Protocol

### Step 1: Lower the Base Parameters (Luxtronik)
1. **Reduce Stooklijn End Point**:
   - Current: $35.0^\circ\text{C}$
   - Target Phase 1: $31.0^\circ\text{C}$
   - Target Phase 2: $28.0^\circ\text{C}$
2. **Reduce Parallel Shift (Foot Point)**:
   - Current: $24.0^\circ\text{C}$
   - Target Phase 1: $22.0^\circ\text{C}$
   - Target Phase 2: $21.0^\circ\text{C}$

> [!IMPORTANT]
> **Thermal Settling Window**: Underfloor heating systems have high thermal inertia (8 to 14 hours). Adjust parameters in increments of no more than $1.0\text{--}1.5\,\text{K}$ and observe room temperatures across 48 to 72 hours before making further changes.

### Step 2: Implement Dynamic HA Room Compensation Automation
Create a closed-loop feedback in Home Assistant using `sensor.temperatuur_woonkamer_temperature`:
- When Room Temp $> 21.8^\circ\text{C}$ $\rightarrow$ Set `number.luxtronik_220131_0144_heating_target_correction` to $-1.0\,\text{K}$.
- When Room Temp $> 22.5^\circ\text{C}$ $\rightarrow$ Set correction to $-2.0\,\text{K}$.
- When Room Temp $\le 21.0^\circ\text{C}$ $\rightarrow$ Reset correction to $0.0\,\text{K}$.

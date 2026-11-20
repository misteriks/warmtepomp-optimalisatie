"""
COP (Coefficient of Performance) and Stooklijn Calculator for Alpha Innotec WZS 81H/K
"""

def calculate_stooklijn_target(outdoor_temp: float, end_point: float = 35.0, shift: float = 24.0, correction: float = 0.0) -> float:
    """
    Calculates the target return temperature (T_RL, target) according to Luxtronik formula.
    
    T_RL,target = shift + ((end_point - shift) / (-40)) * (outdoor_temp - 20) + correction
    """
    slope = (end_point - shift) / -40.0
    return shift + slope * (outdoor_temp - 20.0) + correction


def estimate_thermal_power(flow_temp: float, return_temp: float, flow_rate_lpm: float = 22.0) -> float:
    """
    Estimates thermal power output (kW) using Q_dot = m_dot * c_p * delta_T.
    c_p of water approx 4.184 kJ/(kg*K).
    flow_rate_lpm is flow rate in liters per minute (1 lpm = 1/60 kg/s).
    """
    delta_t = flow_temp - return_temp
    if delta_t <= 0:
        return 0.0
    mass_flow_kg_s = flow_rate_lpm / 60.0
    specific_heat = 4.184  # kJ/(kg*K)
    return mass_flow_kg_s * specific_heat * delta_t  # kW


def calculate_cop(thermal_power_kw: float, electrical_power_w: float) -> float:
    """
    Calculates COP = Thermal Power (kW) / Electrical Power (kW).
    """
    if electrical_power_w <= 100.0 or thermal_power_kw <= 0:
        return 0.0
    electrical_power_kw = electrical_power_w / 1000.0
    return thermal_power_kw / electrical_power_kw


if __name__ == "__main__":
    print("=== Alpha Innotec WZS 81H/K Stooklijn Simulation ===")
    outdoor_temps = [-10, -5, 0, 5, 10, 15]
    
    print("\nCurrent Curve (End=35°C, Shift=24°C):")
    for t in outdoor_temps:
        target = calculate_stooklijn_target(t, end_point=35.0, shift=24.0)
        print(f"Outdoor: {t:3d}°C -> Target Return: {target:.1f}°C")
        
    print("\nOptimized Curve (End=28°C, Shift=21°C):")
    for t in outdoor_temps:
        target = calculate_stooklijn_target(t, end_point=28.0, shift=21.0)
        print(f"Outdoor: {t:3d}°C -> Target Return: {target:.1f}°C")

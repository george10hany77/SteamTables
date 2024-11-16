import numpy as np
from iapws import IAPWS97

def calculate_water_properties(v, p):
    """
    Calculate water/steam properties using IAPWS97 formulations
    given specific volume (v) in m³/kg and pressure (p) in MPa.
    
    Parameters:
    -----------
    v : float
        Specific volume in m³/kg
    p : float
        Pressure in MPa
    
    Returns:
    --------
    dict
        Dictionary containing calculated properties
    """
    try:
        # Initialize properties by guessing temperature
        # Start with saturated temperature at given pressure as initial guess
        sat_water = IAPWS97(P=p, x=0)
        T_guess = sat_water.T
        
        # Iterate to find temperature that matches given specific volume
        def objective(T):
            state = IAPWS97(P=p, T=T)
            return state.v - v
        
        # Simple binary search to find temperature
        T_min, T_max = 273.15, 2273.15  # Valid temperature range
        T = T_guess
        
        for _ in range(50):  # Maximum iterations
            state = IAPWS97(P=p, T=T)
            if abs(state.v - v) < 1e-8:
                break
            if state.v > v:
                T_max = T
            else:
                T_min = T
            T = (T_min + T_max) / 2
        
        # Calculate final state
        state = IAPWS97(P=p, T=T)
        
        # Return dictionary of properties
        properties = {
            'temperature': state.T,          # K
            'pressure': state.P,             # MPa
            'specific_volume': state.v,      # m³/kg
            'density': state.rho,            # kg/m³
            'specific_enthalpy': state.h,    # kJ/kg
            'specific_entropy': state.s,     # kJ/kg·K
            'cp': state.cp,                  # kJ/kg·K
            'cv': state.cv,                  # kJ/kg·K
            'viscosity': state.mu,           # Pa·s
            'thermal_conductivity': state.k,  # W/m·K
            'phase': state.phase
        }
        return properties
        
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Example: Calculate properties for saturated steam at 1 MPa
    v = 0.194  # m³/kg
    p = 1.0    # MPa
    
    properties = calculate_water_properties(v, p)
    
    if isinstance(properties, dict):
        print("\nWater/Steam Properties:")
        for key, value in properties.items():
            if isinstance(value, float):
                print(f"{key:25}: {value:.6g}")
            else:
                print(f"{key:25}: {value}")
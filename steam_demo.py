from iapws import IAPWS97

def steam_properties_calculator(pressure, temperature):
    """
    Calculate steam properties for given pressure and temperature.

    Args:
        pressure (float): Pressure in MPa
        temperature (float): Temperature in °C

    Returns:
        dict: A dictionary containing properties like enthalpy, entropy, and density.
    """
    # Create a state for water/steam based on pressure (MPa) and temperature (Celsius)
    water = IAPWS97(P=pressure, T=temperature + 273.15)  # Convert °C to Kelvin

    properties = {
        "Temperature (°C)": temperature,
        "Pressure (MPa)": pressure,
        "Enthalpy (kJ/kg)": water.h,
        "Entropy (kJ/kg·K)": water.s,
        "Density (kg/m³)": water.rho,
        "Internal Energy (kJ/kg)": water.u,
        "Specific Volume (m³/kg)": 1 / water.rho
    }

    return properties

# Example usage
pressure = 1.0  # MPa
temperature = 150  # °C

properties = steam_properties_calculator(pressure, temperature)

print("Steam Properties:")
for key, value in properties.items():
    print(f"{key}: {value}")
    
from SteamCalculator import SteamCalculator
from STD_TYPES import *


def main():
    pressure = Pressure(0.4)  # MPa
    temperature = Temperature(143.61)  # °C
    enthalpy = Enthalpy(3000)  # kJ/kg
    entropy = Entropy(6.6430)  # kJ/kg·K
    s_volume = Specific_Volume(0.0021)  # m³/kg
    internal_energy = InternalEnergy(301)  # kJ/kg

    calculator = SteamCalculator()
    # calculator.pressure_with_internal_energy(pressure=pressure, internal_energy=internal_energy)
    calculator.pressure_with_enthalpy(pressure=pressure, enthalpy=enthalpy)
    calculator.display()


if __name__ == "__main__":
    main()

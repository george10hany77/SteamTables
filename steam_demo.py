from SteamCalculator import *

def main():
    pressure = Pressure(50)  # MPa
    temperature = Temperature(122)  # °C
    enthalpy = Enthalpy(1826.6)  # kJ/kg
    entropy = Entropy(6.6430)  # kJ/kg·K
    s_volume = Specific_Volume(0.00061)  # m³/kg
    internal_energy = InternalEnergy(13111)  # kJ/kg

    param = {"internal_energy": internal_energy, "temperature": temperature}

    calculator = SteamCalculator()
    calculator.temperature_with_internal_energy(**param)
    calculator.display()

    phase, x = determine_phase(prop_1=internal_energy, prop_2=temperature)
    print(f"Phase: {phase.name}")


if __name__ == "__main__":
    main()

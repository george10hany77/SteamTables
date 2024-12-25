from SteamCalculator import *


def main():
    pressure = Pressure(0.01)  # MPa
    temperature = Temperature(122)  # °C
    enthalpy = Enthalpy(1826.6)  # kJ/kg
    entropy = Entropy(7.6)  # kJ/kg·K
    s_volume = Specific_Volume(0.00061)  # m³/kg
    internal_energy = InternalEnergy(13111)  # kJ/kg

    param = {"pressure": pressure, "entropy": entropy}

    calculator = SteamCalculator()
    calculator.pressure_with_entropy(**param)
    calculator.display()

    phase, x = determine_phase(prop_1=pressure, prop_2=entropy)
    print(f"Phase: {phase.name}, My x: {x}")


if __name__ == "__main__":
    main()

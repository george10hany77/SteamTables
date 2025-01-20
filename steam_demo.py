from SteamCalculator import *


def main():
    pressure = Pressure(0.1)  # MPa
    temperature = Temperature(122)  # °C
    enthalpy = Enthalpy(1826.6)  # kJ/kg
    entropy = Entropy(7.6)  # kJ/kg·K
    s_volume = Specific_Volume(0.00061)  # m³/kg
    internal_energy = InternalEnergy(13111)  # kJ/kg
    x = X(0.1)

    param = {"pressure": pressure, "internal_energy": internal_energy}

    calculator = SteamCalculator()
    calculator.pressure_with_internal_energy(**param)
    calculator.display()

    # phase, x = determine_phase(prop_1=pressure, prop_2=entropy)
    # print(f"Phase: {phase.name}, My x: {x}")


if __name__ == "__main__":
    main()

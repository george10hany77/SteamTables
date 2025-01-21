from SteamCalculator import *


def main():
    pressure = Pressure(111)  # MPa
    temperature = Temperature(122)  # °C
    enthalpy = Enthalpy(1826.6)  # kJ/kg
    entropy = Entropy(1)  # kJ/kg·K
    s_volume = Specific_Volume(0.00061)  # m³/kg
    internal_energy = InternalEnergy(13111)  # kJ/kg
    x = X(0.1)

    param = {"pressure": pressure, "entropy": entropy}

    calculator = SteamCalculator()
    calculator.pressure_with_entropy(**param)
    calculator.display()

    phase, x = determine_phase(prop_1=pressure, prop_2=entropy)
    print(f"Phase: {phase.name}, My x: {x}")

    # calculator.pressure_with_x(pressure=pressure, x=x)
    # calculator.display()


if __name__ == "__main__":
    main()

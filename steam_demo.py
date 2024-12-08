from library.iapws95 import IAPWS95
from STD_TYPES import *
from Phases import *


# the key is the key of property 1
# don't enter prop1 the same as prop2
# the second property must NOT be temperature or
# pressure as they are the same in saturated mixture you will not be able to calculate 'x'

def determine_key(typ):
    """Convert human-readable property names to internal representations."""
    match typ:
        case Temperature():
            return "T"
        case Pressure():
            return "P"
        case Enthalpy():
            return "h"
        case Entropy():
            return "s"
        case InternalEnergy():
            return "u"
        case Specific_Volume():
            return "rho"
    return None


def determine_phase(prop_1, prop_2):
    return determine_phase_helper(prop_1, prop_2, False)


def determine_phase_helper(prop_1, prop_2, flag):
    prop_1_val = prop_1.data
    prop_2_val = prop_2.data
    key_prop_1 = determine_key(prop_1)

    if key_prop_1 == "T":
        prop_1_val += 273.15
    elif key_prop_1 == "rho":
        prop_1_val = 1 / prop_1_val

    param_1 = {key_prop_1: prop_1_val, "x": 0.0}
    sat_liquid = IAPWS95(**param_1)  # Saturated liquid
    param_2 = {key_prop_1: prop_1_val, "x": 1.0}
    sat_vapor = IAPWS95(**param_2)  # Saturated vapor

    p_f = None
    p_g = None
    x = None
    match prop_2:
        case Temperature():
            if sat_liquid.T and sat_vapor.T:
                p_f = sat_liquid.T - 273.15
                p_g = sat_vapor.T - 273.15

        case Pressure():
            p_f = sat_liquid.P
            p_g = sat_vapor.P

        case Enthalpy():
            p_f = sat_liquid.h
            p_g = sat_vapor.h

        case Entropy():
            p_f = sat_liquid.s
            p_g = sat_vapor.s

        case Specific_Volume():
            p_f = sat_liquid.v
            p_g = sat_vapor.v

        case InternalEnergy():
            p_f = sat_liquid.u
            p_g = sat_vapor.u

        case _:
            raise Exception("pass a valid property type")

    # to handle the case when the data is not sufficient to find sat. states from prop 1
    # ,so we switch the order using this recursive call
    # wrapping the function inside a helper function to prevent the stack overflow
    if p_f is None or p_g is None:
        if flag:
            raise Exception("these properties cannot determine the phase !")
        flag = True
        return determine_phase_helper(prop_2, prop_1, flag)

    if (p_g - p_f) > 0:
        x = (prop_2_val - p_f) / (p_g - p_f)

    # Determine phase in case of pressure "the relation is inverse"
    if isinstance(prop_2, Pressure):
        if prop_2_val > p_f:
            return Phases.SUBCOOLED, x
        elif p_f <= prop_2_val <= p_g:
            return Phases.SATMIXTURE, x
        else:
            return Phases.SUPERHEATED, x
    else:
        # Determine phase
        if prop_2_val < p_f:
            return Phases.SUBCOOLED, x
        elif p_f <= prop_2_val <= p_g:
            return Phases.SATMIXTURE, x
        else:
            return Phases.SUPERHEATED, x


class SteamCalculator:
    def __init__(self):
        self.properties = None

    def pressure_with_temperature(self, pressure: Pressure, temperature: Temperature):
        water = IAPWS95(P=pressure.data, T=temperature.data + 273.15)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def pressure_with_enthalpy(self, pressure: Pressure, enthalpy: Enthalpy):
        water = IAPWS95(P=pressure.data, h=enthalpy.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def pressure_with_entropy(self, pressure: Pressure, entropy: Entropy):
        water = IAPWS95(P=pressure.data, s=entropy.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def pressure_with_specific_volume(self, pressure: Pressure, s_volume: Specific_Volume):  # ?
        water = IAPWS95(P=pressure.data, rho=1 / s_volume.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def pressure_with_internal_energy(self, pressure: Pressure, internal_energy: InternalEnergy):  # ?
        try:
            # phase, x = self.determine_phase_p_u(pressure.pressure, internal_energy.internal_energy)
            phase, x = determine_phase(prop_1=pressure, prop_2=internal_energy)
        except:
            # I didn't pass as we need to find x to accurately determine U
            return None
        if phase == Phases.SATMIXTURE:
            water = IAPWS95(P=pressure.data, x=x)
        else:
            water = IAPWS95(P=pressure.data, u=internal_energy.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def temperature_with_enthalpy(self, temperature: Temperature, enthalpy: Enthalpy):
        water = IAPWS95(T=temperature.data + 273.15, h=enthalpy.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def temperature_with_entropy(self, temperature: Temperature, entropy: Entropy):
        water = IAPWS95(T=temperature.data + 273.15, s=entropy.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def temperature_with_specific_volume(self, temperature: Temperature, s_volume: Specific_Volume):  # ?
        water = IAPWS95(T=temperature.data + 273.15, rho=1 / s_volume.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def temperature_with_internal_energy(self, temperature: Temperature, internal_energy: InternalEnergy):  # ?
        water = IAPWS95(T=temperature.data + 273.15, u=internal_energy.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def enthalpy_with_entropy(self, enthalpy: Enthalpy, entropy: Entropy):
        water = IAPWS95(h=enthalpy.data, s=entropy.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def enthalpy_with_specific_volume(self, enthalpy: Enthalpy, s_volume: Specific_Volume):  # ?
        water = IAPWS95(h=enthalpy.data, rho=1 / s_volume.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def enthalpy_with_internal_energy(self, enthalpy: Enthalpy, internal_energy: InternalEnergy):  # ?
        water = IAPWS95(h=enthalpy.data, u=internal_energy.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def entropy_with_specific_volume(self, entropy: Entropy, s_volume: Specific_Volume):  # ?
        water = IAPWS95(s=entropy.data, rho=1 / s_volume.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def entropy_with_internal_energy(self, entropy: Entropy, internal_energy: InternalEnergy):  # ?
        water = IAPWS95(s=entropy.data, u=internal_energy.data)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def _get_properties(self, water: IAPWS95):
        try:
            self.properties = {
                "Temperature (°C)": water.T - 273.15,
                "Pressure (MPa)": water.P,
                "Enthalpy (kJ/kg)": water.h,
                "Entropy (kJ/kg·K)": water.s,
                "Density (kg/m³)": water.rho,
                "Internal Energy (kJ/kg)": water.u,
                "Specific Volume (m³/kg)": 1 / water.rho,
                "X": water.x
            }
        except:
            return None
        return self.properties

    def display(self):
        if self.properties is not None:
            for key, val in self.properties.items():
                print(f"{key}: {val}")


def main():
    pressure = Pressure(0.4)  # MPa
    temperature = Temperature(180)  # °C
    enthalpy = Enthalpy(1826.6)  # kJ/kg
    entropy = Entropy(6.6430)  # kJ/kg·K
    s_volume = Specific_Volume(0.00061)  # m³/kg
    internal_energy = InternalEnergy(609)  # kJ/kg

    param = {"enthalpy": enthalpy, "pressure": pressure}

    calculator = SteamCalculator()
    calculator.pressure_with_enthalpy(**param)
    calculator.display()

    phase, x = determine_phase(prop_1=enthalpy, prop_2=temperature)
    print(f"Phase: {phase.name}")


if __name__ == "__main__":
    main()

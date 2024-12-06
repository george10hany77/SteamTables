from library.iapws95 import IAPWS95
from STD_TYPES import *
from Phases import *


# the key is the key of property 1
# don't enter prop1 the same as prop2
# the second property must NOT be temperature or
# pressure as they are the same in saturated mixture you will not be able to calculate 'x'


def determine_phase(key_prop_1, prop_1_val, prop_2):
    if key_prop_1 == "T":
        prop_1_val += 273.15
    param = {key_prop_1: prop_1_val, "x": 0.0}
    sat_liquid = IAPWS95(**param)  # Saturated liquid
    param_2 = {key_prop_1: prop_1_val, "x": 1.0}
    sat_vapor = IAPWS95(**param_2)  # Saturated vapor

    if isinstance(prop_2, Temperature):
        p_f = sat_liquid.T - 273.15
        p_g = sat_vapor.T - 273.15
        prop_2_val = prop_2.temp
        # raise Exception("Don't use temperature !")
    elif isinstance(prop_2, Pressure):
        p_f = sat_liquid.P
        p_g = sat_vapor.P
        prop_2_val = prop_2.pressure
        # raise Exception("Don't use pressure !")
    elif isinstance(prop_2, Enthalpy):
        p_f = sat_liquid.h
        p_g = sat_vapor.h
        prop_2_val = prop_2.enthalpy
    elif isinstance(prop_2, Entropy):
        p_f = sat_liquid.s
        p_g = sat_vapor.s
        prop_2_val = prop_2.entropy
    elif isinstance(prop_2, Specific_Volume):
        p_f = sat_liquid.v
        p_g = sat_vapor.v
        prop_2_val = prop_2.s_volume
    elif isinstance(prop_2, InternalEnergy):
        p_f = sat_liquid.u
        p_g = sat_vapor.u
        prop_2_val = prop_2.internal_energy
    else:
        raise Exception("pass a valid property type")

    x = None

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

    def determine_phase_p_u(self, pressure, internal_energy):
        sat_liquid = IAPWS95(P=pressure, x=0)  # Saturated liquid
        sat_vapor = IAPWS95(P=pressure, x=1.0)  # Saturated vapor

        # Saturated liquid and vapor internal energies (in kJ/kg)
        u_f = sat_liquid.u  # Saturated liquid internal energy
        u_g = sat_vapor.u  # Saturated vapor internal energy

        x = (internal_energy - u_f) / (u_g - u_f)

        # Determine phase
        if internal_energy < u_f:
            return Phases.SUBCOOLED, x
        elif u_f <= internal_energy <= u_g:
            return Phases.SATMIXTURE, x
        else:
            return Phases.SUPERHEATED, x

    def pressure_with_temperature(self, pressure: Pressure, temperature: Temperature):
        water = IAPWS95(P=pressure.pressure, T=temperature.temp + 273.15)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def pressure_with_enthalpy(self, pressure: Pressure, enthalpy: Enthalpy):
        water = IAPWS95(P=pressure.pressure, h=enthalpy.enthalpy)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def pressure_with_entropy(self, pressure: Pressure, entropy: Entropy):
        water = IAPWS95(P=pressure.pressure, s=entropy.entropy)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def pressure_with_specific_volume(self, pressure: Pressure, s_volume: Specific_Volume):  # ?
        water = IAPWS95(P=pressure.pressure, rho=1 / s_volume.s_volume)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def pressure_with_internal_energy(self, pressure: Pressure, internal_energy: InternalEnergy):  # ?
        # phase, x = self.determine_phase_p_u(pressure.pressure, internal_energy.internal_energy)
        phase, x = determine_phase(key_prop_1="P", prop_1_val=pressure.pressure, prop_2=internal_energy)
        if phase == Phases.SATMIXTURE:
            water = IAPWS95(P=pressure.pressure, x=x)
        else:
            water = IAPWS95(P=pressure.pressure, u=internal_energy.internal_energy)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def temperature_with_enthalpy(self, temperature: Temperature, enthalpy: Enthalpy):
        water = IAPWS95(T=temperature.temp + 273.15, h=enthalpy.enthalpy)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def temperature_with_entropy(self, temperature: Temperature, entropy: Entropy):
        water = IAPWS95(T=temperature.temp + 273.15, s=entropy.entropy)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def temperature_with_specific_volume(self, temperature: Temperature, s_volume: Specific_Volume):  # ?
        water = IAPWS95(T=temperature.temp + 273.15, rho=1 / s_volume.s_volume)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def temperature_with_internal_energy(self, temperature: Temperature, internal_energy: InternalEnergy):  # ?
        water = IAPWS95(T=temperature.temp + 273.15, u=internal_energy.internal_energy)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def enthalpy_with_entropy(self, enthalpy: Enthalpy, entropy: Entropy):
        water = IAPWS95(h=enthalpy.enthalpy, s=entropy.entropy)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def enthalpy_with_specific_volume(self, enthalpy: Enthalpy, s_volume: Specific_Volume):  # ?
        water = IAPWS95(h=enthalpy.enthalpy, rho=1 / s_volume.s_volume)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def enthalpy_with_internal_energy(self, enthalpy: Enthalpy, internal_energy: InternalEnergy):  # ?
        water = IAPWS95(h=enthalpy.enthalpy, u=internal_energy.internal_energy)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def entropy_with_specific_volume(self, entropy: Entropy, s_volume: Specific_Volume):  # ?
        water = IAPWS95(s=entropy.entropy, rho=1 / s_volume.s_volume)
        self.properties = self._get_properties(water)
        if self.properties is not None:
            return self.properties

    def entropy_with_internal_energy(self, entropy: Entropy, internal_energy: InternalEnergy):  # ?
        water = IAPWS95(s=entropy.entropy, u=internal_energy.internal_energy)
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

    calculator = SteamCalculator()
    calculator.pressure_with_temperature(pressure=pressure, temperature=temperature)
    calculator.display()

    phase, x = determine_phase(key_prop_1="T", prop_1_val=temperature.temp, prop_2=pressure)
    print(f"Phase: {phase}, x: {x}")

if __name__ == "__main__":
    main()

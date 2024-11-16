import iapws
from iapws import IAPWS95
from iapws import IAPWS97
from STD_TYPES import *

class SteamCalculator:
    def __init__(self):
        pass

    def pressure_with_temperature(self, pressure: Pressure, temperature: Temperature):
        water = IAPWS95(P=pressure.pressure, T=temperature.temp + 273.15)
        properties = self._get_properties(water)
        if properties != None:
            return properties
         

    def pressure_with_enthalpy(self, pressure: Pressure, enthalpy: Enthalpy):
        water = IAPWS95(P=pressure.pressure, h=enthalpy.enthalpy)
        properties = self._get_properties(water)
        if properties != None:
            return properties
        
    def pressure_with_entropy(self, pressure: Pressure, entropy: Entropy):
        water = IAPWS95(P=pressure.pressure, s=entropy.entropy)
        properties = self._get_properties(water)
        if properties != None:
            return properties
        
    def pressure_with_specific_volume(self, pressure: Pressure, s_volume: Specific_Volume): # !
        water = IAPWS95(P=pressure.pressure, v=s_volume.s_volume)
        properties = self._get_properties(water)
        if properties != None:
            return properties
        
    def pressure_with_internal_energy(self, pressure: Pressure, internal_energy: InternalEnergy): # !
        water = IAPWS95(P=pressure.pressure, u=internal_energy.internal_energy)
        properties = self._get_properties(water)
        if properties != None:
            return properties

    def temperature_with_enthalpy(self, temperature: Temperature, enthalpy: Enthalpy):
        water = IAPWS95(T=temperature.temp + 273.15, h=enthalpy.enthalpy)
        properties = self._get_properties(water)
        if properties != None:
            return properties

    def temperature_with_entropy(self, temperature: Temperature, entropy: Entropy):
        water = IAPWS95(T=temperature.temp + 273.15, s=entropy.entropy)
        properties = self._get_properties(water)
        if properties != None:
            return properties

    def temperature_with_specific_volume(self, temperature: Temperature, s_volume: Specific_Volume): # !
        water = IAPWS95(T=temperature.temp + 273.15, v=s_volume.s_volume)
        properties = self._get_properties(water)
        if properties != None:
            return properties

    def temperature_with_internal_energy(self, temperature: Temperature, internal_energy: InternalEnergy): # ! 
        water = IAPWS95(T=temperature.temp + 273.15, u=internal_energy.internal_energy)
        properties = self._get_properties(water)
        if properties != None:
            return properties

    def enthalpy_with_entropy(self, enthalpy: Enthalpy, entropy: Entropy):
        water = IAPWS95(h=enthalpy.enthalpy, s=entropy.entropy)
        properties = self._get_properties(water)
        if properties != None:
            return properties

    def enthalpy_with_specific_volume(self, enthalpy: Enthalpy, s_volume: Specific_Volume): # !
        water = IAPWS95(h=enthalpy.enthalpy, v=s_volume.s_volume)
        properties = self._get_properties(water)
        if properties != None:
            return properties

    def enthalpy_with_internal_energy(self, enthalpy: Enthalpy, internal_energy: InternalEnergy): # !
        water = IAPWS95(h=enthalpy.enthalpy, u=internal_energy.internal_energy)
        properties = self._get_properties(water)
        if properties != None:
            return properties

    def entropy_with_specific_volume(self, entropy: Entropy, s_volume: Specific_Volume): # !
        water = IAPWS95(s=entropy.entropy, v=s_volume.s_volume)
        properties = self._get_properties(water)
        if properties != None:
            return properties

    def entropy_with_internal_energy(self, entropy: Entropy, internal_energy: InternalEnergy): # !
        water = IAPWS95(s=entropy.entropy, u=internal_energy.internal_energy)
        properties = self._get_properties(water)
        if properties != None:
            return properties

    def _get_properties(self, water:IAPWS95):
        try:
            properties = {
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
        return properties
        
    def calculate(self):
        pass


def main():
    pressure = Pressure(2)  # MPa
    temperature = Temperature(212)  # °C
    enthalpy = Enthalpy(2318.4)  # kJ/kg
    entropy = Entropy(6.6430)  # kJ/kg·K
    s_volume = Specific_Volume(0.001)  # m³/kg
    internal_energy = InternalEnergy(1500)  # kJ/kg

    calculator = SteamCalculator()
    w = IAPWS95(P=1, rho=10)
    print(w.T)
    # properties = calculator.pressure_with_temperature(pressure=pressure, temperature=temperature)
    # print(properties)

if __name__ == "__main__":
    main()

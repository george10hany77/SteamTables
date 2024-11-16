import iapws
from iapws import IAPWS95
from STD_TYPES import *

class SteamCalculator:
    def __init__(self):
        self.properties = None

    def pressure_with_temperature(self, pressure: Pressure, temperature: Temperature):
        water = IAPWS95(P=pressure.pressure, T=temperature.temp + 273.15)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties
         

    def pressure_with_enthalpy(self, pressure: Pressure, enthalpy: Enthalpy):
        water = IAPWS95(P=pressure.pressure, h=enthalpy.enthalpy)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties
        
    def pressure_with_entropy(self, pressure: Pressure, entropy: Entropy):
        water = IAPWS95(P=pressure.pressure, s=entropy.entropy)
        properties = self._get_self.properties(water)
        if self.properties != None:
            return self.properties
        
    def pressure_with_specific_volume(self, pressure: Pressure, s_volume: Specific_Volume): # ?
        water = IAPWS95(P=pressure.pressure, rho=1/s_volume.s_volume)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties
        
    def pressure_with_internal_energy(self, pressure: Pressure, internal_energy: InternalEnergy): # ?
        water = IAPWS95(P=pressure.pressure, u=internal_energy.internal_energy)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties

    def temperature_with_enthalpy(self, temperature: Temperature, enthalpy: Enthalpy):
        water = IAPWS95(T=temperature.temp + 273.15, h=enthalpy.enthalpy)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties

    def temperature_with_entropy(self, temperature: Temperature, entropy: Entropy):
        water = IAPWS95(T=temperature.temp + 273.15, s=entropy.entropy)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties

    def temperature_with_specific_volume(self, temperature: Temperature, s_volume: Specific_Volume): # ?
        water = IAPWS95(T=temperature.temp + 273.15, rho=1/s_volume.s_volume)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties

    def temperature_with_internal_energy(self, temperature: Temperature, internal_energy: InternalEnergy): # ?
        water = IAPWS95(T=temperature.temp + 273.15, u=internal_energy.internal_energy)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties

    def enthalpy_with_entropy(self, enthalpy: Enthalpy, entropy: Entropy):
        water = IAPWS95(h=enthalpy.enthalpy, s=entropy.entropy)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties

    def enthalpy_with_specific_volume(self, enthalpy: Enthalpy, s_volume: Specific_Volume): # ?
        water = IAPWS95(h=enthalpy.enthalpy, rho=1/s_volume.s_volume)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties

    def enthalpy_with_internal_energy(self, enthalpy: Enthalpy, internal_energy: InternalEnergy): # ?
        water = IAPWS95(h=enthalpy.enthalpy, u=internal_energy.internal_energy)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties

    def entropy_with_specific_volume(self, entropy: Entropy, s_volume: Specific_Volume): # ?
        water = IAPWS95(s=entropy.entropy, rho=1/s_volume.s_volume)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties

    def entropy_with_internal_energy(self, entropy: Entropy, internal_energy: InternalEnergy): # ?
        water = IAPWS95(s=entropy.entropy, u=internal_energy.internal_energy)
        self.properties = self._get_properties(water)
        if self.properties != None:
            return self.properties
    
    def _get_properties(self, water:IAPWS95):
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
        if self.properties != None:
            for key, val in self.properties.items():
              print(f"{key}: {val}")  

def main():
    pressure = Pressure(2)  # MPa
    temperature = Temperature(205)  # °C
    enthalpy = Enthalpy(1826.6)  # kJ/kg
    entropy = Entropy(6.6430)  # kJ/kg·K
    s_volume = Specific_Volume(0.0021)  # m³/kg
    internal_energy = InternalEnergy(873)  # kJ/kg

    calculator = SteamCalculator()
    calculator.temperature_with_internal_energy(temperature=temperature, internal_energy=internal_energy)
    calculator.display()

if __name__ == "__main__":
    main()

from pyweb import pydom
from STD_TYPES import *
from steam_demo import SteamCalculator

def get_joke(event):
    #pydom["div#jokes"].html = ""+pydom[".dropdown-menu"][0].html
    pressure = Pressure(2)  # MPa
    temperature = Temperature(205)  # °C
    enthalpy = Enthalpy(1826.6)  # kJ/kg
    entropy = Entropy(6.6430)  # kJ/kg·K
    s_volume = Specific_Volume(0.0021)  # m³/kg
    internal_energy = InternalEnergy(873)  # kJ/kg

    calculator = SteamCalculator()
    pydom["div#jokes"].html = calculator.temperature_with_internal_energy(temperature=temperature, internal_energy=internal_energy)
    print( calculator.temperature_with_internal_energy(temperature=temperature, internal_energy=internal_energy))
    


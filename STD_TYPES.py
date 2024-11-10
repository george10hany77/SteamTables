class Temperature:
    def __init__(self, temperature: float):
        self.temp = temperature  # °C

class Pressure:
    def __init__(self, pressure: float):
        self.pressure = pressure  # MPa

class Enthalpy:
    def __init__(self, enthalpy: float):
        self.enthalpy = enthalpy  # kJ/kg

class Entropy:
    def __init__(self, entropy: float):
        self.entropy = entropy  # kJ/kg·K

class Specific_Volume:
    def __init__(self, s_volume: float):
        self.s_volume = s_volume  # m³/kg

class InternalEnergy:
    def __init__(self, internal_energy: float):
        self.internal_energy = internal_energy  # kJ/kg

class X():
    def __init__(self, x:float):
        if x < 1.0 and x >= 0:
            self.x = x

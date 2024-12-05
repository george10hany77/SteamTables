from pyweb import pydom
from STD_TYPES import *
from steam_demo import SteamCalculator
from iapws import IAPWS95

def switch_property(typ, dat):
    """Convert human-readable property names to internal representations."""
    match typ:
        case "Temperature (°C)":
            return Temperature(dat)
        case "Pressure (MPa)":
            return Pressure(dat)
        case "Enthalpy (kJ/kg)":
            return Enthalpy(dat)
        case "Entropy (kJ/kg·K)":
            return Entropy(dat)
        case "Internal Energy (kJ/kg)":
            return InternalEnergy(dat)
        case "Specific Volume (m³/kg)":
            return Specific_Volume(dat)
    return None


def get_joke(event):
    """Handle user input and calculate steam properties."""
    type1 = pydom["span.one"][0].content
    type2 = pydom["span.two"][0].content
    data1 = float(pydom["#in1"].value[0])
    data2 = float(pydom["#in2"].value[0])

    # Convert property names to internal representations
    prop1 = switch_property(type1, data1)
    prop2 = switch_property(type2, data2)

    if not type1 or not type2:
        pydom["div#jokes"].html = """
            <div class="alert alert-danger d-flex align-items-center" role="alert">
                <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:">
                <use xlink:href="#exclamation-triangle-fill"/>
                </svg>
                <div>Invalid properties chosen</div>
            </div>"""
        return

    # Check for duplicate properties
    if type1 == type2:
        pydom["div#jokes"].html = """
            <div class="alert alert-danger d-flex align-items-center" role="alert">
                <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:">
                <use xlink:href="#exclamation-triangle-fill"/>
                </svg>
                <div>Duplicate properties chosen</div>
            </div>"""
        return

    # Create a SteamCalculator instance
    calculator = SteamCalculator()

    # Determine which method to call based on input properties
    try:
        result = None
        parameters = {"temperature":prop1, "pressure":prop2}
        if type1 == "Pressure (MPa)" and type2 == "Temperature (°C)":
            # result = calculator.pressure_with_temperature(prop1, prop2)
            result = calculator.pressure_with_temperature(**parameters)
            # result = IAPWS95(**parameters)
        elif type1 == "Pressure (MPa)" and type2 == "Enthalpy (kJ/kg)":
            result = calculator.pressure_with_enthalpy(prop1, prop2)
        elif type1 == "Pressure (MPa)" and type2 == "Entropy (kJ/kg·K)":
            result = calculator.pressure_with_entropy(prop1, prop2)
        elif type1 == "Pressure (MPa)" and type2 == "Specific Volume (m³/kg)":
            result = calculator.pressure_with_specific_volume(prop1, prop2)
        elif type1 == "Pressure (MPa)" and type2 == "Internal Energy (kJ/kg)":
            result = calculator.pressure_with_internal_energy(prop1, prop2)
        elif type1 == "Temperature (°C)" and type2 == "Enthalpy (kJ/kg)":
            result = calculator.temperature_with_enthalpy(prop1, prop2)
        elif type1 == "Temperature (°C)" and type2 == "Entropy (kJ/kg·K)":
            result = calculator.temperature_with_entropy(prop1, prop2)
        elif type1 == "Temperature (°C)" and type2 == "Specific Volume (m³/kg)":
            result = calculator.temperature_with_specific_volume(prop1, prop2)
        elif type1 == "Temperature (°C)" and type2 == "Internal Energy (kJ/kg)":
            result = calculator.temperature_with_internal_energy(prop1, prop2)
        elif type1 == "Enthalpy (kJ/kg)" and type2 == "Entropy (kJ/kg·K)":
            result = calculator.enthalpy_with_entropy(prop1, prop2)
        elif type1 == "Enthalpy (kJ/kg)" and type2 == "Specific Volume (m³/kg)":
            result = calculator.enthalpy_with_specific_volume(prop1, prop2)
        elif type1 == "Enthalpy (kJ/kg)" and type2 == "Internal Energy (kJ/kg)":
            result = calculator.enthalpy_with_internal_energy(prop1, prop2)
        elif type1 == "Entropy (kJ/kg·K)" and type2 == "Specific Volume (m³/kg)":
            result = calculator.entropy_with_specific_volume(prop1, prop2)
        elif type1 == "Entropy (kJ/kg·K)" and type2 == "Internal Energy (kJ/kg)":
            result = calculator.entropy_with_internal_energy(prop1, prop2)

        if result:
            # Display the calculated properties
            pydom["div#jokes"].html = f"""
                <div id="jokes">
                    <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">Temperature (°C)</th>
                            <th scope="col">Pressure (MPa)</th>
                            <th scope="col">Enthalpy (kJ/kg)</th>
                            <th scope="col">Entropy (kJ/kg·K)</th>
                            <th scope="col">Internal Energy (kJ/kg)</th>
                            <th scope="col">Specific Volume (m³/kg)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{round(result["Temperature (°C)"], 3)}</td>
                            <td>{round(result["Pressure (MPa)"], 3)}</td>
                            <td>{round(result["Enthalpy (kJ/kg)"], 3)}</td>
                            <td>{round(result["Entropy (kJ/kg·K)"], 3)}</td>
                            <td>{round(result["Internal Energy (kJ/kg)"], 3)}</td>
                            <td>{round(result["Specific Volume (m³/kg)"], 6)}</td>
                        </tr>
                    </tbody>
                    </table>
                </div>"""
        else:
            raise Exception("Calculation failed")

    except Exception as e:
        pydom["div#jokes"].html = f"""
            <div class="alert alert-danger d-flex align-items-center" role="alert">
                <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:">
                <use xlink:href="#exclamation-triangle-fill"/>
                </svg>
                <div>Error: {str(e)}</div>
            </div>"""



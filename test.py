from pyweb import pydom
from STD_TYPES import *  # Imports all the classes like Pressure, Temperature, etc.
from steam_demo import SteamCalculator


def switch_property(typ):
    """Convert human-readable property names to internal representations."""
    match typ:
        case "Temperature (°C)":
            return "Temperature"
        case "Pressure (MPa)":
            return "Pressure"
        case "Enthalpy (kJ/kg)":
            return "Enthalpy"
        case "Entropy (kJ/kg·K)":
            return "Entropy"
        case "Internal Energy (kJ/kg)":
            return "InternalEnergy"
        case "Specific Volume (m³/kg)":
            return "Specific_Volume"
    return None


def get_joke(event):
    """Handle user input and calculate steam properties."""
    type1 = pydom["span.one"][0].content
    type2 = pydom["span.two"][0].content
    data1 = float(pydom["#in1"].value[0])
    data2 = float(pydom["#in2"].value[0])

    # Convert property names to class names
    type1 = switch_property(type1)
    type2 = switch_property(type2)

    if not type1 or not type2:
        pydom["div#jokes"].html = """
            <div class="alert alert-danger d-flex align-items-center" role="alert">
                <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:">
                <use xlink:href="#exclamation-triangle-fill"/>
                </svg>
                <div>Invalid properties chosen</div>
            </div>"""
        return

    # Ensure temperature is converted to Kelvin
    if type1 == "Temperature":
        data1 += 273.15
    if type2 == "Temperature":
        data2 += 273.15

    # Convert specific volume to density (1/rho)
    if type1 == "Specific_Volume":
        data1 = 1 / data1
    if type2 == "Specific_Volume":
        data2 = 1 / data2

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

    # Prepare inputs as instances of property types
    try:
        # Dynamically access the classes from the `STD_TYPES` module
        prop1 = globals()["STD_TYPES"].__dict__[type1](data1)
        prop2 = globals()["STD_TYPES"].__dict__[type2](data2)

        # Determine which method to call based on input properties
        result = None
        if type1 == "Pressure" and type2 == "Temperature":
            result = calculator.pressure_with_temperature(prop1, prop2)
        elif type1 == "Pressure" and type2 == "Enthalpy":
            result = calculator.pressure_with_enthalpy(prop1, prop2)
        elif type1 == "Pressure" and type2 == "Entropy":
            result = calculator.pressure_with_entropy(prop1, prop2)
        elif type1 == "Pressure" and type2 == "Specific_Volume":
            result = calculator.pressure_with_specific_volume(prop1, prop2)
        elif type1 == "Pressure" and type2 == "InternalEnergy":
            result = calculator.pressure_with_internal_energy(prop1, prop2)
        elif type1 == "Temperature" and type2 == "Enthalpy":
            result = calculator.temperature_with_enthalpy(prop1, prop2)
        elif type1 == "Temperature" and type2 == "Entropy":
            result = calculator.temperature_with_entropy(prop1, prop2)
        elif type1 == "Temperature" and type2 == "Specific_Volume":
            result = calculator.temperature_with_specific_volume(prop1, prop2)
        elif type1 == "Temperature" and type2 == "InternalEnergy":
            result = calculator.temperature_with_internal_energy(prop1, prop2)
        elif type1 == "Enthalpy" and type2 == "Entropy":
            result = calculator.enthalpy_with_entropy(prop1, prop2)
        elif type1 == "Enthalpy" and type2 == "Specific_Volume":
            result = calculator.enthalpy_with_specific_volume(prop1, prop2)
        elif type1 == "Enthalpy" and type2 == "InternalEnergy":
            result = calculator.enthalpy_with_internal_energy(prop1, prop2)
        elif type1 == "Entropy" and type2 == "Specific_Volume":
            result = calculator.entropy_with_specific_volume(prop1, prop2)
        elif type1 == "Entropy" and type2 == "InternalEnergy":
            result = calculator.entropy_with_internal_energy(prop1, prop2)

        if result:
            # Display the calculated properties
            pydom["div#jokes"].html = f"""
                <div id="jokes">
                    <table class="table-responsive">
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
                            <td>{result["Temperature (°C)"]}</td>
                            <td>{result["Pressure (MPa)"]}</td>
                            <td>{result["Enthalpy (kJ/kg)"]}</td>
                            <td>{result["Entropy (kJ/kg·K)"]}</td>
                            <td>{result["Internal Energy (kJ/kg)"]}</td>
                            <td>{result["Specific Volume (m³/kg)"]}</td>
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

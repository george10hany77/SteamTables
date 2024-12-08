from pyweb import pydom
from STD_TYPES import *
from steam_demo import *


def get_joke(event):
    """Handle user input and calculate steam properties."""
    type1 = pydom["span.one"][0].content
    type2 = pydom["span.two"][0].content
    data1 = float(pydom["#in1"].value[0])
    data2 = float(pydom["#in2"].value[0])

    # Convert property names to internal representations
    prop1, parameter1 = switch_property(type1, data1)
    prop2, parameter2 = switch_property(type2, data2)

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
        parameters = {parameter1: prop1, parameter2: prop2}

        if (type1 == "Pressure (MPa)" and type2 == "Temperature (°C)") or (
                type1 == "Temperature (°C)" and type2 == "Pressure (MPa)"):
            result = calculator.pressure_with_temperature(**parameters)
        elif (type1 == "Pressure (MPa)" and type2 == "Enthalpy (kJ/kg)") or (
                type1 == "Enthalpy (kJ/kg)" and type2 == "Pressure (MPa)"):
            result = calculator.pressure_with_enthalpy(**parameters)
        elif (type1 == "Pressure (MPa)" and type2 == "Entropy (kJ/kg·K)") or (
                type1 == "Entropy (kJ/kg·K)" and type2 == "Pressure (MPa)"):
            result = calculator.pressure_with_entropy(**parameters)
        elif (type1 == "Pressure (MPa)" and type2 == "Specific Volume (m³/kg)") or (
                type1 == "Specific Volume (m³/kg)" and type2 == "Pressure (MPa)"):
            result = calculator.pressure_with_specific_volume(**parameters)
        elif (type1 == "Pressure (MPa)" and type2 == "Internal Energy (kJ/kg)") or (
                type1 == "Internal Energy (kJ/kg)" and type2 == "Pressure (MPa)"):
            result = calculator.pressure_with_internal_energy(**parameters)
        elif (type1 == "Temperature (°C)" and type2 == "Enthalpy (kJ/kg)") or (
                type1 == "Enthalpy (kJ/kg)" and type2 == "Temperature (°C)"):
            result = calculator.temperature_with_enthalpy(**parameters)
        elif (type1 == "Temperature (°C)" and type2 == "Entropy (kJ/kg·K)") or (
                type1 == "Entropy (kJ/kg·K)" and type2 == "Temperature (°C)"):
            result = calculator.temperature_with_entropy(**parameters)
        elif (type1 == "Temperature (°C)" and type2 == "Specific Volume (m³/kg)") or (
                type1 == "Specific Volume (m³/kg)" and type2 == "Temperature (°C)"):
            result = calculator.temperature_with_specific_volume(**parameters)
        elif (type1 == "Temperature (°C)" and type2 == "Internal Energy (kJ/kg)") or (
                type1 == "Internal Energy (kJ/kg)" and type2 == "Temperature (°C)"):
            result = calculator.temperature_with_internal_energy(**parameters)
        elif (type1 == "Enthalpy (kJ/kg)" and type2 == "Entropy (kJ/kg·K)") or (
                type1 == "Entropy (kJ/kg·K)" and type2 == "Enthalpy (kJ/kg)"):
            result = calculator.enthalpy_with_entropy(**parameters)
        elif (type1 == "Enthalpy (kJ/kg)" and type2 == "Specific Volume (m³/kg)") or (
                type1 == "Specific Volume (m³/kg)" and type2 == "Enthalpy (kJ/kg)"):
            result = calculator.enthalpy_with_specific_volume(**parameters)
        elif (type1 == "Enthalpy (kJ/kg)" and type2 == "Internal Energy (kJ/kg)") or (
                type1 == "Internal Energy (kJ/kg)" and type2 == "Enthalpy (kJ/kg)"):
            result = calculator.enthalpy_with_internal_energy(**parameters)
        elif (type1 == "Entropy (kJ/kg·K)" and type2 == "Specific Volume (m³/kg)") or (
                type1 == "Specific Volume (m³/kg)" and type2 == "Entropy (kJ/kg·K)"):
            result = calculator.entropy_with_specific_volume(**parameters)
        elif (type1 == "Entropy (kJ/kg·K)" and type2 == "Internal Energy (kJ/kg)") or (
                type1 == "Internal Energy (kJ/kg)" and type2 == "Entropy (kJ/kg·K)"):
            result = calculator.entropy_with_internal_energy(**parameters)

        phase, x = determine_phase(prop1, prop2)

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
                            <th scope="col">X (Quality)</th>
                            <th scope="col">Phase</th>
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
                            <td>{round(result["X"], 4)}</td>
                            <td>{str(phase.name)}</td>
                        </tr>
                    </tbody>
                    </table>
                </div>"""
        else:
            raise Exception("This calculation can't be done :(")

    except Exception as e:
        pydom["div#jokes"].html = f"""
            <div class="alert alert-danger d-flex align-items-center" role="alert">
                <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:">
                <use xlink:href="#exclamation-triangle-fill"/>
                </svg>
                <div>Error: {str(e)}</div>
            </div>"""

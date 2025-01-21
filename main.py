from pyweb import pydom
from SteamCalculator import *
import warnings

# to ignor the warnings
warnings.filterwarnings("ignore")


def switch_property(typ, dat):
    """Convert human-readable property names to internal representations."""
    match typ:
        case "Temperature (°C)":
            return Temperature(dat), "temperature"
        case "Pressure (MPa)":
            return Pressure(dat), "pressure"
        case "Enthalpy (kJ/kg)":
            return Enthalpy(dat), "enthalpy"
        case "Entropy (kJ/kg·K)":
            return Entropy(dat), "entropy"
        case "Internal Energy (kJ/kg)":
            return InternalEnergy(dat), "internal_energy"
        case "Specific Volume (m³/kg)":
            return Specific_Volume(dat), "s_volume"
        case "Quality (X)":
            return X(dat), "x"
    return None


def create_table(Temp, Pres, Enth, Entr, Inte, Spec, x, ph):
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
                                    <td>{Temp}</td>
                                    <td>{Pres}</td>
                                    <td>{Enth}</td>
                                    <td>{Entr}</td>
                                    <td>{Inte}</td>
                                    <td>{Spec}</td>
                                    <td>{x}</td>
                                    <td>{ph}</td>
                                </tr>
                            </tbody>
                            </table>
                        </div>"""


def get_joke(event):
    try:
        type1 = pydom["span.one"][0].content
        type2 = pydom["span.two"][0].content
        data1 = float(pydom["#in1"].value[0])
        data2 = float(pydom["#in2"].value[0])
    except Exception:
        pydom["div#jokes"].html = """
                    <div class="alert alert-danger d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:">
                        <use xlink:href="#exclamation-triangle-fill"/>
                        </svg>
                        <div>Enter a number please</div>
                    </div>"""
        return

    phase = Phases.NOTDETERMINED
    result = None
    message = "All is good :)"

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

    # Convert property names to internal representations
    prop1, parameter1 = switch_property(type1, data1)
    prop2, parameter2 = switch_property(type2, data2)

    if (type1 is None) or (type2 is None) or (prop1 is None) or (prop2 is None):
        pydom["div#jokes"].html = """
            <div class="alert alert-danger d-flex align-items-center" role="alert">
                <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:">
                <use xlink:href="#exclamation-triangle-fill"/>
                </svg>
                <div>Invalid properties chosen</div>
            </div>"""
        return

    parameters = {parameter1: prop1, parameter2: prop2}

    # Create a SteamCalculator instance
    calculator = SteamCalculator()

    # to reset the output after each input
    # when the calculate button is pressed it overwrites the previous output and displays the new one
    create_table("X", "X", "X", "X", "X", "X", "X", "X")

    # Determine which method to call based on input properties
    try:
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
        elif (type1 == "Quality (X)" and type2 == "Temperature (°C)") or (
                type1 == "Temperature (°C)" and type2 == "Quality (X)"):
            result = calculator.temperature_with_x(**parameters)
        elif (type1 == "Quality (X)" and type2 == "Pressure (MPa)") or (
                type1 == "Pressure (MPa)" and type2 == "Quality (X)"):
            result = calculator.pressure_with_x(**parameters)

        try:
            returned_phase_x = determine_phase(prop1, prop2)
            if returned_phase_x:
                phase = returned_phase_x[0]  # getting the phase from the tuple
            else:
                message = "Error happened while calculating the phase!!"
                phase = Phases.NOTDETERMINED
        except:
            if result:
                x = result["X"]
                if x:  # if there was an error but there is a value calculated
                    if x >= 1:
                        phase = Phases.SUPERHEATED
                    elif x <= 0:
                        phase = Phases.SUBCOOLED
                    elif 1 > x > 0:
                        phase = Phases.SATMIXTURE
                    else:
                        message = "Error happened while calculating the phase!!"
                        phase = Phases.NOTDETERMINED
            else:
                message = "Error happened while calculating the phase!!"
                phase = Phases.NOTDETERMINED

        if result and phase:
            # Display the calculated properties
            xvalue = "X"
            if phase == Phases.SATMIXTURE or phase == Phases.SATLIQUID or phase == Phases.SATVAPOR:
                xvalue = round(result["X"], 4)

            create_table(round(result["Temperature (°C)"], 3), round(result["Pressure (MPa)"], 5),
                         round(result["Enthalpy (kJ/kg)"], 3), round(result["Entropy (kJ/kg·K)"], 3),
                         round(result["Internal Energy (kJ/kg)"], 3), round(result["Specific Volume (m³/kg)"], 6),
                         xvalue, str(phase.name))

        else:
            raise Exception("This calculation can't be done :(")

    except Exception:
        message = "Error !!"

    new_table = f"""
                <table class="table">
                <thead>
                    <tr>
                        <th scope="col">message</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{message}</td>
                    </tr>
                </tbody>
                </table>"""

    # accessing the second element "table" and adding to it the new table by editing the html of that element
    pydom["div#jokes"][1].html += new_table

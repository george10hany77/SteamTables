from pyweb import pydom
from STD_TYPES import *
from steam_demo import SteamCalculator
from library.iapws95 import IAPWS95

def switchh(typ):
    match typ:
        case "Temperature (°C)": typ = "T" ,
        case "Pressure (MPa)" : typ = "P",
        case "Enthalpy (kJ/kg)": typ = "h",
        case "Entropy (kJ/kg·K)":typ="s",
        case "Internal Energy (kJ/kg)": typ = "u",
        case "Specific Volume (m³/kg)": typ="rho",
    return typ



def get_joke(event):
    #pydom["div#jokes"].html = ""+pydom[".dropdown-menu"][0].html

    type1=pydom["span.one"][0].content
    type2=pydom["span.two"][0].content
    data1=float(pydom["#in1"].value[0])
    data2=float(pydom["#in2"].value[0])

    type1 = switchh(type1)[0]
    type2 = switchh(type2)[0]

    if(type1 == "T"):
        data1 = data1+273.15
    elif(type2=="T"):
        data2 = data2+273.15


    if(type1 == "rho"):
        data1 = (1/data1)
    elif(type2=="rho"):
        data2 = 1/data2


    print(data1 )

    if type1==type2:
        pydom["div#jokes"].html = """
            <div class="alert alert-danger d-flex align-items-center" role="alert">
                <svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
                    <div>
                        duplicate properties choosen
                    </div>
            </div>"""
        return

    kwargss = {type1:data1,type2:data2}
    water = IAPWS95(**kwargss)
    pydom["div#jokes"].html = f"""<div id="jokes">
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
                    <td>{water.T-273.15}</td>
                    <td>{water.P}</td>
                    <td>{water.h}</td>
                    <td>{water.s}</td>
                    <td>{water.u}</td>
                    <td>{1/water.rho}</td>
                    </tr>
                    
                </table>
            </div>"""
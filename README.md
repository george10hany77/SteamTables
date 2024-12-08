# Online Steam Tables Calculator

An online steam tables calculator built using Python and the [IAPWS library](https://iapws.org) to calculate the thermodynamic properties of steam based on user-defined input properties. This project is designed as part of a thermodynamics course at the university.

## Features

- Calculate steam properties such as:
  - Temperature (°C)
  - Pressure (MPa)
  - Enthalpy (kJ/kg)
  - Entropy (kJ/kg·K)
  - Specific Volume (m³/kg)
  - Internal Energy (kJ/kg)
  - Quality (X)
  - Phase (e.g., subcooled, saturated mixture, superheated)
- Handle multiple input property combinations.
- Dynamic and user-friendly interface for property selection and result display.
- Validates inputs to prevent errors, such as selecting duplicate properties.

## How It Works

1. Users select two properties (e.g., temperature and pressure) from a dropdown menu.
2. Enter values for the selected properties.
3. The application calculates and displays the resulting steam properties and phase.

### Example Use Case

If you input:
- **Property 1**: Temperature = 100°C  
- **Property 2**: Pressure = 0.101 MPa  

The program will calculate properties like enthalpy, entropy, specific volume, quality, and phase.

### Use the following link

```
https://george10hany77.github.io/SteamTables/ 
```

## Usage

- **Frontend**: The interface is built using JavaScript (`main.js`) for handling dynamic updates.
- **Backend**: Python modules (`main.py`, `steam_demo.py`, `STD_TYPES.py`, `Phases.py`) handle thermodynamic calculations and property validation.

## Code Overview

- **`main.py`**: Main entry point. Handles user inputs and integrates with the backend to calculate properties.
- **`STD_TYPES.py`**: Defines classes for thermodynamic properties (e.g., temperature, pressure, enthalpy).
- **`Phases.py`**: Defines enums for water phases (e.g., saturated mixture, subcooled, superheated).
- **`steam_demo.py`**: Contains the core calculation logic using the IAPWS library.
- **`main.js`**: Handles frontend dynamic property selection and display updates.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

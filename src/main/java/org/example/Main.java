package org.example;

import com.hummeling.if97.IF97;

public class Main {

    // This method handles different combinations based on P and u
    public static String getPropertiesPU(double P, double u) {
        IF97 if97 = new IF97(IF97.UnitSystem.SI);

        // Convert P from MPa to Pa (if needed) and u from kJ/kg to J/kg
        P *= 1e6;  // Convert MPa to Pa
        u *= 1e3;  // Convert kJ/kg to J/kg

        // Saturation properties at the given pressure
        double u_f = if97.specificEnthalpySaturatedLiquidP(P) - P * if97.specificVolumeSaturatedLiquidP(P);
        double u_g = if97.specificEnthalpySaturatedVapourP(P) - P * if97.specificVolumeSaturatedVapourP(P);

        if (u >= u_f && u <= u_g) {
            // Saturated Mixture Region
            double x = (u - u_f) / (u_g - u_f);
            double T = if97.saturationTemperatureP(P);
            double h = if97.specificEnthalpySaturatedLiquidP(P) + x * (if97.specificEnthalpySaturatedVapourP(P) - if97.specificEnthalpySaturatedLiquidP(P));
            double v = if97.specificVolumeSaturatedLiquidP(P) + x * (if97.specificVolumeSaturatedVapourP(P) - if97.specificVolumeSaturatedLiquidP(P));
            double s = if97.specificEntropySaturatedLiquidP(P) + x * (if97.specificEntropySaturatedVapourP(P) - if97.specificEntropySaturatedLiquidP(P));

            return String.format("Region: Saturated Mixture\n" +
                    "Temperature (T): %.2f °C\n" +
                    "Quality (x): %.4f\n" +
                    "Enthalpy (h): %.2f J/kg\n" +
                    "Specific Volume (v): %.6f m^3/kg\n" +
                    "Entropy (s): %.4f J/(kg·K)", T - 273.15, x, h, v, s);
        } else if (u > u_g) {
            // Superheated Vapor Region
            double T = findTemperatureSuperheated(if97, P, u);
            double h = if97.specificEnthalpyPT(P, T);
            double v = 1 / if97.densityPT(P, T);
            double s = if97.specificEntropyPT(P, T);

            return String.format("Region: Superheated Vapor\n" +
                    "Temperature (T): %.2f °C\n" +
                    "Enthalpy (h): %.2f J/kg\n" +
                    "Specific Volume (v): %.6f m^3/kg\n" +
                    "Entropy (s): %.4f J/(kg·K)", T - 273.15, h, v, s);
        } else {
            // Subcooled Liquid Region
            double T = findTemperatureSubcooled(if97, P, u);
            double h = if97.specificEnthalpyPT(P, T);
            double v = 1 / if97.densityPT(P, T);
            double s = if97.specificEntropyPT(P, T);

            return String.format("Region: Subcooled Liquid\n" +
                    "Temperature (T): %.2f °C\n" +
                    "Enthalpy (h): %.2f J/kg\n" +
                    "Specific Volume (v): %.6f m^3/kg\n" +
                    "Entropy (s): %.4f J/(kg·K)", T - 273.15, h, v, s);
        }
    }

    // Iterative solver for superheated vapor temperature
    private static double findTemperatureSuperheated(IF97 if97, double P, double u) {
        double T_low = if97.saturationTemperatureP(P);
        double T_high = 1500 + 273.15; // Arbitrary high temperature
        double tolerance = 1e-6;

        while (T_high - T_low > tolerance) {
            double T_mid = (T_low + T_high) / 2;
            double u_calc = if97.specificEnthalpyPT(P, T_mid) - P * (1 / if97.densityPT(P, T_mid));
            if (u_calc > u) {
                T_high = T_mid;
            } else {
                T_low = T_mid;
            }
        }
        return (T_low + T_high) / 2;
    }

    // Iterative solver for subcooled liquid temperature
    private static double findTemperatureSubcooled(IF97 if97, double P, double u) {
        double T_low = 273.15; // Near freezing point
        double T_high = if97.saturationTemperatureP(P);
        double tolerance = 1e-6;

        while (T_high - T_low > tolerance) {
            double T_mid = (T_low + T_high) / 2;
            double u_calc = if97.specificEnthalpyPT(P, T_mid) - P * (1 / if97.densityPT(P, T_mid));
            if (u_calc > u) {
                T_high = T_mid;
            } else {
                T_low = T_mid;
            }
        }
        return (T_low + T_high) / 2;
    }

    // Handle T and U
    public static String getPropertiesFromTU(double T, double u) {
        IF97 if97 = new IF97(IF97.UnitSystem.SI);
        T += 273.15; // Convert from Celsius to Kelvin
        u *= 1e3;  // Convert kJ/kg to J/kg

        double P = if97.saturationPressureT(T);
        double h = if97.specificEnthalpyPT(P, T);
        double v = if97.specificVolumePT(P, T);
        double s = if97.specificEntropyPT(P, T);

        return String.format("Region: Based on T and u\n" +
                "Pressure (P): %.2f MPa\n" +
                "Enthalpy (h): %.2f J/kg\n" +
                "Specific Volume (v): %.6f m^3/kg\n" +
                "Entropy (s): %.4f J/(kg·K)", P / 1e6, h, v, s);
    }

    // Handle H and U
    public static String getPropertiesFromHU(double h, double u) {
        IF97 if97 = new IF97(IF97.UnitSystem.SI);
        h *= 1e3;  // Convert from kJ/kg to J/kg
        u *= 1e3;  // Convert from kJ/kg to J/kg

        double T = findTemperatureFromHU(if97, h, u);
        double P = if97.saturationPressureT(T);
        double v = if97.specificVolumePT(P, T);
        double s = if97.specificEntropyPT(P, T);

        return String.format("Region: Based on H and u\n" +
                "Temperature (T): %.2f °C\n" +
                "Pressure (P): %.2f MPa\n" +
                "Specific Volume (v): %.6f m^3/kg\n" +
                "Entropy (s): %.4f J/(kg·K)", T - 273.15, P / 1e6, v, s);
    }

    // Solve for temperature based on H and U
    private static double findTemperatureFromHU(IF97 if97, double h, double u) {
        double T_low = 273.15; // Low temperature boundary
        double T_high = 1500 + 273.15; // High temperature boundary
        double tolerance = 1e-6;

        while (T_high - T_low > tolerance) {
            double T_mid = (T_low + T_high) / 2;
            double h_calc = if97.specificEnthalpyPT(1e6, T_mid);
            if (h_calc > h) {
                T_high = T_mid;
            } else {
                T_low = T_mid;
            }
        }
        return (T_low + T_high) / 2;
    }

    // Main method
    public static void main(String[] args) {
        double pressure = 0.4;  // Pressure in MPa
        double internalEnergy = 1450;  // Internal energy in kJ/kg

        System.out.println(getPropertiesPU(pressure, internalEnergy));
        System.out.println(getPropertiesFromTU(143.61, 1450));
        System.out.println(getPropertiesFromHU(1530.50957, 1450));
    }
}

import numpy as np
import pandas as pd
from data.regions import get_regional_multipliers
from scipy.integrate import odeint

def calculate_biodiversity_impact(frailejon_percentage, ecosystem_resilience):
    """
    Devuelve un índice de biodiversidad (0-100) a partir del porcentaje
    de frailejones (0-100) y resiliencia (0-1).
    """
    # Clamp entradas
    frailejon_percentage = float(np.clip(frailejon_percentage, 0, 100))
    ecosystem_resilience = float(np.clip(ecosystem_resilience, 0.0, 1.0))

    frailejon_norm = frailejon_percentage / 100.0

    k = 6.0
    mid_point = 0.4

    # limitar adjusted_frailejon a [0,1]
    adjusted_frailejon = frailejon_norm + (ecosystem_resilience * 0.25)
    adjusted_frailejon = float(np.clip(adjusted_frailejon, 0.0, 1.0))

    biodiversity_factor = 1.0 / (1.0 + np.exp(-k * (adjusted_frailejon - mid_point)))
    biodiversity_index = biodiversity_factor * 100.0

    return min(biodiversity_index, 100.0)


def calculate_crop_production(frailejon_percentage):
    """
    Mapea el porcentaje de frailejones a la capacidad de regulación hídrica
    expresada como porcentaje (0-100).
    """
    frailejon_norm = float(np.clip(frailejon_percentage, 0, 100)) / 100.0

    if frailejon_norm >= 0.9:
        water_regulation_factor = 1.0
    elif frailejon_norm >= 0.7:
        water_regulation_factor = 0.85 + ((frailejon_norm - 0.7) / 0.2) * 0.15
    elif frailejon_norm >= 0.5:
        water_regulation_factor = 0.6 + ((frailejon_norm - 0.5) / 0.2) * 0.25
    elif frailejon_norm >= 0.3:
        water_regulation_factor = 0.3 + ((frailejon_norm - 0.3) / 0.2) * 0.3
    else:
        water_regulation_factor = (frailejon_norm / 0.3) * 0.3

    return float(np.clip(water_regulation_factor * 100.0, 0.0, 100.0))


def create_ecosystem_simulation(frailejon_percentage, years, ecosystem_resilience,
                                climate_strength=0.02):
    """
    Simula el páramo en el tiempo (años) y devuelve un DataFrame con resolución mensual.

    Parámetros:
    - frailejon_percentage: 0-100
    - years: > 0 (años)
    - ecosystem_resilience: 0-1
    - climate_strength: controla la magnitud del estrés climático (por defecto 0.02)

    Salida:
    - pd.DataFrame con columnas: time (años), biodiversidad, water_regulation,
      endemic_plants, frailejon_population, soil_carbon (todas en % 0-100)
    """
    frailejon_percentage = float(np.clip(frailejon_percentage, 0, 100))
    ecosystem_resilience = float(np.clip(ecosystem_resilience, 0.0, 1.0))
    years = float(years)
    if years <= 0:
        raise ValueError("years debe ser > 0")

    # Tiempo: pasos mensuales, unidad en años
    t = np.arange(0.0, years + 1/12.0, 1/12.0)

    frailejon_norm = frailejon_percentage / 100.0

    # Estado inicial normalizado (0-1)
    initial_state = [1.0, 1.0, 1.0, frailejon_norm, 1.0]

    def paramo_ecosystem_model(y, t_local, resilience):
        biodiversity, water_regulation, endemic_plants, frailejon_pop, soil_carbon = y

        # Parámetros (pueden parametrizarse fuera y calibrarse)
        alpha = 0.08
        beta = 0.12
        gamma = 0.06
        delta = 0.04
        epsilon = 0.05

        # stress creciente en el tiempo: función escalada por climate_strength
        # t_local está en años, normalizamos por el horizonte (years)
        climate_stress = climate_strength * (t_local / max(1e-6, years))

        # Biodiversidad: pérdida por frailejon_pop bajo + estrés climático; recuperación limitada por resiliencia
        dbio_dt = -alpha * (1.0 - frailejon_pop) * biodiversity - climate_stress * biodiversity + (resilience * 0.015 * (1.0 - biodiversity))

        # Regulación hídrica
        dwater_dt = -beta * (1.0 - frailejon_pop) * water_regulation - climate_stress * water_regulation

        # Plantas endémicas
        dplants_dt = -gamma * (1.0 - frailejon_pop) * endemic_plants - climate_stress * endemic_plants

        # Población de frailejones: combinación de declive por clima y posible recuperación ligada a resiliencia
        # Nota: coeficientes ajustables/calibrables
        recovery_rate = 0.01 * resilience
        dfrailejon_dt = -0.05 * climate_stress * frailejon_pop + recovery_rate * (1.0 - frailejon_pop)

        # Carbono del suelo
        dcarbon_dt = -delta * (1.0 - frailejon_pop) * soil_carbon - climate_stress * soil_carbon

        return [dbio_dt, dwater_dt, dplants_dt, dfrailejon_dt, dcarbon_dt]

    # integrador de ecuaciones diferenciales ordinarias (EDO)
    solution = odeint(paramo_ecosystem_model, initial_state, t, args=(ecosystem_resilience,))

    biodiversity = np.maximum(0.0, solution[:, 0]) * 100.0
    water_regulation = np.maximum(0.0, solution[:, 1]) * 100.0
    endemic_plants = np.maximum(0.0, solution[:, 2]) * 100.0
    frailejon_population = np.clip(solution[:, 3], 0.0, 1.0) * 100.0
    soil_carbon = np.maximum(0.0, solution[:, 4]) * 100.0

    df = pd.DataFrame({
        'time': t,
        'biodiversity': biodiversity,
        'water_regulation': water_regulation,
        'endemic_plants': endemic_plants,
        'frailejon_population': frailejon_population,
        'soil_carbon': soil_carbon
    })

    return df


def calculate_economic_impact(frailejon_percentage, region="Todos los páramos"):
    """
    Calcula pérdida económica (en millones USD/año) por servicios ecosistémicos.
    """
    frailejon_percentage = float(np.clip(frailejon_percentage, 0, 100))

    base_values = {
        "water_regulation": 5200.0,
        "carbon_sequestration": 850.0,
        "biodiversity_conservation": 1200.0,
        "tourism": 400.0
    }

    regional_multipliers = get_regional_multipliers()

    multiplier = regional_multipliers.get(region, 1.0)

    frailejon_loss = max(0.0, 100.0 - frailejon_percentage) / 100.0

    economic_losses = {}
    for service, base_value in base_values.items():
        if service == "water_regulation":
            sensitivity = 0.9
        elif service == "carbon_sequestration":
            sensitivity = 0.7
        elif service == "biodiversity_conservation":
            sensitivity = 0.8
        else:
            sensitivity = 0.5

        loss = base_value * multiplier * frailejon_loss * sensitivity
        economic_losses[service] = loss

    return economic_losses


import pandas as pd
import numpy as np


def get_initial_data():
    """
    Genera datos iniciales ficticios sobre frailejones y páramos en Colombia.

    La función simula información sobre especies de frailejones, 
    áreas de páramos, cambios históricos en cobertura y biodiversidad.

    Returns:
    --------
    dict
        Diccionario con DataFrames de diferentes métricas relacionadas
        con la conservación de frailejones y páramos.
    """

    # Especies de frailejones y sus características
    species_data = pd.DataFrame({
        'species': [
            'Espeletia grandiflora', 'Espeletia argentea', 'Espeletia uribei',
            'Espeletia boyacensis', 'Espeletia paipana', 'Espeletia lopezii',
            'Espeletia tunjana', 'Espeletia perijaensis', 'Espeletia barclayana'
        ],
        'altitude_range_masl': [
            '3,000-4,200', '2,800-4,000', '3,100-4,300',
            '2,900-4,000', '3,200-3,800', '3,000-4,200',
            '3,100-3,900', '2,800-3,600', '3,000-3,700'
        ],
        'water_regulation_importance': [
            0.95, 0.90, 0.92,
            0.88, 0.91, 0.94,
            0.87, 0.85, 0.89
        ]
    })

    # Datos históricos de cobertura de frailejones (porcentaje del óptimo)
    years = np.arange(1990, 2025)
    historical_cover = 100 - (0.5 * (years - 1990))  # pérdida del 0.5% anual
    historical_cover = np.maximum(historical_cover, 60)  # mínimo del 60%

    historical_data = pd.DataFrame({
        'year': years,
        'frailejon_cover_percentage': historical_cover
    })

    # Tipos de páramos y sus características
    ecosystems_data = pd.DataFrame({
        'paramo': [
            'Sumapaz', 'Chingaza', 'Rabanal y Río Bogotá',
            'Santurbán', 'Los Nevados', 'Pisba'
        ],
        'area_km2': [
            3337, 766, 150,
            1429, 610, 450
        ],
        'frailejon_species_count': [
            12, 9, 7,
            15, 8, 10
        ],
        'water_supply_million_people': [
            2.0, 1.5, 0.8,
            2.2, 1.0, 0.6
        ]
    })

    # Departamentos y su relación con frailejones
    colombia_data = pd.DataFrame({
        'department': [
            'Cundinamarca', 'Boyacá', 'Santander', 'Norte de Santander', 'Tolima',
            'Cauca', 'Nariño', 'Antioquia', 'Caldas', 'Quindío'
        ],
        'paramo_area_km2': [
            1200, 1800, 950, 870, 400,
            350, 420, 200, 150, 100
        ],
        'frailejon_decline_rate': [
            0.8, 0.7, 0.9, 1.0, 0.6,
            0.5, 0.4, 0.3, 0.5, 0.4
        ],
        'main_paramos': [
            'Sumapaz, Chingaza', 'Pisba, Rabanal', 'Santurbán', 'Santurbán',
            'Los Nevados', 'Páramo de Guanacas', 'Páramo de Paja Blanca',
            'Farallones del Citará', 'Los Nevados', 'Los Nevados'
        ]
    })

    return {
        'species': species_data,
        'historical': historical_data,
        'ecosystems': ecosystems_data,
        'colombia': colombia_data
    }

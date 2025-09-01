import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def get_initial_data():
    """
    Genera datos iniciales ficticios sobre frailejones, páramos y clima en Colombia.
    """
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

    years = np.arange(1990, 2025)
    historical_cover = 100 - (0.5 * (years - 1990))
    historical_cover = np.maximum(historical_cover, 60)
    historical_data = pd.DataFrame({
        'year': years,
        'frailejon_cover_percentage': historical_cover
    })

    ecosystems_data = pd.DataFrame({
        'paramo': [
            'Sumapaz', 'Chingaza', 'Rabanal y Río Bogotá',
            'Santurbán', 'Los Nevados', 'Pisba'
        ],
        'area_km2': [3337, 766, 150, 1429, 610, 450],
        'frailejon_species_count': [12, 9, 7, 15, 8, 10],
        'water_supply_million_people': [2.0, 1.5, 0.8, 2.2, 1.0, 0.6]
    })

    colombia_data = pd.DataFrame({
        'department': [
            'Cundinamarca', 'Boyacá', 'Santander', 'Norte de Santander', 'Tolima',
            'Cauca', 'Nariño', 'Antioquia', 'Caldas', 'Quindío'
        ],
        'paramo_area_km2': [1200, 1800, 950, 870, 400, 350, 420, 200, 150, 100],
        'frailejon_decline_rate': [0.8, 0.7, 0.9, 1.0, 0.6, 0.5, 0.4, 0.3, 0.5, 0.4],
        'main_paramos': [
            'Sumapaz, Chingaza', 'Pisba, Rabanal', 'Santurbán', 'Santurbán',
            'Los Nevados', 'Páramo de Guanacas', 'Páramo de Paja Blanca',
            'Farallones del Citará', 'Los Nevados', 'Los Nevados'
        ]
    })

    climate_data = pd.DataFrame({
        'paramo': [
            'Sumapaz', 'Chingaza', 'Rabanal y Río Bogotá',
            'Santurbán', 'Los Nevados', 'Pisba'
        ],
        'avg_temp_c': [6.5, 7.0, 7.2, 6.8, 5.5, 7.1],
        'annual_precip_mm': [1800, 2000, 1500, 2100, 2500, 1600],
        'projected_temp_increase_2050_c': [1.5, 1.6, 1.4, 1.8, 2.0, 1.5],
        'projected_precip_change_2050_percent': [-10, -8, -12, -15, -5, -9]
    })

    return {
        'species': species_data,
        'historical': historical_data,
        'ecosystems': ecosystems_data,
        'colombia': colombia_data,
        'climate': climate_data
    }

def plot_frailejon_data(data):
    """
    Genera gráficos con Streamlit.
    """
    historical = data['historical']
    climate = data['climate']

    sns.set_theme(style="whitegrid")

    # Gráfico 1: Evolución histórica de cobertura
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.lineplot(x='year', y='frailejon_cover_percentage', data=historical, marker="o", color="green", ax=ax1)
    ax1.set_title("Cobertura Histórica de Frailejones en Colombia", fontsize=14)
    ax1.set_ylabel("Cobertura (%)")
    ax1.set_xlabel("Año")
    ax1.set_ylim(50, 105)
    st.pyplot(fig1)

    # Gráfico 2: Aumento proyectado de temperatura
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='paramo', y='projected_temp_increase_2050_c', data=climate, palette="Reds_r", ax=ax2)
    ax2.set_title("Aumento Proyectado de Temperatura para 2050", fontsize=14)
    ax2.set_ylabel("Aumento (°C)")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=30, ha='right')
    st.pyplot(fig2)

    # Gráfico 3: Cambio proyectado de precipitación
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='paramo', y='projected_precip_change_2050_percent', data=climate, palette="Blues_r", ax=ax3)
    ax3.set_title("Cambio Proyectado de Precipitación para 2050", fontsize=14)
    ax3.set_ylabel("Cambio (%)")
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=30, ha='right')
    st.pyplot(fig3)

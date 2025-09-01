import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import json
from models import (
    calculate_biodiversity_impact, 
    calculate_crop_production, 
    create_ecosystem_simulation
)
from visualizations import (
    plot_frailejon_crop_relationship,
    plot_frailejon_crop_relationship_3d,
    plot_biodiversity_impact,
    plot_biodiversity_impact_3d,
    plot_timeseries_forecast,
    create_risk_map
)
from data_module import get_initial_data
from utils import get_emoji, add_vertical_space

# Page configuration
st.set_page_config(
    page_title="Simulador de Impacto de Frailejones en Colombia",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para tema claro/verde natural
st.markdown("""
<style>
    .main {
        background-color: #f8fffe;
    }
    .main-header {
        font-size: 2.8rem;
        color: #2d5016;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #4a7c2a;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .description {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #2c5530;
    }
    .highlight {
        background-color: #7cb342;
        color: white;
        padding: 0.3rem;
        border-radius: 0.3rem;
        font-weight: bold;
    }
    .card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
        margin-bottom: 1.5rem;
        border: 1px solid #c8e6c9;
    }
    .info-box {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0 0.5rem 0.5rem 0;
    }
    .metric-card {
        background-color: #f1f8e9;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 3px 8px rgba(76, 175, 80, 0.2);
        text-align: center;
        border: 2px solid #aed581;
    }

    /* Estilo para los botones y widgets */
    .stButton button {
        background-color: #4caf50 !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem 1rem !important;
        font-weight: bold !important;
    }

    .stButton button:hover {
        background-color: #45a049 !important;
    }

    .stSlider .stSlider-track {
        background-color: #4caf50 !important;
    }

    /* Estilos para el dashboard */
    .dashboard-header {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
    }

    .dashboard-card {
        background-color: #ffffff;
        border: 2px solid #4caf50;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
    }

    /* Ajustes para el contraste de texto */
    h1, h2, h3, h4, h5, h6 {
        color: #2d5016 !important;
    }

    p, li, span {
        color: #2c5530 !important;
    }

    /* Sección de avances específica */
    .avances-section {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        border: 2px solid #4caf50;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
    }

    .avance-item {
        background-color: #ffffff;
        border-left: 4px solid #4caf50;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 6px rgba(76, 175, 80, 0.1);
    }

    .corte-header {
        background: linear-gradient(90deg, #4caf50 0%, #66bb6a 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 15px 0 10px 0;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Función para cargar/guardar avances
def load_avances():
    """Cargar avances desde archivo o usar valores por defecto"""
    try:
        with open('avances_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "primer_corte": [
                "Revisión bibliográfica sobre el papel de los frailejones en los ecosistemas de páramo",
                "Identificación de especies de frailejones endémicas de Colombia",
                "Análisis preliminar de la distribución geográfica de los frailejones",
                "Definición de parámetros iniciales para el modelo matemático",
                "Implementación de la estructura básica de la aplicación en Streamlit"
            ],
            "segundo_corte": [
                "Desarrollo del modelo matemático para simular el impacto de la pérdida de frailejones",
                "Implementación de ecuaciones diferenciales para modelar la dinámica del ecosistema",
                "Creación de visualizaciones 2D para mostrar relaciones entre variables",
                "Integración de datos específicos de regiones colombianas (Boyacá, Cundinamarca, etc.)",
                "Validación preliminar del modelo con datos reales de páramos"
            ],
            "tercer_corte": [
                "Desarrollo de visualizaciones 3D interactivas con Plotly",
                "Implementación del mapa de riesgo con Folium para páramos colombianos",
                "Creación de métricas económicas y de biodiversidad específicas",
                "Desarrollo de la interfaz de usuario final con controles avanzados",
                "Documentación completa del proyecto y validación final del modelo"
            ]
        }

def save_avances(avances_data):
    """Guardar avances en archivo"""
    with open('avances_data.json', 'w', encoding='utf-8') as f:
        json.dump(avances_data, f, ensure_ascii=False, indent=2)

# Header
st.markdown(f"<h1 class='main-header'>🌿 Impacto de la Pérdida de Frailejones en Ecosistemas de Páramo - Colombia</h1>", unsafe_allow_html=True)

# Introduction
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Sobre esta aplicación</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p class='description'>
    Esta aplicación modela el impacto crítico de la disminución de las poblaciones de frailejones en la biodiversidad y 
    la regulación hídrica de los páramos colombianos. A través de visualizaciones interactivas y modelos matemáticos 
    basados en métodos numéricos, podrás explorar cómo los cambios en las poblaciones de frailejones afectan a los 
    ecosistemas de alta montaña y los servicios ecosistémicos que proporcionan.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
    <p>Los frailejones son especies endémicas de los páramos neotropicales, responsables de la regulación del 
    <span class='highlight'>70% del agua que abastece a Bogotá</span> y otras ciudades andinas, además de albergar 
    <span class='highlight'>más del 60% de la biodiversidad de alta montaña</span> en Colombia, con un valor ecosistémico 
    estimado de <span class='highlight'>15-25 mil millones de dólares anuales</span> en servicios ambientales.
    </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Sección de Avances - Universidad Central 2025-2S
st.markdown("<div class='avances-section'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>📚 Avances del Proyecto - Métodos Numéricos</h2>", unsafe_allow_html=True)
st.markdown("<p class='description'><strong>Universidad Central - 2025 Segundo Semestre</strong></p>", unsafe_allow_html=True)

# Cargar avances existentes
avances = load_avances()

# Editor de avances
with st.expander("✏️ Editar Avances del Proyecto", expanded=False):
    st.info("Puedes modificar los avances de cada corte. Los cambios se guardarán automáticamente.")

    # Primer Corte
    st.markdown("<div class='corte-header'>Primer Corte</div>", unsafe_allow_html=True)
    primer_corte_text = st.text_area(
        "Avances del Primer Corte:",
        value="\n".join([f"• {avance}" for avance in avances["primer_corte"]]),
        height=150,
        key="primer_corte"
    )

    # Segundo Corte
    st.markdown("<div class='corte-header'>Segundo Corte</div>", unsafe_allow_html=True)
    segundo_corte_text = st.text_area(
        "Avances del Segundo Corte:",
        value="\n".join([f"• {avance}" for avance in avances["segundo_corte"]]),
        height=150,
        key="segundo_corte"
    )

    # Tercer Corte
    st.markdown("<div class='corte-header'>Tercer Corte</div>", unsafe_allow_html=True)
    tercer_corte_text = st.text_area(
        "Avances del Tercer Corte:",
        value="\n".join([f"• {avance}" for avance in avances["tercer_corte"]]),
        height=150,
        key="tercer_corte"
    )

    if st.button("💾 Guardar Cambios", type="primary"):
        # Procesar y guardar los cambios
        nuevo_avances = {
            "primer_corte": [line.strip("• ").strip() for line in primer_corte_text.split("\n") if line.strip()],
            "segundo_corte": [line.strip("• ").strip() for line in segundo_corte_text.split("\n") if line.strip()],
            "tercer_corte": [line.strip("• ").strip() for line in tercer_corte_text.split("\n") if line.strip()]
        }
        save_avances(nuevo_avances)
        st.success("¡Avances guardados correctamente!")
        st.rerun()

# Mostrar avances actuales
col_avances1, col_avances2, col_avances3 = st.columns(3)

with col_avances1:
    st.markdown("<div class='corte-header'>🥇 Primer Corte</div>", unsafe_allow_html=True)
    for avance in avances["primer_corte"]:
        st.markdown(f"<div class='avance-item'>• {avance}</div>", unsafe_allow_html=True)

with col_avances2:
    st.markdown("<div class='corte-header'>🥈 Segundo Corte</div>", unsafe_allow_html=True)
    for avance in avances["segundo_corte"]:
        st.markdown(f"<div class='avance-item'>• {avance}</div>", unsafe_allow_html=True)

with col_avances3:
    st.markdown("<div class='corte-header'>🥉 Tercer Corte</div>", unsafe_allow_html=True)
    for avance in avances["tercer_corte"]:
        st.markdown(f"<div class='avance-item'>• {avance}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Main content in two columns
col1, col2 = st.columns([2, 3])

# Left column - Controls and information
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Controles de Simulación</h2>", unsafe_allow_html=True)

    # Slider for frailejón population adjustment
    frailejon_population_percentage = st.slider(
        "🌿Porcentaje de población de frailejones respecto al nivel óptimo",
        min_value=10,
        max_value=100,
        value=100,
        step=5,
        help="Ajusta el porcentaje de la población de frailejones para ver el impacto en el páramo"
    )

    # Additional parameters
    st.markdown("<h3>Parámetros del Ecosistema</h3>", unsafe_allow_html=True)

    selected_region = st.selectbox(
        "🏞️ Páramo/Región de Colombia",
        options=["Todos los páramos", "Páramo de Sumapaz", "Páramo de Chingaza", "Páramo de Guerrero", 
                "Páramo de Rabanal", "Páramo de Pisba", "Páramo de Almorzadero", "Páramo de Santurbán"],
        help="Selecciona un páramo específico para analizar"
    )

    years_to_simulate = st.slider(
        "🕰️ Años a simular",
        min_value=1,
        max_value=40,
        value=15,
        step=1
    )

    ecosystem_resilience = st.select_slider(
        "🔄 Resiliencia del páramo",
        options=["Muy baja", "Baja", "Media", "Alta", "Muy alta"],
        value="Media",
        help="Capacidad del páramo para recuperarse ante perturbaciones"
    )

    climate_scenario = st.radio(
        "🌡️ Escenario climático",
        options=["Estable", "Calentamiento moderado", "Calentamiento severo"],
        horizontal=True,
        help="Escenario de cambio climático para la simulación"
    )

    # Convert resilience to numerical value for calculations
    resilience_mapping = {
        "Muy baja": 0.2,
        "Baja": 0.4,
        "Media": 0.6,
        "Alta": 0.8,
        "Muy alta": 1.0
    }
    resilience_value = resilience_mapping[ecosystem_resilience]

    st.markdown("</div>", unsafe_allow_html=True)

    # Importance of frailejones section
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Importancia de los Frailejones</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p class='description'>
    Los frailejones son fundamentales para los páramos porque:
    </p>
    <ul>
        <li><strong>Regulación hídrica:</strong> Capturan y almacenan agua de la niebla y precipitación.</li>
        <li><strong>Biodiversidad:</strong> Crean microhábitats únicos para especies endémicas.</li>
        <li><strong>Servicios ecosistémicos:</strong> Proporcionan agua limpia a millones de personas.</li>
        <li><strong>Captura de carbono:</strong> Almacenan grandes cantidades de carbono en sus tejidos y suelos.</li>
    </ul>
    """, unsafe_allow_html=True)

    with st.expander("¿Por qué están en peligro los frailejones?"):
        st.markdown("""
        <p class='description'>
        Las principales amenazas para los frailejones incluyen:
        </p>
        <ul>
            <li><strong>Cambio climático</strong>: Aumento de temperatura en páramos.</li>
            <li><strong>Minería</strong>: Degradación de hábitats por actividades extractivas.</li>
            <li><strong>Agricultura</strong>: Expansión de cultivos hacia zonas de páramo.</li>
            <li><strong>Incendios forestales</strong>: Destrucción de poblaciones completas.</li>
            <li><strong>Urbanización</strong>: Fragmentación de ecosistemas de páramo.</li>
        </ul>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Right column - Visualizations
with col2:
    # Calculate impacts based on the slider and parameters
    biodiversity_impact = calculate_biodiversity_impact(frailejon_population_percentage, resilience_value)
    water_regulation_impact = frailejon_population_percentage
    ecosystem_data = create_ecosystem_simulation(frailejon_population_percentage, years_to_simulate, resilience_value)

    # Metrics display
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Impacto Calculado</h2>", unsafe_allow_html=True)

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)

        climate_modifier = 1.0
        if climate_scenario == "Calentamiento moderado":
            climate_modifier = 0.9
        elif climate_scenario == "Calentamiento severo":
            climate_modifier = 0.75

        adjusted_water_impact = min(100, water_regulation_impact * climate_modifier)

        st.metric(
            label="🪴 Regulación Hídrica",
            value=f"{adjusted_water_impact:.1f}%",
            delta=f"{adjusted_water_impact - 100:.1f}%" if frailejon_population_percentage < 100 else None,
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with metric_col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)

        region_modifier = 1.0
        region_name = "Colombia"

        if selected_region == "Páramo de Sumapaz":
            region_modifier = 1.2
            region_name = "Sumapaz"
        elif selected_region == "Páramo de Chingaza":
            region_modifier = 1.15
            region_name = "Chingaza"
        elif selected_region == "Páramo de Santurbán":
            region_modifier = 1.3
            region_name = "Santurbán"

        adjusted_biodiversity = biodiversity_impact * region_modifier
        adjusted_biodiversity = min(100, adjusted_biodiversity)

        st.metric(
            label=f"🌱 Biodiversidad en {region_name}",
            value=f"{adjusted_biodiversity:.1f}%",
            delta=f"{adjusted_biodiversity - 100:.1f}%" if frailejon_population_percentage < 100 else None,
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with metric_col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)

        base_species = 3000  # Especies de páramo
        if selected_region != "Todos los páramos":
            if selected_region in ["Páramo de Sumapaz", "Páramo de Chingaza"]:
                base_species = 1200
            else:
                base_species = 800

        species_at_risk = int(max(0, 100 - frailejon_population_percentage) * 0.25 * base_species / 100)

        st.metric(
            label="⚠️ Especies en Riesgo por pérdida de frailejones",
            value=f"{species_at_risk:,}",
            delta=f"+{species_at_risk}" if frailejon_population_percentage < 100 else "0",
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Add additional metrics
    st.markdown("<div style='padding: 10px;'>", unsafe_allow_html=True)
    metric_col4, metric_col5 = st.columns(2)

    with metric_col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)

        water_base = 450  # Millones de litros/día
        if selected_region != "Todos los páramos":
            if selected_region in ["Páramo de Chingaza", "Páramo de Sumapaz"]:
                water_base = 180
            else:
                water_base = 80

        water_loss = water_base * (max(0, 100 - frailejon_population_percentage) / 100)

        st.metric(
            label="💧 Pérdida de Regulación Hídrica",
            value=f"{water_loss:.1f}M L/día",
            delta=f"-{water_loss:.1f}M" if frailejon_population_percentage < 100 else "0",
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with metric_col5:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)

        carbon_base = 15000  # Toneladas CO2
        if selected_region != "Todos los páramos":
            if selected_region in ["Páramo de Sumapaz", "Páramo de Chingaza"]:
                carbon_base = 6000
            else:
                carbon_base = 3000

        carbon_loss = int(carbon_base * (max(0, 100 - frailejon_population_percentage) / 100) * 0.6)

        st.metric(
            label="🌳 Pérdida de Captura CO₂",
            value=f"{carbon_loss:,} Ton",
            delta=f"-{carbon_loss:,}" if frailejon_population_percentage < 100 else "0",
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Visualizations
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>🌿 Frailejones y su impacto en el páramo</h2>", unsafe_allow_html=True)

    viz_type = st.radio(
        "Selecciona tipo de visualización",
        options=["Gráfico 2D", "Modelo 3D Interactivo"],
        horizontal=True,
        key="frailejon_viz_type"
    )

    if viz_type == "Gráfico 2D":
        fig_relationship = plot_frailejon_crop_relationship(frailejon_population_percentage)
        st.plotly_chart(fig_relationship, use_container_width=True)

        st.markdown("""
        <p class='description'>
        El gráfico muestra la relación crítica entre la población de frailejones y los servicios ecosistémicos 
        del páramo. La pérdida de frailejones tiene efectos exponenciales en la regulación hídrica y 
        la biodiversidad del ecosistema.
        </p>
        """, unsafe_allow_html=True)
    else:
        fig_relationship_3d = plot_frailejon_crop_relationship_3d(frailejon_population_percentage, years_to_simulate)
        st.plotly_chart(fig_relationship_3d, use_container_width=True)

        st.markdown("""
        <p class='description'>
        Esta visualización 3D muestra cómo evoluciona el impacto en los servicios ecosistémicos a lo largo del tiempo
        según diferentes niveles de población de frailejones. El punto rojo indica tu configuración actual.
        </p>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer personalizado para Universidad Central
add_vertical_space(2)
st.markdown("""
<div style="background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%); color: white; text-align: center; padding: 20px; border-radius: 10px; margin-top: 30px;">
<h3 style="color: white !important; margin-bottom: 10px;">🎓 Proyecto de Métodos Numéricos</h3>
<p style="color: white !important; margin: 0; font-size: 1.1rem;">Universidad Central - Facultad de Ingeniería</p>
<p style="color: white !important; margin: 0; font-size: 1rem;">Segundo Semestre 2025 | Simulación de Ecosistemas de Páramo</p>
<p style="color: white !important; margin-top: 10px; font-size: 0.9rem;">Desarrollado para la conservación de frailejones en Colombia 🌿</p>
</div>
""", unsafe_allow_html=True)
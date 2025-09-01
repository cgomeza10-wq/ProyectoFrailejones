import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
from data.regions import get_frailejon_regions

st.set_page_config(
    page_title="Mapa Detallado - Impacto de Frailejones en Colombia",
    page_icon="🌿",
    layout="wide"
)

# ==== Estilos ====
st.markdown("""
<style>
    .main { background-color: #f8fffe; }
    .main-header { font-size: 2.5rem; color: #2d5016; text-align: center; font-weight: bold; }
    .sub-header { font-size: 1.5rem; color: #4a7c2a; font-weight: 600; }
    .description { font-size: 1rem; line-height: 1.5; color: #2c5530; }
    .highlight { background-color: #4caf50; color: white; padding: 0.2rem; border-radius: 0.2rem; }
    .card { background-color: #ffffff; padding: 1.5rem; border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15); margin-bottom: 1rem; border: 1px solid #c8e6c9; }
    .map-container { border: 2px solid #4caf50; border-radius: 1rem; padding: 10px; margin-bottom: 1rem; background-color: #f1f8e9; }
    h1, h2, h3, h4, h5, h6 { color: #2d5016 !important; }
    p, li, span { color: #2c5530 !important; }
    .stButton button { background-color: #4caf50 !important; color: white !important; border: none !important;
                       border-radius: 0.5rem !important; padding: 0.5rem 1rem !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# ==== Título ====
st.markdown("<h1 class='main-header'>🌿 Mapa de Páramos y Frailejones en Colombia</h1>", unsafe_allow_html=True)

# ==== Intro ====
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Análisis de Ecosistemas de Páramos y Frailejones por Región</h2>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
Este mapa muestra los páramos de Colombia y la distribución de frailejones en cada región.
Explora la densidad actual de frailejones y los niveles de riesgo por páramo.
</p>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==== Controles ====
colA, colB, colC = st.columns([1.2, 1, 1])
with colA:
    map_type = st.selectbox("Tipo de visualización", ["Marcadores de Páramos", "Densidad de Frailejones", "Clusters por Región"], index=0)
with colB:
    view = st.radio("Escenario a mostrar", ["Actual", "Proyección"], index=0, horizontal=True)
with colC:
    years_ahead = st.slider("Horizonte (años)", min_value=0, max_value=40, value=20, step=1)

# Filtros adicionales
control_col1, control_col2 = st.columns(2)
with control_col1:
    risk_filter = st.multiselect("Filtrar por nivel de riesgo", ["Crítico", "Alto", "Medio", "Bajo"],
                                  default=["Crítico", "Alto", "Medio", "Bajo"])
with control_col2:
    frailejon_threshold = st.slider("Densidad mínima de frailejones (%)", min_value=0, max_value=100, value=20, step=5)

# ==== Datos base ====
paramos = get_frailejon_regions()

# Preparamos datos
for p in paramos:
    # === Agregar especies de frailejones ===
    # Si el páramo ya tiene especies registradas, las dejamos
    # Si no, le asignamos un valor por defecto
    especies = p.get("frailejon_species", [])
    if not especies:
        especies = ["Espeletia grandiflora", "Espeletia argentea"]  # ejemplo
    p["frailejon_species"] = especies

# === Selección de campos ===
density_field = "frailejon_density"
risk_field = "risk"

# === Filtrado ===
filtered_paramos = [
    p for p in paramos
    if p.get(risk_field, "Bajo") in risk_filter and p.get(density_field, 0) >= frailejon_threshold
]

# ==== Mapa ====
st.markdown("<div class='map-container'>", unsafe_allow_html=True)
m = folium.Map(location=[5.5, -73.5], zoom_start=6, tiles='CartoDB positron')

def color_por_riesgo(r):
    return {'Crítico': 'darkred', 'Alto': 'red', 'Medio': 'orange'}.get(r, 'green')

if map_type == "Marcadores de Páramos":
    for p in filtered_paramos:
        color = color_por_riesgo(p.get(risk_field, 'Bajo'))
        dens = p.get(density_field, 0)
        popup_content = f"""
        <div style="width: 280px">
            <h4>{p.get('name','Páramo')}</h4>
            <p><strong>Vista:</strong> {view}</p>
            <p><strong>Horizonte:</strong> {years_ahead} años</p>
            <p><strong>Departamento:</strong> {p.get('department','N/D')}</p>
            <p><strong>Nivel de riesgo:</strong> {p.get(risk_field,'N/D')}</p>
            <p><strong>Densidad de frailejones:</strong> {dens:.1f}%</p>
            <p><strong>Área aproximada:</strong> {p.get('area','N/D')} km²</p>
            <p><strong>Altitud promedio:</strong> {p.get('altitude','N/D')} msnm</p>
            <p><strong>Servicios ecosistémicos:</strong> {p.get('ecosystem_services','N/D')}</p>
            <p><strong>Tipo de frailejones:</strong> {p.get('type_frailejones','N/D')}</p>
            <p><em>{p.get('description','')}</em></p>
        </div>
        """
        tooltip = f"{p.get('name','Páramo')} - {view}"
        folium.Marker(
            location=[p.get('lat', 0), p.get('lon', 0)],
            popup=folium.Popup(popup_content, max_width=320),
            tooltip=tooltip,
            icon=folium.Icon(color=color, icon='tree', prefix='fa')
        ).add_to(m)

        folium.Circle( 
            radius=max(0, dens) * 800,
            location=[p.get('lat', 0), p.get('lon', 0)],
            color=color,
            fill=True, fill_opacity=0.3, opacity=0.7, weight=2
        ).add_to(m)

elif map_type == "Densidad de Frailejones":
    heat_data = [[p.get('lat', 0), p.get('lon', 0), p.get(density_field, 0)] for p in filtered_paramos]
    
    # Mapa de calor
    HeatMap(
        heat_data,
        radius=20,
        min_opacity=0.4,
        gradient={0.4: '#81c784', 0.6: '#66bb6a', 0.8: '#4caf50', 1.0: '#2e7d32'},
        blur=15
    ).add_to(m)

    # Función para definir color según densidad
    def get_color(density):
        if density < 30:
            return "red"      # Baja densidad
        elif density < 60:
            return "orange"   # Media densidad
        else:
            return "green"    # Alta densidad

    for p in filtered_paramos:
        dens = p.get(density_field, 0)
        popup_content = f"""
        <div style="width: 250px">
            <h4>{p.get('name','Páramo')}</h4>
            <p><strong>Vista:</strong> {view}</p>
            <p><strong>Horizonte:</strong> {years_ahead} años</p>
            <p><strong>Densidad de frailejones:</strong> {dens:.1f}%</p>
            <p><strong>Área aproximada:</strong> {p.get('area','N/D')} km²</p>
            <p><strong>Altitud promedio:</strong> {p.get('altitude','N/D')} msnm</p>
        </div>
        """
        folium.CircleMarker(
            location=[p.get('lat', 0), p.get('lon', 0)],
            radius=8,
            color=get_color(dens),
            fill=True,
            fill_color=get_color(dens),
            fill_opacity=0.7,
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{p.get('name','Páramo')} - {dens:.1f}% frailejones"
        ).add_to(m)

elif map_type == "Clusters por Región":
    marker_cluster = MarkerCluster().add_to(m)
    for p in filtered_paramos:
        color = color_por_riesgo(p.get(risk_field, 'Bajo'))
        dens = p.get(density_field, 0)
        popup_content = f"""
        <div style="width: 280px">
            <h4>{p.get('name','Páramo')}</h4>
            <p><strong>Vista:</strong> {view}</p>
            <p><strong>Horizonte:</strong> {years_ahead} años</p>
            <p><strong>Nivel de riesgo:</strong> {p.get(risk_field,'N/D')}</p>
            <p><strong>Densidad de frailejones:</strong> {dens:.1f}%</p>
        </div>
        """
        folium.Marker(
            location=[p.get('lat', 0), p.get('lon', 0)],
            popup=folium.Popup(popup_content, max_width=320),
            tooltip=p.get('name', 'Páramo'),
            icon=folium.Icon(color=color, icon='tree', prefix='fa')
        ).add_to(marker_cluster)

st_folium(m, width=1200, height=600)
st.markdown("</div>", unsafe_allow_html=True)

# ==== Análisis ====
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Análisis de Páramos por Región</h2>", unsafe_allow_html=True)

# Construir DataFrame
paramo_df = pd.DataFrame([{
    'Páramo': p.get('name','Páramo'),
    'Departamento': p.get('department', 'N/A'),
    'Tipo de Frailejón': p.get('type_frailejones', 'N/D'),
    'Riesgo': p.get('risk', 'N/A'),
    'Densidad (%)': p.get('frailejon_density', 0.0),
    'Área (km²)': p.get('area', 0.0),
    'Altitud (msnm)': p.get('altitude', 0.0)
} for p in filtered_paramos])

# ==== Gráficos ====
analysis_col1, analysis_col2 = st.columns(2)
with analysis_col1:
    st.subheader("Páramos por nivel de riesgo")
    risk_counts = paramo_df['Riesgo'].value_counts()
    st.bar_chart(risk_counts)

with analysis_col2:
    st.subheader("Densidad promedio de frailejones")
    avg_density = paramo_df['Densidad (%)'].mean()
    st.bar_chart(pd.Series({"Densidad Promedio": avg_density}))

# ==== Métricas ====
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
with metric_col1:
    total_paramos = len(filtered_paramos)
    st.metric("Total de Páramos", total_paramos)
with metric_col2:
    critical_count = (paramo_df['Riesgo'] == 'Crítico').sum()
    st.metric("Páramos en Riesgo Crítico", critical_count,
              delta=f"{(critical_count/max(1,total_paramos))*100:.1f}%")
with metric_col3:
    avg_density = paramo_df['Densidad (%)'].mean()
    st.metric("Densidad Promedio", f"{avg_density:.1f}%")
with metric_col4:
    total_area = paramo_df['Área (km²)'].sum()
    st.metric("Área Total de Páramos", f"{total_area:,.0f} km²")

st.markdown("</div>", unsafe_allow_html=True)

# ==== Tabla ====
st.subheader("Datos detallados por páramo")
st.dataframe(paramo_df, use_container_width=True)

# ==== Conclusiones ====
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown(f"""
<h2 class='sub-header'>Conclusiones y Recomendaciones</h2>
<p class='description'>
El análisis muestra la distribución actual de frailejones en los páramos de Colombia.
La densidad promedio es de <strong>{avg_density:.1f}%</strong> y existen <strong>{critical_count}</strong>
páramos en riesgo crítico que requieren atención inmediata.
</p>
<ul>
    <li>Refuerza restauración ecológica en páramos con densidad ≤ 10%.</li>
    <li>Prioriza monitoreo hídrico en regiones con riesgo <em>Alto/Crítico</em>.</li>
    <li>Evalúa restricciones a actividades mineras y expansión agropecuaria en zonas sensibles.</li>
</ul>
<div class='highlight'>
<p><strong>Horizonte seleccionado:</strong> {years_ahead} años en vista {view}</p>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==== Footer ====
st.markdown("""
<div style="background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%); color: white; text-align: center; padding: 15px; border-radius: 10px; margin-top: 20px;">
<h4 style="color: white !important; margin: 0;">🌿 Conservación de Frailejones en Colombia | Universidad Central 2025</h4>
<p style="color: white !important; margin: 5px 0 0 0; font-size: 0.9rem;">Proyecto de Métodos Numéricos - Análisis de Ecosistemas</p>
</div>
""", unsafe_allow_html=True)
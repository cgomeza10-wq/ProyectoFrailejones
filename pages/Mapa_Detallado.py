import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
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

# ==== Función de proyección-- metodo numerico implementado Ecuaciones Diferenciales Ordinarias (EDO) ====
def proyectar_paramos(paramos, years_ahead, view):
    proyectados = []

    for p in paramos:
        nuevo = p.copy()

        if view == "Proyección":
            # Parámetros ecológicos base
            r = 0.03   # tasa base
            K = 100.0  # capacidad de carga (densidad máxima)
            resiliencia = p.get("resilience", 1.0)
            clima = p.get("climate_scenario", "Estable")

            # Ajustar tasa según riesgo inicial
            riesgo = p.get("risk", "Medio")
            if riesgo == "Crítico":
                r = -0.05 
            elif riesgo == "Alto":
                r = -0.03
            elif riesgo == "Medio":
                r = 0.00  
            else:  # Bajo
                r = 0.02 

            # Ajustar tasa según escenario climático
            if clima == "Calentamiento moderado":
                r *= 0.8
            elif clima == "Calentamiento severo":
                r *= 0.5

            # Ajustar capacidad según resiliencia
            K *= resiliencia

            # Densidad inicial
            D = p.get("frailejon_density", 50)
            t = 0
            h = 1  # paso temporal (años)

            # Ecuación diferencial logística: dD/dt = r*D*(1 - D/K)
            def f(t, D):
                return r * D * (1 - D / K)

            # Resolver con Runge-Kutta 4
            for _ in range(years_ahead):
                k1 = h * f(t, D)
                k2 = h * f(t + h/2, D + k1/2)
                k3 = h * f(t + h/2, D + k2/2)
                k4 = h * f(t + h, D + k3)
                D = D + (k1 + 2*k2 + 2*k3 + k4) / 6
                t += h

            # Limitar valores
            D = max(0, min(D, 100))
            nuevo["frailejon_density"] = D

            # Clasificar el riesgo según densidad final
            if D < 20:
                nuevo["risk"] = "Crítico"
            elif D < 40:
                nuevo["risk"] = "Alto"
            elif D < 60:
                nuevo["risk"] = "Medio"
            else:
                nuevo["risk"] = "Bajo"

            # Servicios ecosistémicos
            import math
            R = 100 / (1 + math.exp(-0.1 * (D - 50)))
            nuevo["water_regulation"] = round(R, 2)
            nuevo["carbon_capture"] = round(D * 0.1, 2)
            nuevo["biodiversity"] = round(70 + D * 0.3, 2)

        proyectados.append(nuevo)

    return proyectados

st.markdown("<h1 class='main-header'>🌿 Mapa de Páramos y Frailejones en Colombia</h1>", unsafe_allow_html=True)

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
    years_ahead = 0
if view == "Proyección":
    years_ahead = st.slider("Horizonte de años", 1, 50, 10)

# Filtros adicionales
control_col1, control_col2 = st.columns(2)
with control_col1:
    risk_filter = st.multiselect("Filtrar por nivel de riesgo", ["Crítico", "Alto", "Medio", "Bajo"],
                                  default=["Crítico", "Alto", "Medio", "Bajo"])
with control_col2:
    frailejon_threshold = st.slider("Densidad mínima de frailejones (%)", min_value=0, max_value=100, value=20, step=5)

# ==== Datos base + proyección ====
paramos_base = get_frailejon_regions()
paramos = proyectar_paramos(paramos_base, years_ahead, view)

# Preparamos datos
for p in paramos:
    especies = p.get("frailejon_species", [])
    if not especies:
        especies = ["Espeletia grandiflora", "Espeletia argentea"]
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
    
    HeatMap(
        heat_data,
        radius=20,
        min_opacity=0.4,
        gradient={0.4: '#81c784', 0.6: '#66bb6a', 0.8: '#4caf50', 1.0: '#2e7d32'},
        blur=15
    ).add_to(m)

    def get_color(density):
        if density < 30:
            return "red"
        elif density < 60:
            return "orange"
        else:
            return "green"

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

paramo_df = pd.DataFrame([{
    'Páramo': p.get('name','Páramo'),
    'Departamento': p.get('department', 'N/A'),
    'Tipo de Frailejón': p.get('type_frailejones', 'N/D'),
    'Riesgo': p.get('risk', 'N/A'),
    'Densidad (%)': p.get('frailejon_density', 0.0),
    'Área (km²)': p.get('area', 0.0),
    'Altitud (msnm)': p.get('altitude', 0.0)
} for p in filtered_paramos])

analysis_col1, analysis_col2 = st.columns(2)

# --- Gráfico de páramos (izquierda) ---
with analysis_col1:
    st.subheader("Distribución de Páramos por Nivel de Riesgo")
    risk_counts = paramo_df['Riesgo'].value_counts().reset_index()
    risk_counts.columns = ['Riesgo', 'Cantidad']

    # Paleta de colores personalizados
    risk_palette = {
        "Crítico": "#E53935", 
        "Alto": "#FB8C00",    
        "Medio": "#FDD835",  
        "Bajo": "#43A047"   
    }

    chart_risk = (
        alt.Chart(risk_counts)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("Riesgo:N", sort=["Crítico", "Alto", "Medio", "Bajo"]),
            y=alt.Y("Cantidad:Q"),
            color=alt.Color("Riesgo:N", scale=alt.Scale(domain=list(risk_palette.keys()),
                                                       range=list(risk_palette.values()))),
            tooltip=["Riesgo", "Cantidad"]
        )
        .properties(width=300, height=300)
        .configure_axis(labelColor="white", titleColor="white")
    )
    st.altair_chart(chart_risk, use_container_width=True)


# --- Gráfico de densidad (derecha) ---

with analysis_col2:
    st.subheader("Distribución de Densidad de Frailejones")

    if not paramo_df.empty:
        bins = [0, 20, 40, 60, 80, 100]
        labels = ['0–20%', '21–40%', '41–60%', '61–80%', '81–100%']

        # Crear categorías con etiquetas
        density_bins = pd.cut(paramo_df['Densidad (%)'], bins=bins, labels=labels, include_lowest=True)
        density_counts = density_bins.value_counts().sort_index()

        # Crear DataFrame
        df_counts = pd.DataFrame({
            'Rango de Densidad (%)': density_counts.index,
            'Cantidad de Páramos': density_counts.values
        })

        color_scale = alt.Scale(
            domain=labels,
            range=["#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF", "#845EC2"]
        )

        chart = alt.Chart(df_counts).mark_bar().encode(
            x=alt.X('Rango de Densidad (%)', sort=labels, title='Rango de Densidad (%)'),
            y=alt.Y('Cantidad de Páramos', title='Cantidad de Páramos'),
            color=alt.Color('Rango de Densidad (%)', scale=color_scale, legend=None),
            tooltip=['Rango de Densidad (%)', 'Cantidad de Páramos']
        ).properties(
            width=400,
            height=300
        )

        st.altair_chart(chart, use_container_width=True)

    else:
        st.info("No hay páramos en el filtro actual para mostrar la distribución.")


# === Métricas ===
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
with metric_col1:
    total_paramos = len(filtered_paramos)
    st.metric("Total de Páramos", total_paramos)
with metric_col2:
    alto_count = (paramo_df['Riesgo'] == 'Alto').sum()
    st.metric("Páramos en Riesgo Alto", alto_count,
              delta=f"{(alto_count/max(1,total_paramos))*100:.1f}%")
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
El análisis muestra la distribución {'proyectada' if view=='Proyección' else 'actual'} de frailejones en los páramos de Colombia.
La densidad promedio es de <strong>{avg_density:.1f}%</strong>, indicando cuántos frailejones
permanecerían en un horizonte de <strong>{years_ahead} años</strong>.
Actualmente existen <strong>{alto_count}</strong> páramos en riesgo alto que requieren atención inmediata.
</p>
<ul>
    <li>Fortalece los programas de restauración ecológica en páramos con densidad de frailejones ≤ 20%, especialmente en zonas del altiplano cundiboyacense y Nariño.</li>
    <li>Intensifica el monitoreo hídrico en regiones con riesgo <em>Alto</em> y <em>Crítico</em>, donde la pérdida de vegetación afecta la regulación del agua y la captura de carbono.</li>
    <li>Implementa controles más estrictos sobre la minería, ganadería y expansión agrícola en áreas con degradación acelerada de cobertura vegetal.</li>
    <li>Promueve proyectos de conservación comunitaria en páramos con resiliencia ecológica media, incentivando la reforestación con especies nativas como los frailejones.</li>
    <li>Apoya investigaciones sobre los efectos del cambio climático en la densidad y regeneración natural de frailejones a largo plazo.</li>
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

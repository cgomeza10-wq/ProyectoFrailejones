
import streamlit as st

st.set_page_config(
    page_title="Sobre el Proyecto - Impacto de Frailejones en Colombia",
    page_icon="🌿",
    layout="wide"
)

# Estilo para mantener consistencia con la página principal
st.markdown("""
<style>
    .main {
        background-color: #f8fffe;
    }
    .main-header {
        font-size: 2.5rem;
        color: #2d5016;
        text-align: center;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4a7c2a;
        font-weight: 600;
    }
    .description {
        font-size: 1rem;
        line-height: 1.5;
        color: #2c5530;
    }
    .highlight {
        background-color: #4caf50;
        color: white;
        padding: 0.2rem;
        border-radius: 0.2rem;
    }
    .card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
        margin-bottom: 1rem;
        border: 1px solid #c8e6c9;
    }
    .info-box {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0 0.5rem 0.5rem 0;
    }
    /* Ajustes para el contraste de texto */
    h1, h2, h3, h4, h5, h6 {
        color: #2d5016 !important;
    }
    p, li, span {
        color: #2c5530 !important;
    }
    
    .methodology-box {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        border: 2px solid #4caf50;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>🌿 Sobre el Proyecto</h1>", unsafe_allow_html=True)

# Contenido principal
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Acerca de esta Aplicación</h2>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
Este proyecto tiene como objetivo modelar el impacto crítico de la pérdida de frailejones en los ecosistemas de páramo 
de Colombia. La aplicación utiliza métodos numéricos avanzados y modelos matemáticos para simular cómo diferentes 
niveles de población de frailejones afectan la biodiversidad, la regulación hídrica y los servicios ecosistémicos 
que estos ecosistemas únicos proporcionan al país.
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class='info-box'>
<p><strong>¿Por qué son importantes los frailejones?</strong></p>
<p>Los frailejones son plantas endémicas de los páramos neotropicales que actúan como "fábricas de agua", 
capturando humedad de las nubes y regulando el flujo hídrico que abastece a más de 25 millones de personas 
en Colombia, Venezuela y Ecuador. Su pérdida representa una amenaza directa al suministro de agua potable 
y a la estabilidad climática regional.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3>Objetivos del Proyecto</h3>", unsafe_allow_html=True)
st.markdown("""
<ul>
    <li><strong>Educación y concienciación:</strong> Crear conciencia sobre la importancia crítica de los frailejones para los ecosistemas de páramo</li>
    <li><strong>Simulación científica:</strong> Proporcionar una herramienta educativa que muestre visualmente el impacto de la pérdida de frailejones</li>
    <li><strong>Datos específicos:</strong> Ofrecer información detallada sobre páramos colombianos para la toma de decisiones</li>
    <li><strong>Conservación:</strong> Promover acciones de conservación de páramos a nivel individual, institucional y gubernamental</li>
    <li><strong>Investigación aplicada:</strong> Facilitar el estudio de métodos numéricos aplicados a ecosistemas de alta montaña</li>
</ul>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sección de metodología
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Metodología y Métodos Numéricos</h2>", unsafe_allow_html=True)

st.markdown("<div class='methodology-box'>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
La aplicación utiliza una combinación de métodos numéricos avanzados y modelos matemáticos para simular el impacto 
de la disminución de poblaciones de frailejones en los páramos colombianos. Los métodos implementados incluyen:
</p>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<h3>🔢 Métodos Numéricos Implementados</h3>", unsafe_allow_html=True)
st.markdown("""
<ol>
    <li><strong>Ecuaciones Diferenciales Ordinarias (EDO):</strong> 
        <ul>
            <li>Modelo de dinámicas poblacionales de frailejones</li>
            <li>Simulación de interacciones ecológicas en páramos</li>
            <li>Método de Runge-Kutta para resolver sistemas de EDO</li>
        </ul>
    </li>
    <li><strong>Modelos de Regresión No Lineal:</strong>
        <ul>
            <li>Funciones sigmoidales para modelar respuestas ecosistémicas</li>
            <li>Análisis de sensibilidad paramétrica</li>
            <li>Calibración con datos empíricos de páramos</li>
        </ul>
    </li>
    <li><strong>Interpolación y Aproximación:</strong>
        <ul>
            <li>Interpolación espacial para mapas de riesgo</li>
            <li>Aproximación de funciones de servicios ecosistémicos</li>
            <li>Métodos de elementos finitos para modelado espacial</li>
        </ul>
    </li>
    <li><strong>Análisis de Sistemas Dinámicos:</strong>
        <ul>
            <li>Modelado de retroalimentación ecosistémica</li>
            <li>Análisis de estabilidad de puntos de equilibrio</li>
            <li>Simulación de escenarios de cambio climático</li>
        </ul>
    </li>
</ol>
""", unsafe_allow_html=True)

st.markdown("<h3>📊 Fuentes de Datos Científicos</h3>", unsafe_allow_html=True)
st.markdown("""
<ul>
    <li><strong>Instituto Alexander von Humboldt:</strong> Datos de biodiversidad y distribución de frailejones en Colombia</li>
    <li><strong>IDEAM:</strong> Información meteorológica y climática de páramos</li>
    <li><strong>Sistema Nacional de Áreas Protegidas (SINAP):</strong> Datos sobre estado de conservación de páramos</li>
    <li><strong>Universidad Nacional de Colombia:</strong> Investigaciones sobre ecología de frailejones</li>
    <li><strong>IPCC (2021):</strong> Modelos de cambio climático para ecosistemas de alta montaña</li>
    <li><strong>Fundación ProAves:</strong> Monitoreo de biodiversidad en páramos</li>
</ul>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sección técnica
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Aspectos Técnicos y Desarrollo</h2>", unsafe_allow_html=True)

st.markdown("<h3>⚙️ Arquitectura del Sistema</h3>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
El proyecto está desarrollado siguiendo principios de programación científica y buenas prácticas de desarrollo:
</p>

<ul>
    <li><strong>Modularidad:</strong> Separación clara entre modelos matemáticos, visualizaciones y datos</li>
    <li><strong>Escalabilidad:</strong> Diseño que permite agregar nuevos páramos y variables ecosistémicas</li>
    <li><strong>Reproducibilidad:</strong> Código documentado y versionado para garantizar resultados consistentes</li>
    <li><strong>Interactividad:</strong> Interfaz intuitiva que permite explorar diferentes escenarios</li>
</ul>

<h3>🛠️ Herramientas y Tecnologías</h3>
<ul>
    <li><strong>Python:</strong> Lenguaje principal para cálculos científicos y modelado</li>
    <li><strong>NumPy/SciPy:</strong> Bibliotecas para métodos numéricos y computación científica</li>
    <li><strong>Pandas:</strong> Análisis y manipulación de datos ecosistémicos</li>
    <li><strong>Streamlit:</strong> Framework para desarrollo de aplicaciones web científicas</li>
    <li><strong>Plotly:</strong> Visualizaciones interactivas 2D y 3D</li>
    <li><strong>Folium:</strong> Mapas interactivos con datos geoespaciales</li>
    <li><strong>JSON:</strong> Almacenamiento estructurado de datos de páramos</li>
</ul>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sección educativa
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Contexto Educativo - Universidad Central</h2>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
Este proyecto forma parte del curso de <strong>Métodos Numéricos</strong> de la Universidad Central, 
segundo semestre de 2025, donde se aplican conceptos teóricos a problemas reales de conservación ambiental.
</p>

<h3>🎓 Competencias Desarrolladas</h3>
<ul>
    <li><strong>Modelado matemático:</strong> Traducción de problemas ecológicos a ecuaciones matemáticas</li>
    <li><strong>Programación científica:</strong> Implementación de algoritmos numéricos en Python</li>
    <li><strong>Análisis de datos:</strong> Procesamiento y visualización de información ambiental</li>
    <li><strong>Pensamiento sistémico:</strong> Comprensión de interacciones complejas en ecosistemas</li>
    <li><strong>Comunicación científica:</strong> Presentación clara de resultados complejos</li>
</ul>

<h3>🌍 Impacto Social y Ambiental</h3>
<p class='description'>
El proyecto demuestra cómo las matemáticas y la programación pueden contribuir a la solución de problemas 
ambientales críticos, conectando el aprendizaje académico con la realidad nacional y la urgencia de 
conservar los páramos colombianos.
</p>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sección de créditos
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Créditos y Reconocimientos</h2>", unsafe_allow_html=True)
st.markdown("""
<h3>🏛️ Instituciones Colaboradoras</h3>
<ul>
    <li><strong>Universidad Central:</strong> Facultad de Ingeniería - Programa de Métodos Numéricos</li>
    <li><strong>Instituto Humboldt:</strong> Datos de biodiversidad y ecosistemas de páramo</li>
    <li><strong>IDEAM:</strong> Información meteorológica y climática</li>
    <li><strong>Ministerio de Ambiente y Desarrollo Sostenible:</strong> Políticas de conservación de páramos</li>
</ul>

<h3>📚 Referencias Científicas Principales</h3>
<ul>
    <li>Luteyn, J.L. (1999). Páramos: A checklist of plant diversity, geographical distribution, and botanical literature</li>
    <li>Rangel-Ch, J.O. (2000). Colombia Diversidad Biótica III: La región de vida paramuna</li>
    <li>Hofstede, R. et al. (2003). Los páramos del mundo: proyecto Atlas Mundial de los Páramos</li>
    <li>Buytaert, W. et al. (2006). Human impact on the hydrology of the Andean páramos</li>
    <li>Young, K.R. et al. (2002). Plant evolution and endemism in Andean South America</li>
</ul>

<h3>💻 Tecnologías Open Source</h3>
<ul>
    <li><strong>Python Scientific Stack:</strong> NumPy, SciPy, Pandas, Matplotlib</li>
    <li><strong>Streamlit:</strong> Framework de aplicaciones web para ciencia de datos</li>
    <li><strong>Plotly:</strong> Biblioteca de visualización interactiva</li>
    <li><strong>Folium:</strong> Biblioteca de mapas interactivos basada en Leaflet.js</li>
    <li><strong>OpenStreetMap:</strong> Datos cartográficos colaborativos</li>
</ul>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Footer actualizado
st.markdown("""
<div style="background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%); color: white; text-align: center; padding: 20px; border-radius: 10px; margin-top: 20px;">
<h3 style="color: white !important; margin-bottom: 10px;">🌿 Conservación de Frailejones en Colombia</h3>
<p style="color: white !important; margin: 0; font-size: 1.1rem;">Universidad Central - Facultad de Ingeniería</p>
<p style="color: white !important; margin: 0; font-size: 1rem;">Métodos Numéricos | Segundo Semestre 2025</p>
<p style="color: white !important; margin-top: 10px; font-size: 0.9rem;">
"Los páramos son fábricas de agua que no se pueden replicar" - Instituto Humboldt
</p>
<p style="color: white !important; margin-top: 5px; font-size: 0.8rem;">
Proyecto desarrollado para la conservación de ecosistemas de alta montaña en Colombia
</p>
</div>
""", unsafe_allow_html=True)

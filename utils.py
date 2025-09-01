
import streamlit as st

def get_emoji(category):
    """
    Get relevant emoji for the application.
    
    Parameters:
    -----------
    category : str
        Category of emoji needed
        
    Returns:
    --------
    str
        Appropriate emoji
    """
    emoji_map = {
        'frailejon': '🌿',
        'paramo': '🏔️',
        'water': '💧',
        'biodiversity': '🌱',
        'climate': '🌡️',
        'warning': '⚠️',
        'success': '✅',
        'research': '🔬',
        'university': '🎓',
        'colombia': '🇨🇴'
    }
    
    return emoji_map.get(category, '🌿')

def add_vertical_space(lines=1):
    """
    Add vertical space to the app.
    
    Parameters:
    -----------
    lines : int
        Number of lines of vertical space
    """
    for _ in range(lines):
        st.write("")

def format_number(number, suffix=""):
    """
    Format large numbers with appropriate suffixes.
    
    Parameters:
    -----------
    number : float/int
        Number to format
    suffix : str
        Additional suffix to add
        
    Returns:
    --------
    str
        Formatted number string
    """
    if number >= 1000000:
        return f"{number/1000000:.1f}M {suffix}".strip()
    elif number >= 1000:
        return f"{number/1000:.1f}K {suffix}".strip()
    else:
        return f"{number:.1f} {suffix}".strip()

def get_risk_level_color(risk_percentage):
    """
    Get color based on risk level.
    
    Parameters:
    -----------
    risk_percentage : float
        Risk percentage (0-100)
        
    Returns:
    --------
    str
        Color code
    """
    if risk_percentage <= 30:
        return '#4CAF50'  # Green - low risk
    elif risk_percentage <= 60:
        return '#FF9800'  # Orange - medium risk
    else:
        return '#F44336'  # Red - high risk

def calculate_paramo_health_score(frailejon_percentage, water_regulation, biodiversity):
    """
    Calculate overall páramo health score.
    
    Parameters:
    -----------
    frailejon_percentage : float
        Frailejón population percentage
    water_regulation : float
        Water regulation capacity percentage
    biodiversity : float
        Biodiversity index percentage
        
    Returns:
    --------
    dict
        Health score and category
    """
    # Weighted average with frailejones having highest weight
    health_score = (
        frailejon_percentage * 0.4 + 
        water_regulation * 0.35 + 
        biodiversity * 0.25
    )
    
    if health_score >= 80:
        category = "Excelente"
        color = "#4CAF50"
    elif health_score >= 60:
        category = "Buena"
        color = "#8BC34A"
    elif health_score >= 40:
        category = "Regular"
        color = "#FF9800"
    elif health_score >= 20:
        category = "Mala"
        color = "#FF5722"
    else:
        category = "Crítica"
        color = "#F44336"
    
    return {
        "score": health_score,
        "category": category,
        "color": color
    }

def get_conservation_recommendations(frailejon_percentage):
    """
    Get conservation recommendations based on frailejón population level.
    
    Parameters:
    -----------
    frailejon_percentage : float
        Current frailejón population percentage
        
    Returns:
    --------
    list
        List of recommendations
    """
    if frailejon_percentage >= 80:
        return [
            "Mantener programas de monitoreo continuo",
            "Fortalecer medidas de protección existentes",
            "Desarrollar investigación sobre resistencia al cambio climático",
            "Promover turismo ecológico sostenible"
        ]
    elif frailejon_percentage >= 60:
        return [
            "Implementar programas de restauración ecológica",
            "Controlar actividades humanas en zonas de páramo",
            "Establecer corredores biológicos",
            "Fortalecer educación ambiental en comunidades locales"
        ]
    elif frailejon_percentage >= 40:
        return [
            "Implementar medidas de restauración urgentes",
            "Prohibir actividades extractivas en páramos",
            "Establecer zonas de protección estricta",
            "Desarrollar programas de propagación ex-situ"
        ]
    else:
        return [
            "Declarar emergencia ecológica para páramos afectados",
            "Implementar programas de restauración intensiva",
            "Establecer vedas totales para actividades humanas",
            "Desarrollar bancos de germoplasma para especies críticas",
            "Implementar programas de reintroducción de especies"
        ]


import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from models import calculate_crop_production, calculate_biodiversity_impact

def plot_frailejon_crop_relationship_3d(current_frailejon_percentage, years=10):
    """
    Create a 3D interactive visualization showing the relationship between
    frailejón population, time, and ecosystem services.
    
    Parameters:
    -----------
    current_frailejon_percentage : float
        Current frailejón population percentage to highlight
    years : int
        Number of years to simulate
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive 3D plot
    """
    # Generate frailejón population range
    frailejon_range = np.linspace(0, 100, 40)
    
    # Generate time range
    time_range = np.linspace(0, years, 20)
    
    # Create meshgrid
    frailejon_grid, time_grid = np.meshgrid(frailejon_range, time_range)
    
    # Initialize ecosystem services grid
    services_grid = np.zeros_like(frailejon_grid)
    
    # Calculate ecosystem services for each point with time decay
    for i in range(frailejon_grid.shape[0]):
        for j in range(frailejon_grid.shape[1]):
            frailejon_val = frailejon_grid[i, j]
            time_val = time_grid[i, j]
            
            # Base ecosystem services based on current frailejón population
            base_services = calculate_crop_production(frailejon_val)
            
            # Apply time effect - long-term decline if frailejón population is low
            time_factor = 1.0
            if frailejon_val < 50:
                # Calculate decline over time for frailejones (they grow very slowly)
                time_factor = max(0.3, 1.0 - (time_val / years) * (0.15 * (50 - frailejon_val) / 50))
            
            services_grid[i, j] = base_services * time_factor
    
    # Create 3D surface plot
    fig = go.Figure()
    
    # Add surface with green colorscale for frailejones
    fig.add_trace(go.Surface(
        x=frailejon_grid,
        y=time_grid,
        z=services_grid,
        colorscale=[[0, '#8B4513'], [0.3, '#CD853F'], [0.6, '#90EE90'], [0.8, '#228B22'], [1, '#006400']],
        colorbar=dict(
            title=dict(
                text="Servicios Ecosistémicos (%)",
                side="right"
            )
        ),
        lighting=dict(
            ambient=0.7,
            diffuse=0.8,
            roughness=0.5,
            specular=0.6,
            fresnel=0.8
        ),
        contours={
            "z": {"show": True, "start": 20, "end": 100, "size": 10, "color":"white"}
        }
    ))
    
    # Add marker for current position
    fig.add_trace(go.Scatter3d(
        x=[current_frailejon_percentage], 
        y=[0], 
        z=[calculate_crop_production(current_frailejon_percentage)],
        mode='markers',
        marker=dict(
            size=10,
            color='red',
            symbol='circle'
        ),
        name='Situación Actual'
    ))
    
    # Update layout
    fig.update_layout(
        title='Proyección 3D: Relación entre Población de Frailejones, Tiempo y Servicios Ecosistémicos',
        scene=dict(
            xaxis_title='Población de Frailejones (%)',
            yaxis_title='Años',
            zaxis_title='Servicios Ecosistémicos (%)',
            xaxis=dict(gridcolor="white", gridwidth=2),
            yaxis=dict(gridcolor="white", gridwidth=2),
            zaxis=dict(gridcolor="white", gridwidth=2),
            bgcolor='#f8fffe'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor='#ffffff',
        font=dict(color='#2d5016'),
        autosize=True,
        height=600
    )
    
    return fig

def plot_frailejon_crop_relationship(current_frailejon_percentage):
    """
    Create an interactive plot showing the relationship between
    frailejón population and ecosystem services.
    
    Parameters:
    -----------
    current_frailejon_percentage : float
        Current frailejón population percentage to highlight
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive plot
    """
    # Generate data points
    frailejon_percentages = np.arange(0, 101, 1)
    ecosystem_services = [calculate_crop_production(p) for p in frailejon_percentages]
    
    # Create figure
    fig = go.Figure()
    
    # Add line with green color for frailejones
    fig.add_trace(go.Scatter(
        x=frailejon_percentages,
        y=ecosystem_services,
        mode='lines',
        name='Servicios Ecosistémicos',
        line=dict(color='#4CAF50', width=3),
        hovertemplate='<b>Frailejones:</b> %{x}%<br><b>Servicios:</b> %{y:.1f}%<extra></extra>'
    ))
    
    # Add point for current value
    current_service = calculate_crop_production(current_frailejon_percentage)
    fig.add_trace(go.Scatter(
        x=[current_frailejon_percentage],
        y=[current_service],
        mode='markers',
        name='Nivel actual',
        marker=dict(color='#FF5722', size=12, symbol='circle'),
        hovertemplate='<b>Actual:</b> %{x}% frailejones<br><b>Servicios:</b> %{y:.1f}%<extra></extra>'
    ))
    
    # Add threshold lines and areas for frailejones
    fig.add_shape(
        type="line",
        x0=30, y0=0, x1=30, y1=100,
        line=dict(color="red", width=2, dash="dash"),
    )
    
    # Add annotations for threshold explanation
    fig.add_annotation(
        x=20, y=35,
        text="Zona crítica<br>para páramos",
        showarrow=False,
        font=dict(color="red", size=10),
        align="center"
    )
    
    fig.add_annotation(
        x=75, y=15,
        text="Frailejones: plantas<br>clave de páramo",
        showarrow=True,
        font=dict(color="#2d5016", size=10),
        align="center",
        arrowcolor="#4CAF50"
    )
    
    # Add title and axis labels
    fig.update_layout(
        title="Relación entre Población de Frailejones y Servicios Ecosistémicos del Páramo",
        xaxis_title="Población de Frailejones (%)",
        yaxis_title="Servicios Ecosistémicos (%)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        shapes=[
            # Add rectangle for critical zone
            dict(
                type="rect",
                xref="x",
                yref="y",
                x0=0,
                y0=0,
                x1=30,
                y1=100,
                fillcolor="rgba(255, 0, 0, 0.1)",
                line_width=0,
                layer="below"
            ),
            # Add rectangle for warning zone
            dict(
                type="rect",
                xref="x",
                yref="y",
                x0=30,
                y0=0,
                x1=60,
                y1=100,
                fillcolor="rgba(255, 165, 0, 0.1)",
                line_width=0,
                layer="below"
            ),
            # Add rectangle for optimal zone
            dict(
                type="rect",
                xref="x",
                yref="y",
                x0=60,
                y0=0,
                x1=100,
                y1=100,
                fillcolor="rgba(76, 175, 80, 0.1)",
                line_width=0,
                layer="below"
            )
        ]
    )
    
    # Update axes
    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 105])
    
    return fig

def plot_biodiversity_impact_3d(frailejon_percentage, ecosystem_resilience):
    """
    Create a 3D interactive plot showing biodiversity impact based on
    frailejón population percentage and páramo ecosystem resilience.
    
    Parameters:
    -----------
    frailejon_percentage : float
        Frailejón population percentage
    ecosystem_resilience : float
        Páramo ecosystem resilience factor
        
    Returns:
    --------
    plotly.graph_objects.Figure
        3D interactive plot
    """
    # Generate a grid of x-y points
    frailejon_range = np.linspace(10, 100, 30)
    resilience_range = np.linspace(0.2, 1.0, 30)
    frailejon_grid, resilience_grid = np.meshgrid(frailejon_range, resilience_range)
    
    # Calculate biodiversity for each point on the grid
    biodiversity_values = np.zeros_like(frailejon_grid)
    for i in range(frailejon_grid.shape[0]):
        for j in range(frailejon_grid.shape[1]):
            biodiversity_values[i, j] = calculate_biodiversity_impact(
                frailejon_grid[i, j], resilience_grid[i, j]
            )
    
    # Create the 3D surface plot with green colorscale
    fig = go.Figure(data=[
        go.Surface(
            x=frailejon_grid, 
            y=resilience_grid, 
            z=biodiversity_values,
            colorscale=[[0, '#8B4513'], [0.3, '#CD853F'], [0.6, '#90EE90'], [0.8, '#228B22'], [1, '#006400']],
            colorbar=dict(
                title=dict(
                    text="Biodiversidad del Páramo (%)",
                    side="right"
                )
            )
        )
    ])
    
    # Highlight the current point
    fig.add_trace(
        go.Scatter3d(
            x=[frailejon_percentage],
            y=[ecosystem_resilience],
            z=[calculate_biodiversity_impact(frailejon_percentage, ecosystem_resilience)],
            mode='markers',
            marker=dict(
                size=8,
                color='red',
            ),
            name='Situación Actual'
        )
    )
    
    # Update layout
    fig.update_layout(
        title='Modelo 3D de Impacto en Biodiversidad de Páramos',
        scene=dict(
            xaxis_title='Población de Frailejones (%)',
            yaxis_title='Resiliencia del Páramo',
            zaxis_title='Biodiversidad (%)',
            xaxis=dict(gridcolor="white", gridwidth=2),
            yaxis=dict(gridcolor="white", gridwidth=2),
            zaxis=dict(gridcolor="white", gridwidth=2),
            bgcolor='#f8fffe'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor='#ffffff',
        font=dict(color='#2d5016'),
        autosize=True,
        height=500
    )
    
    return fig

def plot_biodiversity_impact(frailejon_percentage, ecosystem_resilience):
    """
    Create an interactive plot showing the impact on different páramo ecosystems
    based on frailejón population percentage.
    
    Parameters:
    -----------
    frailejon_percentage : float
        Frailejón population percentage
    ecosystem_resilience : float
        Páramo ecosystem resilience factor
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive plot
    """
    # Define páramo ecosystem types with different resilience modifiers
    paramo_types = [
        "Páramo seco", 
        "Páramo húmedo", 
        "Superpáramo",
        "Páramo azonal",
        "Páramo de frailejones",
        "Páramo arbustivo"
    ]
    
    # Different resilience modifiers for each páramo type
    resilience_modifiers = [0.8, 1.2, 0.6, 0.9, 1.4, 1.0]
    
    # Calculate biodiversity impact for each páramo type
    biodiversity_impacts = []
    for modifier in resilience_modifiers:
        # Adjust resilience based on páramo type, but keep within 0-1 range
        adjusted_resilience = min(1.0, max(0.0, ecosystem_resilience * modifier))
        impact = calculate_biodiversity_impact(frailejon_percentage, adjusted_resilience)
        biodiversity_impacts.append(impact)
    
    # Create color scale based on impact values (green theme)
    colors = []
    for impact in biodiversity_impacts:
        if impact >= 80:
            colors.append('#2E7D32')  # Dark green
        elif impact >= 60:
            colors.append('#4CAF50')  # Green
        elif impact >= 40:
            colors.append('#8BC34A')  # Light green
        elif impact >= 20:
            colors.append('#FFC107')  # Yellow
        else:
            colors.append('#F44336')  # Red
    
    # Create figure
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        x=paramo_types,
        y=biodiversity_impacts,
        marker_color=colors,
        text=[f"{impact:.1f}%" for impact in biodiversity_impacts],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Biodiversidad: %{y:.1f}%<extra></extra>'
    ))
    
    # Add reference line for current average
    avg_impact = sum(biodiversity_impacts) / len(biodiversity_impacts)
    fig.add_shape(
        type="line",
        x0=-0.5, y0=avg_impact, x1=len(paramo_types)-0.5, y1=avg_impact,
        line=dict(color="#2d5016", width=2, dash="dash"),
    )
    
    # Add annotation for average
    fig.add_annotation(
        x=len(paramo_types)-1,
        y=avg_impact + 3,
        text=f"Promedio: {avg_impact:.1f}%",
        showarrow=False,
        font=dict(color="#2d5016"),
    )
    
    # Update layout
    fig.update_layout(
        title=f"Impacto en la Biodiversidad por Tipo de Páramo",
        xaxis_title="Tipo de Páramo",
        yaxis_title="Biodiversidad Remanente (%)",
        template="plotly_white",
        yaxis=dict(range=[0, 105]),
        font=dict(color='#2d5016')
    )
    
    return fig

def plot_timeseries_forecast(ecosystem_data):
    """
    Create a time series forecast plot based on páramo ecosystem simulation data.
    
    Parameters:
    -----------
    ecosystem_data : pd.DataFrame
        Data frame with simulation results
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive plot
    """
    # Create figure
    fig = go.Figure()
    
    # Add lines for each variable with green color scheme
    fig.add_trace(go.Scatter(
        x=ecosystem_data['time'],
        y=ecosystem_data['biodiversity'],
        mode='lines',
        name='Biodiversidad del páramo',
        line=dict(color='#2E7D32', width=3),
        hovertemplate='Año %{x:.1f}<br>Biodiversidad: %{y:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=ecosystem_data['time'],
        y=ecosystem_data['water_regulation'],
        mode='lines',
        name='Regulación hídrica',
        line=dict(color='#1976D2', width=3),
        hovertemplate='Año %{x:.1f}<br>Regulación hídrica: %{y:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=ecosystem_data['time'],
        y=ecosystem_data['endemic_plants'],
        mode='lines',
        name='Plantas endémicas',
        line=dict(color='#388E3C', width=3),
        hovertemplate='Año %{x:.1f}<br>Plantas endémicas: %{y:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=ecosystem_data['time'],
        y=ecosystem_data['frailejon_population'],
        mode='lines',
        name='Población de frailejones',
        line=dict(color='#FF6F00', width=3, dash='dash'),
        hovertemplate='Año %{x:.1f}<br>Frailejones: %{y:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=ecosystem_data['time'],
        y=ecosystem_data['soil_carbon'],
        mode='lines',
        name='Carbono del suelo',
        line=dict(color='#5D4037', width=3, dash='dot'),
        hovertemplate='Año %{x:.1f}<br>Carbono suelo: %{y:.1f}%<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title="Proyección Temporal del Ecosistema de Páramo",
        xaxis_title="Años",
        yaxis_title="Porcentaje del nivel óptimo (%)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(color='#2d5016')
    )
    
    # Add annotations for important thresholds
    # Find if biodiversity crosses below 50%
    if any(ecosystem_data['biodiversity'] < 50):
        # Get first time it crosses below 50%
        crossing_time = ecosystem_data.loc[ecosystem_data['biodiversity'] < 50, 'time'].iloc[0]
        
        fig.add_shape(
            type="line",
            x0=crossing_time, y0=0, x1=crossing_time, y1=100,
            line=dict(color="red", width=2, dash="dash"),
        )
        
        fig.add_annotation(
            x=crossing_time,
            y=20,
            text="Punto crítico de biodiversidad del páramo",
            showarrow=True,
            arrowhead=1,
            font=dict(color="red")
        )
    
    return fig

def create_risk_map(frailejon_percentage):
    """
    Create an interactive map showing páramos at risk due to frailejón loss in Colombia.
    
    Parameters:
    -----------
    frailejon_percentage : float
        Current frailejón population percentage
        
    Returns:
    --------
    folium.Map
        Interactive map
    """
    # Create a base map centered on Colombia's páramos
    m = folium.Map(location=[5.5, -73.5], zoom_start=6, tiles='CartoDB positron')
    
    # Import regions data from data module
    from data.regions import get_frailejon_regions
    colombia_paramos = get_frailejon_regions()
    
    # Adjust risk based on current frailejón population
    # Lower frailejón population = higher risk
    risk_multiplier = max(0.1, (100 - frailejon_percentage) / 100 * 2)
    
    # Add markers for each páramo
    for paramo in colombia_paramos:
        name = paramo["name"]
        lat = paramo["lat"]
        lon = paramo["lon"]
        risk_level = paramo["risk"]
        frailejon_density = paramo["frailejon_density"]
        area = paramo["area"]
        altitude = paramo["altitude"]
        ecosystem_services = paramo["ecosystem_services"]
        description = paramo["description"]
        
        # Determine color based on risk level
        if risk_level == "Crítico":
            color = 'darkred'
        elif risk_level == "Alto":
            color = 'red'
        elif risk_level == "Medio":
            color = 'orange'
        else:
            color = 'green'
            
        # Create tooltip and popup content
        tooltip = f"{name} - Riesgo: {risk_level}"
        popup_content = f"""
        <div style="width: 280px">
            <h4>🌿 {name}</h4>
            <p><strong>Nivel de riesgo:</strong> {risk_level}</p>
            <p><strong>Densidad de frailejones:</strong> {frailejon_density}%</p>
            <p><strong>Área del páramo:</strong> {area} km²</p>
            <p><strong>Altitud promedio:</strong> {altitude} msnm</p>
            <p><strong>Servicios ecosistémicos:</strong> {ecosystem_services}</p>
            <p><strong>Estado actual:</strong> {description}</p>
        </div>
        """
        
        # Add marker with popup
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=320),
            tooltip=tooltip,
            icon=folium.Icon(color=color, icon='tree', prefix='fa')
        ).add_to(m)
        
        # Add circle with radius proportional to risk and frailejón density
        adjusted_risk = min(1.0, (frailejon_density/100) * risk_multiplier)
        folium.Circle(
            radius=adjusted_risk * 25000,  # Scale for visibility
            location=[lat, lon],
            color=color,
            fill=True,
            fill_opacity=0.3,
            opacity=0.7,
            weight=2
        ).add_to(m)
    
    # Add legend as HTML
    legend_html = '''
    <div style="position: fixed; 
        bottom: 50px; left: 10px; width: 200px; height: 140px; 
        border:2px solid grey; z-index:9999; background-color:white;
        padding: 10px;
        font-size: 14px;
        border-radius: 5px;
        ">
        <p><strong>🌿 Nivel de Riesgo en Páramos</strong></p>
        <p style="margin:0; color: darkred;">■ Crítico: Pérdida severa</p>
        <p style="margin:0; color: red;">■ Alto: Alta vulnerabilidad</p>
        <p style="margin:0; color: orange;">■ Medio: Riesgo moderado</p>
        <p style="margin:0; color: green;">■ Bajo: Estado conservado</p>
    </div>
    '''
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add title
    title_html = '''
    <div style="position: fixed; 
        top: 10px; left: 50px; width: 350px;
        z-index:9999; background-color:white;
        padding: 15px;
        font-size: 16px;
        opacity: 0.95;
        border-radius: 10px;
        border: 2px solid #4caf50;
        ">
        <p><strong>🌿 Páramos en Riesgo por Pérdida de Frailejones - Colombia</strong></p>
        <p style="font-size: 12px; margin: 5px 0 0 0; color: #666;">
        Ecosistemas críticos para la regulación hídrica nacional
        </p>
    </div>
    '''
    
    m.get_root().html.add_child(folium.Element(title_html))
    
    return m

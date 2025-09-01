
import numpy as np
import pandas as pd
from scipy.integrate import odeint

def calculate_biodiversity_impact(frailejon_percentage, ecosystem_resilience):
    """
    Calculate the impact on biodiversity based on frailejón population percentage
    and páramo ecosystem resilience.
    
    Parameters:
    -----------
    frailejon_percentage : float
        Percentage of frailejón population (0-100)
    ecosystem_resilience : float
        Páramo ecosystem resilience factor (0-1)
        
    Returns:
    --------
    float
        Biodiversity index (0-100)
    """
    # Base model: biodiversity in páramos declines non-linearly with frailejón population
    # The decline is mitigated by ecosystem resilience
    
    # Calculate normalized frailejón population (0-1)
    frailejon_norm = frailejon_percentage / 100
    
    # Parameters for sigmoid function (more sensitive for páramos)
    k = 6  # Higher steepness for páramo ecosystems
    mid_point = 0.4  # Lower inflection point due to frailejón importance
    
    # Apply sigmoid function to model non-linear relationship
    # Higher resilience helps but páramos are inherently fragile
    adjusted_frailejon = frailejon_norm + (ecosystem_resilience * 0.25)
    
    # Sigmoid function to model how biodiversity responds to frailejón population
    biodiversity_factor = 1 / (1 + np.exp(-k * (adjusted_frailejon - mid_point)))
    
    # Scale to 0-100
    biodiversity_index = biodiversity_factor * 100
    
    # Biodiversity can't exceed 100%
    return min(biodiversity_index, 100)

def calculate_crop_production(frailejon_percentage):
    """
    Calculate the impact on ecosystem services (water regulation) based on frailejón population.
    
    Parameters:
    -----------
    frailejon_percentage : float
        Percentage of frailejón population (0-100)
        
    Returns:
    --------
    float
        Ecosystem services index (0-100), primarily water regulation
    """
    # Frailejones are critical for water regulation in páramos
    # Their loss has immediate and severe impacts
    
    # Normalize frailejón population (0-1)
    frailejon_norm = frailejon_percentage / 100
    
    # Water regulation capacity based on frailejón population
    if frailejon_norm >= 0.9:
        # Optimal water regulation
        water_regulation_factor = 1.0
    elif frailejon_norm >= 0.7:
        # Good water regulation with some reduction
        water_regulation_factor = 0.85 + ((frailejon_norm - 0.7) / 0.2) * 0.15
    elif frailejon_norm >= 0.5:
        # Moderate water regulation
        water_regulation_factor = 0.6 + ((frailejon_norm - 0.5) / 0.2) * 0.25
    elif frailejon_norm >= 0.3:
        # Severely compromised water regulation
        water_regulation_factor = 0.3 + ((frailejon_norm - 0.3) / 0.2) * 0.3
    else:
        # Critical collapse of water regulation
        water_regulation_factor = frailejon_norm / 0.3 * 0.3
    
    # Scale to percentage
    return water_regulation_factor * 100

def create_ecosystem_simulation(frailejon_percentage, years, ecosystem_resilience):
    """
    Simulate páramo ecosystem changes over time based on frailejón population.
    
    Parameters:
    -----------
    frailejon_percentage : float
        Percentage of frailejón population (0-100)
    years : int
        Number of years to simulate
    ecosystem_resilience : float
        Páramo ecosystem resilience factor (0-1)
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with simulation results for páramo ecosystem
    """
    # Initialize time points (in years)
    t = np.linspace(0, years, years * 12)  # Monthly intervals
    
    # Normalize frailejón population
    frailejon_norm = frailejon_percentage / 100
    
    # Initial conditions for páramo ecosystem
    # [biodiversity, water_regulation, endemic_plants, frailejon_population, soil_carbon]
    initial_state = [1.0, 1.0, 1.0, frailejon_norm, 1.0]
    
    # Define the system of differential equations for páramo ecosystem
    def paramo_ecosystem_model(y, t, resilience):
        biodiversity, water_regulation, endemic_plants, frailejon_pop, soil_carbon = y
        
        # Parameters specific to páramo ecosystems
        alpha = 0.08  # Rate of biodiversity decline due to frailejón loss (higher than general ecosystems)
        beta = 0.12   # Rate of water regulation decline due to frailejón loss (very sensitive)
        gamma = 0.06  # Rate of endemic plant decline due to frailejón loss
        delta = 0.04  # Rate of soil carbon loss due to frailejón loss
        epsilon = 0.05 # Feedback rate from biodiversity to ecosystem health
        
        # Climate change additional stress factor
        climate_stress = 0.01 * (t / years)  # Increasing stress over time
        
        # Differential equations for páramo ecosystem
        dbio_dt = -alpha * (1 - frailejon_pop) * biodiversity - climate_stress * biodiversity + (resilience * 0.015 * (1 - biodiversity))
        dwater_dt = -beta * (1 - frailejon_pop) * water_regulation - climate_stress * water_regulation
        dplants_dt = -gamma * (1 - frailejon_pop) * endemic_plants - climate_stress * endemic_plants
        dfrailejon_dt = -0.02 * climate_stress * frailejon_pop  # Slow decline due to climate change
        dcarbon_dt = -delta * (1 - frailejon_pop) * soil_carbon - climate_stress * soil_carbon
        
        return [dbio_dt, dwater_dt, dplants_dt, dfrailejon_dt, dcarbon_dt]
    
    # Solve ODE system
    solution = odeint(paramo_ecosystem_model, initial_state, t, args=(ecosystem_resilience,))
    
    # Extract solutions
    biodiversity = solution[:, 0]
    water_regulation = solution[:, 1]
    endemic_plants = solution[:, 2]
    frailejon_population = solution[:, 3]
    soil_carbon = solution[:, 4]
    
    # Create DataFrame
    df = pd.DataFrame({
        'time': t,
        'biodiversity': np.maximum(0, biodiversity * 100),  # Prevent negative values
        'water_regulation': np.maximum(0, water_regulation * 100),
        'endemic_plants': np.maximum(0, endemic_plants * 100),
        'frailejon_population': np.maximum(0, frailejon_population * 100),
        'soil_carbon': np.maximum(0, soil_carbon * 100)
    })
    
    return df

def calculate_economic_impact(frailejon_percentage, region="Colombia"):
    """
    Calculate economic impact of frailejón loss in terms of ecosystem services.
    
    Parameters:
    -----------
    frailejon_percentage : float
        Percentage of frailejón population (0-100)
    region : str
        Region name for specific calculations
        
    Returns:
    --------
    dict
        Economic impact metrics
    """
    # Base economic values for ecosystem services (millions USD per year)
    base_values = {
        "water_regulation": 5200,
        "carbon_sequestration": 850,
        "biodiversity_conservation": 1200,
        "tourism": 400
    }
    
    # Regional modifiers
    regional_multipliers = {
        "Páramo de Chingaza": 0.35,
        "Páramo de Sumapaz": 0.25,
        "Páramo de Santurbán": 0.20,
        "Todos los páramos": 1.0
    }
    
    multiplier = regional_multipliers.get(region, 1.0)
    
    # Calculate losses based on frailejón population decline
    frailejon_loss = max(0, 100 - frailejon_percentage) / 100
    
    economic_losses = {}
    for service, base_value in base_values.items():
        # Different services have different sensitivities to frailejón loss
        if service == "water_regulation":
            sensitivity = 0.9  # Very high sensitivity
        elif service == "carbon_sequestration":
            sensitivity = 0.7  # High sensitivity
        elif service == "biodiversity_conservation":
            sensitivity = 0.8  # High sensitivity
        else:
            sensitivity = 0.5  # Moderate sensitivity
            
        loss = base_value * multiplier * frailejón_loss * sensitivity
        economic_losses[service] = loss
    
    return economic_losses

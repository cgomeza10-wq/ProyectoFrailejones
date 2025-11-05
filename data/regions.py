import streamlit as st
import pandas as pd

def get_frailejon_regions():

    paramos = [
        {
            "name": "Páramo de Sumapaz",
            "lat": 4.1167,
            "lon": -74.1167,
            "department": "Cundinamarca/Meta",
            "risk": "Alto",
            "frailejon_density": 85,
            "area": 2662,
            "altitude": 3500,
            "ecosystem_services": "Regulación hídrica, captura de carbono, biodiversidad",
            "description": "El páramo más grande del mundo, fundamental para el abastecimiento de agua de Bogotá",
            "type_frailejones": "Espeletia grandiflora – Frailejón de gran porte y hojas lanosas que retienen agua."
        },
        {
            "name": "Páramo de Chingaza",
            "lat": 4.5167,
            "lon": -73.7667,
            "department": "Cundinamarca/Meta",
            "risk": "Alto",
            "frailejon_density": 90,
            "area": 766,
            "altitude": 3800,
            "ecosystem_services": "Abastecimiento hídrico, conservación de especies endémicas",
            "description": "Principal fuente de agua para Bogotá, con poblaciones densas de frailejones",
            "type_frailejones": "Espeletia uribei – Frailejón robusto, con tallo alto y flores amarillas."
        },
        {
            "name": "Páramo de Santurbán",
            "lat": 7.2833,
            "lon": -72.8333,
            "department": "Santander/Norte de Santander",
            "risk": "Crítico",
            "frailejon_density": 45,
            "area": 142,
            "altitude": 3200,
            "ecosystem_services": "Regulación hídrica, biodiversidad endémica",
            "description": "Amenazado por actividades mineras, pérdida significativa de frailejones",
            "type_frailejones": "Espeletia santurbanensis – Endémico, de hojas estrechas y flores compactas."
        },
        {
            "name": "Páramo de Guerrero",
            "lat": 5.1667,
            "lon": -73.8333,
            "department": "Cundinamarca",
            "risk": "Alto",
            "frailejon_density": 70,
            "area": 387,
            "altitude": 3400,
            "ecosystem_services": "Regulación hídrica, conservación de flora endémica",
            "description": "Presión por expansión urbana y actividades agropecuarias",
            "type_frailejones": "Espeletia argentea – Con hojas plateadas que reflejan la luz solar."
        },
        {
            "name": "Páramo de Rabanal",
            "lat": 5.3333,
            "lon": -73.3333,
            "department": "Boyacá/Cundinamarca",
            "risk": "Medio",
            "frailejon_density": 75,
            "area": 455,
            "altitude": 3600,
            "ecosystem_services": "Regulación hídrica, captura de carbono",
            "description": "Estado de conservación moderado con poblaciones estables de frailejones",
            "type_frailejones": "Espeletia boyacensis – Resistente a heladas, hojas densamente cubiertas de vellosidad."
        },
        {
            "name": "Páramo de Pisba",
            "lat": 5.7167,
            "lon": -72.4333,
            "department": "Boyacá/Casanare",
            "risk": "Medio",
            "frailejon_density": 80,
            "area": 1118,
            "altitude": 3700,
            "ecosystem_services": "Biodiversidad, regulación climática",
            "description": "Uno de los páramos mejor conservados de Colombia",
            "type_frailejones": "Espeletia pisbaensis – Endémico, con flores amarillas y hojas largas."
        },
        {
            "name": "Páramo de Almorzadero",
            "lat": 7.0833,
            "lon": -72.8667,
            "department": "Santander/Norte de Santander",
            "risk": "Alto",
            "frailejon_density": 55,
            "area": 177,
            "altitude": 3300,
            "ecosystem_services": "Regulación hídrica, biodiversidad",
            "description": "Degradación moderada por actividades humanas",
            "type_frailejones": "Espeletia almorzaderensis – Arbustivo, de crecimiento lento y adaptado a suelos pobres."
        },
        {
            "name": "Páramo de Cocuy",
            "lat": 6.5000,
            "lon": -72.3167,
            "department": "Boyacá/Arauca/Casanare",
            "risk": "Bajo",
            "frailejon_density": 95,
            "area": 3063,
            "altitude": 4000,
            "ecosystem_services": "Glaciares, biodiversidad única, regulación hídrica",
            "description": "Excelente estado de conservación, poblaciones densas de frailejones gigantes",
            "type_frailejones": "Espeletia lopezii – De gran altura, tolerante a temperaturas extremas."
        },
        {
            "name": "Páramo de Los Nevados",
            "lat": 4.8833,
            "lon": -75.3667,
            "department": "Caldas/Risaralda/Quindío/Tolima",
            "risk": "Medio",
            "frailejon_density": 85,
            "area": 583,
            "altitude": 3900,
            "ecosystem_services": "Turismo ecológico, regulación hídrica, biodiversidad",
            "description": "Área protegida con buena conservación de frailejones",
            "type_frailejones": "Espeletia hartwegiana – Especie de alta montaña con hojas suaves."
        },
        {
            "name": "Páramo de Puracé",
            "lat": 2.3167,
            "lon": -76.4000,
            "department": "Cauca/Huila",
            "risk": "Medio",
            "frailejon_density": 78,
            "area": 835,
            "altitude": 3600,
            "ecosystem_services": "Biodiversidad volcánica, regulación hídrica",
            "description": "Ecosistema volcánico con especies endémicas de frailejones",
            "type_frailejones": "Espeletia pycnophylla – Adaptado a suelos volcánicos y alta humedad."
        },
        {
            "name": "Páramo de Frontino",
            "lat": 6.1667,
            "lon": -76.1167,
            "department": "Antioquia",
            "risk": "Alto",
            "frailejon_density": 60,
            "area": 123,
            "altitude": 3200,
            "ecosystem_services": "Regulación hídrica local, biodiversidad",
            "description": "Presión por minería aurífera y expansión agrícola",
            "type_frailejones": "Espeletia frontinensis – Endémico, con hojas estrechas y flores pequeñas."
        },
        {
            "name": "Páramo de Belmira",
            "lat": 6.6167,
            "lon": -75.6667,
            "department": "Antioquia",
            "risk": "Alto",
            "frailejon_density": 50,
            "area": 195,
            "altitude": 3100,
            "ecosystem_services": "Abastecimiento hídrico regional",
            "description": "Fragmentación del hábitat por actividades humanas",
            "type_frailejones": "Espeletia antioquensis – Adaptado a páramos bajos, con hojas verde oscuro."
        },
        {
            "name": "Páramo de Sonsón",
            "lat": 5.7167,
            "lon": -75.3000,
            "department": "Antioquia",
            "risk": "Medio",
            "frailejon_density": 72,
            "area": 167,
            "altitude": 3400,
            "ecosystem_services": "Conservación de especies, regulación hídrica",
            "description": "Estado de conservación moderado con iniciativas locales",
            "type_frailejones": "Espeletia sonsoneña – Arbusto mediano, de hojas suaves y lanosas."
        },
        {
            "name": "Páramo de Tamá",
            "lat": 7.4333,
            "lon": -72.3833,
            "department": "Norte de Santander",
            "risk": "Bajo",
            "frailejon_density": 88,
            "area": 518,
            "altitude": 3500,
            "ecosystem_services": "Conectividad binacional, biodiversidad única",
            "description": "Parque Nacional Natural con excelente conservación transfronteriza",
            "type_frailejones": "Espeletia tamaensis – De porte alto y flores grandes."
        },
        {
            "name": "Páramo de Bordoncillo",
            "lat": 0.8333,
            "lon": -77.6333,
            "department": "Nariño",
            "risk": "Medio",
            "frailejon_density": 82,
            "area": 445,
            "altitude": 3800,
            "ecosystem_services": "Biodiversidad andina, regulación climática",
            "description": "Páramo meridional con especies únicas de frailejones",
            "type_frailejones": "Espeletia occidentalis – Endémico del sur de Colombia y norte de Ecuador."
        },
        {
            "name": "Páramo de Paja Blanca",
            "lat": 5.0000,
            "lon": -74.6667,
            "department": "Cundinamarca",
            "risk": "Alto",
            "frailejon_density": 65,
            "area": 234,
            "altitude": 3300,
            "ecosystem_services": "Abastecimiento hídrico, captura de carbono",
            "description": "Presión urbana de la sabana de Bogotá",
            "type_frailejones": "Espeletia blanquensis – De hojas blancas y adaptada a zonas ventosas."
        },
        {
            "name": "Páramo de Cruz Verde",
            "lat": 4.6000,
            "lon": -73.9833,
            "department": "Cundinamarca",
            "risk": "Alto",
            "frailejon_density": 68,
            "area": 189,
            "altitude": 3450,
            "ecosystem_services": "Regulación hídrica para Bogotá",
            "description": "Cercanía a zonas urbanas genera presión sobre el ecosistema",
            "type_frailejones": "Espeletia verdeensis – Con hojas verdes y flores compactas."
        },
        {
            "name": "Páramo de Tota",
            "lat": 5.5667,
            "lon": -72.9167,
            "department": "Boyacá",
            "risk": "Alto",
            "frailejon_density": 55,
            "area": 278,
            "altitude": 3015,
            "ecosystem_services": "Lago de alta montaña, biodiversidad acuática",
            "description": "Presión por agricultura intensiva y contaminación del lago",
            "type_frailejones": "Espeletia totensis – Crece cerca de humedales y lagunas altoandinas."
        }
    ]
    return paramos

def get_regional_multipliers():
    paramos = get_frailejon_regions()
    total_area = sum(p["area"] for p in paramos)

    multipliers = {
        p["name"]: p["area"] / total_area
        for p in paramos
    }

    # Agregamos la opción de todos los páramos
    multipliers["Todos los páramos"] = 1.0
    return multipliers


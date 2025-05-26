import pandas as pd

# Coordenadas aproximadas del centroide de cada departamento de Colombia
departamentos = [
    ("Amazonas", -1.4429, -71.5724),
    ("Antioquia", 6.2442, -75.5812),
    ("Arauca", 6.5489, -71.0022),
    ("Atlántico", 10.9685, -74.7813),
    ("Bolívar", 9.2315, -74.7335),
    ("Boyacá", 5.4545, -73.3620),
    ("Caldas", 5.2983, -75.2479),
    ("Caquetá", 0.8699, -73.8419),
    ("Casanare", 5.7589, -71.5721),
    ("Cauca", 2.7085, -76.7819),
    ("Cesar", 9.3373, -73.6536),
    ("Chocó", 5.2528, -76.6612),
    ("Córdoba", 8.7490, -75.8785),
    ("Cundinamarca", 4.6811, -74.0937),
    ("Guainía", 2.5854, -68.5247),
    ("Guaviare", 2.0439, -72.3311),
    ("Huila", 2.5359, -75.5277),
    ("La Guajira", 11.3548, -72.5203),
    ("Magdalena", 10.4113, -74.4057),
    ("Meta", 3.9686, -73.9120),
    ("Nariño", 1.2896, -77.3579),
    ("Norte de Santander", 7.9073, -72.5046),
    ("Putumayo", 0.4350, -76.6354),
    ("Quindío", 4.4610, -75.6674),
    ("Risaralda", 5.3158, -75.9928),
    ("San Andrés", 12.5847, -81.7006),
    ("Santander", 7.1193, -73.1227),
    ("Sucre", 9.3041, -75.3978),
    ("Tolima", 4.4389, -75.2322),
    ("Valle del Cauca", 3.4372, -76.5225),
    ("Vaupés", 0.8550, -70.8110),
    ("Vichada", 4.4234, -69.2878)
]

df_deptos = pd.DataFrame(departamentos, columns=["departamento", "lat", "lon"])
import ace_tools as tools; tools.display_dataframe_to_user(name="Coordenadas Departamentos Colombia", dataframe=df_deptos)


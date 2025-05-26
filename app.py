import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import plotly.express as px

# Cargar modelo preentrenado en formato .h5
modelo = load_model("modelo_red_neuronal.h5")

# Columnas usadas por el modelo
columnas_utiles = [
    'periodo', 'edad', 'estu_nacionalidad', 'estu_depto_reside',
    'estu_mcpio_reside', 'fami_estratovivienda', 'fami_tieneautomovil',
    'fami_tienecomputador', 'fami_tieneinternet', 'fami_tienelavadora',
    'punt_global', 'cole_bilingue'
]

# Cargar datos de estudiantes
df_estudiantes = pd.read_excel("datos_utiles.xlsx")
df_elegibles = df_estudiantes[df_estudiantes["es_elegible_beca"] == 1]
df_por_depto = df_elegibles.groupby("estu_depto_reside").size().reset_index(name="n_eligibles")

# Cargar coordenadas de departamentos
df_geo = pd.read_csv("coordenadas_departamentos.csv")
df_mapa = df_por_depto.merge(df_geo, left_on="estu_depto_reside", right_on="departamento", how="left")

# Crear aplicación
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Predicción de elegibilidad para beca"),

    html.Div([
        html.Label("Periodo:"),
        dcc.Input(id='periodo', type='text', value='20241'),

        html.Label("Edad:"),
        dcc.Input(id='edad', type='number', min=10, max=100),

        html.Label("Nacionalidad:"),
        dcc.Input(id='nacionalidad', type='text'),

        html.Label("Departamento de residencia:"),
        dcc.Input(id='departamento', type='text'),

        html.Label("Municipio de residencia:"),
        dcc.Input(id='municipio', type='text'),

        html.Label("Estrato (1 a 6):"),
        dcc.Input(id='estrato', type='number', min=1, max=6),

        html.Label("¿Tiene automóvil? (0 = No, 1 = Sí):"),
        dcc.Input(id='automovil', type='number', min=0, max=1),

        html.Label("¿Tiene computador? (0 = No, 1 = Sí):"),
        dcc.Input(id='computador', type='number', min=0, max=1),

        html.Label("¿Tiene internet? (0 = No, 1 = Sí):"),
        dcc.Input(id='internet', type='number', min=0, max=1),

        html.Label("¿Tiene lavadora? (0 = No, 1 = Sí):"),
        dcc.Input(id='lavadora', type='number', min=0, max=1),

        html.Label("Puntaje global ICFES:"),
        dcc.Input(id='puntaje', type='number', min=0, max=500),

        html.Label("¿Colegio bilingüe? (0 = No, 1 = Sí):"),
        dcc.Input(id='bilingue', type='number', min=0, max=1),

        html.Br(),
        html.Button("Predecir", id="boton-predecir", n_clicks=0),
        html.Div(id="salida-prediccion", style={"marginTop": "20px", "fontWeight": "bold", "fontSize": "18px"})
    ], style={"maxWidth": "500px", "margin": "auto"}),

    html.Hr(),
    html.H2("Mapa de estudiantes elegibles por departamento"),
    dcc.Graph(
        id="mapa-elegibles",
        figure=px.scatter_mapbox(
            df_mapa,
            lat="lat",
            lon="lon",
            size="n_eligibles",
            hover_name="departamento",
            hover_data={"n_eligibles": True, "lat": False, "lon": False},
            zoom=4,
            color_discrete_sequence=["blue"],
            height=600
        ).update_layout(
            mapbox_style="carto-positron",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
    )
])

@app.callback(
    Output("salida-prediccion", "children"),
    Input("boton-predecir", "n_clicks"),
    State("periodo", "value"),
    State("edad", "value"),
    State("nacionalidad", "value"),
    State("departamento", "value"),
    State("municipio", "value"),
    State("estrato", "value"),
    State("automovil", "value"),
    State("computador", "value"),
    State("internet", "value"),
    State("lavadora", "value"),
    State("puntaje", "value"),
    State("bilingue", "value")
)
def predecir(n_clicks, periodo, edad, nacionalidad, depto, municipio,
             estrato, automovil, computador, internet, lavadora,
             puntaje, bilingue):

    if n_clicks == 0:
        return ""

    try:
        datos = pd.DataFrame([[
            periodo, edad, nacionalidad, depto, municipio,
            estrato, automovil, computador, internet, lavadora,
            puntaje, bilingue
        ]], columns=columnas_utiles)

        entrada = datos.to_numpy()
        proba = modelo.predict(entrada)[0][0]
        return f"✅ Probabilidad estimada de ser elegible para beca: {proba*100:.2f}%"
    except Exception as e:
        return f"❌ Error al predecir: {e}"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)


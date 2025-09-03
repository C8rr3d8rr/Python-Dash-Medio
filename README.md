# Python-Dash-Intermedio

## Dashboard

<img width="963" height="392" alt="Captura de pantalla 2025-09-03 141522" src="https://github.com/user-attachments/assets/415cfe09-51f4-4e5f-87d0-3dd34c1c7df2" />


## **Objetivo**
* Construir un dashboard con python con la biblioteca de Dash.

## **Descripción**
* Este código lee un archivo xlxs, para que por medio de codigo de python cree un Dashboard. 

## **Qué voy a Aprender?** 
Al final del laboratorio seremos capaces de:
* Descargar las bibliotecas necesarias para crear un dashboard con python
* Crear un bloque de codigo con la bilioteca Dash
* Leer archivos mediante pandas 

## **Servicios de AWS a Utilizar**
* [VSC]    (https://code.visualstudio.com/)
* [Pandas] (https://pandas.pydata.org/)
* [DASH]   (https://dash.plotly.com/)

## **Explicación del Código**
A continuación voy a explicar detalladamente el código del archivo Python_Dash

## 1. Importación de librerías
```
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
```
* dash → base de la librería para crear dashboards.
* dcc (Dash Core Components) → componentes como dropdowns, sliders y gráficos.
* html → permite crear títulos, divisores, contenedores (Div).
* Input / Output → necesarios para los callbacks (interactividad).
* plotly.express → gráficos interactivos.
* pandas → para manejar los datos del archivo Excel.

## 2. Cargar los datos desde Excel
```
df = pd.read_excel(r"C:\Users\99dcorredorm\OneDrive - Sonova\Desktop\Prueba_dash.xlsx")
```
* Lee el archivo Excel y lo guarda en un DataFrame (df).
* Se asume que tiene columnas: Mes, Ventas, Costos, Categoria.

## 3. Inicializar la aplicación
```
app = dash.Dash(__name__)
```
* Se crea la aplicación Dash.
* Es como decir: "a partir de aquí empieza mi dashboard".
  
## 4. Definir el Layout
```
app.layout = html.Div(
    style={"backgroundColor": "#111111", "padding": "20px"},
    children=[
        html.H1("📊 Dashboard Intermedio con Filtros", style={...}),

        # Dropdown de filtro
        html.Div([
            html.Label("Selecciona una Categoría:", style={"color": "white", "fontWeight": "bold"}),
            dcc.Dropdown(
                id="filtro_categoria",
                options=[{"label": cat, "value": cat} for cat in df["Categoria"].unique()],
                value=df["Categoria"].unique()[0],
                style={"color": "black"}
            )
        ], style={"width": "50%", "margin": "auto"}),

        # Gráficos
        html.Div([
            html.Div([
                html.H3("📈 Ventas vs Costos (Filtradas por Categoría)", style={...}),
                dcc.Graph(id="grafico_lineas")
            ], style={"width": "48%", "display": "inline-block"}),

            html.Div([
                html.H3("📊 Ventas por Mes", style={...}),
                dcc.Graph(id="grafico_barras")
            ], style={"width": "48%", "display": "inline-block"})
        ])
    ]
)
```
* Título principal (H1) → centrado, blanco, negrita, subrayado.
* Dropdown (dcc.Dropdown) → permite seleccionar una Categoría del Excel.
* options → se llena automáticamente con los valores únicos de la columna Categoria.
* value → toma como valor inicial la primera categoría.
* Dos gráficos (dcc.Graph):
* Uno de líneas para Ventas vs Costos.
* Uno de barras para Ventas por mes.
* Estilos → el fondo es oscuro, títulos blancos, gráficos en dos columnas (50% cada uno).

## 5. Callback (interactividad)
```
@app.callback(
    [Output("grafico_lineas", "figure"),
     Output("grafico_barras", "figure")],
    [Input("filtro_categoria", "value")]
)
def actualizar_graficos(categoria):
    df_filtrado = df[df["Categoria"] == categoria]

    fig_line = px.line(
        df_filtrado,
        x="Mes",
        y=["Ventas", "Costos"],
        title=f"Ventas vs Costos - {categoria}"
    )

    fig_bar = px.bar(
        df_filtrado,
        x="Mes",
        y="Ventas",
        title=f"Ventas por Mes - {categoria}",
        color="Mes"
    )

    return fig_line, fig_bar
```
@app.callback → conecta entradas (Inputs) y salidas (Outputs).
* Input("filtro_categoria", "value") → escucha los cambios en el dropdown.
* Output("grafico_lineas", "figure") y Output("grafico_barras", "figure") → actualizan los gráficos dinámicamente.
* Dentro de la función:
     * Se filtran los datos según la categoría elegida (df_filtrado).
     * Se crea un gráfico de líneas (Ventas vs Costos).
     * Se crea un gráfico de barras (Ventas por mes).
     * Se devuelven ambos gráficos.
Así, cuando el usuario selecciona otra categoría, ambos gráficos cambian automáticamente. 🎯


## 6. Ejecutar el servidor
```
if __name__ == "__main__":
    app.run(debug=True)
```
* Arranca el servidor de Dash.
* Se abre en el navegador en http://127.0.0.1:8050/.
* Con debug=True → el servidor se recarga solo cada vez que guardas cambios.


🎯 Diferencias con el Dashboard Básico

✅ En el básico → solo mostrabas gráficos fijos.
✅ En el intermedio → ahora hay filtros interactivos, y los gráficos cambian según lo que el usuario seleccione.




# ============================
# Dashboard Avanzado con Dash
# ============================
# pip install dash plotly pandas openpyxl

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Paso 1: Cargar datos
df = pd.read_excel(r"C:\Users\99dcorredorm\OneDrive - Sonova\Desktop\Prueba_dash.xlsx")

# Paso 2: Inicializar la app
app = dash.Dash(__name__)
app.title = "Dashboard Avanzado"

# Paso 3: Layout con Tabs
app.layout = html.Div(style={"backgroundColor": "#111111", "padding": "20px"}, children=[
    html.H1("📊 Dashboard Avanzado con Dash",
            style={"textAlign": "center",
                   "fontWeight": "bold",
                   "textDecoration": "underline",
                   "color": "white"}),

    # Tabs
    dcc.Tabs(
        id="tabs",
        value="tab_kpi",
        children=[
            dcc.Tab(label="📌 KPIs", value="tab_kpi", style={"color": "black"}),
            dcc.Tab(label="📈 Gráficos", value="tab_graficos", style={"color": "black"}),
            dcc.Tab(label="📊 Distribución", value="tab_pie", style={"color": "black"})
        ]
    ),

    html.Div(id="contenido_tabs")  # Aquí se cargará el contenido dinámico
])

# Paso 4: Callbacks para cambiar contenido según la pestaña
@app.callback(
    Output("contenido_tabs", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "tab_kpi":
        # ======== TAB KPIs ========
        total_ventas = df["Ventas"].sum()
        total_costos = df["Costos"].sum()
        utilidad = total_ventas - total_costos

        return html.Div([
            html.H2("📌 Indicadores Clave",
                    style={"textAlign": "center",
                           "color": "white",
                           "textDecoration": "underline"}),
            html.Div([
                html.Div([
                    html.H3("💰 Ventas Totales", style={"color": "white"}),
                    html.H4(f"${total_ventas:,.0f}", style={"color": "lime", "fontWeight": "bold"})
                ], style={"backgroundColor": "#222", "padding": "20px", "margin": "10px", "borderRadius": "10px",
                          "width": "30%", "display": "inline-block", "textAlign": "center"}),

                html.Div([
                    html.H3("📉 Costos Totales", style={"color": "white"}),
                    html.H4(f"${total_costos:,.0f}", style={"color": "red", "fontWeight": "bold"})
                ], style={"backgroundColor": "#222", "padding": "20px", "margin": "10px", "borderRadius": "10px",
                          "width": "30%", "display": "inline-block", "textAlign": "center"}),

                html.Div([
                    html.H3("📊 Utilidad", style={"color": "white"}),
                    html.H4(f"${utilidad:,.0f}", style={"color": "cyan", "fontWeight": "bold"})
                ], style={"backgroundColor": "#222", "padding": "20px", "margin": "10px", "borderRadius": "10px",
                          "width": "30%", "display": "inline-block", "textAlign": "center"})
            ])
        ])

    elif tab == "tab_graficos":
        # ======== TAB GRÁFICOS ========
        return html.Div([
            html.H2("📈 Análisis de Ventas y Costos",
                    style={"textAlign": "center", "color": "white", "textDecoration": "underline"}),

            html.Label("Selecciona una Categoría:", style={"color": "white", "fontWeight": "bold"}),
            dcc.Dropdown(
                id="filtro_categoria",
                options=[{"label": cat, "value": cat} for cat in df["Categoria"].unique()],
                value=df["Categoria"].unique()[0],
                style={"color": "black"}
            ),

            html.Div([
                dcc.Graph(id="grafico_lineas"),
                dcc.Graph(id="grafico_barras")
            ])
        ])

    elif tab == "tab_pie":
        # ======== TAB DISTRIBUCIÓN ========
        fig_pie = px.pie(df, names="Categoria", values="Ventas",
                         title="Distribución de Ventas por Categoría")
        return html.Div([
            html.H2("📊 Distribución de Categorías",
                    style={"textAlign": "center", "color": "white", "textDecoration": "underline"}),
            dcc.Graph(figure=fig_pie)
        ])

# Paso 5: Callback para los gráficos en Tab "Gráficos"
@app.callback(
    [Output("grafico_lineas", "figure"),
     Output("grafico_barras", "figure")],
    Input("filtro_categoria", "value"),
    prevent_initial_call=True
)
def actualizar_graficos(categoria):
    df_filtrado = df[df["Categoria"] == categoria]

    fig_line = px.line(df_filtrado, x="Mes", y=["Ventas", "Costos"],
                       title=f"Ventas vs Costos - {categoria}")
    fig_bar = px.bar(df_filtrado, x="Mes", y="Ventas",
                     title=f"Ventas por Mes - {categoria}", color="Mes")

    return fig_line, fig_bar

# Paso 6: Correr servidor
if __name__ == "__main__":
    app.run(debug=True)

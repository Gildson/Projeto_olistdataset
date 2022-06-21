import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

olist_dataset = pd.read_csv('my_dataset.csv')

df = olist_dataset['seller_state'].value_counts().sort_values(ascending=False)
df1 = olist_dataset.groupby('seller_state').price.sum().sort_values(ascending=False)
df2 = olist_dataset.groupby('seller_state').price.min().sort_values(ascending=False)
df3 = olist_dataset.groupby('seller_state').price.max().sort_values(ascending=False)
df4 = olist_dataset.groupby('seller_state').price.mean().sort_values(ascending=False)
df5 = olist_dataset.groupby('seller_state').freight_value.sum().sort_values(ascending=False)
df6 = olist_dataset.groupby('seller_state').freight_value.mean().sort_values(ascending=False)

df7 = pd.merge(df, df1, on=df.index)
df8 = pd.merge(df7, df2, left_on='key_0', right_on='seller_state')
df9 = pd.merge(df8, df3, left_on='key_0', right_on='seller_state')
df10 = pd.merge(df9, df4, left_on='key_0', right_on='seller_state')
df11 = pd.merge(df10, df5, left_on='key_0', right_on='seller_state')
df12 = pd.merge(df11, df6, left_on='key_0', right_on='seller_state')
df12.set_axis(['Estado', 'Quantidade', 'Preço_total', 'Preço_min', 'Preço_max',
               'Preço_médio', 'Frete_total', 'Frete_médio'], axis='columns', inplace=True)

select_columns = {"Quantidade": "Quantidade",
                "Preço_médio": "Preço médio",
                "Frete_médio": "Frete médio"}

brazil_states = json.load(open("brazil_geo.json", "r"))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig = px.choropleth_mapbox(df12, locations="Estado", color="Quantidade",
                            center={"lat": -16.95, "lon": -47.78}, zoom=3,
                            geojson=brazil_states, color_continuous_scale="Redor",
                            opacity=0.4, hover_data={"Preço_total":True, "Preço_min": True, "Preço_max": True,
                            "Preço_médio": True, "Frete_total": True, "Frete_médio": True, "Estado": True})
fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)

fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Bar(x=df12["Estado"], y=df12["Quantidade"]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
)
app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col([
                    html.Div([
                        html.Img(id="logo", src=app.get_asset_url("logo_dark.png"), height=50),
                        html.H5(children="Brazilian E-Commerce Public Dataset by Olist"),
                    ], style={"background-color": "#1E1E1E", "margin": "-25px", "padding": "25px"}),
                    html.Div(
                            className="div-for-dropdown",
                            id="div-test",
                            children=[
                                dcc.Dropdown(['RR','AP','AM','PA','AC','RO',
                                            'TO','MA','PI','CE','RN','PB',
                                            'PE','AL','SE','BA','MT','DF',
                                            'GO','MS','MG','ES','RJ','SP',
                                            'PR','SC','RS'], 'RN', id='dropdown-state')
                            ],
                        ),

                    dbc.Row([
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Quantidade", className="card-text"),
                                    html.H3(style={"color": "#adfc92"}, id="quantidade-text"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Preço total", className="card-text"),
                                    html.H3(style={"color": "#adfc92"}, id="preco_total-text"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Frete total", className="card-text"),
                                    html.H3(style={"color": "#adfc92"}, id="frete_total-text"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                    ]),

                    html.Div([
                        html.P("Selecione que tipo de dado deseja visualizar:", style={"margin-top": "25px"}),
                        dcc.Dropdown(
                                        id="location-dropdown",
                                        options=[{"label": j, "value": i}
                                            for i, j in select_columns.items()
                                        ],
                                        value="Quantidade",
                                        style={"margin-top": "10px"}
                                    ),
                        dcc.Graph(id="line-graph", figure=fig2, style={
                            "background-color": "#242424",
                            }),
                        ], id="teste")
                ], md=5, style={
                          "padding": "25px",
                          "background-color": "#242424"
                          }), 

            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[dcc.Graph(id="choropleth-map", figure=fig, 
                            style={'height': '1000px', 'margin-right': '10px'})],
                    ),
                ], md=7),
            ])
    ], fluid=True, 
)
@app.callback(
    [
        Output("quantidade-text", "children"),
        Output("preco_total-text", "children"),
        Output("frete_total-text", "children"),
    ],
    [Input("dropdown-state", "value")]
)
def display_status(value):
    quant = df12.Quantidade[df12.Estado == value]
    price = df12.Preço_total[df12.Estado == value].round(2)
    frete = df12.Frete_total[df12.Estado == value].round(2)
    return(quant, price, frete)

@app.callback(
        Output("line-graph", "figure"),
        [Input("location-dropdown", "value")]
)
def plot_line_graph(plot_type):
    for plot_type in select_columns:
        fig2.add_trace(go.Scatter(x=df12.Estado, y=df12[plot_type]))
    
    fig2.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
        )
    return fig2

if __name__ == "__main__":
    app.run_server(debug=True)

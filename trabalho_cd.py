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

#Criar dataframe com analise das vendas
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

#Criar dataframe com análise das compras
df20 = olist_dataset['customer_state'].value_counts().sort_values(ascending=False)
df21 = olist_dataset.groupby('customer_state').price.sum().sort_values(ascending=False)
df22 = olist_dataset.groupby('customer_state').price.min().sort_values(ascending=False)
df23 = olist_dataset.groupby('customer_state').price.max().sort_values(ascending=False)
df24 = olist_dataset.groupby('customer_state').price.mean().sort_values(ascending=False)
df25 = olist_dataset.groupby('customer_state').freight_value.sum().sort_values(ascending=False)
df26 = olist_dataset.groupby('customer_state').freight_value.mean().sort_values(ascending=False)

df27 = pd.merge(df20, df21, on=df20.index)
df28 = pd.merge(df27, df22, left_on='key_0', right_on='customer_state')
df29 = pd.merge(df28, df23, left_on='key_0', right_on='customer_state')
df30 = pd.merge(df29, df24, left_on='key_0', right_on='customer_state')
df31 = pd.merge(df30, df25, left_on='key_0', right_on='customer_state')
df32 = pd.merge(df31, df26, left_on='key_0', right_on='customer_state')

df32.set_axis(['Estado', 'Quantidade', 'Preço_total', 'Preço_min', 'Preço_max',
               'Preço_médio', 'Frete_total', 'Frete_médio'], axis='columns', inplace=True)

select_columns_compras = {"Quantidade": "Quantidade",
                "Preço_total": "Preço total",
                "Frete_total": "Frete total"}

df_vt = olist_dataset.groupby('seller_state').payment_type.value_counts().sort_values(ascending=False)
df_ct = olist_dataset.groupby('customer_state').payment_type.value_counts().sort_values(ascending=False)
resultado = pd.concat([df_vt, df_ct], axis=1, join='outer')
resultado.fillna(value=0, inplace=True)
resultado.columns = ['Vendas', 'Compras']
resultado.rename_axis(index=["Estado", "Metodo"], inplace=True)
pd_test = pd.MultiIndex.to_frame(resultado.index)
result = pd.concat([resultado, pd_test], axis=1, join='outer')
result.set_axis(['Vendas', 'Compras', 'Estados', 'Metodos'], axis='columns', inplace=True)
compras = result.groupby(['Metodos','Estados']).Compras.sum()
vendas = result.groupby(['Metodos', 'Estados']).Vendas.sum()
df_geral = pd.merge(compras, vendas, left_index=True, right_index=True)

select_estado_pie ={"RR": "RR","AP": "AP","AM": "AM","PA": "PA","AC": 'AC','RO': 'RO',
                    'TO': 'TO','MA':'MA','PI':'PI','CE':'CE','RN':'RN','PB':'PB',
                    'PE': 'PE','AL': 'AL','SE': 'SE','BA': 'BA','MT':'MT','DF':'DF',
                    'GO':'GO','MS':'MS','MG':'MG','ES':'ES','RJ':'RJ',"SP":"SP",
                    'PR':'PR','SC':'SC','RS':'RS'}
                                            
#Criar dados geojson dos estados brasileiros
brazil_states = json.load(open("brazil_geo.json", "r"))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

colorscale = [
[0, 'rgb(38, 53, 113)'], 
[0.5, 'rgb(100, 127, 225)'],
[1, 'rgb(234, 32, 41)']
]
#Criando mapa da análise das vendas
fig = px.choropleth_mapbox(df12, locations="Estado", color="Quantidade",
                            center={"lat": -15.95, "lon": -46.78}, zoom=3,
                            geojson=brazil_states, color_continuous_scale=colorscale,
                            opacity=0.4, hover_data={"Preço_total":True, "Preço_min": True, "Preço_max": True,
                            "Preço_médio": True, "Frete_total": True, "Frete_médio": True, "Estado": True})
fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)

#Criando mapa da análise das compras
fig_compras = px.choropleth_mapbox(df32, locations="Estado", color="Quantidade",
                            center={"lat": -16.95, "lon": -47.78}, zoom=3,
                            geojson=brazil_states, color_continuous_scale=colorscale,
                            opacity=0.4, hover_data={"Preço_total":True, "Preço_min": True, "Preço_max": True,
                            "Preço_médio": True, "Frete_total": True, "Frete_médio": True, "Estado": True})

fig_compras.update_layout(
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

fig2_compras = go.Figure(layout={"template": "plotly_dark"})
fig2_compras.add_trace(go.Bar(x=df32["Estado"], y=df32["Quantidade"]))
fig2_compras.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
)

fig2_pie = go.Figure(layout={"template": "plotly_dark"})
fig2_pie.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
)

#Criando o dashboard
app.layout = dbc.Container(
    children=[
        html.Div([
            html.H3(children="Brazilian E-Commerce Public Dataset by Olist"),
        ], style={"background-color": "#1E1E1E", "margin": "25px", "padding": "25px"}),
        html.Div([
            html.H2(children="Análise das vendas por estado"),
        ], style={"background-color": "#1E1E1E", "margin": "25px", "padding": "25px"}),

        dbc.Row([
            dbc.Col([
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
                                    html.H5("R$", style={"color": "#adfc92"}),
                                    html.H5(style={"color": "#adfc92"}, id="preco_total-text"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Frete total", className="card-text"),
                                    html.H5("R$", style={"color": "#adfc92"}),
                                    html.H5(style={"color": "#adfc92"}, id="frete_total-text"),
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

                    ], id="teste"),
                    html.Div([
                        html.P("Selecione que tipo de dado deseja visualizar:", style={"margin-top": "25px"}),
                        dcc.Dropdown(
                                        id="location-dropdown-pie",
                                        options=[{"label": j, "value": i}
                                            for i, j in select_estado_pie.items()
                                        ],
                                        value="SP",
                                        multi=False,
                                        clearable=False,
                                        style={"margin-top": "10px"}
                                    ),
                        dcc.Graph(id="pie-graph", style={
                            "background-color": "#242424",
                            }),

                    ], id="teste1")
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
                            style={'height': '1400px', 'margin-right': '10px'})],
                    ),
                ], md=7),
            ]),

        html.Div([
            html.H2(children="Análise das compras por estado"),
        ], style={"background-color": "#1E1E1E", "margin": "25px", "padding": "25px"}),

        dbc.Row([
            dbc.Col([
                    html.Div(
                            className="div-for-dropdown",
                            id="div-test-compras",
                            children=[
                                dcc.Dropdown(['RR','AP','AM','PA','AC','RO',
                                            'TO','MA','PI','CE','RN','PB',
                                            'PE','AL','SE','BA','MT','DF',
                                            'GO','MS','MG','ES','RJ','SP',
                                            'PR','SC','RS'], 'RN', id='dropdown-state-compras')
                            ],
                        ),

                    dbc.Row([
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Quantidade", className="card-text"),
                                    html.H3(style={"color": "#adfc92"}, id="quantidade-text-compras"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Preço total", className="card-text"),
                                    html.H5("R$", style={"color": "#adfc92"}),
                                    html.H5(style={"color": "#adfc92"}, id="preco_total-text-compras"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Frete total", className="card-text"),
                                    html.H5("R$", style={"color": "#adfc92"}),
                                    html.H5(style={"color": "#adfc92"}, id="frete_total-text-compras"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                    ]),

                    html.Div([
                        html.P("Selecione que tipo de dado deseja visualizar:", style={"margin-top": "25px"}),
                        dcc.Dropdown(
                                        id="location-dropdown-compras",
                                        options=[{"label": j, "value": i}
                                            for i, j in select_columns_compras.items()
                                        ],
                                        value="Quantidade",
                                        style={"margin-top": "10px"}
                                    ),
                        dcc.Graph(id="line-graph-compras", figure=fig2_compras, style={
                            "background-color": "#242424",
                            }),
                        ], id="teste-compras"),
                    html.Div([
                        html.P("Selecione que tipo de dado deseja visualizar:", style={"margin-top": "25px"}),
                        dcc.Dropdown(
                                        id="location-dropdown-pie_compras",
                                        options=[{"label": j, "value": i}
                                            for i, j in select_estado_pie.items()
                                        ],
                                        value="SP",
                                        multi=False,
                                        clearable=False,
                                        style={"margin-top": "10px"}
                                    ),
                        dcc.Graph(id="pie-graph-compras", style={
                            "background-color": "#242424",
                            }),
                    ], id="teste2")
                ], md=5, style={
                          "padding": "25px",
                          "background-color": "#242424"
                          }), 

            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-1-compras",
                        type="default",
                        children=[dcc.Graph(id="choropleth-map-compras", figure=fig_compras, 
                            style={'height': '1400px', 'margin-right': '10px'})],
                    ),
                ], md=7),
            ])
    ], fluid=True, 
)

#vendas
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

#compras
@app.callback(
    [
        Output("quantidade-text-compras", "children"),
        Output("preco_total-text-compras", "children"),
        Output("frete_total-text-compras", "children"),
    ],
    [Input("dropdown-state-compras", "value")]
)
def display_status(value):
    quant = df32.Quantidade[df32.Estado == value]
    price = df32.Preço_total[df32.Estado == value].round(2)
    frete = df32.Frete_total[df32.Estado == value].round(2)
    return(quant, price, frete)

#gráfico interativo pie vendas
@app.callback(
        Output("pie-graph", "figure"),
        [Input("location-dropdown-pie", "value")]
)
def update_graph(dropdown_state):
    df_estado = df_geral.xs(dropdown_state, level="Estados")
    piechart = px.pie(df_estado, values=df_estado.Vendas, names=df_estado.index, hole=.3,)
    
    piechart.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
        )
    return (piechart)

#gráfico interativo pie compras
@app.callback(
        Output("pie-graph-compras", "figure"),
        [Input("location-dropdown-pie_compras", "value")]
)
def update_graph(dropdown_state_compras):
    df_estado = df_geral.xs(dropdown_state_compras, level="Estados")
    piechart_compras = px.pie(df_estado, values=df_estado.Compras, names=df_estado.index, hole=.3,)
    
    piechart_compras.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
        )
    return (piechart_compras)

#vendas
@app.callback(
        Output("line-graph", "figure"),
        [Input("location-dropdown", "value")]
)
def plot_line_graph(plot_type):
    fig2 = px.histogram(x=df12.Estado, y=df12[plot_type])
    
    fig2.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
        )
    return fig2

#compras
@app.callback(
        Output("line-graph-compras", "figure"),
        [Input("location-dropdown-compras", "value")]
)
def plot_line_graph(plot_type):
    fig2_compras = px.histogram(x=df32.Estado, y=df32[plot_type])
    
    fig2_compras.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
        )
    return fig2_compras

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)
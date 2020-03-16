# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import pandas as pd
from datetime import datetime
import plotly.express as px
import numpy as np
import copy

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

riddles = pd.read_csv('data/Complete_Menus.csv')


def make_datetime(date):
    try:
        d =  datetime.strptime(str(date), "'%Y-%m-%d")
        if d.year < 1700:
            return None
        return d
    except:
        return None

def fix_country(country):
    try:
        return country.strip()
    except:
        return None

riddles["Newspaper Issue Date"] = riddles.apply(
    lambda row: make_datetime(row['Newspaper Issue Date']),
    axis=1,
)

riddles["Event Date"] = riddles.apply(
    lambda row: make_datetime(row['Event_Date']),
    axis=1,
)



riddles["Country"] = riddles.apply(
    lambda row: fix_country(row['Country']),
    axis=1,
)


distribution_types = ['Distribution by Year', 'Distribution by Month', 'Distribution by Weekday']
classes = ['Newspaper Issue Date', 'Event Date']

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in distribution_types],
                value=distribution_types[0]
            ),
        ],
        style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in classes],
                value=classes[0]
            ), 
        ], style={'width': '30%', 'display': 'inline-block', 'float': 'right',}),
    ]),



    dcc.Graph(id='indicator-graphic'),

])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
    Input('xaxis-type', 'value')])

def update_graph(xaxis_column_name,
                 xaxis_type):
        cur = copy.deepcopy(riddles.dropna(subset=[xaxis_type, 'Country']))

        if xaxis_column_name == 'Distribution by Year':
            cur['Year'] = [date.year for date in cur[xaxis_type]]
            fig = px.histogram(cur, x="Year", color='Country', marginal="box",)

        
        elif xaxis_column_name == 'Distribution by Month':
            cur['Day'] = [int(date.strftime('%j')) for date in cur[xaxis_type]]
            fig = px.histogram(cur, x="Day", color='Country', marginal="box",)

            fig.update_layout(xaxis_title="Month",
                xaxis = dict(
                tickmode = 'array',
                tickvals = [15, 46, 74, 105, 135, 166, 197, 228, 258, 289, 319, 350],
                ticktext = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                )
            )
        
        elif xaxis_column_name == 'Distribution by Weekday':

            cur['Weekday'] = [int(date.strftime('%w')) for date in cur[xaxis_type]]
            
            fig = px.histogram(cur, x="Weekday", color='Country', marginal="box",)
            fig.update_layout(
                xaxis = dict(
                tickmode = 'array',
                tickvals = [0, 1, 2, 3, 4, 5, 6],
                ticktext = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                )
            )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)


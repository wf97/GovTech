import requests

import json
import pandas as pd
from datetime import datetime, timezone, timedelta
from dateutil.parser import parse

import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# Reguest data from the API
def request_data():
    res = requests.get('https://api.covid19api.com/country/singapore')
    data = res.json()
    df = pd.json_normalize(data)
    return df

# Process Data into usable format for plottiing on Dash
def process_data():
    df = request_data()
    df = df.loc[:, ['Date', 'Confirmed', 'Deaths', 'Recovered', 'Active']]
    df['Date'] = df['Date'].apply(parse)
    df = df.set_index('Date')
    # Some entries are 0, so I forward fill using the last available value
    df = df.replace(to_replace=0, method='ffill')
    # subtract to show daily numbers as the API gives running total
    df = (df - df.shift(1)).fillna(0).astype('Int64')
    return df

df = process_data()

app = dash.Dash()

app.layout = html.Div(id='parent',
                      children=[
                          html.H1(id='H1',
                                  children='Covid19 Statistics in Singapore',
                                  style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),

                          # Three dropdowns
                          # Frequency: Daily/Monthly
                          dcc.Dropdown(id='frequency',
                                       options=[
                                           {'label': 'Daily', 'value': 'D'},
                                           {'label': 'Monthly', 'value': 'M'},
                                       ], value='D'),
                          # Type of Metric
                          dcc.Dropdown(id='type',
                                       options=[
                                           {'label': 'Confirmed Cases', 'value': 'Confirmed'},
                                           {'label': 'Deaths', 'value': 'Deaths'},
                                           {'label': 'Actives', 'value': 'Active'},
                                           {'label': 'Recovered', 'value': 'Recovered'},
                                       ], value='Confirmed'),
                          # Cumulative or Non-Cumulative
                          dcc.Dropdown(id='value',
                                       options = [
                                           {'label':'Non-Cumulative', 'value':'N' },
                                           {'label': 'Cumulative', 'value':'C'},
                                       ], value = 'N'),

                          dcc.Graph(id='bar_plot')])

@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='frequency', component_property= 'value'),
               Input(component_id='type', component_property= 'value'),
               Input(component_id='value', component_property= 'value')],)

def graph_update(dropdown_value1, dropdown_value2, dropdown_value3):
    print(dropdown_value1, dropdown_value2, dropdown_value3)
    data = df.resample(dropdown_value1).sum()
    if dropdown_value3 == 'C':
        data = data.cumsum()
    fig = go.Figure([go.Scatter(x = data.index,
                                y = data[dropdown_value2],
                                line = dict(color = 'cyan', width = 4))
                     ])

    fig.update_layout(title = 'Covid19 Statistics in Singapore',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Cases'
                      )
    return fig



if __name__ == '__main__':
    app.run_server()
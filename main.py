from dash import Dash, html, dcc, callback, Output, Input
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import dash_daq as daq

df = pd.read_csv('COR_AWS.dat', skiprows=[0, 2, 3])

print(df.head())

df['AirTemperature'] = pd.to_numeric(df["AirTemperature"], errors='coerce')

# Describe data and lines
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Line( 
            x = df.TIMESTAMP, y = df.AirTemperature, name = 'Temperatura'),
            secondary_y = False
)

fig.add_trace(
    go.Line(
            x = df.TIMESTAMP, y = df.DewPoint, name = 'Punto de Rocío'),
            secondary_y = False
)

fig.add_trace(
    go.Line(
            x = df.TIMESTAMP, y = df.RelHumidity, name = 'Humedad'),
            secondary_y = True
)

# Set x-axis title
fig.update_xaxes(title_text="Tiempo")

# Set y-axes titles
fig.update_yaxes(title_text="<b>Temperatura</b> (°C)", secondary_y=False)
fig.update_yaxes(title_text="<b>Humedad</b> (%))", secondary_y=True)


app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        children='AWS Pilar, Córdoba', 
        style={'textAlign':'center'}),
    dcc.Graph(
        figure = fig),
    daq.Thermometer(
        id='thermo-temp',
        value= df.iloc[-1]['AirTemperature'],
        min=-5,
        max=40,
        showCurrentValue=True,
        units="°C",
        style={
            'margin-bottom': '5%'
        },
        label='Temperatura actual',
        labelPosition='top'
    ),
    daq.Thermometer(
        id='thermo-dewpoint',
        value= df.iloc[-1]['DewPoint'],
        min=-20,
        max=60,
        showCurrentValue=True,
        units="°C",
        style={
            'margin-bottom': '5%'
        },
        label='Punto de rocío actual',
        labelPosition='top'
    ),
    daq.Gauge(
        id='humidity',
        value = df.iloc[-1]['RelHumidity'],
        units = "%",
        min = 0,
        max = 100,
        showCurrentValue = True,
        label = "Humedad actual",
        style={
            'margin-bottom': '5%'
        },
    )        
])

if __name__ == '__main__':
    app.run(debug=True)
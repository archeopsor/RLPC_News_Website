import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from flask_caching import Cache
import pandas as pd

from abbreviations import abbreviations

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
TIMEOUT = 60

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

league = "major"

data = pd.read_csv(f"./forecasts/{league} Forecast.csv")

new_data = pd.DataFrame(columns=['Count'])
for team in abbreviations[league].keys():
    new_data.loc[team, 'Count'] = len(data.loc[data['Quarterfinals'].str.contains(abbreviations[league][team])])
new_data.reset_index(drop=False, inplace=True)

fig = px.bar(new_data, x='index', y="Count")

app.layout = html.Div(children=[
    html.H1(children="Major Forecast"),
    dcc.Graph(id="forecast", figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)
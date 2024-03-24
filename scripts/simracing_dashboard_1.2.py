import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

# Load the data
df = pd.read_pickle('/Users/macbook/Dropbox/Mac/Documents/Pro/Data_Analyst/simracing-players/data/interim/sim_racing_games-1.0.pkl')

# -----------------------------------------------------------------------------
# Aggregate data to calculate the average players across all games
global_trend = df.groupby('datetime')['players'].mean().reset_index()

# Calculate the average player count across all games
average_players = df['players'].mean()

# ----------------------------------------------------------------------------
# Create Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("Global trend of average players"),
    dcc.Graph(
        id='line-chart',
        figure={'data': [ go.Scatter(
                    x=global_trend['datetime'],
                    y=global_trend['players'],
                    mode='lines',
                    name='Global Trend',
                    line=dict(color='purple', width=1)
                )
            ],
            'layout': go.Layout(
                title='Global trend of average players',
                width=1000,
                height=400,
                #yaxis=dict(title='Average players'),
                template='plotly_dark',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False)
            )
        }
    )
])

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
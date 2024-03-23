import dash
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Load your data (replace this with your data loading code)
df = pd.read_pickle('/Users/macbook/Dropbox/Mac/Documents/Pro/Data_Analyst/simracing-players/data/interim/sim_racing_games-1.0.pkl')

# Aggregate data to calculate the average players across all games
global_trend = df.groupby('datetime')['players'].mean().reset_index()

# Calculate the average player count across all games
average_players = df['players'].mean()

# Create line chart for global trend
fig_global_trend = go.Figure()
fig_global_trend.add_trace(
    go.Scatter(
        x=global_trend['datetime'],
        y=global_trend['players'],
        mode='lines',
        name='Global Trend',
        line=dict(color='purple', width=1)
    )
)
fig_global_trend.update_layout(
    title='Global trend of average players',
    width=600,
    height=400,
    yaxis_title='Average players',
    template='plotly_dark',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

# Create line chart for the current game
line_chart = px.line(df, x='datetime', y='players', color='game', title='Number of players per game', template='plotly_dark')
line_chart.update_layout(
    xaxis=dict(
        showgrid=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=3, label="3y", step="year", stepmode="backward"),
                dict(step="all")
            ]),
            bgcolor="rgba(255, 255, 255, 0.5)",  
            activecolor="rgba(255, 255, 255, 0.8)",  
            bordercolor="rgba(0, 0, 0, 0.2)",  
            borderwidth=1,  
            font=dict(color="rgba(0, 0, 0, 0.8)")  
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ),
    yaxis=dict(showgrid=False),
)

# Relationship between players & twitch viewers
fig_players_vs_viewers = px.scatter(df, x="players", y="twitch_viewers", color="game", template='plotly_dark')
fig_players_vs_viewers.update_layout(
    xaxis=dict(showgrid=False), 
    yaxis=dict(showgrid=False)
)

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1("Steam Sim Racing Dashboard", style={'textAlign': 'center'}),
    
    # Global trend of average players plot
    dcc.Graph(figure=fig_global_trend),
    
    # Number of players per game plot
    dcc.Graph(figure=line_chart),
    
    # Relationship between players & twitch viewers plot
    dcc.Graph(figure=fig_players_vs_viewers)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

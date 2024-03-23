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

# Find the top day with the highest average number of players
top_day = global_trend.loc[global_trend['players'].idxmax(), 'datetime']

# Find the most played game
most_played_game = df['game'].value_counts().idxmax()

# List of available games for multi-select dropdown
available_games = df['game'].unique()

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div(style={'backgroundColor': '#282c34', 'color': 'white'}, children=[
    
    # Dash Player container
    html.Div([
        html.Iframe(id='video-container', src='https://www.youtube.com/embed/V_Sle4ItgDQ?&t=148&autoplay=1&mute=1', width='100%', height='300px', style={'border': 'none'})
    ]),

    # Top day with the highest average number of players
    html.Div([
        html.H2("Top Day:", style={'textAlign': 'center'}),
        html.H3(f"{top_day}", style={'textAlign': 'center'})
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'}),

    # Vertical separator
    html.Div(style={'width': '2px', 'background-color': 'gray', 'height': '100%', 'margin': '0 10px', 'display': 'inline-block'}),

    # Most played game
    html.Div([
        html.H2("Most Played Game:", style={'textAlign': 'left'}),
        html.H3(f"{most_played_game}", style={'textAlign': 'left'})
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
    
    # Vertical separator
    html.Div(style={'width': '2px', 'background-color': 'gray', 'height': '100%', 'margin': '0 10px', 'display': 'inline-block'}),

    # Multi-select dropdown for selecting games
    dcc.Dropdown(
        id='game-dropdown',
        options=[{'label': game, 'value': game} for game in available_games],
        value=[most_played_game],
        multi=True,
        style={'width': '50%', 'margin': '20px auto'}
    ),
    # Horizontal separator
    html.Div(style={'height': '2px', 'background-color': 'gray', 'margin': '10px 0'}),

    # Global trend of average players plot
    dcc.Graph(figure=fig_global_trend),
    # Horizontal separator
    html.Div(style={'height': '2px', 'background-color': 'gray', 'margin': '10px 0'}),

    # Number of players per game plot
    dcc.Graph(figure=line_chart),
    
    # Horizontal separator
    html.Div(style={'height': '2px', 'background-color': 'gray', 'margin': '10px 0'}),
    # Relationship between players & twitch viewers plot
    dcc.Graph(figure=fig_players_vs_viewers)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

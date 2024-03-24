import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Load your data (replace this with your data loading code)
df = pd.read_pickle('/Users/macbook/Dropbox/Mac/Documents/Pro/Data_Analyst/simracing-players/data/interim/sim_racing_games-1.0.pkl')

# Aggregate data to calculate the metrics
max_players_day = df.groupby('datetime')['players'].sum().idxmax().strftime('%Y-%m-%d')
game_most_players = df.groupby('game')['players'].sum().idxmax()
game_most_played_avg = df.groupby('game')['players'].mean().idxmax()

# Aggregate data to calculate the average players across all games
global_trend = df.groupby('datetime')['players'].mean().reset_index()

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

# Streamlit app layout
st.title("Steam Sim Racing Dashboard")

# Day with the most players
st.subheader(f"Day with the most players: {max_players_day}")

# Game with the most registered players
st.subheader(f"Game with the most registered players: {game_most_players}")

# Game most played on average
st.subheader(f"Game most played on average: {game_most_played_avg}")

# Layout with two columns
col1, col2 = st.columns(2)

# Global trend of average players plot
col1.plotly_chart(fig_global_trend)

# Number of players per game plot
col2.plotly_chart(line_chart)

# Relationship between players & twitch viewers plot
st.plotly_chart(fig_players_vs_viewers)

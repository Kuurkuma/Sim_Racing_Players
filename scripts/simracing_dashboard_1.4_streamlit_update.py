import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Load data
data_path = '/Users/macbook/Dropbox/Mac/Documents/Pro/Data_Analyst/simracing-players/data/interim/sim_racing_games-1.0.pkl'
df = pd.read_pickle(data_path)

# Calculate metrics
max_players_day = df.groupby('datetime')['players'].sum().idxmax()
game_most_players = df.groupby('game')['players'].sum().idxmax()
game_most_played_avg = df.groupby('game')['players'].mean().idxmax()
global_trend = df.groupby('datetime')['players'].mean().reset_index()

# Plot global trend
fig_global_trend = px.line(global_trend, x='datetime', y='players', title='Global trend of average players')
fig_global_trend.update_traces(line=dict(color='purple', width=1))
fig_global_trend.update_layout(
    width=1200, height=600,
    yaxis_title='Average players',
    template='plotly_dark',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

# Plot number of players per game
line_chart = px.line(df, x='datetime', y='players', color='game', title='Number of players per game')
line_chart.update_layout(
    width=1200, height=600,
    xaxis=dict(
        showgrid=False,
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=3, label="3y", step="year", stepmode="backward"),
                dict(step="all")
            ],
            bgcolor="rgba(255, 255, 255, 0.5)",
            activecolor="rgba(255, 255, 255, 0.8)",
            bordercolor="rgba(0, 0, 0, 0.2)",
            borderwidth=1,
            font=dict(color="rgba(0, 0, 0, 0.8)")
        ),
        rangeslider=dict(visible=True),
        type="date"
    ),
    yaxis=dict(showgrid=False)
)

# Relationship between players & twitch viewers
fig_players_vs_viewers = px.scatter(df, x="players", y="twitch_viewers", color="game",
                                    title="Relationship between Players & Twitch Viewers")

# Calculate daily average players
avg_daily = df.groupby('game')['average_players'].mean().sort_values(ascending=False)
most_avg_daily = avg_daily.idxmax()

# Plot daily average player counts
bar_avg_daily = px.bar(avg_daily, x=avg_daily.index, y=avg_daily.values,
                        title='Daily average player counts (2013-2023)',
                        labels={'x': 'Game', 'y': 'Average Players'})
bar_avg_daily.update_layout(
    width=600, height=600,
    template='plotly_dark',
    showlegend=False,
    xaxis=dict(title=''),
    yaxis=dict(title='')
)
# Define the game names using a dictionary to remove the undescores
game_names = {
    'American_truck_simulator': 'American truck simulator',
    'Assetto_corsa': 'Assetto corsa',
    'Assetto_corsa_competizione': 'Assetto corsa competizione',
    'Automobilista_2': 'Automobilista 2',
    'BeamNG': 'BeamNG',
    'CarX_drift_racing_online': 'CarX drift racing online',
    'Dirt_rally_2.0': 'Dirt rally 2.0',
    'Euro_truck_2': 'Euro truck 2',
    'Forza_horizon_4': 'Forza horizon 4',
    'Forza_horizon_5': 'Forza horizon 5'
}

#bar_avg_daily.update_xaxes(labelalias=game_names)

bar_avg_daily.add_hline(
    y=avg_daily.max(),
    line_dash="dash",
    line_color="red",
    annotation_text=f"Max Average Players ({round(avg_daily.max())})",
    annotation_position="top right"
)

# Game with the most average players
average_players = df.groupby('game')['players'].mean().sort_values(ascending=False)
most_average_players = average_players.idxmax()

# Plot average player activity
fig_average_players = px.bar(x=average_players.index, y=average_players.values,
                              title='Average player activity (2013-2023)',
                              labels={'x': 'Game', 'y': 'Average Players'},
                              color=average_players.index,
                              color_discrete_sequence=px.colors.sequential.matter_r)

fig_average_players.update_layout(
    width=600, height=600,
    template='plotly_dark',
    showlegend=False,
    xaxis=dict(title=''),
    yaxis=dict(title='')
)

#fig_average_players.update_xaxes(labelalias=game_names)

fig_average_players.add_hline(
    y=average_players.max(),
    line_dash="dash",
    line_color="red",
    annotation_text=f"Max Average Players ({round(average_players.max())})",
    annotation_position="top right"
)
#---------------------------------
# Key Metrics
st.subheader(f"Game with the most registered players: {game_most_players}")
st.subheader(f"Game most played on average: {game_most_played_avg}")

# Global Trend of Average Players
st.header("Global Trend of Average Players")
st.plotly_chart(fig_global_trend)

# Number of Players per Game
st.header("Number of Players per Game")
st.plotly_chart(line_chart)

# Relationship between Players & Twitch Viewers
st.header("Relationship between Players & Twitch Viewers")
st.plotly_chart(fig_players_vs_viewers)

# Daily Average Player Counts
st.header("Daily Average Player Counts (2013-2023)")
st.plotly_chart(bar_avg_daily)

# Average Player Activity
st.header("Average Player Activity (2013-2023)")
st.plotly_chart(fig_average_players)
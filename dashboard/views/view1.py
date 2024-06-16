import streamlit as st
from dashboard.data_prep import load_data, get_data_path, calculate_global_trend, calculate_global_trend_viewers
from dashboard.viz_script import global_trend_chart, global_trend_viewers

def display_view1():
    st.header("View 1 - Global Trend of Players and Viewers")

    # Define paths
    local_path = '/Users/macbook/Development/Sim_Racing_Players/data/interim/sim_racing_games-1.0.pkl'
    net_path = 'data/interim/sim_racing_games-1.0.pkl'

    # Get the correct data path
    data_path = get_data_path(local_path, net_path)

    # Load data
    df = load_data(data_path)

    if df.empty:
        st.error("Data could not be loaded.")
        return

    # Calculate global trends
    global_trend_players = calculate_global_trend(df)
    global_trend_viewers_data = calculate_global_trend_viewers(df)

    if global_trend_players.empty or global_trend_viewers_data.empty:
        st.error("Data processing error.")
        return

    # Plot global trends
    fig_players = global_trend_chart(global_trend_players)
    fig_viewers = global_trend_viewers(global_trend_viewers_data)

    # Display charts
    st.plotly_chart(fig_players)
    st.plotly_chart(fig_viewers)
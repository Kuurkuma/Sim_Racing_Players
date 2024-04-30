import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Define page config
st.set_page_config(
    page_title="Steam Sim racing Dashboard (BETA VERSION)",
    page_icon=":bar_chart:",
    layout='wide'    
)

# Title and subheader
st.title('Steam Sim racing Dashboard')
st.markdown('_10 years of data from Steam tagged "Automobile Sim Racing"_')

# Define function to load data 
@st.cache_data
def load_data(data_path:str):
    data = pd.read_pickle(data_path)
    return data

# Define dataframe
df = load_data('data/interim/sim_racing_games-1.0.pkl')


#########################
# Create multiselect widget for selecting games
default_game = ['Forza_horizon_4']
selected_games = st.multiselect(
    label="Select games to compare",
    options=df['game'].unique(),
    default=default_game
)

# Function to create line chart for selected games
def line_chart_games(selected_games):
    # Filter DataFrame based on selected games
    filtered_df = df[df['game'].isin(selected_games)]

    # Calculate global trend line
    global_trend = filtered_df.groupby('datetime')['players'].mean().reset_index()

    # Create line chart for the selected games
    line_chart = px.line(
        filtered_df,
        x='datetime',
        y='players',
        color='game',
        title='Active players per game (2013-2023)',
        template='plotly_dark'
    )

    # Add global trend line to the chart
    line_chart.add_trace(
        go.Scatter(
            x=global_trend['datetime'],
            y=global_trend['players'],
            mode='lines',
            name='Global Trend',
            line=dict(color='#d62728', width=2)  # Brick red color
        )
    )

    # Update layout of the chart
    line_chart.update_layout(
        height=720,
        width=1200,
        showlegend=True,  # Set to True if you want to display the legend
        xaxis=dict(
            showgrid=False,
            title='Date'
        ),
        yaxis=dict(
            showgrid=False,
            title='Active Players'
        ),
        legend=dict(
            title='Games',
            font=dict(color="rgba(255, 100, 100, 100)")
        ),
        xaxis_rangeslider_visible=True  # Enable range slider for zooming
    )

    return line_chart

st.subheader('Active players per game (2013-2023)')
st.plotly_chart(line_chart_games(selected_games))

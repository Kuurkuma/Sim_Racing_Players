import streamlit as st
import plotly.express as px
import pandas as pd

# Define page config
st.set_page_config(
    page_title="Steam Sim racing Dashboard",
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
df = load_data('/Users/macbook/Dropbox/Mac/Documents/Pro/Data_Analyst/simracing-players/data/interim/sim_racing_games-1.0.pkl')

# Create multiselect widget for selecting games
default_game = ['Assetto_corsa','Euro_truck_2']
selected_games = st.multiselect(
    label="Select games to compare",
    options=df['game'].unique(),
    default=default_game
)
#########################

# Function to create line chart for selected games
def line_chart_games(selected_games):
    # Filter dataframe based on selected games
    filtered_df = df[df['game'].isin(selected_games)]
    
    # Create line chart
    line_chart = px.line(
        filtered_df, 
        x='datetime', 
        y='players', 
        color='game', 
        title='', 
        template='plotly_dark'
    )
    
    # Customize layout
    line_chart.update_layout(
        xaxis=dict(
            showgrid=False,
            title='Adjust the sliders to modify the time window. Select game labels to reveal the corresponding games',
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=3, label="3y", step="year", stepmode="backward"),
                    dict(step="all")
                ]),
                bgcolor="rgba(255, 255, 255, 0.8)",  # Background color of the rangeselector
                activecolor="rgba(255, 255, 255, 0.8)",  # Active button color
                bordercolor="rgba(0, 0, 0, 0.2)",
                borderwidth=1,
                font=dict(color="rgba(0, 0, 0, 0.8)")  # Font color
            ),
            rangeslider=dict(
                visible=True,
                thickness=0.05,
                bgcolor="rgba(255, 255, 255, 0.2)"
            ),
            type="date"
        ),
        yaxis=dict(showgrid=False,title=''),
        yaxis_tickmode="array",
        yaxis_tickvals=[],
        yaxis_ticktext=[],
        showlegend=False
    )
    return line_chart

st.subheader('Active players per game (2013-2023)')
st.plotly_chart(line_chart_games(selected_games))

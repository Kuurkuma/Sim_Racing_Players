import streamlit as st
import plotly.graph_objects as go
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

#-----------------

# Create expander to show raw data
with st.expander('Show raw data'):
    st.dataframe(df[['game','datetime','players','twitch_viewers']])

# Create sidebar
with st.sidebar:
    st.header('Select a view')

#------------------

# Defining all charts
def table_games():
    st.dataframe(df.groupby('game')['players'].max().sort_values(ascending=False))

def plot_global_trend():

    # Group data to calculate the average players across all games
    global_trend = df.groupby('datetime')['players'].mean().reset_index()

    # Create line chart for global trend
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=global_trend['datetime'],
            y=global_trend['players'],
            mode='lines',
            name='Global Trend',
            line=dict(color='#d62728', width=1) # brick red = #d62728
        )
    )

    fig.update_layout(
        title='',
        yaxis_title='Average players',
        template='plotly_dark',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        width=900
    )

    st.plotly_chart(fig)

def bar_chart_games():
     # Game with the most average players
    average_players = round(df.groupby('game')['players'].mean().sort_values(ascending=False))
    most_average_players = average_players.idxmax()

    # Define dictionnary of the game names
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

    # Plot the bar chart for the game with the most average players
    fig_average_players = px.bar(
        x=average_players.index,
        y=average_players.values,
        title='',
        labels={'x': 'Game', 'y': 'Average Players'},
        color=average_players.index,
        color_discrete_sequence= px.colors.sequential.matter_r
    )

    fig_average_players.update_layout(
    template='plotly_dark',
    showlegend=False,
        xaxis=dict(
            title=''),
        yaxis=dict(
            title='')
    )
    #fig_average_players.update_xaxes(labelalias=game_names)

    fig_average_players.add_hline(
        y=average_players.max(),
        line_dash="dash",
        line_color="red",
        annotation_text=f"Max Average Players ({round(average_players.max())})",
        annotation_position="top right"
    )

    st.plotly_chart(fig_average_players)

def bar_chart_days():
    # define avg_players_per_day 
    weekdays = round(df.groupby('weekday')['players'].mean()).sort_values(ascending=False)

    # Reset the index of the weekdays DataFrame
    days = weekdays.reset_index()

    # Create a bar plot
    bar_day = px.bar(
        days,
        x='weekday',
        y='players',
        title='',
        text_auto='2',
        labels={'players': 'Average Players', 'weekday': 'Day of the Week'},
        color='weekday',
        color_discrete_sequence= px.colors.sequential.Plasma
    )

    bar_day.update_layout(
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        template='plotly_dark',
        showlegend=False,  # Remove the legend
    )
    st.plotly_chart(bar_day)

# Create column layout 
col1, col2 = st.columns([1,2],gap="small")
subcol1, subcol2 = st.columns([1,1])

with col1:
   st.subheader('Max players recorded per game')
   table_games()
   

with col2:
   st.subheader('Global trend of average players')
   plot_global_trend()

#with col3:
#   st.header('')

with subcol1:
    st.subheader('Average players per game')
    bar_chart_games()

with subcol2:
    st.subheader('Average players per day')
    bar_chart_days()

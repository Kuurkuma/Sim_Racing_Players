import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Define page config
st.set_page_config(
    page_title="Steam Sim racing Dashboard",
    page_icon=":bar_chart:",
    layout='wide'    
)

# Title and subheader
st.title('Steam Sim racing Dashboard (BETA VERSION)')
st.markdown('_10 years of data from Steam tagged "Automobile Sim Racing"_')

# Define function to load data 
@st.cache_data
def load_data(data_path:str):
    data = pd.read_pickle(data_path)
    return data

# Define dataframe
local_path = '/Users/macbook/Dropbox/Mac/Documents/Pro/Data_Analyst/Sim_Racing_Players/data/interim/sim_racing_games-1.0.pkl'
net_path = 'data/interim/sim_racing_games-1.0.pkl'
df = load_data(local_path)

#________________________
# Define all elements of the dashboard as function to make the dashboard layout easier
def table_games():
    df_players = df.groupby('year')['players'].mean()
    st.dataframe(
        df_players,
        #column_config={'players':st.column_config.ProgressColumn}
    )

def global_trend_player():
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
        template='plotly_dark',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig)

def global_trend_viewers():
    # Remove null values from the DataFrame
    global_trend_viewers = df[df['datetime'] >= '2015-07-01'] # records of twitch viewers start from July 2015

    # Group data to calculate the average players across all games
    global_trend_viewers = global_trend_viewers.groupby('datetime')['twitch_viewers'].mean().reset_index()

    # Create line chart for global trend
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=global_trend_viewers['datetime'],
            y=global_trend_viewers['twitch_viewers'],
            mode='lines',
            name='Global Trend',
            line=dict(color='purple', width=1.5)
        )
    )

    fig.update_layout(
        yaxis_title='Twitch viewers',
        template='plotly_dark',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig)

def table_viewers():
    df_viewers = df.groupby('year')['twitch_viewers'].mean()
    st.dataframe(df_viewers)        

def player_per_game():
        # Create line chart for the current game
    line_chart = px.line(
        df, 
        x='datetime', 
        y='players', 
        color='game', 
        title='Active players per game (2013-2023)', 
        template='plotly_dark'
    )

    # Add date picker widget with customized button colors using CSS
    line_chart.update_layout(
        xaxis=dict(
            showgrid=False,
            title='',
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
                bgcolor="rgba(255, 255, 255, 0.2)"),
                type="date"
        ),
        yaxis=dict(showgrid=False,
            title=''),
        yaxis_tickmode="array",
        yaxis_tickvals=[],
        yaxis_ticktext=[],
        showlegend=False,
        legend_title=dict(text='Double-click on a game to select it exclusively.',
                    font=dict(color="rgba(255, 100, 100, 100)")                  
        )
    )
    st.plotly_chart(line_chart)

#________________________

# Dashboard layout
tab1, tab2, tab3 = st.tabs(['Trend','Per Game','Seasonality'])

with tab1:
    #st.markdown('Average players & twitch viewers')
    col1, col2 = st.columns([0.2,0.8],gap='medium')
    subcol1, subcol2 = st.columns([0.8,0.2],gap='small')
    with col1:
        st.subheader('')
        table_games()

    with col2:
        st.subheader('Average players 2013-2023')
        global_trend_player()

    with subcol1:
        st.subheader('Twitch viewers 2015-2023')
        global_trend_viewers()
    
    with subcol2:
        st.subheader('')
        table_viewers()

with tab2:
    col1 = st.columns(1)
    subcol1, subcol2 = st.columns([0.8,0.2],gap='medium')
    with col1:
        st.subheader('')
        player_per_game()
        
    #with col2:
     #   st.subheader('')
   
with tab3:
    player_per_game()
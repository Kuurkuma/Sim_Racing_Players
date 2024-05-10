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
st.title('Steam Sim racing Dashboard (_BETA VERSION_)')
st.markdown('_10 years of data from Steam tagged "Automobile Sim Racing"_')

# Define function to load data 
@st.cache_data
def load_data(data_path:str):
    data = pd.read_pickle(data_path)
    return data

# Define paths
local_path = '/Users/macbook/Dropbox/Mac/Documents/Pro/Data_Analyst/Sim_Racing_Players/data/interim/sim_racing_games-1.0.pkl'
net_path = 'data/interim/sim_racing_games-1.0.pkl'
df = load_data(local_path)

#________________________
# Define all elements of the dashboard as function to make the dashboard layout easier
def table_games():
    df_players = df.groupby('year')['players'].mean()
    st.dataframe(
        df_players,
        column_config={
            'year': st.column_config.NumberColumn(
                format="%d",
                label='Year'
            ),
            'players': st.column_config.ProgressColumn(
                label='Average player', 
                width='medium',
                format='%.0f', 
                min_value=0,
                max_value=12000
            )
        }
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
    
    df_viewers = df.groupby('year')['twitch_viewers'].mean().sort_values(ascending=False)
    st.dataframe(
        df_viewers,
        column_config={
            'year': st.column_config.NumberColumn(
                format="%d",
                label='Year'
            ),
            'twitch_viewers': st.column_config.ProgressColumn(
                label='Average viewer', 
                width='medium',
                format='%.0f', 
                min_value=0,
                max_value=3000
            )
        }
    )        

def player_per_game():
        # Create line chart for the current game
    line_chart = px.line(
        df, 
        x='datetime', 
        y='players', 
        color='game', 
        height=500,
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

# define the game names for 2 functions representing the 2 bar plots for average players & viewers per game
game_names = {
        'American_truck_simulator': 'American truck simulator',
        'Assetto_corsa': 'Assetto corsa',
        'Assetto_corsa_competizione': 'Assetto corsa competizione',
        'Automobilista_2': 'Automobilista 2',
        'BeamNG': 'BeamNG',
        'CarX_drift_racing': 'CarX drift racing',
        'Dirt_rally_2.0': 'Dirt rally 2.0',
        'Euro_truck_2': 'Euro truck 2',
        'Forza_horizon_4': 'Forza horizon 4',
        'Forza_horizon_5': 'Forza horizon 5'
    }

def average_player_per_game():
    # Game with the most average players
    average_players = round(df.groupby('game')['players'].mean().sort_values(ascending=False))
    most_average_players = average_players.idxmax()

    fig_average_players = px.bar(
        x=average_players.index,
        y=average_players.values,
        text_auto='2',
        title='Average player activity (2013-2023)',
        color=average_players.index,
        color_discrete_sequence= px.colors.sequential.Plasma
    )

    fig_average_players.update_layout(
        template='plotly_dark',
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    # Update x-axis tick labels
    fig_average_players.update_xaxes(
        tickvals=average_players.index, 
        ticktext=[game_names[name] for name in average_players.index]
    )

    fig_average_players.add_hline(
        y=average_players.max(),
        line_dash="dash",
        line_color="red",
        annotation_text=f"Max Average Players ({round(average_players.max())})",
        annotation_position="top right")

    st.plotly_chart(fig_average_players)


    fig_average_players.update_xaxes(labelalias=game_names)

    fig_average_players.add_hline(
        y=average_players.max(),
        line_dash="dash",
        line_color="red",
        annotation_text=f"Max Average Players ({round(average_players.max())})",
        annotation_position="top right")

    st.plotly_chart(fig_average_players)

def average_viewer_per_game():
    game_names = {
        'American_truck_simulator': 'American truck simulator',
        'Assetto_corsa': 'Assetto corsa',
        'Assetto_corsa_competizione': 'Assetto corsa competizione',
        'Automobilista_2': 'Automobilista 2',
        'BeamNG': 'BeamNG',
        'CarX_drift_racing': 'CarX drift racing',
        'Dirt_rally_2.0': 'Dirt rally 2.0',
        'Euro_truck_2': 'Euro truck 2',
        'Forza_horizon_4': 'Forza horizon 4',
        'Forza_horizon_5': 'Forza horizon 5'
    }

    weekdays_viewers = round(df.groupby('game')['twitch_viewers'].mean()).sort_values(ascending=False)
    days_viewers = weekdays_viewers.reset_index()

    viewers_day = px.bar(
        days_viewers,
        x='game',
        y='twitch_viewers',
        title='Average viewers per game',
        text_auto='2',
        color='game',
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    viewers_day.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        template='plotly_dark',
        showlegend=False,
    )

    #viewers_day.update_xaxes(tickvals=weekdays_viewers.index,ticktext=[game_names[name] for name in weekdays_viewers['game']])

    st.plotly_chart(viewers_day)


def average_player_per_day():
    # Extract the day of the week as an integer (0 for Monday, 1 for Tuesday, etc.)
    df['day_of_week'] = df['datetime'].dt.dayofweek

    # Map the integer day of the week to the corresponding weekday name
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['weekday'] = df['day_of_week'].map(lambda x: weekday_names[x])
    df.drop(columns=['day_of_week'], inplace=True)

    # avg_players_per_day 
    weekdays = round(df.groupby('weekday')['players'].mean()).sort_values(ascending=False)
    days = weekdays.reset_index()

    # Create a bar plot for average players per day
    players_day = px.bar(
        days,
        x='weekday',
        y='players',
        title='Average players per day',
        text_auto='2',
        labels={'players': 'Average Players', 'weekday': 'Day of the Week'},
        color='weekday',
        color_discrete_sequence= px.colors.sequential.Plasma
    )

    players_day.update_layout(
        xaxis=dict(title=''),
        yaxis=dict(showgrid=False,title=''),
        template='plotly_dark',
        showlegend=False,  # Remove the legend
    )

    st.plotly_chart(players_day)

def correlation_player_viewers():
    df_last_3 = df[df['year'] > 2020]

    month_names = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    # Violin plot for the 3 last years
    violin_twitch = px.violin(
        df_last_3,
        x='month',
        y='twitch_viewers',
        title='Distribution Twitch viewers',
        color='year',
        color_discrete_sequence=['blue','magenta','red']
    )

    violin_twitch.update_layout(
        template='plotly_dark',
        xaxis=dict(showgrid=False, title=''),
        yaxis=dict(showgrid=False, title=''),
        showlegend=True,
        legend_title=dict(
            text='Year',
        )
    )

    # Update x-axis labels for showing all months
    violin_twitch.update_xaxes(
        tickvals=list(range(1, 13)), 
        ticktext=list(month_names.values())
    )
    st.plotly_chart(violin_twitch)


#________________________

# Dashboard layout
tab1, tab2, tab3 = st.tabs(['Trend','Per Game','Seasonality'])

with tab1:
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
    with st.container():
        st.subheader('')
        player_per_game()
    
    subcol1, subcol2 = st.columns([8,2])
    with subcol1:
            st.subheader('')
            average_player_per_game()
    with subcol2:
            st.subheader('')
            average_viewer_per_game()
'''
with tab3:
    player_per_game()'''  
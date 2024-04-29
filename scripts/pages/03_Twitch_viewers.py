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
df = load_data('data/interim/sim_racing_games-1.0.pkl')

#-----------------

# Create expander to show raw data
with st.expander('Show raw data'):
    st.dataframe(df[['game','datetime','players','twitch_viewers']])

#------------------

# Defining all charts
def bar_chart_twitch():
    # Calculate the average viewers per game
    avg_viewers_per_game = round(df.groupby('game')['twitch_viewers'].mean().sort_values(ascending=False))
    
    # Reset the index to make 'game' a regular column
    avg_viewers_per_game = avg_viewers_per_game.reset_index()

    # Create a bar plot
    viewers_day = px.bar(
        avg_viewers_per_game,
        x='game',
        y='twitch_viewers',
        title='',
        text_auto='2',
        labels={'twitch_viewers': 'Twitch viewers'},
        color='game',
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    # Customize layout
    viewers_day.update_layout(
        xaxis=dict(title='Game'),
        yaxis=dict(title='Average Twitch Viewers'),
        template='plotly_dark',
        showlegend=False
    )

    # Display the plot
    st.plotly_chart(viewers_day)


# Create column layout 
col1, col2 = st.columns([1,2],gap="small")
subcol1, subcol2 = st.columns([1,1],gap="small")

with col1:
   st.subheader('Most viewd games on Twitch')

with col2:
   st.subheader('Most viewed games on Twitch')
   bar_chart_twitch()

with subcol1:
    st.subheader('Average players per game')
    

with subcol2:
    st.subheader('Average players per day')
    


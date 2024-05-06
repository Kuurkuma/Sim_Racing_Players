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
df = load_data('data/interim/sim_racing_games-1.0.pkl')


#_________________________

def global_trend_player():
    global_trend = df.groupby('datetime')['players'].mean().reset_index()

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
    st.plotly_chart(fig)

    fig.update_layout(
        title='Global trend of average players',
        yaxis_title='Average players',
        template='plotly_dark',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    
    #return global_trend_player 

st.subheader('Global trend of average players (2013-2023)')
#st.plotly_chart(global_trend_player)

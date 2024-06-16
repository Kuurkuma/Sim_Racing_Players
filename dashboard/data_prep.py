import pandas as pd
import streamlit as st

@st.cache_data
def load_data(data_path: str) -> pd.DataFrame:
   
    data = pd.read_pickle(data_path)
    return data

def get_data_path(local_path: str, net_path: str) -> str:
    
    import os
    if os.path.exists(local_path):
        return local_path
    return net_path

def global_trend(df):
    global_trend = df.groupby('datetime')['players'].mean().reset_index()
    return global_trend

def global_trend_viewers(df):

    global_trend_viewers = df[df['datetime'] >= '2015-07-01'] # records of twitch viewers start from July 2015
    global_trend_viewers = global_trend_viewers.groupby('datetime')['twitch_viewers'].mean().reset_index()
    return global_trend_viewers
    

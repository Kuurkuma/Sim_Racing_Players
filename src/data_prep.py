import pandas as pd

def global_trend(df):
    """
    Group data to calculate the average players across all games.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing the data with 'datetime' and 'players' columns.
    
    Returns:
    pd.DataFrame: DataFrame with 'datetime' and average 'players' columns.
    """
    global_trend = df.groupby('datetime')['players'].mean().reset_index()
    return global_trend


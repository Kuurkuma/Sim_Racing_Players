import plotly.graph_objs as go
import plotly.express as px

def global_trend_chart(global_trend):
    """
    Create a line chart for the global trend of average players.
    
    Parameters:
    global_trend (pd.DataFrame): DataFrame with 'datetime' and average 'players' columns.
    
    Returns:
    go.Figure: Plotly figure object with the line chart.
    """
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
        title='Global trend of average players',
        yaxis_title='Average players',
        template='plotly_dark',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    
    return fig

def global_trend_vievers_chart(global_trend_viewers):
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
    return fig

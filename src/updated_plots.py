
import plotly.express as px
from pandas import DataFrame

def plot_promotion_distribution(df: DataFrame):
    fig = px.pie(
        data_frame=df, 
        names="ToBePromoted", 
        title="Promotion Distribution",
        color_discrete_sequence=["#63ad69", "#d62728"]
    )
    return fig

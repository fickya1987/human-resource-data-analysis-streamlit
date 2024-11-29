
import pandas as pd
import streamlit as st
import plots

def render(df: pd.DataFrame):
    st.title("Executive Summary")
    
    # Promotion Analysis Section
    with st.expander("Promotion Analysis Summary"):
        st.markdown("### Promotion Distribution")
        fig = plots.plot_promotion_distribution(df)
        st.plotly_chart(fig, use_container_width=True)

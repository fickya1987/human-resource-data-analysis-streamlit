
import pandas as pd
import streamlit as st
from pandas import DataFrame

def load_transform(file) -> DataFrame:
    """Load the raw data and prepare/transform it"""
    df = pd.read_csv(file)

    # Handle missing data
    df.fillna(0, inplace=True)

    # Feature Engineering for Promotion Analysis
    df['ToBePromoted'] = ((df['YearsSinceLastPromotion'] >= 5) & 
                          (df['PerformanceRating'] > 2)).astype(int)
    return df

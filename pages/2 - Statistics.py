import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from seaborn import heatmap, diverging_palette
import time

import streamlit as st
from st_aggrid import AgGrid

st.set_page_config(layout="wide")

ratings = pd.read_csv("ratings.csv").set_index("Unnamed: 0")
movie_information = pd.read_csv("movie_information.csv").set_index("Unnamed: 0")
df = pd.merge(ratings, movie_information, on="Film")

if "users" not in st.session_state:
    st.session_state["users"] = [x for x in list(ratings.columns) if x not in ["Film"]] 


st.header("Statistics")

correlations, user_correlations, stats = st.tabs(["correlation", "user_correlation", "stats"])

with correlations.container():
    correlations.header("Correlations")
    
    f, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr()

    heatmap(corr, 
                    mask=np.zeros_like(corr, dtype=np.bool), 
                    cmap=diverging_palette(220, 10, as_cmap=True),
                    square=True, 
                    ax=ax)

    correlations.pyplot(f)
    
    with correlations.container():
        correlations.write("")
    

with user_correlations.container():
    user_correlations.header("User Correlations")
    
    user_option = user_correlations.selectbox("Select your user:",
                                              st.session_state["users"]
                                              )
    
    corr = df.corr()[user_option].to_frame()
    
    col1, col2 = user_correlations.columns(2)
    
    col1.dataframe(corr.iloc[0:14],
                    width = 700,
                    height = 550)
    
    col2.dataframe(corr.iloc[15:],
                width = 500,
                height = 750)
    
    with user_correlations.container():
        user_correlations.write("")
    
with stats.container():
    with stats.empty():
        for seconds in range(15):
            stats.write(f"⏳ {seconds} seconds have passed")
            time.sleep(1)
        stats.write("✔️ 1 minute over!")
        
    with stats.container():
        stats.write("")
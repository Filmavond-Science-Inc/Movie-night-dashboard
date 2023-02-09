import pandas as pd
import matplotlib as mpl

import streamlit as st
from st_aggrid import AgGrid

st.set_page_config(layout="wide")

ratings = pd.read_csv("ratings.csv").set_index("Unnamed: 0")
movie_information = pd.read_csv("movie_information.csv").set_index("Unnamed: 0")

   
if "users" not in st.session_state:
    st.session_state["users"] = ['Seb', 'Jos', 'Coen', 'Stijn', 'Merle', 'Twan', 'Annick', 'Guest (gemiddelde)']
   
if "movie_columns" not in st.session_state:
    st.session_state["movie_columns"] = ["Budget", "Cumulative Worldwide Gross", "year", "rating", "votes"]

if "genre_columns" not in st.session_state:
    st.session_state["genre_columns"] = ['Action', 'Adventure', 'Sci-Fi', 'Thriller', 'Drama', 'Romance', 'Horror', 'Mystery', 'Biography',
                                         'Crime', 'History', 'War', 'Western', 'Comedy', 'Music', 'Animation', 'Family', 'Fantasy', 'Sport',
                                         'Musical', 'Documentary']

st.header("Home")

tab1, tab2 = st.tabs(["🗃 Ratings", "📈 Averages"])

with tab1.container():    
    tab1.subheader("Ratings")

    def make_pretty(styler):
        styler.background_gradient(axis=None, vmin=3, vmax=9, cmap="RdYlGn") #RdYlGn
        return styler

    tab1.dataframe(ratings.style.pipe(make_pretty),
                width = 2000,
                height = 3900)

    # AgGrid(ratings, fit_columns_on_grid_load=True) 
    
    with tab1.container():
        tab1.write("\n\n")


with tab2.container():
    tab2.subheader("Averages")

    averages_df = pd.DataFrame()
    averages_df["Film"] = ratings.Film
    averages_df["User Averages"] = list(ratings[st.session_state["users"]].mean(axis=1).values)
    averages_df["IMDB Score"] = movie_information.rating
    averages_df["Differences"] = averages_df["User Averages"] - averages_df["IMDB Score"]

    tab2.dataframe(averages_df.style.background_gradient(axis=0, cmap="RdYlGn"),
                use_container_width = True,
                # width = 800,
                height = 3900
                )

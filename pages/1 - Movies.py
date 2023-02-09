import pandas as pd
import numpy as np

import streamlit as st

# set page configurations. Must be after importing Streamlit
st.set_page_config(layout="wide")

# load data
movie_information = pd.read_csv("movie_information.csv").set_index("Unnamed: 0")
ratings = pd.read_csv("ratings.csv").set_index("Unnamed: 0")

# set session info
if "users" not in st.session_state:
    st.session_state["users"] = ['Seb', 'Jos', 'Coen', 'Stijn', 'Merle', 'Twan', 'Annick', 'Guest (gemiddelde)']
    
if "movie_columns" not in st.session_state:
    st.session_state["movie_columns"] = ["Budget", "Cumulative Worldwide Gross", "year", "rating", "votes"]

if "genre_columns" not in st.session_state:
    st.session_state["genre_columns"] = ['Action', 'Adventure', 'Sci-Fi', 'Thriller', 'Drama', 'Romance', 'Horror', 'Mystery', 'Biography',
                                         'Crime', 'History', 'War', 'Western', 'Comedy', 'Music', 'Animation', 'Family', 'Fantasy', 'Sport',
                                         'Musical', 'Documentary']
    
    
# start of the page
st.header("Movies")

# create tabs
info, genres, synopsis = st.tabs(["Info", "Genres", "Synopsis"])

with info.container():
    info.subheader("IMDB information")
    
    info.dataframe(movie_information[["Film"] + st.session_state["movie_columns"]],
                width = 2000,
                height = 2000,
                use_container_width = True)

with genres.container():
    genres.subheader("Genres")
    genre_options = genres.multiselect(
        "Select your preferred genres:",
        st.session_state["genre_columns"],
        st.session_state["genre_columns"]    
    )    
    
    # TO DO: st.selectbox for selecting using ["AND", "OR", "XOR"}

    row_mask = movie_information[genre_options].any(axis=1)

    genres.dataframe(movie_information[["Film"] + st.session_state["movie_columns"]][row_mask],
                width = 2000,
                height = 2000)

with synopsis.container():    
    synopsis.subheader("Movie synopsis")
    
    selected_IDs = synopsis.multiselect("Select movie ID(s):", movie_information.index)
    
    
    
    for id in selected_IDs:
        synopsis.subheader(movie_information.iloc[id-1].Film + ":  " + str(np.nanmean(list(ratings.iloc[id-1][st.session_state["users"]]))))
        synopsis.write(movie_information.iloc[id-1].synopsis)
    
    # synopsis.dataframe(movie_information[["Film", "synopsis"]].iloc[movie_search],
    #             width = 2000,
    #             height = 2000,
    #             use_container_width = True)
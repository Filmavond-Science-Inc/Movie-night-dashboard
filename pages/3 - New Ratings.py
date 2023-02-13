import pandas as pd
import numpy as np
import re

from imdb import Cinemagoer

import streamlit as st

st.set_page_config(layout="wide")

if "users" not in st.session_state:
    st.session_state["users"] = ['Seb', 'Jos', 'Coen', 'Stijn', 'Merle', 'Twan', 'Annick', 'Guest (Mean)']

if "movie_columns" not in st.session_state:
    st.session_state["movie_columns"] = ["Budget", "Cumulative Worldwide Gross", "year", "rating", "votes"]

if "genre_columns" not in st.session_state:
    st.session_state["genre_columns"] = ['Action', 'Adventure', 'Sci-Fi', 'Thriller', 'Drama', 'Romance', 'Horror', 'Mystery', 'Biography',
                                         'Crime', 'History', 'War', 'Western', 'Comedy', 'Music', 'Animation', 'Family', 'Fantasy', 'Sport',
                                         'Musical', 'Documentary']


# Defining functions

def process_budget(budget):
    budget = re.findall("\d{1,3},{0,1}\d{1,3},{0,1}\d{1,3}", str(budget))
    if budget == []: return float(np.nan)
    else: return float(budget[0].replace(",", ""))
    
def process_director(director):
    director = re.findall("name:_[a-zA-Z ]{0,}", str(director))
    if director == []: return float(np.nan)
    else: return director[0].split("_")[1]

    
    
def retrieve_movie_stats(movie_info, interesting_stats):    
    res = {}
    
    res["Film"] = movie_info["title"]
    
    for key in interesting_stats:
        try:
            if key in movie_info:
                
                if key == "box office":
                    res["Budget"] = process_budget(movie_info[key]["Budget"])
                    
                    if "Cumulative Worldwide Gross" in movie_info[key]: 
                        res["Cumulative Worldwide Gross"] = process_budget(movie_info[key]["Cumulative Worldwide Gross"])
                    else:
                         res["Cumulative Worldwide Gross"] = 0
                        
                elif key == "plot outline":
                    res["synopsis"] = movie_info[key]
                    
                elif key == "director":
                    res[key] = process_director(movie_info[key])
                    
                elif key == "rating":
                    res[key] = float(movie_info[key])
                    
                elif key == "genres":
                    for genre in st.session_state["genre_columns"]:
                        if genre in movie_info[key]:
                            res[genre] = True
                        else:
                            res[genre] = False
                    
                else:                        
                    res[key] = str(movie_info[key])
                    
            # if this information element was not available then still add it
            else:
                res[key] = np.nan
        except:
            res[key] = np.nan
        
    return pd.DataFrame.from_dict(res, orient="index")

# define variables
interesting_stats = ['director', 'box office', 'year', 'rating', 'votes', 'plot outline', 'genres'] 

movies = pd.read_csv("movie_information.csv").set_index("Unnamed: 0")
ratings = pd.read_csv("ratings.csv").set_index("Unnamed: 0")


# Starting the dashboard functionalities
st.header("New ratings")


st.subheader("1. Add the ratings")

new_ratings_dict = dict.fromkeys(st.session_state["users"])
score_cols = st.columns(3)

for i in range(len(st.session_state["users"])):
    user = st.session_state["users"][i]
    new_ratings_dict[st.session_state["users"][i]] = score_cols[i % len(score_cols)].number_input(user+":", min_value=0.0000000, max_value=10.00000)

new_ratings_df = pd.DataFrame.from_dict(new_ratings_dict, orient="index").T
new_ratings_df = new_ratings_df.replace(0, None)

if new_ratings_df.count(axis=0).sum() < 2:    
    st.info(f"You need to add at least 2 ratings. Current number: {new_ratings_df.count(axis=0).sum()}")



st.subheader("2. Select the movie night date")
new_ratings_df["date"] = st.date_input("Date: (YY/MM/DD)")


st.subheader("3. Search for the movie") 
movie_search = st.text_input("Seach movie:")


st.subheader("4. Check if the movie information is correct") 

# What to do once a query has been given
if movie_search != "":   
     
    # create an instance of the Cinemagoer class
    cnm = Cinemagoer()
    
    # search for the movie
    search_result = cnm.search_movie(movie_search)
    st.write()
    
    if search_result[0].values()[0] in list(movies.Film.values):
        st.warning('This movie has already been rated', icon="⚠️")
    
    else:           
        # getting the id
        id = search_result[0].movieID
        
        # get a movie's info
        movie_info = cnm.get_movie(id)
        
        # convert cinemagoer info to a pandas dataframe
        new_movie_information = retrieve_movie_stats(movie_info, interesting_stats)

        # diplay the two dataframes next two each other
        col1, col2 = st.columns(2)   
        with col1:
            st.write("Your movie:")
            st.dataframe(new_movie_information,
                    width = 1500,
                    height = 1053)
        
        with col2:
            "Example movie:"
            st.dataframe(movies.iloc[0],
                    width = 1500,
                    height = 1053) 
            
            
        # finalise the new movie information
        new_movie_information = new_movie_information.T
        new_movie_information.index = [movies.index[-1] + 1]      
        
    
        st.subheader("5. Saving the ratings")
        
        st.write("Check if the following is what you want to save:")
        new_ratings_df["Film"] = movie_info["title"]
        new_ratings_df.index = [ratings.index[-1] + 1] # last index of ratings + 1 is the new index
        
        st.dataframe(pd.concat([ratings, new_ratings_df]),
                    width = 2500)    
        
        add_movie_clicked = st.button("Save ratings")
        
        if add_movie_clicked:
            if new_ratings_df[st.session_state["users"]].count(axis=0).sum() >= 2:   
                
                # save the ratings    
                ratings = pd.concat([ratings, new_ratings_df])
                ratings.to_csv("ratings.csv")
                
                # save the movie information
                movies = pd.concat([movies, new_movie_information])
                movies.to_csv("movie_information.csv")
                
                st.write("Added the movie and ratings!")  
                st.experimental_rerun()        
                

            else:                
                st.warning(f'Not enough ratings added: {new_ratings_df[st.session_state["users"]].count(axis=0).sum()}', icon="⚠️")

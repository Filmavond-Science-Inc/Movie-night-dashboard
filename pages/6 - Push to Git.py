import base64
from github import Github
from github import InputGitTreeElement

import streamlit as st

user = st.text_input("User:")
password = st.text_input("Password:")


button_clicked = st.button("Acces Github")

if button_clicked:
    
    g = Github(user, password)
    st.write(g)
    st.write([repo for repo in g.get_user().get_repos()])
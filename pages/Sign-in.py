import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from pathlib import Path 
import pickle
import time

#Page configuration setup

st.set_page_config(page_title= 'Sign-in', layout='centered', initial_sidebar_state= 'expanded')

# User Authentication

user_data= pd.read_csv("DATA/user_data.csv")


hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""



st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.sidebar.html('''<p data-testid = "stHeader" style="text-align: left; word-spacing: 1100px; font-family: arial; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 1px; color : #626769;">P2S_SOLUTIONS</p>''')

def user_type():
    data = user_data[user_data['Username'] == name]
    for user in data.User_type:
        user_type= user
        return user_type

users= []
user_ids= []
usertypes= []
for user, ids, types in zip(user_data.Username, user_data.User_id, user_data.User_type):
    users.append(user)
    user_ids.append(ids)
    usertypes.append(types)

# Load credentials except passwords

names= users
usernames= user_ids
usertype= usertypes

# Load passwords

file_path = Path("secrets/hashed_pw.pkl")
with file_path.open('rb') as file:
    hashed_passwords= pickle.load(file)


# Transform credentials as a dictionary

credentials = {"usernames":{}}
for un, name, pswd, char in zip(usernames, names, hashed_passwords, usertype):   
    user_dict = {"name":name, "password" : pswd, "role":char}
    credentials["usernames"].update({un:user_dict})

authenticator= stauth.Authenticate(credentials, "", "", cookie_expiry_days=0)


name, authentication_status, username= authenticator.login('main', 'Login')

if authentication_status == False:
    st.error("Invalid Username/Password")



if authentication_status == True:
    st.sidebar.write(f'Welcome **{name}**')
    if user_type() == 'customer':
        st.switch_page("pages/Home-page.py")
    elif user_type() == 'supplier':
        st.switch_page("pages/Supplier-Home-page.py")
    
    elif user_type() == 'Admin':
        st.switch_page("pages/admin_page.py")
    else:
        st.error("Invalid username/password")
   
    
if st.sidebar.button('Main'):
    st.switch_page('Main_page-copy.py')

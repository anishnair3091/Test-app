import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from pathlib import Path 
import pickle   

# User Authentication

user_data= pd.read_csv(r"https://github.com/anishnair3091/My-datas/blob/main/user_data.csv")


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

file_path = Path("https://github.com/anishnair3091/My-datas/blob/main/hashed_pw.pkl")
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
        st.switch_page("https://github.com/anishnair3091/Test-app/raw/refs/heads/pages/Home-page.py")
    elif user_type() == 'supplier':
        st.switch_page("https://github.com/anishnair3091/Test-app/raw/refs/heads/pages/Supplier-Home-page.py")
    
    elif user_type() == 'Admin':
        st.switch_page("https://github.com/anishnair3091/Test-app/raw/refs/heads/pages/admin_page.py")
    else:
        st.error("Invalid username/password")
        
    



if st.sidebar.button('Main'):
    st.switch_page('Main_page-copy.py')
import pandas as pd
import streamlit as st  
from PIL import Image
import streamlit as st
import extra_streamlit_components as stx  
from selenium import webdriver
from rembg import remove
from PIL import Image
import time  
from pathlib import Path  
import streamlit_authenticator as stauth 
import pickle

user_data= pd.read_csv("DATA/user_data.csv")

def authentication_status():
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

	return authentication_status

if authentication_status() == True:
	name= st.session_state["name"]
	st.sidebar.write(f'Welcome {name}')

def usertype():
	data= user_data[user_data['Username'] == name]
	for user in data.User_type:
		user_type= user 
	return user_type

if usertype()== 'Admin':
	st.write("Welcome to admin page")


if st.sidebar.button('Log Out'):
	st.logout()

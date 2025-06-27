import pandas as pd
import streamlit as st  

import streamlit as st
import extra_streamlit_components as stx  
from selenium import webdriver
from rembg import remove
from PIL import Image
import time  
from pathlib import Path  
import streamlit_authenticator as stauth 
import pickle


#Main Page config setup
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

Home= st.Page('pages/Supplier-Home-page.py', title= 'Home page', icon= '🏡')

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


page_bg_head= f"""
<p>P2S</p>
<style>
.st-emotion-cache-gkoddq{{
text-align: left;
color: #7B8181;
}}
"""
st.markdown(page_bg_head, unsafe_allow_html=True)

page_bg_img= f"""
<style>
.st-emotion-cache-1yiq2ps{{
	background-image: url("https://wallpapercat.com/w/full/2/2/9/177444-3840x2160-desktop-4k-clouds-background-image.jpg");
	
	background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;

}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

if usertype() == 'supplier':


	Supplier_Home= st.Page('pages/Supplier-Home-page.py', title= 'Home page', icon= '🏡')



	st.markdown("<h1 style='text-align: center; color : #625656; font-size : 40px '> WELCOME TO COMPANY SERVICE PORTAL</h1>", unsafe_allow_html= True)

	st.markdown("<h1 style='text-align: center; color : #625656; font-size: 25px; '> HOW MAY WE HELP YOU!</h1>", unsafe_allow_html= True)

	st.markdown("<h1 style='text-align: center; color : #625656; font-size: 15px; '> Please choose any of the below options!</h1>", unsafe_allow_html= True)

	
	row1= st.columns(1)

	for col in row1:
		container= col.container(height= 100, border=False)

	col11, col12, col13, col14, col15, col16= st.columns(6, gap= 'large', border=False)



	
		

		

	with col12:
		
		if st.button("**View Tickets**", icon= '📈', use_container_width=True, type='tertiary'):
			st.switch_page("pages/Supplier-View-Tickets-copy.py")
		

	

	with col15:
		if st.button("**View Enquiries**", icon= '📈', use_container_width=True, type= 'tertiary'):
			st.switch_page("pages/Supplier-View-Enquiries-copy.py")


	


	



if st.sidebar.button('Log Out'):
	st.logout()

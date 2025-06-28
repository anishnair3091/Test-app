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
from streamlit_extras.stylable_container import stylable_container


#Main Page config setup
st.set_page_config(page_title= "Customer Home Page", layout='wide', initial_sidebar_state='collapsed')

# User Authentication

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

page_bg_img= f"""
<style>
.st-emotion-cache-1yiq2ps{{
	background-image: url("https://w0.peakpx.com/wallpaper/323/21/HD-wallpaper-plain-white-abstract.jpg");
	
	background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;

}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)



Home= st.Page('pages/Home-page.py', title= 'Home page', icon= '🏡')

def logout():
	signout= st.logout()
	if signout:
		page= st.switch_page("Main_page-copy.py")
		return page
				     

if usertype() == 'customer' or usertype() == 'Admin':


	st.markdown("<h1 style='text-align: center; color : #7B8181; font-size : 40px '> WELCOME TO COMPANY SERVICE PORTAL</h1>", unsafe_allow_html= True)

	

	with stylable_container(
					key= 'button2',
					css_styles=[
					"""
					p {
					font-size: 15px
					
					
					}""",

					""" 

					p:hover {
					font-size: 20px;

					
					
					}""",

					"""
					button {
					border: 1.5px solid #E4A8A8;
					color: #E4A8A8;
					font-size:26px;
					text-align: left;
					text-decoration: none;
					display: inline-block;
					transition-duration: 0.4s;
					cursor: pointer;
					position: left;
					float: left;
					text-align:center;
					width: 180px;
					height: 110px;
					border-radius: 20px;

					}""",
					"""
					button {
					background-color: transparent;
					color: black;
					text-color: #BACBEC;
					border: 1.5px solid gray;
					border-color:gray;
					text-align: center;
					width: 220px;
					height: 180px;
					border-radius: 30px;
					padding-left:10px;
					margin-right:30px;
					margin-left:0px;
					font-size:30px;
					
					}""",
					"""
					button:hover {
					background-color: gray;
					color: white;
					box-shadow: 10px 10px 10px gray;
					border: 1.5px solid none;
					border-color: none;
					shadow: grey;
					text-transform: blue;

					
					}""",
					]
					):


				row1= st.columns(1)

				for col in row1:
					container= col.container(height= 100, border=False)

				col11, col12, col13, col14, col15, col16= st.columns(6, gap= 'large', border=False)



				with col11:


					if st.button("**Create Tickets**",icon='🎫', use_container_width=True, type='tertiary'):
						
						
						st.switch_page("pages/Tickets.py")
					

					

				with col12:
					
					if st.button("**Tickets Dashboard**", icon= '📈', use_container_width=True, type='tertiary'):
						st.switch_page("pages/Tickets-Dashboard.py")
					

				with col13:
					if st.button("**Raise Enquiry**", icon= '📧', use_container_width= True, type='tertiary'):
						st.switch_page("pages/Enquiries.py")


				with col14:
					if st.button("**Enquiry Dashboard**", icon= '📈', use_container_width=True, type= 'tertiary'):
						st.switch_page("pages/Enquiries-Dashboard.py")


				with col15:
					if st.button("**Supplier Performance**", icon='👨‍🏫', use_container_width= True, type= 'tertiary'):
						st.switch_page("pages/performance.py")



				with col16:
					if st.button("**Reports**", icon='📝', use_container_width=True, type='tertiary'):
						st.switch_page("pages/reports.py")

authenticator= create_authenticator()

if st.sidebar.button('Logout'):
	st.logout(location='unrendered')
	st.experimental_rerun()



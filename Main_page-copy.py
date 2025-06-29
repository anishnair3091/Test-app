import pandas as pd
import streamlit as st 
from PIL import Image
import streamlit as st
import extra_streamlit_components as stx  
from selenium import webdriver
from rembg import remove
from PIL import Image
import time  


#Main Page config setup
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

page_bg_img= f"""
<style>
.st-emotion-cache-1yiq2ps{{
	background-image: url("https://w0.peakpx.com/wallpaper/323/21/HD-wallpaper-plain-white-abstract.jpg");
	
	background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;

}}
</style>
<div class="st-emotion-cache-1yiq2ps">
<h1>My App<h1>
</div>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

main_page= st.Page("Main_page-copy.py", title= 'Main page', icon= '🏢', )

st.html('''
	<html>
	  <head>
	  <style>
	    h3{
	      word-spacing: 1100px;
	      text-align: left;
	      color: #888E8E;
	      text-shadow: 3px 3px 3px;
	    }
	    :root {
	  --header-height: 50px;
	  --header-height-padded: 59px;
	}
	
	#stHeader {
	    background-repeat: no-repeat;
	    background-size: contain;
	    background-orgin: content-box;
	    background-color: grey;
	    padding-top: var(--header-height);
	}
	  </style>
	</head>
	<body>
	  <h3 data-testid = "stHeader">P2S_SOLUTIONS {userlogin()}</h3>
	</body>
	</html>''')

col1, col2, col3, col4, col5, col6, col7, col8= st.columns(8)

with col7:
	st.page_link('https://www.bmts.ae', label= 'WEBSITE', icon= "🌍")
		
with col8:
	st.page_link('pages/Sign-in.py', label= "SIGN-IN", icon= ':material/login:')
	



st.markdown("<h1 style='text-align: center; color : #625656; font-size : 40px '> WELCOME TO COMPANY SERVICE PORTAL</h1>", unsafe_allow_html= True)

st.markdown("<h1 style='text-align: center; color : #625656; font-size: 15px; '> Please choose any of the below options!</h1>", unsafe_allow_html= True)



row1= st.columns(1)

for col in row1:
	container= col.container(height= 100, border=False)

col11, col12, col13, col14, col15= st.columns(5, gap= 'large', border=False)


with col12:
	
	if st.button("**CUSTOMER PORTAL**", icon= '👨🏻‍💻', use_container_width=True, type='tertiary'):
		st.switch_page("pages/Sign-in.py")
	


with col14:
	if st.button("**SUPPLIER PORTAL**", icon= '🚛', use_container_width=True, type= 'tertiary'):
		st.switch_page("pages/Sign-in.py")




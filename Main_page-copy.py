import pandas as pd
import streamlit as st 
from PIL import Image
import streamlit as st
import extra_streamlit_components as stx  
from selenium import webdriver
from rembg import remove
from PIL import Image
import time  
from streamlit_extras.stylable_container import stylable_container


#Main Page config setup
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

hide_st_style = “”"

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

“”"
st.markdown(hide_st_style, unsafe_allow_html=True)

page_bg_img= f"""
<style>
.st-emotion-cache-1yiq2ps{{
	background-image: url("https://wallpapercave.com/wp/wp2912405.jpg");
	
	background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;

}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

main_page= st.Page("Main_page-copy.py", title= 'Main page', icon= '🏢', )


col1, col2, col3, col4, col5, col6, col7, col8= st.columns(8)

with col1:
	st.html(F'''<p data-testid = "stHeader" style="text-align: left; word-spacing: 1100px; font-family: arial; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 1px; color : #626769;">P2S_SOLUTIONS</p>''')

with col7:
	st.page_link('https://www.bmts.ae', label= 'WEBSITE', icon= "🌍")
		
with col8:
	st.page_link('pages/Sign-in.py', label= "SIGN-IN", icon= ':material/login:')



	



st.markdown("<h1 style='text-align: center; color : #626769; font-size : 40px '> WELCOME TO COMPANY SERVICE PORTAL</h1>", unsafe_allow_html= True)

st.markdown("<h1 style='text-align: center; color : #626769; font-size: 15px; '> Please choose any of the below options!</h1>", unsafe_allow_html= True)



row1= st.columns(1)

for col in row1:
	container= col.container(height= 100, border=False)

col11, col12, col13, col14, col15= st.columns(5, gap= 'large', border=False)

with col12:
	with stylable_container(

		key= 'button',
		css_styles=[
		"""
		p {
		font-size: 15px
		}""",

		""" 
		button {
		border: 1.5px solid #626769;
		color: #BACBEC;
		font-size:30px;
		text-align: left;
		text-decoration: none;
		display: inline-block;
		transition-duration: 0.4s;
		cursor: pointer;
		position: relative;
		
		text-align:center;
		width: 180px;
		height: 90px;
		border-radius: 20px;

		}""",
		"""
		button {
		background-color: transparent;
		color: #626769;
		text-color: #BACBEC;
		border: 1.5px solid none;
		border-color:none;
		text-align: center;
		icon-align:left;
		width: 200px;
		height: 200px;
		border-radius: 30px;
		padding-left:10px;
		margin-right:30px;
		margin-left:0px;
		font-size:30px;
		position: relative;
		
		}""",
		"""
		button:hover {
		background-color:  #CAE1E2;
		color: #626769;
		font-weight:bolder;
		border: 3.5px solid transparent;
		border-color: none;
		shadow: grey;
		text-transform: blue;
		box-shadow:5px 5px 5px 5px;
		shadow-color: #BACBEC;
		
		
		}""",
		
		]


		):


		
			
			if st.button("**CUSTOMER PORTAL**", icon= '👨🏻‍💻', use_container_width=True, type= 'tertiary'):
				st.switch_page("pages/Sign-in.py")
			


with col14:

	with stylable_container(

		key= 'button2',
		css_styles=[
		"""
		p {
		font-size: 15px
		}""",

		""" 
		button {
		border: 1.5px solid #626769;
		color: #BACBEC;
		font-size:30px;
		text-align: left;
		text-decoration: none;
		display: inline-block;
		transition-duration: 0.4s;
		cursor: pointer;
		position: relative;
		
		text-align:center;
		width: 180px;
		height: 90px;
		border-radius: 20px;

		}""",
		"""
		button {
		background-color: transparent;
		color: #626769;
		text-color: #BACBEC;
		border: 1.5px solid none;
		border-color:none;
		text-align: center;
		icon-align:left;
		width: 200px;
		height: 200px;
		border-radius: 30px;
		padding-left:10px;
		margin-right:30px;
		margin-left:0px;
		font-size:30px;
	        position: relative;
		
		}""",
		"""
		button:hover {
		background-color: #CAE1E2;
		color: #626769;
		font-weight:bolder;
		border: 3.5px solid transparent;
		border-color: none;
		shadow: grey;
		text-transform: blue;
		box-shadow:5px 5px 5px 5px;
		shadow-color: #BACBEC;
		
		
		}""",
		
		]


		):

		if st.button("**SUPPLIER PORTAL**", icon= '🚛', use_container_width=True, type= 'tertiary'):
			st.switch_page("pages/Sign-in.py")




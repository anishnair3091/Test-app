import streamlit as st  
import pandas as pd  
import numpy as np 
import matplotlib.pyplot as plt  
import seaborn as sns; sns.set()
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt 
import matplotlib
from sklearn.preprocessing import LabelEncoder
import datetime
import folium
from streamlit_folium import st_folium
import pickle
from pathlib import Path 
import streamlit_authenticator as stauth
from streamlit_extras.stylable_container import stylable_container

Home= st.Page('pages/Tickets-Dashboard.py', title= 'Home page', icon= '🏡')

if st.sidebar.button('Home', icon= '🏡'):
	st.switch_page(Home)

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

    file_path = Path("/Users/anishmnair/Desktop/Streamlit/My_new_app/Customer-app/New/secrets/hashed_pw.pkl")
    with file_path.open('rb') as file:
        hashed_passwords= pickle.load(file)

    # Transform credentials as a dictionary

    credentials = {"usernames":{}}
    for un, name, pswd, char in zip(usernames, names, hashed_passwords, usertype):   
        user_dict = {"name":name, "password" : pswd, "role":char}
        credentials["usernames"].update({un:user_dict})

    authenticator= stauth.Authenticate(credentials, "", "", cookie_expiry_days=30)
    name, authentication_status, username= authenticator.login('main', 'Login')
    return authentication_status

if st.session_state['authentication_status']:

	our_data= st.session_state['keys301']
	text = st.session_state['keys401']

data= our_data
text1= text 

history_data= pd.read_csv(r'/Users/anishmnair/Desktop/Streamlit/My_new_app/Customer-app/New/DATA/History.csv')

			
def ticket_num():
	for ref in data.Ticket_ref:
		for num in ref.split('/'):
			tick_num = num  
		return tick_num


st.markdown(f'''<h4 style= "text-align:left; color:#747581; ">{text1}</h4>''', unsafe_allow_html=True)
container = st.container(height= 800, border=False)



with container:

	

	data1 = data.sort_values('Datetime', axis=0, ascending= False, ignore_index=True)

	

	for k in range(0, len(data1)):
		with stylable_container(
				key= f'container{k}',
				css_styles=[
				"""
				p {
				font-size: 18px
				font-color:black;
				word-spacing:10px;
				}""",

				""" 
				[data-testid="stVerticalBlockBorderWrapper"] {
				border: 0.5px solid #BACBEC;
				color: #BACBEC;
				font-size:30px;
				text-align: left;
				text-decoration: none;
				display: inline-block;
				transition-duration: 0.4s;
				cursor: pointer;
				position: center;
				float: left;
				text-align:left;
				width: 80px;
				height: 90px;
				border-radius: 20px;

				}""",
				"""
				[data-testid="stVerticalBlockBorderWrapper"] {
				background-color: white;
				color: black;
				text-color: #BACBEC;
				border: 0.5px solid none;
				border-color:none;
				text-align: center;
				width: 1250px;
				height: 130px;
				border-radius: 20px;
				
				font-size:30px;
				
				}""",
				"""
				[data-testid="stVerticalBlockBorderWrapper"]:hover {
				background-color: white;
				color: black;
				font-weight:bolder;
				border: 0.5px solid #BACBEC;
				border-color: #BACBEC;
				box-shadow: 5px 10px 10px #BACBEC;
				text-transform: blue;
				border-radius:15px;
				position: relative;

				
				
				}""",
				
				
				]

				):


			containerk = st.container(border=False)
			with containerk:
			
				col1, col2, col3= st.columns([.10, .80, .10], gap='small', border=False)
				if data1['Status'][k] == 'Open':

					if data1['Priority'][k] == 'P1':
						col1.html(f'''<p style= "text-align: center;">Ref: {ticket_num()}</p><p style= "text-align: center; color:black; background-color: #F3D6B2; border-radius: 5px;">{data1.Status[k]}</p><p style= "text-align: center; background-color: #DA9595; border-radius: 5px;">{data1.Priority[k]}</p>''')
						

						col2.html(f'''<p style= "text-align: left; font-size: 15px; text-indent: 30px; font-family:Monospace;">{data1['Troubles_Name'][k]}</p>''')

						option= col3.button(f'''View''', icon='👉🏻', type='tertiary', key=f'key{k}')

					
					elif data1['Priority'][k] == 'P2':
						col1.html(f'''<p style= "text-align: center;">Ref: {ticket_num()}</p><p style= "text-align: center; color:black; background-color: #F3D6B2; border-radius: 5px;">{data1.Status[k]}</p><p style= "text-align: center; background-color: #ECECAA; border-radius: 5px;">{data1.Priority[k]}</p>''')
						

						col2.html(f'''<p style= "text-align: left; font-size: 15px; text-indent: 30px; font-family:Monospace;">{data1['Troubles_Name'][k]}</p>''')

						option= col3.button(f'''View''', icon='👉🏻', type='tertiary', key=f'key{k}')
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')

					elif data1['Priority'][k] == 'P3':
						col1.html(f'''<p style= "text-align: center;">Ref: {ticket_num()}</p><p style= "text-align: center; color:black; background-color: #F3D6B2; border-radius: 5px;">{data1.Status[k]}</p><p style= "text-align: center; background-color: #BFD5DA; border-radius: 5px;">{data1.Priority[k]}</p>''')
						

						col2.html(f'''<p style= "text-align: left; font-size: 15px; text-indent: 30px; font-family:Monospace;">{data1['Troubles_Name'][k]}</p>''')

						option= col3.button(f'''View''', icon='👉🏻', type='tertiary', key=f'key{k}')
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')

				elif data1['Status'][k] == 'Close':
					if data1['Priority'][k] == 'P1':
						col1.html(f'''<p style= "text-align: center;">Ref: {ticket_num()}</p><p style= "text-align: center; color:black; background-color: #C8E490; border-radius: 5px;">{data1.Status[k]}</p><p style= "text-align: center; background-color: #DA9595; border-radius: 5px;">{data1.Priority[k]}</p>''')
						

						col2.html(f'''<p style= "text-align: left; font-size: 15px; text-indent: 30px; font-family:Monospace;">{data1['Troubles_Name'][k]}</p>''')

						option= col3.button(f'''View''', icon='👉🏻', type='tertiary', key=f'key{k}')

					
					elif data1['Priority'][k] == 'P2':
						col1.html(f'''<p style= "text-align: center;">Ref: {ticket_num()}</p><p style= "text-align: center; color:black; background-color: #C8E490; border-radius: 5px;">{data1.Status[k]}</p><p style= "text-align: center; background-color: #ECECAA; border-radius: 5px;">{data1.Priority[k]}</p>''')
						

						col2.html(f'''<p style= "text-align: left; font-size: 15px; text-indent: 30px; font-family:Monospace;">{data1['Troubles_Name'][k]}</p>''')

						option= col3.button(f'''View''', icon='👉🏻', type='tertiary', key=f'key{k}')
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')

					elif data1['Priority'][k] == 'P3':
						col1.html(f'''<p style= "text-align: center;">Ref: {ticket_num()}</p><p style= "text-align: center; color:black; background-color: #C8E490; border-radius: 5px;">{data1.Status[k]}</p><p style= "text-align: center; background-color: #BFD5DA; border-radius: 5px;">{data1.Priority[k]}</p>''')
						

						col2.html(f'''<p style= "text-align: left; font-size: 15px; text-indent: 30px; font-family:Monospace;">{data1['Troubles_Name'][k]}</p>''')

						option= col3.button(f'''View''', icon='👉🏻', type='tertiary', key=f'key{k}')
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')



		



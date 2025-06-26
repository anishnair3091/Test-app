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


#Page config setup

st.set_page_config('Tickets_Dashboard', layout='wide', initial_sidebar_state= 'collapsed')

st.markdown('''<h3 style= "text-align:left; color:#8C98AF; ">WELCOME TO TICKET DASHBOARD</h3>''', unsafe_allow_html=True)

Home= st.Page('pages/Supplier-Home-page.py', title= 'Home page', icon= '🏡')

Ticket_page = st.Page('pages/Supplier-View-Tickets-copy.py', title= 'View Tickets', icon = '📈')

if st.sidebar.button('Home', icon= '🏡'):
	st.switch_page(Home)


history_data= pd.read_csv(r'/Users/anishmnair/Desktop/Streamlit/My_new_app/Customer-app/New/DATA/History.csv')


performance_data= history_data[['AMC_Company', 'Ticket_ref', 'Response_time_difference']].groupby(['AMC_Company']).count().reset_index()

performances= performance_data.Response_time_difference/performance_data.Ticket_ref

dfs= performances.to_frame()

perform_data= pd.concat([performance_data, dfs], axis=1)

perform_data.columns= ['AMC_Company', 'Ticket_ref', 'Response_time_difference', 'Performance']

AMC_data= pd.read_csv(r"/Users/anishmnair/Desktop/Streamlit/My_new_app/Customer-app/New/DATA/AMC.csv")

times= []
data= history_data[history_data['Status'] == 'Open']
for time in pd.to_datetime(data['Response']):
    current_time = datetime.datetime.now()
    time_diff = time- current_time
    times.append(time_diff.total_seconds())

data['Time_remaining_secs']= times

times1= []
data1= history_data[history_data['Status'] == 'Close']
for time, his in zip(pd.to_datetime(data1['Response']), pd.to_datetime(data1['Actual_Completion_time'])) :
    
    time_diff = time- his
    times1.append(time_diff.total_seconds())

data1['Time_remaining_secs']= times1

history_data = pd.concat([data1, data], axis= 0)

#To distinguish tickets based on SLA status

SLAs = []
for secs in history_data['Time_remaining_secs']:
	if secs > 0:
		SLA= 'SLA met'
		SLAs.append(SLA)
	elif secs <= 0:
		SLA= 'SLA not met'
		SLAs.append(SLA)

history_data['SLA'] = SLAs

dummies = pd.get_dummies(history_data['SLA'])

encoder= LabelEncoder()
encoder.fit(dummies['SLA met'])

history_data['SLA met'] = encoder.transform(dummies['SLA met'])

encoder= LabelEncoder()
encoder.fit(dummies['SLA not met'])
history_data['SLA not met']= encoder.transform(dummies['SLA not met'])

#To extract the integer part from the ticket

ticks= []
for ref in history_data['Ticket_ref']:
    for number in ref.split("/"):
        tick= number
    ticks.append(tick)

history_data['Ticket_num']= ticks

# To extract the week number
week_num= []
for date in pd.to_datetime(history_data['Date']):
    week = date.strftime("%W")
    week_num.append(week)

history_data['Week']= week_num



# To Open & Close columns

dummy_variable = pd.get_dummies(history_data.Status)

encoder= LabelEncoder()
encoder1= LabelEncoder()
encoder.fit(dummy_variable.Close)
encoder1.fit(dummy_variable.Open)
dummy_variable['Close']= encoder.transform(dummy_variable.Close)
dummy_variable['Open']= encoder.transform(dummy_variable.Open)

history_data.Open= dummy_variable.Open
history_data.Close= dummy_variable.Close

Datetime= []
for date, time in zip(history_data['Date'], history_data['Time']):
    my_datetime_str= date + ' ' + time
    my_datetime= pd.to_datetime(my_datetime_str)
    Datetime.append(my_datetime)

history_data['Datetime']= Datetime


team_list= pd.read_csv(r"/Users/anishmnair/Desktop/Streamlit/My_new_app/BMTS-APP/Service/Team_list.csv", skiprows=1)


user_data= pd.read_csv(r"/Users/anishmnair/Desktop/Streamlit/My_new_app/Customer-app/New/DATA/user_data.csv")



# User Authentication

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

    file_path = Path("/Users/anishmnair/Desktop/Streamlit/My_new_app/BMTS-APP/secrets/hashed_pw.pkl")
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

# Defining name

if authentication_status() == True:
    name= st.session_state["name"]
    st.sidebar.write(f'Welcome **{name}**')
    
def user_type():
    data = user_data[user_data['Username'] == name]
    for user in data.User_type:
        usertype= user
    return usertype

def load_data(nrows):
	data = pd.read_csv(r"/Users/anishmnair/Desktop/Streamlit/My_new_app/Customer-app/New/DATA/History.csv")
	data1 = data[data['AMC_Company'] == name]
	return data1 
	


data = load_data(1000)


def data_table(nrows):
	data_table= data[['AMC_Company', 'Close', 'Open']].groupby(['AMC_Company']).sum().reset_index()
	return data_table


data_table= data_table(100)

def trouble_data(nrows):
	trouble_data= data['Troubles_Name'].value_counts().to_frame().reset_index()
	trouble_data = trouble_data.head(6)
	return trouble_data
	

def project_trouble(nrows):
	project_trouble= data['Project'].value_counts().to_frame().reset_index()
	project_trouble= project_trouble.head(6)
	return project_trouble
	

trouble= trouble_data(13)
project= project_trouble(13)


def handle_action(action):
	st.page_link("pages/BMTS-view tickets.py")




def area_chart():
	hist_sum_person = data[['Date', 'AMC_Company', 'Status']].groupby(['Date', 'AMC_Company']).count().reset_index()
	fig= plt.figure(figsize=(4, 3))
	fig = px.area(hist_sum_person, x = 'Date', y = 'Status', color= 'AMC_Company', line_group= 'AMC_Company')
	return fig 	

def view_data(k):
	view_data= data.iloc[[k]]
	return view_data
	

def top_performer():
	data = perform_data[perform_data['Performance'] == perform_data['Performance'].max()]
	for person in data.AMC_Company:
		performer= person 
	return performer

		
# Facetted Subplots

history_data_total = data[['AMC_Company', 'Status', 'Ticket_ref', 'Weekday', 'Week']].groupby(['AMC_Company', 'Status', 'Week','Weekday']).count().reset_index()

history_data_total_week = history_data_total[history_data_total['Week'] == history_data_total['Week'].max()]

total_tickets= data[['Day', 'Ticket_ref']].groupby(['Day']).count().reset_index()

open_tickets= data[['Day', 'Open']].groupby(['Day']).sum().reset_index()

close_tickets= data[['Day', 'Close']].groupby(['Day']).sum().reset_index()

progress_data= data[data['Status'] == 'In progress']

progress_tickets = progress_data[['Day', 'Status']].groupby(['Day']).count().reset_index()	

#To display SLA status chart and table

SLA_summary= load_data(100)[['AMC_Company', 'Ticket_ref', "Status", 'SLA', 'Day', 'Open', 'Close', 'SLA met', 'SLA not met']].groupby(['AMC_Company', 'Ticket_ref', 'Status', 'SLA']).sum().reset_index()

SLA_table= SLA_summary[['AMC_Company', 'Open', 'Close', 'SLA met', 'SLA not met']].groupby(['AMC_Company']).sum().reset_index()

SLA_chart= SLA_summary[[ 'Open', 'Close', 'Day', 'SLA met', 'SLA not met']].groupby(['Day']).sum().reset_index()

data= load_data(100)
open_data = data[data['Status'] == 'Open']

data1 = open_data.sort_values('Date', ascending=False, axis=0, ignore_index= True)

if st.session_state['authentication_status']:
	if user_type() == 'supplier' or user_type() == 'Admin':


		st.markdown('''<h5 style= "text-align:center; color:white; background-color:#747581;">ALL OPEN TICKETS</h5>''', unsafe_allow_html=True)
		container = st.container(height= 500, border=True)

		
		
		with container:

			col1, col2, col3, col4, col5 = st.columns(5)

			data1 = data.sort_values('Datetime', axis=0, ascending= False, ignore_index=True)

			with col1:

				for k in range(0, (len(data1))//5):
					if data1['Priority'][k] == 'P1':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :red-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')
					
					elif data1['Priority'][k] == 'P2':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :green-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')

					elif data1['Priority'][k] == 'P3':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :blue-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')


			with col2:

				for k in range((len(data1))//5, ((len(data1))//5)+ (len(data1)//5)):
					if data1['Priority'][k] == 'P1':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :red-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')
					
					elif data1['Priority'][k] == 'P2':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :green-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')

					elif data1['Priority'][k] == 'P3':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :blue-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')
			
			
			with col3:

				for k in range(((len(data1)//5)+ (len(data1)//5)), (len(data1) - ((len(data1)//5) + (len(data1)//5)))):
					if data1['Priority'][k] == 'P1':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :red-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')
					
					elif data1['Priority'][k] == 'P2':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :green-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')

					elif data1['Priority'][k] == 'P3':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :blue-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')

			with col4:

				for k in range((len(data1) - ((len(data1)//5) + (len(data1)//5))), (len(data1) - len(data1)//5)):
					if data1['Priority'][k] == 'P1':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :red-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')
					
					elif data1['Priority'][k] == 'P2':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :green-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')

					elif data1['Priority'][k] == 'P3':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :blue-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')

			with col5:

				for k in range((len(data1) - len(data1)//5), len(data1)):
					if data1['Priority'][k] == 'P1':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :red-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')
					
					elif data1['Priority'][k] == 'P2':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :green-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')

					elif data1['Priority'][k] == 'P3':
						option=  st.button(f''':red-background[```{data1.Ticket_ref[k]}```] :blue-background[```{data1.Status[k]}```]\n :blue-badge[**{data1.Priority[k]}**]''', key=k)
						if option:
							history_1 = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							
							df = history_1
							st.session_state.df = df
							st.session_state['keys101'] = history_data[history_data['Ticket_ref'] == data1.Ticket_ref[k]]
							st.switch_page('pages/Customer-view-tickets.py')


		container= st.container(height= 250, border=True)
		
		with container:
			col6, col7 = st.columns(2)

			with col6:

				st.markdown('''<h5 style= "text-align:center; color:white; background-color:#DEADAD;"> ENQUIRIES RESPONSE TIME EXPIRED</h5>''', unsafe_allow_html=True)
				container= st.container(height=220, border=True)
				with container:
					
					row1= st.columns(1)

			with col7:

				st.markdown('''<h5 style= "text-align:center; color:white; background-color:#E6E593;"> ENQUIRIES RESPONSE TIME ABOUT TO EXPIRE</h5>''', unsafe_allow_html=True)
				container= st.container(height=220, border=True)
				with container:
					
					row1= st.columns(1)

	

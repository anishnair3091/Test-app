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


st.markdown('''<h3 style= "text-align:left; color:#8C98AF; ">ENQUIRIES DASHBOARD</h3>''', unsafe_allow_html=True)

Home= st.Page('pages/Supplier-Home-page.py', title= 'Home page', icon= '🏡')

Enquiry_page = st.Page('pages/Supplier-View-Enquiries-copy.py', title= 'View Enquiries', icon = '📈')

if st.sidebar.button('Home', icon= '🏡'):
	st.switch_page(Home)


enquiry_data= pd.read_csv(r"/Users/anishmnair/Desktop/Streamlit/My_new_app/Customer-app/New/DATA/enquiry_data.csv")


group = enquiry_data[['Company', 'SLA met', 'SLA not met']].groupby(['Company']).sum().reset_index()

group1 = enquiry_data[['Company', 'Enquiry_ref']].groupby(['Company']).count().reset_index()

group['Enquiry_count']= group1['Enquiry_ref']

group['SLA marks']= group['SLA met']/group['Enquiry_count']

AMC_data= pd.read_csv(r"/Users/anishmnair/Desktop/Streamlit/My_new_app/Customer-app/New/DATA/AMC.csv")


times2= []
data2= enquiry_data[enquiry_data['Enquiry status'] == 'Quoted']
for time, his in zip(pd.to_datetime(data2['Response']), pd.to_datetime(data2['Actual_Completion_time'])) :
    
    time_diff = time- his
    times2.append(time_diff.total_seconds())

data2['Time_remaining_secs']= times2



#To distinguish tickets based on SLA status

SLAs = []
for secs in enquiry_data['Time_remaining_secs']:
	if secs > 0:
		SLA= 'SLA met'
		SLAs.append(SLA)
	elif secs <= 0:
		SLA= 'SLA not met'
		SLAs.append(SLA)

enquiry_data['SLA'] = SLAs

dummy_variable= pd.get_dummies(enquiry_data['Enquiry status'])
encoder1= LabelEncoder()
encoder2= LabelEncoder()
encoder3= LabelEncoder()

encoder1.fit(dummy_variable['Under review'])
encoder2.fit(dummy_variable['Moved for estimation'])
encoder3.fit(dummy_variable['Quoted'])
enquiry_data['Under review']= encoder1.transform(dummy_variable['Under review'])
enquiry_data['Moved for estimation']= encoder2.transform(dummy_variable['Moved for estimation'])
enquiry_data['Quoted'] = encoder3.transform(dummy_variable['Quoted'])

dummy_variable2= pd.get_dummies(enquiry_data['SLA'])
encoder3= LabelEncoder()
encoder4= LabelEncoder()

encoder3.fit(dummy_variable2['SLA met'])
encoder4.fit(dummy_variable2['SLA not met'])
enquiry_data['SLA met'] = encoder3.transform(dummy_variable2['SLA met'])
enquiry_data['SLA not met'] = encoder4.transform(dummy_variable2['SLA not met'])

#To extract the integer part from the ticket

ticks= []
for ref in enquiry_data['Enquiry_ref']:
    for number in ref.split("/"):
        tick= number
    ticks.append(tick)

enquiry_data['Ticket_num']= ticks

# To extract the week number
week_num= []
for date in pd.to_datetime(enquiry_data['Created date']):
    week = date.strftime("%W")
    week_num.append(week)

enquiry_data['Week']= week_num




Datetime= []
for date, time in zip(enquiry_data['Created date'], enquiry_data['Time']):
    my_datetime_str= date + ' ' + time
    my_datetime= pd.to_datetime(my_datetime_str)
    Datetime.append(my_datetime)

enquiry_data['Datetime']= Datetime


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
	data = pd.read_csv(r"/Users/anishmnair/Desktop/Streamlit/My_new_app/Customer-app/New/DATA/enquiry_data.csv")
	
	data1 = data[data['Company'] == name]
	data2= data1[data1['Enquiry status'] != 'Quoted']
	return data2
	


data = load_data(1000)


def data_table(nrows):
	data_table= data[['Company', 'Under review', 'Moved for estimation', 'Quoted']].groupby(['Company']).sum().reset_index()
	return data_table


data_table= data_table(100)

def job_type():
	job_data= data['Job type'].value_counts().to_frame().reset_index()
	return job_data
	

def enq_company():
	enqcompany= data['Company'].value_counts().to_frame().reset_index()
	
	return enqcompany
	

jobtype= job_type()
company= enq_company()


def handle_action(action):
	st.page_link("pages/BMTS-view tickets.py")




def area_chart():
	hist_sum_person = data[['Date', 'Company', 'Status']].groupby(['Date', 'Company']).count().reset_index()
	fig= plt.figure(figsize=(4, 3))
	fig = px.area(hist_sum_person, x = 'Date', y = 'Status', color= 'Company', line_group= 'Company')
	return fig 	

def view_data(k):
	view_data= data.iloc[[k]]
	return view_data
	

def top_performer():
	data = group[group['SLA marks'] == group['SLA marks'].max()]
	for company in data.Company:
		performer= company 
	return performer

		
# Facetted Subplots

enquiry_data_total = data[['Company', 'Enquiry status', 'Enquiry_ref', 'Monthname', 'Month']].groupby(['Company', 'Enquiry status', 'Monthname','Month']).count().reset_index()

enquiry_data_total_month = enquiry_data_total[enquiry_data_total['Month'] == enquiry_data_total['Month'].max()]

total_enquiries= data[['Day', 'Enquiry_ref']].groupby(['Day']).count().reset_index()

awaiting_response= data[['Day', 'Under review']].groupby(['Day']).sum().reset_index()

quote_received= data[['Day', 'Quoted']].groupby(['Day']).sum().reset_index()

progress_data= data[['Day', 'Moved for estimation']].groupby(['Day']).sum().reset_index()

	

#To display SLA status chart and table

SLA_summary= load_data(100)[['Company', 'Enquiry_ref', "Enquiry status", 'SLA', 'Day', 'Under review', 'Moved for estimation', 'Quoted', 'SLA met', 'SLA not met']].groupby(['Company', 'Enquiry_ref', 'Enquiry status', 'SLA']).sum().reset_index()

SLA_table= SLA_summary[['Company', 'Under review', 'Moved for estimation', 'Quoted', 'SLA met', 'SLA not met']].groupby(['Company']).sum().reset_index()

SLA_chart= SLA_summary[[ 'Under review', 'Moved for estimation', 'Quoted', 'Day', 'SLA met', 'SLA not met']].groupby(['Day']).sum().reset_index()

data= load_data(100)
open_data = data[data['Enquiry status'] == 'Under review']

data1 = open_data.sort_values('Created date', ascending=False, axis=0, ignore_index= True)

if st.session_state['authentication_status']:
	if user_type() == 'supplier' or user_type() == 'Admin':


		button_data= load_data(1000)

		data= load_data(1000)

		sorted_data= data.sort_values('Datetime', axis= 0, ascending = False, ignore_index= True)

		for sla in sorted_data['SLA']:
			if sla == 'SLA met':
				slas = 'SLA not exceeded' 
				sorted_data['SLA'].replace(sla, slas, inplace=True)

			elif sla == 'SLA not met':
				slas = 'SLA exceeded'
				sorted_data['SLA'].replace(sla, slas, inplace=True)



		container = st.container(height= 800, border= False)
		with container:

			col1, col2, col3 = st.columns(3, gap='small', border=False)

			with col1:
				
				for i in range(0, (len(sorted_data))//3):
					data1= AMC_data[AMC_data['SYSTEM SHORTFORM'] == sorted_data['System'][i]]
					for sys in data1['SYSTEM']:
						systemname = sys
					
				
					containeri = st.container(height=100, border=True)
					with containeri:
						col5, col6= st.columns([.25, .75])

						current_datetime= pd.to_datetime((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
						time= []
						for datetimes in pd.to_datetime(sorted_data['Datetime']):
							time_diff= (current_datetime- datetimes).total_seconds()
							time.append(time_diff)
						with col5:
							if time[i] < 14400:
								option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
								:blue-badge[New]  
								:orange-badge[View]''', type='tertiary')
								if option:
									enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
									
									df = enquiry_1
									st.session_state.df = df
									st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
									st.switch_page('pages/Supplier-each-enquiries-copy.py')
							else:
								if sorted_data['Enquiry status'][i] == 'Under review':
									option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
										:red-badge[Open]  
										:orange-badge[View]''', type='tertiary')
									if option:
										enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										
										df = enquiry_1
										st.session_state.df = df
										st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										st.switch_page('pages/Supplier-each-enquiries-copy.py')
								if sorted_data['Enquiry status'][i] == 'Moved for estimation':
									option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
										:orange-badge[Progress]  
										:orange-badge[View]''', type='tertiary')
									if option:
										enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										
										df = enquiry_1
										st.session_state.df = df
										st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										st.switch_page('pages/Supplier-each-enquiries-copy.py')
								if sorted_data['Enquiry status'][i] == 'Quoted':
									option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
										:green-badge[Done]  
										:orange-badge[View]''', type='tertiary')
									if option:
										enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										
										df = enquiry_1
										st.session_state.df = df
										st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										st.switch_page('pages/Supplier-each-enquiries-copy.py')
						with col6:
							st.markdown(f''' {sorted_data['Job type'][i]} -    {sorted_data['Scope'][i]}  
								```{sorted_data['Company'][i]}```   ```{sorted_data['Organization'][i]}```''', unsafe_allow_html= True)
		 
			with col2:
				
				for i in range((len(sorted_data))//3, (len(sorted_data) - (len(sorted_data))//3)):
					data1= AMC_data[AMC_data['SYSTEM SHORTFORM'] == sorted_data['System'][i]]
					for sys in data1['SYSTEM']:
						systemname = sys
					
				
					containeri = st.container(height=100, border=True)
					with containeri:
						col5, col6= st.columns([.25, .75])

						current_datetime= datetime.datetime.now()
						for datetimes in pd.to_datetime(sorted_data['Datetime']):
							time_diff= (current_datetime- datetimes).total_seconds()
						with col5:
							if time_diff < 14400:
								option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
								:blue-badge[New]  
								:orange-badge[View]''', type='tertiary')
								if option:
									enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
									
									df = enquiry_1
									st.session_state.df = df
									st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
									st.switch_page('pages/Supplier-each-enquiries-copy.py')
							else:
								if sorted_data['Enquiry status'][i] == 'Under review':
									option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
										:red-badge[Open]  
										:orange-badge[View]''', type='tertiary')
									if option:
										enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										
										df = enquiry_1
										st.session_state.df = df
										st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										st.switch_page('pages/Supplier-each-enquiries-copy.py')
								if sorted_data['Enquiry status'][i] == 'Moved for estimation':
									option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
										:orange-badge[Progress]  
										:orange-badge[View]''', type='tertiary')
									if option:
										enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										
										df = enquiry_1
										st.session_state.df = df
										st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										st.switch_page('pages/Supplier-each-enquiries-copy.py')
								if sorted_data['Enquiry status'][i] == 'Quoted':
									option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
										:green-badge[Done]  
										:orange-badge[View]''', type='tertiary')
									if option:
										enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										
										df = enquiry_1
										st.session_state.df = df
										st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										st.switch_page('pages/Supplier-each-enquiries-copy.py')
						with col6:
							st.markdown(f''' {sorted_data['Job type'][i]} -    {sorted_data['Scope'][i]}  
								```{sorted_data['Company'][i]}```   ```{sorted_data['Organization'][i]}```''', unsafe_allow_html= True)
		 
			with col3:
				
				for i in range((len(sorted_data) - (len(sorted_data))//3), len(sorted_data)):
					data1= AMC_data[AMC_data['SYSTEM SHORTFORM'] == sorted_data['System'][i]]
					for sys in data1['SYSTEM']:
						systemname = sys

					containeri = st.container(height=100, border=True)
					with containeri:
						col5, col6= st.columns([.25, .75], gap= 'small')
						current_datetime= datetime.datetime.now()
						for datetimes in pd.to_datetime(sorted_data['Datetime']):
							time_diff= (current_datetime- datetimes).total_seconds()
						with col5:
							if time_diff < 14400:
								option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
								:blue-badge[New]  
								:orange-badge[View]''', type='tertiary')
								if option:
									enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
									
									df = enquiry_1
									st.session_state.df = df
									st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
									st.switch_page('pages/Supplier-each-enquiries-copy.py')
							else:
								if sorted_data['Enquiry status'][i] == 'Under review':
									option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
										:red-badge[Open]  
										:orange-badge[View]''', type='tertiary')
									if option:
										enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										
										df = enquiry_1
										st.session_state.df = df
										st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										st.switch_page('pages/Supplier-each-enquiries-copy.py')
								if sorted_data['Enquiry status'][i] == 'Moved for estimation':
									option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
										:orange-badge[Progress]  
										:orange-badge[View]''', type='tertiary')
									if option:
										enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										
										df = enquiry_1
										st.session_state.df = df
										st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										st.switch_page('pages/Supplier-each-enquiries-copy.py')
								if sorted_data['Enquiry status'][i] == 'Quoted':
									option= st.button(f'''```{sorted_data['Enquiry_ref'][i]}```  
										:green-badge[Done]  
										:orange-badge[View]''', type='tertiary')
									if option:
										enquiry_1 = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										
										df = enquiry_1
										st.session_state.df = df
										st.session_state['keys201'] = enquiry_data[enquiry_data['Enquiry_ref'] == sorted_data.Enquiry_ref[i]]
										st.switch_page('pages/Supplier-each-enquiries-copy.py')

						with col6:
							st.markdown(f''' {sorted_data['Job type'][i]} -    {sorted_data['Scope'][i]}  
								```{sorted_data['Company'][i]}```   ```{sorted_data['Organization'][i]}```''', unsafe_allow_html= True)

							


						
import streamlit as st
from dotenv import load_dotenv
from os import getenv
import pandas as pd
import requests
import json
import datetime
import seaborn as sns

st.title('NASA Near Earth Objects Application')
st.write('''
        **This application utilizes Pandas, Streamlit, Seaborn and Python to intake a date 
        and user API key for a day\'s worth of data on Near Earth Objects.**
        ''')
st.write('Please note that this application only allows searches for the last calendar year.')


st.header('Getting Started')
st.write('''
         In order to utilize this application, you will need an API key from NASA. 
         NASA\'s has an open API and keys are free and available to the public. 
         Please use the button below to go to NASA\'s website to register for a key.''')
st.link_button('Get NASA API Key', 'https://api.nasa.gov/', help='This button will take you to NASA\'s website.')
st.write("""
         Below are examples of what can be done on the history and visualizations pages.
         """)

load_dotenv()
api_key = getenv('MY_API_KEY')

url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date=2023-06-10&end_date=2023-06-10&api_key={api_key}'
my_neows = requests.get(url)
df = pd.DataFrame(my_neows.json()['near_earth_objects']['2023-06-10'])
df = df[['is_potentially_hazardous_asteroid']]
df.rename(columns={'is_potentially_hazardous_asteroid': 'Potentially Hazardous Asteroids'}, inplace=True)
df['Potentially Hazardous Asteroids'] = df['Potentially Hazardous Asteroids'].replace({True: 'True', False: 'False'})


history_url = f'http://api.nasa.gov/neo/rest/v1/neo/3735684?api_key={api_key}'
my_history = requests.get(history_url)

st.subheader('History Example')
neow_name = my_neows.json()['near_earth_objects']['2023-06-10'][0]['name']
st.write(f'**History of Near Earth Object {neow_name}**')

history_df = pd.DataFrame(my_history.json()['close_approach_data'])
history_df.rename(columns={'close_approach_date': "Close Approach Date"}, inplace=True)
history_df[['Close Approach Date']]


st.subheader('Visualization Example')
x='Potentially Hazardous Asteroids'
month_date_str = 'June 10, 2023'
plot = sns.histplot(data=df, x=x, discrete=True)
plot.set(yticks=range(0, int(max(plot.get_yticks()))+5, 5))
st.write(f'**{x} on {month_date_str}**')
st.pyplot(plot.get_figure())
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
        for a day\'s worth of data on Near Earth Objects.**
        ''')



st.header('Getting Started')
st.write('''
         The National Aeronautics and Space Administration (NASA)'s mission statement is to drive advances
         in science, technology, aeronautics, and space exploration to enchance knowledge, education,
         innovation, and economic vitality, and stewardship of Earth.
         This application will allow you to take a closer look at a small portion of NASA's work by
         showcasing Near Earth Objects, also known as NEOs. To learn more about Near Earth Objects, 
         please check out our FAQ page. You can also click on the link below to visit NASA's Near Earth
         Objects page to learn more.''')
st.link_button('NASA Near Earth Objects page', 'https://cneos.jpl.nasa.gov/', help='This button will take you to NASA\'s website.')
st.write("""
         Below are examples of the results that can be rendered on the history and visualizations pages.
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
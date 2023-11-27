import pandas as pd
import streamlit as st
import datetime
import requests
import json
from dotenv import load_dotenv
from os import getenv

st.header('History of Near Earth Objects')

#st.subheader('**Enter API Key and selected date**')
#intake user API key input
#api_key = st.text_input('**API Key:**', value=None, max_chars=45)


#create datetime variables for the date input calendar
today = datetime.datetime.now()
last_year = today.day - 1
end = today - datetime.timedelta(days=1)

#create variable for the date input
user_date = st.date_input(
    label='**Select your date:**', 
    value=None,
    max_value=end,
    format='YYYY-MM-DD'
)

#if statement to trigger next steps if user inputs a date
if user_date:
    #set the user input date to a new variable
    load_dotenv()
    api_key = getenv('MY_API_KEY')
    date = user_date
    #transform date variable into a date string
    date_str = date.strftime('%Y-%m-%d')
    #add api key and date string to api url
    url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={date_str}&end_date={date_str}&api_key={api_key}'
    #call the api
    response = requests.get(url)
    #redefine the date string so that the day now reads the date with the month spelled out
    month_date_str = user_date.strftime('%B %m, %Y')
    #allows user to see how many near earth objects were present on the day selected
    st.write(f"""
             **On {month_date_str}, there were a total of {len(response.json()['near_earth_objects'][date_str])} Near Earth Objects.
             Below is the history and NASA assigned name for each Near Earth Object on that day.**
             """)
    #create for loop to loop through index with the API to call each object's history
    for i in range(len(response.json()['near_earth_objects'][date_str])):
        #define the response for that day
        neow_name = response.json()['near_earth_objects'][date_str][i]['name']
        #insert name for history of each near earth object 
        st.write(f'History of Near Earth Object {neow_name}')
        #retrieve the url for each near earth object history within the json response
        history_url = response.json()['near_earth_objects'][date_str][i]['links']['self']
        #calls to api
        history = requests.get(history_url)
        #create dataframe from json response
        history_data = pd.DataFrame(history.json()['close_approach_data'])
        #reanme the columns within the dataframe
        history_data.rename(columns={'close_approach_date': "Close Approach Date"}, inplace=True)
        #display dataframe with only the close approach date
        history_data[['Close Approach Date']]



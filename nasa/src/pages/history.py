import pandas as pd
import streamlit as st
import datetime
import requests
import json

st.header('History of Near Earth Objects')
st.subheader('Enter API Key and selected date range:')
api_key = st.text_input('API Key:', value=None, max_chars=45)

today = datetime.datetime.now()
last_year = today.day - 1

end = today - datetime.timedelta(days=1)


user_date = st.date_input(
    label='Select your date:', 
    value=None,
    max_value=end,
    format='YYYY-MM-DD'
)

#dates_history_list = []
if user_date:
    date = user_date
    #while date <= end_date:
    date_str = date.strftime('%Y-%m-%d')
    #dont forget to remove your api key and put in {api_key}
    url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={date_str}&end_date={date_str}&api_key={api_key}'
    response = requests.get(url)

    month_date_str = user_date.strftime('%B %m, %Y')
    st.write(f"""
             **On {month_date_str}, there were a total of {len(response.json()['near_earth_objects'][date_str])} Near Earth Objects.
             Below is the history and NASA assigned name for each Near Earth Object on that day.**
             """)

    for i in range(len(response.json()['near_earth_objects'][date_str])):
        neow_name = response.json()['near_earth_objects'][date_str][i]['name']
        st.write(f'History of Near Earth Object {neow_name}')
        history_url = response.json()['near_earth_objects'][date_str][i]['links']['self']
        history = requests.get(history_url)
        history_data = pd.DataFrame(history.json()['close_approach_data'])
        history_data.rename(columns={'close_approach_date': "Close Approach Date"}, inplace=True)
        history_data[['Close Approach Date']]



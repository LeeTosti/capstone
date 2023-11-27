import matplotlib as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import datetime
import requests
import json
from dotenv import load_dotenv
from os import getenv


st.subheader('Create your own visualizations based on your selected date')
#st.write('**Enter API Key and selected date**')
#api_key = st.text_input('**API Key:**', value=None, max_chars=45)

today = datetime.datetime.now()
last_year = today.day - 1

end = today - datetime.timedelta(days=1)


user_date = st.date_input(
    label='**Select your date:**', 
    value=None,
    max_value=end,
    format='YYYY-MM-DD'
)


if user_date:
    date_str = user_date.strftime('%Y-%m-%d')
    load_dotenv()
    api_key = getenv('MY_API_KEY')
    api_url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={date_str}&end_date={date_str}&api_key={api_key}'
    neows = requests.get(api_url)

    df = pd.DataFrame(neows.json()['near_earth_objects'][date_str])
    diameter_list = []

    for i in range(len(neows.json()['near_earth_objects'][date_str])):
        diameter_list.append(neows.json()['near_earth_objects'][date_str][i]['estimated_diameter']['feet'])
        df.loc[i,'diameter_min'] = round(diameter_list[i]['estimated_diameter_min'], 2)
        df.loc[i,'diameter_max'] = round(diameter_list[i]['estimated_diameter_max'], 2)
        df.loc[i, 'avg_diameter'] = round((diameter_list[i]['estimated_diameter_min'] + diameter_list[i]['estimated_diameter_max'])/2, 2)

    df = df[['diameter_min', 'diameter_max', 'avg_diameter', 'absolute_magnitude_h', 'is_potentially_hazardous_asteroid']]

    df.rename(columns={'diameter_min': "Minimum Estimated Diameter (feet)"}, inplace=True)
    df.rename(columns={'diameter_max': "Maximum Estimated Diameter (feet)"}, inplace=True)
    df.rename(columns={'avg_diameter': "Estimated Average Diameter (feet)"}, inplace=True)
    df.rename(columns={'absolute_magnitude_h': "Absolute Magnitude"}, inplace=True)
    df.rename(columns={'is_potentially_hazardous_asteroid': 'Potentially Hazardous Asteroids'}, inplace=True)
    df['Potentially Hazardous Asteroids'] = df['Potentially Hazardous Asteroids'].replace({True: 'True', False: 'False'})


    visualization_type = ['select', 'histogram', 'scatterplot', 'boxplot']
    visualization = st.selectbox('**Choose your visualization type:**', options=visualization_type)

    if visualization == 'histogram':
        x = st.selectbox('**Select an X-axis value:**', options=list(df.columns))
        if x in list(df.columns[:4]):
            try:
                plot = sns.histplot(data=df, x=x)
                month_date_str = user_date.strftime('%B %d, %Y')
                st.subheader(f'{x} of Near Earth Objects on {month_date_str}')
                st.pyplot(plot.get_figure())
            except BaseException:
                st.error('**Unable to visualize using X-axis value. Please select another option.**')
        if x in list(df.columns[4:]):
            try:  
                plot = sns.histplot(data=df, x=x, discrete=True)
                plot.set(yticks=range(0, int(max(plot.get_yticks()))+5, 5))
                month_date_str = user_date.strftime('%B %d, %Y')
                st.subheader(f'{x} on {month_date_str}')
                st.pyplot(plot.get_figure())
            except BaseException:
                st.error('**Unable to visualize using X-axis value. Please select another option.**')


    elif visualization == 'scatterplot':
        x = st.selectbox('**Select an X-axis value:**', options=list(df.columns[:4]))
        y = st.selectbox('**Select an Y-axis value:**', options=list(df.columns[:4]))
        if x and y:
            try:
                plot = sns.scatterplot(
                    data=df,
                    x=x,
                    y=y
                )
                st.pyplot(plot.get_figure())
            except BaseException:
                st.error('**Unable to visualize using selected values. Please select different values.**')

    if visualization == 'boxplot':
        x = st.selectbox('**Select an X-axis value:**', options=list(df.columns[:4]))
        if x:
            try:
                plot = sns.boxplot(data=df, x=x)
                st.pyplot(plot.get_figure())
            except BaseException:
                st.error('**Unable to visualize using X-axis value. Please select another option.**')

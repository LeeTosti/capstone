import streamlit as st

st.header('Commonly asked questions')
st.subheader('What is a Near Earth Object?')
st.write("""
         According to NASA, Near Earth Objects (NEOs) are 'comets and asteroids that have nudged 
         by the gravitational attraction of nearby planet into orbits that allow them to enter Earth's neighborhood.'
         Basically this is a fancy way of saying comets and asteroids that come near to earth.
         """)
st.subheader('What is Absolute Magnitude?')
st.write("""
         Absolute Magnitude is the measure of the luminosity of a celestial object. Another way to think about 
         Absolute Magnitude is it represents how bright a comet or asteroid is the observer. However, the numbers are
         assigned on an inverse logarithmic astronomical magnitude scale, meaning the smaller the number, the
         brighter it appears. For example, the sun in our solar system has an absolute magnitude of 4.83.
         A near earth object with that is one kilometer in size will have an absolute magnnitude of 17.75.
         """)
st.subheader('What does it mean if an asteroid is potentially hazardous?')
st.write("""
         It means that the asteroid has an orbit that comes nearer than 7.5 million kilometers to the earth
         and it's absolute magnitude implies a size of more than 100 meters in diameter.
         """)
st.subheader('Why do I need an API key?')
st.write("""
         The API key allows you to access NASA's open API and brings the data that you want to your searches. 
         A lot of the apps you use utilize API keys. For example, your weather app on your phone might link 
         to the National Weather Service's API.
         """)
#Second | Flask integrated + required elements.

import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
import requests
from flask import Flask, render_template, request
import pytz
from geopy.geocoders import Photon
from timezonefinder import TimezoneFinder
from datetime import datetime

class OpenWeatherAPIConnection(ExperimentalBaseConnection):

    def __init__(self):
        super().__init__("openweatherapi")

    def _connect(self):
        self.api_key = st.secrets["openweatherapi_key"]
        self.connection = requests.Session()

    def cursor(self):
        return self.connection

    @st.cache_data(ttl=60 * 60, hash_funcs={})
    def query(self, city):  # Add hash_funcs={} to disable hashing for self parameter
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = self.connection.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

def get_weather_info(city):
    # Get the location of the city
    geolocator = Photon(user_agent="geoapiExercises")
    location = geolocator.geocode(city)

    # Get the timezone of the city
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

    # Get the current time in the city
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")

    # Get the weather for the city
    connection = OpenWeatherAPIConnection()
    connection._connect()
    weather = connection.query(city)

    return current_time, weather

def main():
    st.title("City Weather and Time Information")

    city = st.text_input("Enter the city name:")
    if not city:
        st.info("Please enter a city name.")
        return

    current_time, weather = get_weather_info(city)

    if weather is not None:
        st.write(f"City: {city}")
        st.write(f"Current Local Time: {current_time}")
        st.write(f"Weather Condition: {weather['weather'][0]['main']}")
        st.write(f"Weather Description: {weather['weather'][0]['description']}")
        st.write(f"Temperature: {int(weather['main']['temp'] - 273.15)} °C")
        st.write(f"Humidity: {weather['main']['humidity']} %")
        st.write(f"Pressure: {weather['main']['pressure']} hPa")
        st.write(f"Wind Speed: {weather['wind']['speed']} m/s")
    else:
        st.warning(f"No weather data found for {city}.")

if __name__ == "__main__":
    main()
#First | Only Streamlit with all the required elements.


import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
import requests

class OpenWeatherAPIConnection(ExperimentalBaseConnection):

    def __init__(self):
        super().__init__("openweatherapi")

    def _connect(self):
        self.api_key = st.secrets["openweatherapi_key"]
        self.connection = requests.Session()

    def cursor(self):
        return self.connection

    @st.cache_data(ttl=60 * 60)
    def query(_self, city):  # Add leading underscore to the self argument
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={_self.api_key}"
        response = _self.connection.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

def main():
    connection = OpenWeatherAPIConnection()
    connection._connect()
    weather = connection.query("London")
    if weather is not None:
        st.write(weather)

if __name__ == "__main__":
    main()
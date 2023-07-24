import requests
import json
from streamlit.connections import ExperimentalBaseConnection

class OpenWeatherMapConnection(ExperimentalBaseConnection[requests.Session]):
    def __init__(self, *args, connection_name=None, **kwargs):
        super().__init__(*args, connection_name=connection_name, **kwargs)
        self._resource = self._connect()

    def _connect(self) -> requests.Session:
        return requests.Session()

    def cursor(self):
        return self._resource

    def query(self, cities, ttl: int = 3600):
        def _get_weather_data(_cities):
            weather_data = {}
            for city in _cities:
                url = 'http://api.openweathermap.org/data/2.5/weather'
                params = {
                    'q': city,
                    'appid': 'fe952f9b69a7b12dd4e42d3f2a55f6f4',
                    'units': 'metric' 
                }

                response = self._resource.get(url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    weather_description = data['weather'][0]['description']
                    temperature = data['main']['temp']
                    humidity = data['main']['humidity']
                    pressure = data['main']['pressure']
                    wind_speed = data['wind']['speed']

                    weather_data[city] = {
                        "weather_description": weather_description,
                        "temperature": temperature,
                        "humidity": humidity,
                        "pressure": pressure,
                        "wind_speed": wind_speed
                    }
                else:
                    weather_data[city] = f"Failed to retrieve weather information for {city}."

            return weather_data

        return _get_weather_data(cities)
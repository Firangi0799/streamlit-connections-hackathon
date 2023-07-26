import requests
import json
from streamlit.connections import ExperimentalBaseConnection

class OpenWeatherMapConnection(ExperimentalBaseConnection[requests.Session]):
    """
    A connection class to fetch weather data from the OpenWeatherMap API.

    Attributes:
        connection_name (str): The name of the connection (optional).
    """
    def __init__(self, *args, connection_name=None, **kwargs):
        """
        Initializes the OpenWeatherMapConnection.

        Args:
            *args: Variable-length argument list.
            connection_name (str, optional): The name of the connection (default is None).
            **kwargs: Keyword arguments.
        """
        super().__init__(*args, connection_name=connection_name, **kwargs)
        self._resource = self._connect()

    def _connect(self) -> requests.Session:
        """
        Creates a new requests session as the underlying resource.

        Returns:
            requests.Session: A new requests session.
        """
        return requests.Session()

    def cursor(self):
        """
        Returns the underlying requests session as the cursor.

        Returns:
            requests.Session: The requests session object.
        """
        return self._resource

    def query(self, cities, ttl: int = 3600):
        """
        Fetches weather data for the specified cities from the OpenWeatherMap API.

        Args:
            cities (list): A list of city names for which weather data is to be fetched.
            ttl (int, optional): Time-to-live for the cached data in seconds (default is 3600).

        Returns:
            dict: A dictionary containing weather data for each city.
                  The structure of the returned dictionary:
                  {
                      "city_name": {
                          "weather_description": str,
                          "temperature": float,
                          "humidity": int,
                          "pressure": int,
                          "wind_speed": float
                      },
                      ...
                  }
        """
        def _get_weather_data(_cities):
            """
            Helper function to fetch weather data for the given cities.

            Args:
                _cities (list): A list of city names.

            Returns:
                dict: A dictionary containing weather data for each city (refer to the format above).
            """
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

# Streamlit Connections Hackathon - Weather Information App

![Streamlit Connections Hackathon](https://www.streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png)

Welcome to the Weather Information App created as part of the Streamlit Connections Hackathon. This app allows you to get current weather information for cities of your choice.

## Usage

1. First, enter the names of cities you want to check the weather for. You can enter multiple cities separated by commas.

2. Click the "Get Weather" button to retrieve the weather information for the provided cities.

## Custom Styling

The app is designed with a custom CSS style to make it visually appealing and easy to use.

```python
import streamlit as st

# Custom CSS styles (already applied in the app)
st.markdown(
    """
    <style>
    .stApp {
        max-width: 700px;
        margin: 0 auto;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #f0f0f0;
        color: black;  /* Keep the user input text as black */
        font-size: 16px;
        padding: 12px 15px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: #0078E7;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stMarkdown {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
```

## Code

Below is the code used to fetch weather information from the OpenWeatherMap API and display it in the app.

```python
import streamlit as st
import requests
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

def main():
    weather_connection = OpenWeatherMapConnection(connection_name='openweathermap')

    st.title("Weather Information")
    st.markdown("Enter the names of cities (comma-separated) to get their current weather information.")

    cities_input = st.text_input("Enter city names (comma-separated)")

    if st.button("Get Weather"):
        try:
            cities = [city.strip() for city in cities_input.split(",")]
            weather_data = weather_connection.query(cities)
            display_weather_data(weather_data)
        except Exception as e:
            st.error(f"Error occurred: {e}")

def display_weather_data(weather_data):
    for city, data in weather_data.items():
        st.markdown(f"### Weather Information for {city}")
        if isinstance(data, str):
            st.markdown(data)
        else:
            st.markdown(f"**Description:** {data['weather_description']}")
            st.markdown(f"**Temperature:** {data['temperature']} °C")
            st.markdown(f"**Humidity:** {data['humidity']} %")
            st.markdown(f"**Pressure:** {data['pressure']} hPa")
            st.markdown(f"**Wind Speed:** {data['wind_speed']} m/s")
        st.markdown("---")

if __name__ == "__main__":
    main()
```

## Installation

To run the app locally, you need to have Python and Streamlit installed. You can install Streamlit using pip:

```bash
pip install streamlit
```

## Running the App

Save the code above into a Python file, let's say `weather_app.py`, and run the app using the following command:

```bash
streamlit run weather_app.py
```

The app will open in your web browser, and you can start checking the weather for your favorite cities!

## About the Author

This app was created by [Your Name], as a submission for the Streamlit Connections Hackathon. Connect with the author on [LinkedIn/Twitter/GitHub] to explore more exciting projects.

---

Have fun exploring the weather with the Weather Information App! 🌤️🌦️🌧️

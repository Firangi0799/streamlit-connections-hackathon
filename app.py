import streamlit as st
from main import OpenWeatherMapConnection

# Custom CSS styles
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

def main():
    """
    The main function to run the weather information web app.

    This function sets up the Streamlit app, connects to the OpenWeatherMap API,
    and handles user interactions to fetch and display weather data.
    """
    weather_connection = OpenWeatherMapConnection(connection_name='openweathermap')

    st.title("Weather Information")
    st.markdown("Enter the names of cities (comma-separated) to get their current weather information.")
    st.markdown("Created and maintained by: Abhishek Kumar")

    cities_input = st.text_input("Enter city names (comma-separated)")

    if st.button("Get Weather"):
        try:
            cities = [city.strip() for city in cities_input.split(",")]
            weather_data = weather_connection.query(cities)
            display_weather_data(weather_data)
        except Exception as e:
            st.error(f"Error occurred: {e}")

def display_weather_data(weather_data):
    """
    Display weather data for each city.

    Args:
        weather_data (dict): A dictionary containing weather data for each city.
                             The structure of the dictionary:
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

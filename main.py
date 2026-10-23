from datetime import datetime

import requests

weather_codes = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️",
    2: "Partly cloudy ⛅",
    3: "Overcast ☁️",
    45: "Fog 🌫️",
    48: "Fog 🌫️",
    51: "Drizzle 🌦️",
    53: "Drizzle 🌦️",
    55: "Drizzle 🌦️",
    61: "Rain 🌧️",
    63: "Rain 🌧️",
    65: "Rain 🌧️",
    71: "Snowfall ❄️",
    73: "Snowfall ❄️",
    75: "Snowfall ❄️",
    80: "Rain showers 🌧️",
    81: "Rain showers 🌧️",
    82: "Rain showers 🌧️",
    95: "Thunderstorm ⛈️",
}


def display_forecast(city_name, weather_data):
    print(f"\n7-Day Forecast for {city_name}:")

    for i in range(7):
        date = weather_data["daily"]["time"][i]
        date_object = datetime.strptime(date, "%Y-%m-%d")
        day_name = date_object.strftime("%A")
        max_temp = weather_data["daily"]["temperature_2m_max"][i]
        min_temp = weather_data["daily"]["temperature_2m_min"][i]
        code = weather_data["daily"]["weather_code"][i]
        condition = weather_codes.get(code, "Unknown weather conditions")
        print(f"{day_name}: High {max_temp}°C | Low {min_temp}°C | {condition}")


def display_weather(city_name, weather_data):

    code = weather_data["current"]["weather_code"]

    print(f"Weather in {city_name}")
    print(f"Temperature: {weather_data['current']['temperature_2m']}°C")
    print(f"Humidity: {weather_data['current']['relative_humidity_2m']}%")
    print(f"Wind speed: {weather_data['current']['wind_speed_10m']}km/h")
    print(f"Weather outside: {weather_codes.get(code, 'Unknown weather conditions')}")


def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException:
        print("Could not retrieve weather data. Please check your internet connection.")


def find_city():
    while True:
        city = input("Enter a city: ").strip()
        if not city:
            print("Please enter a city name.")
            continue
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city, "count": 1}
        try:
            response_geo = requests.get(geo_url, params=geo_params, timeout=10)
            response_geo.raise_for_status()
            data_geo = response_geo.json()
        except requests.exceptions.RequestException:
            print("Could not connect to the city search service.")
            return None
        if "results" in data_geo:
            print("City found!")
            found_city = data_geo["results"][0]["name"]
            if city.lower() != found_city.lower():
                while True:
                    answer = input(f"Did you mean {found_city}? (y/n): ")
                    if answer.lower() not in ("y", "n"):
                        print("Invalid input.")
                    else:
                        break
                if answer.lower() == "n":
                    continue
            break
        else:
            print("City not found! Please try again.")
    latitude = data_geo["results"][0]["latitude"]
    longitude = data_geo["results"][0]["longitude"]
    return found_city, latitude, longitude


while True:
    result = find_city()

    if result is not None:
        found_city, latitude, longitude = result
        data = get_weather(latitude, longitude)

        if data is not None:
            display_weather(found_city, data)
            display_forecast(found_city, data)

    while True:
        choice = input("\nWould you like to search another city? (y/n): ").lower()
        if choice not in ("y", "n"):
            print("Invalid option.")
            continue
        break
    if choice == "n":
        print("Goodbye!")
        break

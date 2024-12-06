import requests
import json

def get_weather_data(latitude, longitude):
    url = "http://localhost:8080/RestfulService/webresources/api"
    json_input_string = {
        "latitude": latitude,
        "longitude": longitude
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=json_input_string, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}"

def parse_weather_data(weather_data):
    # Parse the weather data string inside the "weather_data" field
    weather_json = json.loads(weather_data)
    
    # Extract the actual weather information
    weather_info = json.loads(weather_json['weather_data'])

    # Return the parsed weather data in a more readable format
    return {
        "city": weather_info.get("city"),
        "temperature": weather_info.get("temperature"),
        "humidity": weather_info.get("humidity"),
        "pressure": weather_info.get("pressure"),
        "wind_speed": weather_info.get("wind_speed"),
        "wind_direction": weather_info.get("wind_direction"),
        "cloudiness": weather_info.get("cloudiness"),
        "weather_description": weather_info.get("weather_description"),
        "sunrise": weather_info.get("sunrise"),
        "sunset": weather_info.get("sunset")
    }
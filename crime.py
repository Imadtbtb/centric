import requests
import json

def crime_client(latitude, longitude):
    try:
        url = "http://localhost:8080/RestfulService/webresources/api/crime"
        json_input = {"latitude": latitude, "longitude": longitude}

        response = requests.post(url, json=json_input, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            return response.json()  # Return JSON directly for API
        else:
            return {"error": f"Error: {response.status_code}"}  # Return error message in JSON format

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}



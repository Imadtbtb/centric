import requests
import json

# URL of the server endpoint (Make sure your server is running and accessible)
url = 'http://localhost:8080/RestfulService/webresources/apply'  # Replace with the actual URL of your ApplyForRoom service

# Data to send in the POST request (username and userId as input)
data = {
    "userName": "JohnDoe",  # Replace with the actual user name
    "userId": 12345         # Replace with the actual user ID
}

# Send POST request to the server
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    print("Application Submitted Successfully!")
    print("Response:", response.json())  # Prints the response JSON from the server
else:
    print("Failed to submit application.")
    print("Error:", response.status_code, response.text)

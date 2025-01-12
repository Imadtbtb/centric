import requests
import json
 
url = 'http://localhost:8080/RestfulService/webresources/apply'  
 
data = {
    "userName": "JohnDoe",  # Replace with the actual user name
    "userId": 12345         # Replace with the actual user ID
}

# Send POST request to the server
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    print("Application Submitted Successfully!")
    print("Response:", response.json())  
else:
    print("Failed to submit application.")
    print("Error:", response.status_code, response.text)

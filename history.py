import requests
import json

# URL of the RESTful service
BASE_URL = "http://localhost:8080/RestfulService/webresources/history"

# Send a POST request to set the user ID
def post_user_id(user_id):
    url = BASE_URL
    headers = {'Content-Type': 'application/json'}
    
    # Create the data to be sent in JSON format
    data = json.dumps({'userId': user_id})

    # Send the POST request
    response = requests.post(url, headers=headers, data=data)
    
    # Return the response content
    return response.text

# Send a GET request to retrieve the application history for the set user ID
def get_history():
    url = BASE_URL
    headers = {'Accept': 'application/json'}

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Return the response content
    return response.text

# Function to deserialize and parse JSON response
def deserialize(json_response):
    try:
        # Strip the outer quotes and handle the escaped characters
        clean_response = json_response.strip('"')  # Remove extra quotes around the response
        clean_response = clean_response.replace(r'\"', '"')  # Replace escaped quotes with actual quotes

        # Now parse the cleaned response string
        data = json.loads(clean_response)

        # Initialize a list to hold the parsed entries
        parsed_entries = []

        if data:
            # Loop through the list and extract the values
            for entry in data:
                # Extract individual fields
                entry_id = entry.get('id')
                user_id = entry.get('userId')
                room_id = entry.get('roomId')
                status = entry.get('status')

                # Append the extracted values to the list
                parsed_entries.append({
                    'entry_id': entry_id,
                    'user_id': user_id,
                    'room_id': room_id,
                    'status': status
                })

        return parsed_entries  # Return the list of parsed entries
    except json.JSONDecodeError:
        return "Error: Unable to deserialize the response. Please check the response format."
    except Exception as e:
        return f"Error: {e}"

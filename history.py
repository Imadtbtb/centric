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

 
def get_history():
    url = BASE_URL
    headers = {'Accept': 'application/json'}

   
    response = requests.get(url, headers=headers)

   
    return response.text
 
def deserialize(json_response):
    try:
  
        clean_response = json_response.strip('"')  # Remove extra quotes around the response
        clean_response = clean_response.replace(r'\"', '"')  # Replace escaped quotes with actual quotes

        # Now parse the cleaned response string
        data = json.loads(clean_response)

 
        parsed_entries = []

        if data:
            # Loop through the list and extract the values
            for entry in data:
                # Extract individual fields
                entry_id = entry.get('id')
                user_id = entry.get('userId')
                room_id = entry.get('roomId')
                status = entry.get('status')

                 
                parsed_entries.append({
                    'entry_id': entry_id,
                    'user_id': user_id,
                    'room_id': room_id,
                    'status': status
                })

        return parsed_entries  
    except json.JSONDecodeError:
        return "Error: Unable to deserialize the response. Please check the response format."
    except Exception as e:
        return f"Error: {e}"

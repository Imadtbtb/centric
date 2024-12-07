import requests

def apply_room(user_id, room_id):
    try:
        # Define the endpoint URL of the REST service
        api_url = "http://localhost:8080/RestfulService/webresources/applo"  # Change this to your actual REST service URL

        # Create the data to send in the POST request
        post_data = {'userId': user_id, 'roomId': room_id}

        # Send the POST request
        response = requests.post(api_url, data=post_data)

        # Check the status code of the response
        if response.status_code == 200:
            # Return the response text from the server
            return response.text
        else:
            return f"Error: {response.status_code}"

    except Exception as e:
        return f"Request failed: {e}"


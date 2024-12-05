import requests

def fetch_room_details(room_id):
    """Fetch room details using the provided room ID."""
    url = f'http://152.71.62.30:8080/RestfulService/webresources/WeatherApp/{room_id}'
    response = requests.get(url)
    print(f"Room fetch response: {response.status_code}")
    if response.status_code == 200:
        return response.json()  # Assuming the response is in JSON format
    else:
        raise Exception(f"Error fetching room details. Status code: {response.status_code}")

def send_application_data(user_name, room_id, room_details, application_id):
    """Send application data to the server."""
    application_data = {
        'applicationId': application_id,
        'UserID': user_name,
        'roomId': room_id,
        'roomDetails': room_details,
        
    }

    url = 'http://152.71.62.30:8080/RestfulService/webresources/apply'
    response = requests.post(url, json=application_data)
    print(f"Application sent, response: {response.status_code}")

    if response.status_code != 200:
        raise Exception(f"Error sending application data. Status code: {response.status_code}")







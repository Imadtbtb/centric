import requests

API_URL = "http://localhost:8080/RestfulService/webresources/api/distance"

# Function to calculate and fetch distance information
def calculate_distance(lat1, lon1, lat2, lon2, unit):
    try:
        # Prepare the request body for the distance calculation
        request_body = {
            "lat1": lat1,
            "lon1": lon1,
            "lat2": lat2,
            "lon2": lon2,
            "unit": unit
        }

        # Send POST request to the distance API
        json_response = send_post_request(request_body)

        # Send GET request to fetch the last calculated distance
        distance_info = send_get_request()
        return json_response, distance_info

    except Exception as e:
        return str(e), None

# Send a POST request with the given data
def send_post_request(json_input):
    response = requests.post(API_URL, json=json_input)
    return response.text

# Send a GET request to fetch the distance information
def send_get_request():
    response = requests.get(API_URL)
    return response.text

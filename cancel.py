import requests

def cancel_application(application_id, user_id):
    # URL of the cancel endpoint
    url = "http://localhost:8080/RestfulService/webresources/applo/cancel"
    
    # Prepare the POST data
    post_data = {'applicationId': application_id, 'userId': user_id}

    try:
        # Send the POST request to the server
        response = requests.post(url, data=post_data)

        # Check the response code
        if response.status_code == 200:  # HTTP OK
            print("Application canceled successfully.")
        else:
            print(f"Failed to cancel application. Response Code: {response.status_code}")

    except Exception as e:
        print(f"Error occurred: {e}")



import requests

def cancel_application(application_id, user_id):
 
    url = "http://localhost:8080/RestfulService/webresources/applo/cancel"
 
    post_data = {'applicationId': application_id, 'userId': user_id}

    try:
 
        response = requests.post(url, data=post_data)
 
        if response.status_code == 200:   
            print("Application canceled successfully.")
        else:
            print(f"Failed to cancel application. Response Code: {response.status_code}")

    except Exception as e:
        print(f"Error occurred: {e}")



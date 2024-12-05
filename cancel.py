import requests

def cancel_application_request(application_id):
    """Cancel application by ID."""
    url = f'http://152.71.62.30:8080/RestfulService/webresources/apply/{application_id}'
    response = requests.delete(url)
    print(f"Cancel response: {response.status_code}")

    if response.status_code != 200:
        raise Exception(f"Error cancelling application. Status code: {response.status_code}")


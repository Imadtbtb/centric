import requests

def apply_room(user_id, room_id):
    try:
        
        api_url = "http://localhost:8080/RestfulService/webresources/applo"   
 
        post_data = {'userId': user_id, 'roomId': room_id}

      
        response = requests.post(api_url, data=post_data)

    
        if response.status_code == 200:
    
            return response.text
        else:
            return f"Error: {response.status_code}"

    except Exception as e:
        return f"Request failed: {e}"


import requests

def search_room(price_max, city, county):
    """Search for rooms based on user input parameters."""
    
    url = f'http://127.0.0.1:8080/RestfulService/webresources/WeatherApp/searchRoom?priceMax={price_max}&city={city}&county={county}'
 
    response = requests.get(url)
    
    if response.status_code == 200:
        rooms = response.json()
        if rooms: 
            return rooms
        else:
            return None   
    else:
        raise Exception(f"Error fetching room data. Status code: {response.status_code}")




import requests
from pprint import pprint
import folium

from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
link = "https://api.twitter.com/1.1/friends/list.json"
def get_friends_list(nickname: str, token: str) -> dict:
    '''
    '''
    my_headers = {"Authorization": f"Bearer {token}"}

    my_params = {'screen_name': nickname,
                 'count': 30}

    result = requests.get(link, headers=my_headers, params=my_params)

    try:
        if result.json()["error"] == "Not authorized.":
            return False
    except KeyError:
        return result.json()

def get_needed_values(data: dict) -> dict:
    '''
    '''
    result = []
    for user in data["users"]:
        if user["location"] != '': 
            result.append({"name": user["name"], "location": user["location"]})
    return result

def get_location(data: dict) -> dict:
    """

    """

    for i, user in enumerate(data):
        locator = Nominatim(user_agent="FL")
        location = locator.geocode(user['location'])

        if location != None:
            user['location'] = (location.latitude, location.longitude)
        else:
            user['location'] = None

    return data


def load_map(user_data: dict):
    """
    """
    mapp = folium.Map()

    fg = folium.FeatureGroup(name="Locations")
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)


    for user in user_data:
        if user['location'] != None:
            popup = user['name']
            folium.Marker(location=user['location'], popup=popup).add_to(marker_cluster)

    mapp.add_child(fg)
    mapp.add_child(folium.LayerControl())
    mapp.save("map.html")

    return mapp
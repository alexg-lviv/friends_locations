'''
a module to analyze twitter API data and make a map
map is made to show the user's friends locations
to use the app, you need to enter the user name and your twitter API token
'''

from flask import Flask, render_template, request
import csv
import requests
from pprint import pprint
import folium

from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    if not request.form.get("username") or not request.form.get("token"):
        return render_template("failure.html")

    data = get_friends_list(request.form.get(
        "username"), request.form.get("token"))

    if data == False:
        return render_template("failure.html")

    mapp = load_map(get_location(get_needed_values(data)))

    return mapp._repr_html_()


link = "https://api.twitter.com/1.1/friends/list.json"


def get_friends_list(nickname: str, token: str) -> dict:
    '''
    a function to get a list of friends with information about them
    takes an information to access twitter API and find a user
    returns a dict out of json file
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
    extracts only needed values out of a dictionary from get_friends_list function
    these are only names and locations
    '''
    result = []
    for user in data["users"]:
        if user["location"] != '':
            result.append({"name": user["name"], "location": user["location"]})
    return result


def get_location(data: dict) -> dict:
    """
        a function to add actual latitude and longitude by the locations from get_needed_values function
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
    a function to load map with all friends locations pointed there
    """
    mapp = folium.Map()

    fg = folium.FeatureGroup(name="Locations")
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)

    for user in user_data:
        if user['location'] != None:
            popup = user['name']
            folium.Marker(location=user['location'],
                          popup=popup).add_to(marker_cluster)

    mapp.add_child(fg)
    mapp.add_child(folium.LayerControl())
    mapp.save("map.html")

    return mapp


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

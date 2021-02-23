'''
This module is used in pulling data from Twitter
'''

from flask import Flask, render_template, request
import csv
from helper import *
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if not request.form.get("username") or not request.form.get("bearer_token"):
        return render_template("failure.html")

    data = get_friends_list(request.form.get("username"), request.form.get("token"))

    if data == False:
        return render_template("failure.html")

    mapp = load_map(get_location(get_needed_values(data)))
    
    return mapp._repr_html_()




if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
#!/usr/bin/python3
"""
Starts a Flask web application.
The application listens on 0.0.0.0, port 5000.
Routes:
    /hbnb_filters: HBnB HTML filters page.
"""


from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from flask import Flask
from flask import render_template, url_for


app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Displays the main HBnB filters HTML page. """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    return render_template("100-hbnb.html", states=states,
                           amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exc):
    """ Remove current Database session """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

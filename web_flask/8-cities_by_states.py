#!/usr/bin/python3
"""
Starts a Flask web application.
The application listens on 0.0.0.0, port 5000.
Routes:
    /cities_by_states:A HTML page with a list of all State with related cities.
"""

from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """
    Displats a HTML page with a list of all State with related cities.
    States and cities are sorted by name.
    """
    states = storage.all(State)
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def tearsown(exc):
    """ Remove current Database session """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

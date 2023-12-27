#!/usr/bin/python3
"""
Starts a Flask web application.
The application listens on 0.0.0.0, port 5000.
Routes:
    /states: Display HTML page with a list of all State objects.
    /states/<id>: HTML page displaying the given state with id.
"""


from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """ Displays a HTML page with citys of that state """
    states = storage.all(State)
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Displays information about a specific City."""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def tearsown(exc):
    """ Remove current Database session """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

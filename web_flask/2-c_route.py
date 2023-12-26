#!/usr/bin/python3

"""
Starts a Flask web application.
The application listens on 0.0.0.0, port 5000.
Routes:
    /: Displays 'Hello HBNB!'
    /hbnb: display 'HBNB'
    /c/<text>: display “C ” followed by the value of the text variable
"""

from flask import Flask

""" Creates an application object """
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ returns Hello HBNB """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Returns 'HBNB' """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """ Displays 'C' followed by the value of <text> """
    replaced = text.replace("_", " ")
    return f"C {replaced}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

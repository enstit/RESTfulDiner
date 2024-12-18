#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route("/")
def hello_world():
    return "Hello, World2!"


# Creating an Flask instance
if __name__ == "__main__":
    app.run()

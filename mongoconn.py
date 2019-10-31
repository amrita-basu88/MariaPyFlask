# For flask implementation
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from flask import jsonify
from bson import json_util
import os
import json

app = Flask(__name__)
title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

client = MongoClient(
    "mongodb://kpi_owner:login123@ds263156.mlab.com:63156/mern_kpi")  # host uri
db = client.mern_kpi  # Select the database
todos = db.testFlask  # Select the collection name
print(todos.find_one())


@app.route("/data")
def index():
    json_results = []
    for result in todos.find_one():
        json_results.append(result)
    return toJson(json_results)


def toJson(data):

    return json.dumps(data, default=json_util.default)


if __name__ == "__main__":
    app.run()

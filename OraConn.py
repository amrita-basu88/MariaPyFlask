# For flask implementation
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
# from bson import ObjectId  # For ObjectId to work
#from pymongo import MongoClient
from flask import jsonify
import os
import sys
import json
import cx_Oracle
#from coalesce import UniqueValue
#import numpy as np
from datetime import date, timedelta
sys.path.append('opt/data/devtop/bin/')
sys.path.insert(0, 'opt/data/devtop/bin/')
#import goe_pck_tfn
#from goe_pck_tfn import *

dsn_tns = cx_Oracle.makedsn(
    'exadata01.figs.test.ing.intranet', '1521', service_name='srv_ufgs37_cia')
conn = cx_Oracle.connect(
    user=r'CIA_OWNER', password='Tcia_ownerjun19', dsn=dsn_tns)

c = conn.cursor()

b_hly_rel_id = '0271'
c_hrt = "select hrt.ic_abb from gre_hr_rep_ent hrt"
g_sav_ic_abb = c.execute(c_hrt)


app = Flask(__name__)
title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"


@app.route("/index")
def index():
    row_headers = [x[0] for x in c.description]
    rv = c.fetchall()
    json_data = []
    for row in rv:
        json_data.append(dict(zip(row_headers, row)))

    return json.dumps(json_data)


@app.route("/list")
def lists():
    # Display the all Tasks
    todos_l = todos.find()
    a1 = "active"
    return render_template('index.html', a1=a1, todos=todos_l, t=title, h=heading)


@app.route("/")
@app.route("/uncompleted")
def tasks():
    # Display the Uncompleted Tasks
    todos_l = todos.find({"done": "no"})
    a2 = "active"
    return render_template('index.html', a2=a2, todos=todos_l, t=title, h=heading)


@app.route("/completed")
def completed():
    # Display the Completed Tasks
    todos_l = todos.find({"done": "yes"})
    a3 = "active"
    return render_template('index.html', a3=a3, todos=todos_l, t=title, h=heading)


@app.route("/done")
def done():
    # Done-or-not ICON
    id = request.values.get("_id")
    task = todos.find({"_id": ObjectId(id)})
    if (task[0]["done"] == "yes"):
        todos.update({"_id": ObjectId(id)}, {"$set": {"done": "no"}})
    else:
        todos.update({"_id": ObjectId(id)}, {"$set": {"done": "yes"}})
    redir = redirect_url()

    # return redirect(redir)
    return jsonify(
        name=task.name,
        desc=task.email,
        date=task.id
    )


@app.route("/action", methods=['POST'])
def action():
    # Adding a Task
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    todos.insert({"name": name, "desc": desc,
                  "date": date, "pr": pr, "done": "no"})
    return redirect("/list")


@app.route("/remove")
def remove():
    # Deleting a Task with various references
    key = request.values.get("_id")
    todos.remove({"_id": ObjectId(key)})
    return redirect("/")


@app.route("/update")
def update():
    id = request.values.get("_id")
    task = todos.find({"_id": ObjectId(id)})
    return render_template('update.html', tasks=task, h=heading, t=title)


@app.route("/action3", methods=['POST'])
def action3():
    # Updating a Task with various references
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    id = request.values.get("_id")
    todos.update({"_id": ObjectId(id)}, {
                 '$set': {"name": name, "desc": desc, "date": date, "pr": pr}})
    return redirect("/")


@app.route("/search", methods=['GET'])
def search():
    # Searching a Task with various references

    key = request.values.get("key")
    refer = request.values.get("refer")
    if (key == "_id"):
        todos_l = todos.find({refer: ObjectId(key)})
    else:
        todos_l = todos.find({refer: key})
    return render_template('searchlist.html', todos=todos_l, t=title, h=heading)


if __name__ == "__main__":
    app.run()

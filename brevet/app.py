import os
import sys
import flask 
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import arrow 
import acp_times # brevet time calculations
import logging
import random




app = Flask(__name__)
app.secret_key = 'al;sdjf;wiejrtwkf'


client = MongoClient('db', 27017)
db = client.tododb
collection = db.control
collection.delete_many({})

@app.route("/")
def root():
    collection.delete_many({})
    return flask.render_template('calc.html')

@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

# copied from flask_brevets project. 
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")

    #Get data recieved
    km = request.args.get('km', 999, type=float)
    brevet_dist = request.args.get('brevet_dist', 0, type=float)
    begin_date = request.args.get('begin_date', 0, type=str)
    begin_time = request.args.get('begin_time', 0, type=str)
    message = ""

    #Check for negative values
    if km < 0:
      message = "Control distance cannot be negative."
      km = 0

    #Control distance cannot exceed 120% brevet distance
    if km > (brevet_dist*1.2):
      message = "Control distance cannot be longer than 120% brevet distance."


    #Brevet start format
    brevet_start = begin_date + " " + begin_time + ":00"
    brevet_start_time = arrow.get(brevet_start, 'YYYY-MM-DD HH:mm:ss')

    open_time = acp_times.open_time(km, brevet_dist, brevet_start_time.isoformat())
    close_time = acp_times.close_time(km, brevet_dist, brevet_start_time.isoformat())
    result = {"open": open_time, "close": close_time, "message": message}
    return flask.jsonify(result=result)

@app.route('/display')
def display():
    """
    Display opening and closing times from
    database.
    """
    app.logger.debug("Displaying times.")
    flask.g.kms = []
    flask.g.open = []
    flask.g.close = []
    for entry in collection.find():
       
        flask.g.kms.append(entry['km'])
        flask.g.open.append(entry['open_time'])
        flask.g.close.append(entry['close_time'])

    return flask.render_template("display.html")

@app.route('/new', methods = ['POST'])
def new():
    open_times = request.form.getlist("open")
    close_times = request.form.getlist("close")
    kms = request.form.getlist("km")

    if kms == []:
        flask.flash("Table is empty!")
        return flask.redirect(flask.url_for("index"))

    # app.logger.debug("PRINTING OPENS:", opens)
    # app.logger.debug(opens)
    for item in range(20):
        if kms[item] == '':
            continue
        record = {
        'open_time' : open_times[item],
        'close_time' : close_times[item],
        'km' : kms[item]
        }

        collection.insert_one(record)
    # record = {
    #     'session_token': flask.session['id'],
    #     'brevet_dist' : distance,
    #     'km_list' : kms,
    #     'open_list' : open_times,
    #     'close_list' : close_times

    flask.flash("The controle times were saved.")
    
    return flask.redirect(flask.url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
    # added port number

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page.")
    return("Welcome to my SQLAlchemy Challenge Hawaii Weather API!<br><br>"
    f"Available Routes:<br/>"
    f"<br/>"
    f"Precipitation Data for The Last Year:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"<br/>"
    f"Station Data:<br/>"
    f"/api/v1.0/stations<br/>"
    f"<br/>"
    f"Temperature Observations from the Most Active Station for the Previous Year:<br/>"
    f"/api/v1.0/tobs<br/>"
    f"<br/>"
    f"To Query Min, Max, & Avg Temperature beginning at a specified date:<br/>"
    f"Example: /api/v1.0/2016-11-09<br/>"
    f"/api/v1.0/<start><br/>"
    f"<br/>"
    f"To Query Min, Max, & Avg Temperature for a specified date range:<br/>"
    f"Example: /api/v1.0/2016-11-09/2017-08-23<br/>"
    f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    one_year_from_recent = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>= one_year_from_recent).\
        order_by(Measurement.date).all()

    session.close()

    precipitation = []
    for date, prcp in precipitation_results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_results = session.query(Station.station, Station.name).all()

    session.close()

    station_list = list(np.ravel(station_results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    one_year_from_recent = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_from_recent).\
        order_by(Measurement.date).all()

    session.close() 
    
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()
    
    session.close()

    start_date_list = list(np.ravel(start_date))

    return jsonify(start_date_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()
    
    session.close()
    
    start_end_list = list(np.ravel(start_end))

    return jsonify(start_end_list)

if __name__ == "__main__":
    app.run(debug=True)
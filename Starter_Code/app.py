# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Climate = Base.classes.climate

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/&lt;start&gt;'>/api/v1.0/&lt;start&gt;</a><br/>"
        f"<a href='/api/v1.0/&lt;start&gt;/&lt;end&gt;'>/api/v1.0/&lt;start&gt;/&lt;end&gt;</a>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the last 12 months of precipitation data
    last_12_months_precipitation = session.query(Climate.date, Climate.prcp).filter(Climate.date >= '2016-08-23').all()

    # Convert the query results to a dictionary
    precipitation_dict = {}
    for date, prcp in last_12_months_precipitation:
        precipitation_dict[date] = prcp

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    stations = session.query(Climate.station).group_by(Climate.station).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(stations))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the previous year of data
    # You need to define your most-active station here
    most_active_station = 'USC00519281'

    # Query the last 12 months of temperature data for the most active station
    last_12_months_tobs = session.query(Climate.date, Climate.tobs).filter(Climate.station == most_active_station).filter(Climate.date >= 'your_start_date_here').all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(last_12_months_tobs))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Query to calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    results = session.query(func.min(Climate.tobs), func.avg(Climate.tobs), func.max(Climate.tobs)).filter(Climate.date >= start).all()

    # Convert list of tuples into normal list
    temp_list = list(np.ravel(results))

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Query to calculate TMIN, TAVG, and TMAX for dates between the start and end date inclusive
    results = session.query(func.min(Climate.tobs), func.avg(Climate.tobs), func.max(Climate.tobs)).filter(Climate.date >= start).filter(Climate.date <= end).all()

    # Convert list of tuples into normal list
    temp_list = list(np.ravel(results))

    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)

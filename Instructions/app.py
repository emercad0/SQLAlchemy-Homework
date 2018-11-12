
## Step 2 - Climate App

#Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# Use FLASK to create your routes.

### Routes


## Hints

# You will need to join the station and measurement tables for some of the analysis queries.

# Use Flask `jsonify` to convert your API data into a valid JSON response object.
#

import sqlalchemy
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

app = Flask(__name__)

# Create an engine to a SQLite database file called `hawaii.sqlite`
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#`/api/v1.0/precipitation`
# Query for the dates and temperature observations from the last year.
# Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
# Return the JSON representation of your dictionary.

@app.route('/api/v1.0/precipitation',methods=['GET', 'POST'])
def precipitation():

    query_run = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-11-12').order_by(Measurement.date)

    precip_vals = []
    for p in query_run:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precip_vals.append(prcp_dict)

    return jsonify(precip_vals)

# /api/v1.0/stations
# Return a json list of stations from the dataset.
#
@app.route('/api/v1.0/stations' ,methods=['GET', 'POST'])
def stations():
    
    query_run = session.query(Station.name).all()

    stations_n = list(np.ravel(query_run))

    return jsonify(stations_n)


# `/api/v1.0/tobs`

# Return a JSON list of Temperature Observations (tobs) for the previous year
#
@app.route('/api/v1.0/tobs',methods=['GET', 'POST'])
def tobs():
    query_run = session.query(Measurement.tobs).all()

    tobs_list = list(np.ravel(query_run))
    
    return jsonify(tobs_list)


# `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route('/api/v1.0/<start>',methods=['GET', 'POST'])
def temp_start(start):
    query_run = session.query(func.min(Measurement.tobs),
     func.avg(Measurement.tobs),
      func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    temp_start = list(np.ravel(query_run))
    return jsonify(temp_start)

@app.route('/api/v1.0/<start>/<end>',methods=['GET', 'POST'])
def temp_start_end(start, end):
    query_run = session.query(func.min(Measurement.tobs),
     func.avg(Measurement.tobs),
      func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    temp_start_end = list(np.ravel(query_run))
    return jsonify(temp_start_end)

if __name__ == '__main__':
    app.run(debug=True)
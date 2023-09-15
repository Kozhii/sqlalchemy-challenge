from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Create a Flask app
app = Flask(__name__)

# Create the database connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Reference the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Define a function to create a new session for each request
def create_session():
    return Session(engine)

# Define the routes
@app.route("/")
def homepage():
    return (
        "Welcome to the Climate API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/&lt;start&gt;<br/>"
        "/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a new session
    session = create_session()

    # Calculate the date 1 year ago from the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    # Close the session
    session.close()

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create a session
    session = create_session()

    # Query the stations and return them as a JSON list
    stations = session.query(Base.classes.station.station).all()
    
    # Convert the query results to a list
    station_list = [station[0] for station in stations]

    # Close the session
    session.close()

    # Return the JSON representation of the list
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create a new session
    session = create_session()

    # Calculate the date 1 year ago from the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Query the dates and temperature observations for the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a list of dictionaries
    tobs_list = [{"Date": date, "TOBS": tobs} for date, tobs in tobs_data]

    # Close the session
    session.close()

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create a session
    session = Session(engine)

    # Query the TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    results = session.query(func.min(Base.classes.measurement.tobs), func.avg(Base.classes.measurement.tobs), func.max(Base.classes.measurement.tobs)).\
        filter(Base.classes.measurement.date >= start).all()

    # Close the session
    session.close()

    # Convert the query results to a dictionary
    temp_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    # Return the JSON representation of the dictionary
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create a session
    session = Session(engine)

    # Query the TMIN, TAVG, and TMAX for the specified date range
    results = session.query(func.min(Base.classes.measurement.tobs), func.avg(Base.classes.measurement.tobs), func.max(Base.classes.measurement.tobs)).\
        filter(Base.classes.measurement.date >= start).filter(Base.classes.measurement.date <= end).all()

    # Close the session
    session.close()

    # Convert the query results to a dictionary
    temp_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    # Return the JSON representation of the dictionary
    return jsonify(temp_data)

# Other route functions should also create and close sessions in a similar manner

if __name__ == "__main__":
    app.run(debug=True)

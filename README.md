# sqlalchemy-challenge

Precipitation Analysis

I found the most recent date in the dataset.
Using the most recent date, I retrieved the previous 12 months of precipitation data:
I selected only the "date" and "prcp" values.
Loaded the query results into a Pandas DataFrame with explicitly set column names.
Sorted the DataFrame values by "date."
Plotted the results using Pandas' plot method as a bar chart.
Using Pandas, I printed the summary statistics for the precipitation data.


Station Analysis

I designed a query to calculate the total number of stations in the dataset.
I designed a query to find the most-active station(s) based on the number of observations:
I listed the stations and observation counts in descending order.
I determined the station ID with the greatest number of observations.
I designed a query to calculate the lowest, highest, and average temperatures for the most-active station.
I designed a query to retrieve the previous 12 months of temperature observation (TOBS) data for the most-active station:
I plotted the results as a histogram with 12 bins.
I closed my SQLAlchemy session.



I created a Flask API with the following routes:

/ (Homepage): Started at the homepage and listed all available routes.
/api/v1.0/precipitation: Converted the last 12 months of precipitation data to a JSON dictionary and returned it.
/api/v1.0/stations: Returned a JSON list of stations from the dataset.
/api/v1.0/tobs: Queried the temperature observations of the most-active station for the previous year and returned a JSON list of temperature observations.
/api/v1.0/<start> and /api/v1.0/<start>/<end>: Returned a JSON list of the minimum temperature (TMIN), average temperature (TAVG), and maximum temperature (TMAX) for a specified start or start-end range.
In my Flask application, I used the Flask jsonify function to convert my API data to valid JSON response objects.
That's it! I now have a Flask API for exploring climate data in Honolulu, Hawaii, and I can use it for vacation planning.

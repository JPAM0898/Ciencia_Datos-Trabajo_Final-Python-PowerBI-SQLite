import os
import pandas as pd
from geopy.distance import geodesic
from components import extract_send
from components import processdata
from components import print
from components import conec_sqlite3

#Create paths to find the data 
gpx_directory = os.path.dirname(__file__)
gpx_subdirectory = os.path.join(gpx_directory,'data')
gpx_files = [f for f in os.listdir(gpx_subdirectory) if f.endswith(".gpx")]
DBMS_Path = os.path.join(gpx_directory, 'data', 'DBMS.db')
Resulth_Path = os.path.join(gpx_directory, 'data', 'ResultGPXprocessrun_{}.xlsx')

# Read each GPX file and calculate distance, slope, speed, and acceleration
if __name__ == '__main__':
    for indice, gpx_file in enumerate(gpx_files):
        # Get the data object
        gpx = extract_send.read_data(gpx_subdirectory, gpx_file)
        # Create a list of data from the GPX data
        data = extract_send.get_data(gpx)
        # Create a dataframe from the data
        df = pd.DataFrame(data, columns=["lat", "lon", "ele", "time"])
        # Calculate the distance between each point and the next point in the route
        df["Distance"] = processdata.distance(df)
        df["DistanceTotal"] = df["Distance"].cumsum()
        # Calculate the slope between each point and the next point in the route
        df["Slope"] = processdata.slope(df)
        # Calculate the speed between each point and the next point in the route
        df["Speed"] = processdata.speed(df)
        # Calculate the acceleration between each point and the next point in the route
        df["Acceleration"] = processdata.acceleration(df)
        # Rename column names
        df.rename(columns={"lat": "Latitude","lon":"Longitude","ele":"Elevation","time":"Time"}, inplace=True)
        # Change time column
        df["Time"] = pd.to_datetime(df["Time"]).dt.strftime("%H:%M:%S")
        # Print results
        print.print_results(df)
        # Create database
        BD = conec_sqlite3.database(df, indice, DBMS_Path)
        # Save the dataframe as a CSV file with the same name as the GPX file
        extract_send.send_data(df,Resulth_Path.format(indice+1))


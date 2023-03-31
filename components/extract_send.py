import os
import gpxpy
from geopy.distance import geodesic
import xlsxwriter
import pandas as pd

# Read the data from the gpx_file
def read_data(gpx_subdirectory,gpx_file):
    try:
        print('Get the data object')
        with open(os.path.join(gpx_subdirectory, gpx_file), "r") as f:
            gpx = gpxpy.parse(f)
    except Exception as e:
        print("Error",e)
        print('Error reading the file')
    return gpx

# Create a list of data from the GPX data
def get_data(gpx):
    data = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append([point.latitude, point.longitude, point.elevation, point.time])
    return data

# Send the result data
def send_data(df,file_path):
    try:
        writer = pd.ExcelWriter(file_path,engine='xlsxwriter')
        df_result = df.to_excel(writer,index=False)
        writer.close()
        print('Result file created')
    except Exception as e:
        print("Error",e)
        print('Result file not created')
    return df_result

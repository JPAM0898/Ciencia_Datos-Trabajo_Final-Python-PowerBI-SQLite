import pandas as pd
from geopy.distance import geodesic

# Calculate the distance between each point and the next point in the route
def distance(df):
    distances = []
    for index, row in df.iterrows():
        if index < len(df) - 1:
            point1 = (row["lat"], row["lon"])
            point2 = (df.iloc[index+1]["lat"], df.iloc[index+1]["lon"])
            distances.append(geodesic(point1, point2).meters)
        else:
            distances.append(0)
    return distances

# Calculate the slope between each point and the next point in the route
def slope(df):
    slopes = []
    distances = df["Distance"]
    for index, row in df.iterrows():
        if index < len(df) - 1:
            if distances[index] == 0:
                slopes.append(0)
            else:
                slope = (df.iloc[index+1]["ele"] - row["ele"]) / distances[index]
                slopes.append(slope)
        else:
            slopes.append(0)
    return slopes

# Calculate the speed between each point and the next point in the route
def speed(df):
    speeds = []
    distances = df["Distance"]
    for index, row in df.iterrows():
        if index < len(df) - 1:
            time_diff = (pd.to_datetime(df.iloc[index+1]["time"]) - pd.to_datetime(row["time"])).total_seconds()
            speed = distances[index] / time_diff
            speeds.append(speed)
        else:
            speeds.append(0)
    return speeds

# Calculate the acceleration between each point and the next point in the route
def acceleration(df):
    accelerations = []
    speeds = df["Speed"]
    for index, row in df.iterrows():
        if index < len(df) - 1:
            time_diff = (pd.to_datetime(df.iloc[index+1]["time"]) - pd.to_datetime(row["time"])).total_seconds()
            speed_diff = speeds[index+1] - speeds[index]
            acceleration = speed_diff / time_diff
            accelerations.append(acceleration)
        else:
            accelerations.append(0)
    return accelerations
    

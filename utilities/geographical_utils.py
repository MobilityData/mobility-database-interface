import re
from LatLon23 import Latitude, Longitude


def get_geographical_coordinates(dataset):
    max_latitude = get_maximum_latitude_as_string(dataset.stops)
    min_latitude = get_minimum_latitude_as_string(dataset.stops)
    max_longitude = get_maximum_longitude_as_string(dataset.stops)
    min_longitude = get_minimum_longitude_as_string(dataset.stops)
    return max_latitude, min_latitude, max_longitude, min_longitude


def get_maximum_latitude_as_string(dataset_stops):
    max_latitude_as_float = dataset_stops["stop_lat"].max()
    max_latitude = Latitude(max_latitude_as_float)
    max_latitude_as_string = convert_coordinate_to_degrees_and_minutes_string(max_latitude)
    return max_latitude_as_string


def get_minimum_latitude_as_string(dataset_stops):
    min_latitude_as_float = dataset_stops["stop_lat"].min()
    min_latitude = Latitude(min_latitude_as_float)
    min_latitude_as_string = convert_coordinate_to_degrees_and_minutes_string(min_latitude)
    return min_latitude_as_string


def get_maximum_longitude_as_string(dataset_stops):
    max_longitude_as_float = dataset_stops["stop_lon"].max()
    max_longitude = Longitude(max_longitude_as_float)
    max_longitude_as_string = convert_coordinate_to_degrees_and_minutes_string(max_longitude)
    return max_longitude_as_string


def get_minimum_longitude_as_string(dataset_stops):
    min_longitude_as_float = dataset_stops["stop_lon"].min()
    min_longitude = Longitude(min_longitude_as_float)
    min_longitude_as_string = convert_coordinate_to_degrees_and_minutes_string(min_longitude)
    return min_longitude_as_string


def convert_coordinate_to_degrees_and_minutes_string(coordinate_as_float):
    # Get the degrees, without the minus sign
    degrees = re.sub('-', '', coordinate_as_float.to_string('d'))

    # Get the minutes
    minutes = coordinate_as_float.to_string('m')

    # Get the seconds, rounded up to 3 decimals
    seconds = "%.3f" % float(coordinate_as_float.to_string('S'))

    # Get the hemisphere
    hemisphere = coordinate_as_float.to_string('H')

    # Join the strings together
    coordinate_as_string = degrees + "°" + minutes + "\'" + seconds + "\"" + hemisphere
    return coordinate_as_string

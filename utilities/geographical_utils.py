import re
from LatLon23 import Latitude, Longitude


def get_geographical_coordinates_as_string(dataset):
    max_lat_float, min_lat_float, max_lon_float, min_lon_float = get_geographical_coordinates_as_float(dataset.stops)

    max_lat_string = get_latitude_as_string(max_lat_float)
    min_lat_string = get_latitude_as_string(min_lat_float)
    max_lon_string = get_longitude_as_string(max_lon_float)
    min_lon_string = get_longitude_as_string(min_lon_float)

    return max_lat_string, min_lat_string, max_lon_string, min_lon_string


def get_geographical_coordinates_as_float(dataset_stops):
    max_lat_float = dataset_stops["stop_lat"].max()
    min_lat_float = dataset_stops["stop_lat"].min()
    max_lon_float = dataset_stops["stop_lon"].max()
    min_lon_float = dataset_stops["stop_lon"].min()

    return max_lat_float, min_lat_float, max_lon_float, min_lon_float


def get_latitude_as_string(lat_float):
    latitude = Latitude(lat_float)
    lat_string = convert_coordinate_to_degrees_and_minutes_string(latitude)
    return lat_string


def get_longitude_as_string(lon_float):
    longitude = Longitude(lon_float)
    lon_string = convert_coordinate_to_degrees_and_minutes_string(longitude)
    return lon_string


def get_octagon_corners_coordinates_as_string(dataset):
    # Get maximum and minimum geographical coordinates for further computation
    max_lat_float, min_lat_float, max_lon_float, min_lon_float = get_geographical_coordinates_as_float(dataset.stops)

    # Get octagon corners
    bottom_right_corner, right_bottom_corner = get_lower_right_octagon_corners(dataset.stops, min_lat_float,
                                                                               max_lon_float)
    bottom_left_corner, left_bottom_corner = get_lower_left_octagon_corners(dataset.stops, min_lat_float, min_lon_float)
    top_left_corner, left_top_corner = get_upper_left_octagon_corners(dataset.stops, max_lat_float, min_lon_float)
    top_right_corner, right_top_corner = get_upper_right_octagon_corners(dataset.stops, max_lat_float, max_lon_float)

    return [right_bottom_corner, bottom_right_corner,
            bottom_left_corner, left_bottom_corner,
            left_top_corner, top_left_corner,
            top_right_corner, right_top_corner]


def get_upper_right_octagon_corners(dataset_stops, max_lat_float, max_lon_float):
    maximum = 0
    max_stop = None

    for index, stop in dataset_stops.iterrows():
        current = stop["stop_lat"] + stop["stop_lon"]

        if max_stop is None:
            max_stop = stop
            maximum = current

        if current > maximum:
            maximum = current
            max_stop = stop

    # Compute the corners as float using maximum
    top_right_corner_lat_float = max_lat_float
    top_right_corner_lon_float = maximum - max_lat_float

    right_top_corner_lat_float = maximum - max_lon_float
    right_top_corner_lon_float = max_lon_float

    # Convert the corners coordinates to strings
    top_right_corner_lat_string = get_latitude_as_string(top_right_corner_lat_float)
    top_right_corner_lon_string = get_longitude_as_string(top_right_corner_lon_float)

    right_top_corner_lat_string = get_latitude_as_string(right_top_corner_lat_float)
    right_top_corner_lon_string = get_longitude_as_string(right_top_corner_lon_float)

    # Corners as strings
    top_right_corner_string = top_right_corner_lat_string + ", " + top_right_corner_lon_string
    right_top_corner_string = right_top_corner_lat_string + ", " + right_top_corner_lon_string

    return top_right_corner_string, right_top_corner_string


def get_lower_right_octagon_corners(dataset_stops, min_lat_float, max_lon_float):
    minimum = 0
    min_stop = None

    for index, stop in dataset_stops.iterrows():
        current = stop["stop_lat"] - stop["stop_lon"]

        if min_stop is None:
            min_stop = stop
            minimum = current

        if current < minimum:
            minimum = current
            min_stop = stop

    # Compute the corners as float using maximum
    bottom_right_corner_lat_float = min_lat_float
    bottom_right_corner_lon_float = (minimum - min_lat_float) * -1

    right_bottom_corner_lat_float = minimum + max_lon_float
    right_bottom_corner_lon_float = max_lon_float

    # Convert the corners coordinates to strings
    bottom_right_corner_lat_string = get_latitude_as_string(bottom_right_corner_lat_float)
    bottom_right_corner_lon_string = get_longitude_as_string(bottom_right_corner_lon_float)

    right_bottom_corner_lat_string = get_latitude_as_string(right_bottom_corner_lat_float)
    right_bottom_corner_lon_string = get_longitude_as_string(right_bottom_corner_lon_float)

    # Corners as strings
    bottom_right_corner_string = bottom_right_corner_lat_string + ", " + bottom_right_corner_lon_string
    right_bottom_corner_string = right_bottom_corner_lat_string + ", " + right_bottom_corner_lon_string

    return bottom_right_corner_string, right_bottom_corner_string


def get_lower_left_octagon_corners(dataset_stops, min_lat_float, min_lon_float):
    minimum = 0
    min_stop = None

    for index, stop in dataset_stops.iterrows():
        current = stop["stop_lat"] + stop["stop_lon"]

        if min_stop is None:
            min_stop = stop
            minimum = current

        if current < minimum:
            minimum = current
            min_stop = stop

    # Compute the corners as float using maximum
    bottom_left_corner_lat_float = min_lat_float
    bottom_left_corner_lon_float = minimum - min_lat_float

    left_bottom_corner_lat_float = minimum - min_lon_float
    left_bottom_corner_lon_float = min_lon_float

    # Convert the corners coordinates to strings
    bottom_left_corner_lat_string = get_latitude_as_string(bottom_left_corner_lat_float)
    bottom_left_corner_lon_string = get_longitude_as_string(bottom_left_corner_lon_float)

    left_bottom_corner_lat_string = get_latitude_as_string(left_bottom_corner_lat_float)
    left_bottom_corner_lon_string = get_longitude_as_string(left_bottom_corner_lon_float)

    # Corners as strings
    bottom_left_corner_string = bottom_left_corner_lat_string + ", " + bottom_left_corner_lon_string
    left_bottom_corner_string = left_bottom_corner_lat_string + ", " + left_bottom_corner_lon_string

    return bottom_left_corner_string, left_bottom_corner_string


def get_upper_left_octagon_corners(dataset_stops, max_lat_float, min_lon_float):
    maximum = 0
    max_stop = None

    for index, stop in dataset_stops.iterrows():
        current = stop["stop_lat"] - stop["stop_lon"]

        if max_stop is None:
            max_stop = stop
            maximum = current

        if current > maximum:
            maximum = current
            max_stop = stop

    # Compute the corners as float using maximum
    top_left_corner_lat_float = max_lat_float
    top_left_corner_lon_float = (maximum - max_lat_float) * -1

    left_top_corner_lat_float = maximum + min_lon_float
    left_top_corner_lon_float = min_lon_float

    # Convert the corners coordinates to strings
    top_left_corner_lat_string = get_latitude_as_string(top_left_corner_lat_float)
    top_left_corner_lon_string = get_longitude_as_string(top_left_corner_lon_float)

    left_top_corner_lat_string = get_latitude_as_string(left_top_corner_lat_float)
    left_top_corner_lon_string = get_longitude_as_string(left_top_corner_lon_float)

    # Corners as strings
    top_left_corner_string = top_left_corner_lat_string + ", " + top_left_corner_lon_string
    left_top_corner_string = left_top_corner_lat_string + ", " + left_top_corner_lon_string

    return top_left_corner_string, left_top_corner_string


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

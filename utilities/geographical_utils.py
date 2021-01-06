import re
from LatLon23 import Latitude, Longitude


def get_box_corners_coordinates_as_string(dataset):
    # Get max and min geographical coordinates as string
    max_lat_str, min_lat_str, max_lon_str, min_lon_str = get_geographical_coordinates_as_string(dataset.stops)

    # Create the box corners in string format from the max and min geographical coordinates
    # 4 corners : South-East, South-West, North-West and North-East
    se_corner_str, sw_corner_str, nw_corner_str, ne_corner_str = convert_geographical_coordinates_to_box_corners_string(
                                                                    max_lat_str, min_lat_str, max_lon_str, min_lon_str)

    return [se_corner_str, sw_corner_str, nw_corner_str, ne_corner_str]


def get_octagon_corners_coordinates_as_string(dataset):
    # Get max and min geographical coordinates as float for further computation
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


def get_geographical_coordinates_as_string(dataset_stops):
    max_lat_float, min_lat_float, max_lon_float, min_lon_float = get_geographical_coordinates_as_float(dataset_stops)

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
    # Use Latitude object to process conversion
    latitude = Latitude(lat_float)
    lat_string = convert_coordinate_to_degrees_and_minutes_string(latitude)

    return lat_string


def get_longitude_as_string(lon_float):
    # Use Longitude object to process conversion
    longitude = Longitude(lon_float)
    lon_string = convert_coordinate_to_degrees_and_minutes_string(longitude)

    return lon_string


def get_upper_right_octagon_corners(dataset_stops, max_lat_float, max_lon_float):
    # Maximize the addition maximum latitude + maximum longitude
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
    top_right_corner_string, right_top_corner_string = convert_octagon_section_corners_coordinates_to_string(
                                                                top_right_corner_lat_float, top_right_corner_lon_float,
                                                                right_top_corner_lat_float, right_top_corner_lon_float)

    return top_right_corner_string, right_top_corner_string


def get_lower_right_octagon_corners(dataset_stops, min_lat_float, max_lon_float):
    # Minimize the subtraction minimum latitude - maximum longitude
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
    btm_right_corner_lat_float = min_lat_float
    btm_right_corner_lon_float = (minimum - min_lat_float) * -1

    right_btm_corner_lat_float = minimum + max_lon_float
    right_btm_corner_lon_float = max_lon_float

    # Convert the corners coordinates to strings
    btm_right_corner_string, right_btm_corner_string = convert_octagon_section_corners_coordinates_to_string(
                                                            btm_right_corner_lat_float, btm_right_corner_lon_float,
                                                            right_btm_corner_lat_float, right_btm_corner_lon_float)

    return btm_right_corner_string, right_btm_corner_string


def get_lower_left_octagon_corners(dataset_stops, min_lat_float, min_lon_float):
    # Minimize the addition minimum latitude + minimum longitude
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
    btm_left_corner_lat_float = min_lat_float
    btm_left_corner_lon_float = minimum - min_lat_float

    left_btm_corner_lat_float = minimum - min_lon_float
    left_btm_corner_lon_float = min_lon_float

    # Convert the corners coordinates to strings
    btm_left_corner_string, left_btm_corner_string = convert_octagon_section_corners_coordinates_to_string(
                                                                btm_left_corner_lat_float, btm_left_corner_lon_float,
                                                                left_btm_corner_lat_float, left_btm_corner_lon_float)

    return btm_left_corner_string, left_btm_corner_string


def get_upper_left_octagon_corners(dataset_stops, max_lat_float, min_lon_float):
    # Maximize the subtraction maximum latitude - minimum longitude
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
    top_left_corner_string, left_top_corner_string = convert_octagon_section_corners_coordinates_to_string(
                                                                top_left_corner_lat_float, top_left_corner_lon_float,
                                                                left_top_corner_lat_float, left_top_corner_lon_float)

    return top_left_corner_string, left_top_corner_string


def convert_geographical_coordinates_to_box_corners_string(max_lat_str, min_lat_str, max_lon_str, min_lon_str):
    # Create the corner strings
    south_east_corner_str = min_lat_str + ", " + max_lon_str
    south_west_corner_str = min_lat_str + ", " + min_lon_str
    north_west_corner_str = max_lat_str + ", " + min_lon_str
    north_east_corner_str = max_lat_str + ", " + max_lon_str

    return south_east_corner_str, south_west_corner_str, north_west_corner_str, north_east_corner_str


def convert_octagon_section_corners_coordinates_to_string(corner_1_lat_float, corner_1_lon_float,
                                                          corner_2_lat_float, corner_2_lon_float):
    # Convert the corners coordinates to strings
    corner_1_lat_string = get_latitude_as_string(corner_1_lat_float)
    corner_1_lon_string = get_longitude_as_string(corner_1_lon_float)

    corner_2_lat_string = get_latitude_as_string(corner_2_lat_float)
    corner_2_lon_string = get_longitude_as_string(corner_2_lon_float)

    # Corners as strings
    corner_1_string = corner_1_lat_string + ", " + corner_1_lon_string
    corner_2_string = corner_2_lat_string + ", " + corner_2_lon_string

    return corner_1_string, corner_2_string


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

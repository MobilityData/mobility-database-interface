import re
from LatLon23 import Latitude, Longitude

STOP_LAT = "stop_lat"
STOP_LON = "stop_lon"

LAT_LON_23_DEGREES = "d"
LAT_LON_23_MINUTES = "m"
LAT_LON_23_SECONDS = "S"
LAT_LON_23_HEMISPHERE = "H"

IS_ADDITION = "is_addition"
IS_MAXIMUM = "is_maximum"

OCTAGON_LOWER_RIGHT_CORNER_MAP = {
    IS_ADDITION: False,
    IS_MAXIMUM: False,
}

OCTAGON_LOWER_LEFT_CORNER_MAP = {
    IS_ADDITION: True,
    IS_MAXIMUM: False,
}

OCTAGON_UPPER_LEFT_CORNER_MAP = {
    IS_ADDITION: False,
    IS_MAXIMUM: True,
}

OCTAGON_UPPER_RIGHT_CORNER_MAP = {
    IS_ADDITION: True,
    IS_MAXIMUM: True,
}


def process_bounding_box_corner_strings(dataset):
    #  max and min geographical coordinates as string
    (
        max_lat_str,
        min_lat_str,
        max_lon_str,
        min_lon_str,
    ) = process_geographical_coordinates_as_string(dataset.stops)

    # Create the box corners in string format from the max and min geographical coordinates
    # 4 corners : South-East, South-West, North-West and North-East
    (
        se_corner_str,
        sw_corner_str,
        nw_corner_str,
        ne_corner_str,
    ) = convert_geographical_coordinates_to_box_corner_strings(
        max_lat_str, min_lat_str, max_lon_str, min_lon_str
    )

    return [se_corner_str, sw_corner_str, nw_corner_str, ne_corner_str]


def process_bounding_octagon_corner_strings(dataset):
    # Get max and min geographical coordinates as float for further computation
    (
        max_lat_float,
        min_lat_float,
        max_lon_float,
        min_lon_float,
    ) = extract_geographical_coordinates_as_float(dataset.stops)

    # Minimize the subtraction latitude - longitude
    # Then use the min_lat and max_long to compute the lower right quadrant corners
    bottom_right_corner, right_bottom_corner = process_octagon_local_corners(
        dataset.stops, min_lat_float, max_lon_float, OCTAGON_LOWER_RIGHT_CORNER_MAP
    )

    # Minimize the addition latitude + longitude
    # Then use the min_lat and min_long to compute the lower left quadrant corners
    bottom_left_corner, left_bottom_corner = process_octagon_local_corners(
        dataset.stops, min_lat_float, min_lon_float, OCTAGON_LOWER_LEFT_CORNER_MAP
    )

    # Maximize the subtraction latitude - longitude
    # Then use the max_lat and min_long to compute the upper left quadrant corners
    top_left_corner, left_top_corner = process_octagon_local_corners(
        dataset.stops, max_lat_float, min_lon_float, OCTAGON_UPPER_LEFT_CORNER_MAP
    )

    # Maximize the addition latitude + longitude
    # Then use the max_lat and max_long to compute the upper right quadrant corners
    top_right_corner, right_top_corner = process_octagon_local_corners(
        dataset.stops, max_lat_float, max_lon_float, OCTAGON_UPPER_RIGHT_CORNER_MAP
    )

    return [
        right_bottom_corner,
        bottom_right_corner,
        bottom_left_corner,
        left_bottom_corner,
        left_top_corner,
        top_left_corner,
        top_right_corner,
        right_top_corner,
    ]


def process_geographical_coordinates_as_string(dataset_stops):
    (
        max_lat_float,
        min_lat_float,
        max_lon_float,
        min_lon_float,
    ) = extract_geographical_coordinates_as_float(dataset_stops)

    max_lat_string = convert_coordinate_to_degrees_and_minutes_string(
        Latitude, max_lat_float
    )
    min_lat_string = convert_coordinate_to_degrees_and_minutes_string(
        Latitude, min_lat_float
    )
    max_lon_string = convert_coordinate_to_degrees_and_minutes_string(
        Longitude, max_lon_float
    )
    min_lon_string = convert_coordinate_to_degrees_and_minutes_string(
        Longitude, min_lon_float
    )

    return max_lat_string, min_lat_string, max_lon_string, min_lon_string


def extract_geographical_coordinates_as_float(dataset_stops):
    max_lat_float = dataset_stops[STOP_LAT].max()
    min_lat_float = dataset_stops[STOP_LAT].min()
    max_lon_float = dataset_stops[STOP_LON].max()
    min_lon_float = dataset_stops[STOP_LON].min()

    return max_lat_float, min_lat_float, max_lon_float, min_lon_float


def process_octagon_local_corners(
    dataset_stops, lat_float, lon_float, octagon_corner_map
):
    # Process the corners of an octagon which are located in the same Cartesian quadrant
    # For example, top_right_corner and right_top_corner both belong to the 1st quadrant
    best_value = 0
    best_stop = None

    # Process local corners according to the situation
    # For example, for the 1st quadrant, we want to maximize the addition of latitude and longitude
    # Each situation is detailed above when this function is called
    # within the process_bounding_octagon_corner_strings method
    for index, stop in dataset_stops.iterrows():
        if octagon_corner_map[IS_ADDITION]:
            current = stop[STOP_LAT] + stop[STOP_LON]
        else:
            current = stop[STOP_LAT] - stop[STOP_LON]

        if best_stop is None:
            best_stop = stop
            best_value = current

        if octagon_corner_map[IS_MAXIMUM]:
            comparison_result = current > best_value
        else:
            comparison_result = current < best_value

        if comparison_result:
            best_value = current
            best_stop = stop

    # Compute the corners as float using best value
    # Corner follow the Y and X axis, where Y is Tor or Bottom, and X is Right or Left
    # For example, y_x_corner can stand for top_right_corner, where x_y_corner is right_top_corner
    y_x_corner_lat_float = lat_float

    if octagon_corner_map[IS_ADDITION]:
        y_x_corner_lon_float = best_value - lat_float
        x_y_corner_lat_float = best_value - lon_float
    else:
        y_x_corner_lon_float = (best_value - lat_float) * -1
        x_y_corner_lat_float = best_value + lon_float

    x_y_corner_lon_float = lon_float

    # Convert the corners coordinates to strings
    (
        y_x_corner_string,
        x_y_corner_string,
    ) = convert_octagon_section_corners_coordinates_to_corner_strings(
        y_x_corner_lat_float,
        y_x_corner_lon_float,
        x_y_corner_lat_float,
        x_y_corner_lon_float,
    )

    return y_x_corner_string, x_y_corner_string


def convert_geographical_coordinates_to_box_corner_strings(
    max_lat_str, min_lat_str, max_lon_str, min_lon_str
):
    # Create the corner strings
    south_east_corner_str = f"{min_lat_str}, {max_lon_str}"
    south_west_corner_str = f"{min_lat_str}, {min_lon_str}"
    north_west_corner_str = f"{max_lat_str}, {min_lon_str}"
    north_east_corner_str = f"{max_lat_str}, {max_lon_str}"

    return (
        south_east_corner_str,
        south_west_corner_str,
        north_west_corner_str,
        north_east_corner_str,
    )


def convert_octagon_section_corners_coordinates_to_corner_strings(
    corner_1_lat_float, corner_1_lon_float, corner_2_lat_float, corner_2_lon_float
):
    # Convert the corners coordinates to strings
    corner_1_lat_string = convert_coordinate_to_degrees_and_minutes_string(
        Latitude, corner_1_lat_float
    )
    corner_1_lon_string = convert_coordinate_to_degrees_and_minutes_string(
        Longitude, corner_1_lon_float
    )

    corner_2_lat_string = convert_coordinate_to_degrees_and_minutes_string(
        Latitude, corner_2_lat_float
    )
    corner_2_lon_string = convert_coordinate_to_degrees_and_minutes_string(
        Longitude, corner_2_lon_float
    )

    # Corners as strings
    corner_1_string = f"{corner_1_lat_string}, {corner_1_lon_string}"
    corner_2_string = f"{corner_2_lat_string}, {corner_2_lon_string}"

    return corner_1_string, corner_2_string


def convert_coordinate_to_degrees_and_minutes_string(
    coordinate_class, coordinate_float
):
    # Create LatLon23 object with the coordinate_class and coordinate_float
    coordinate = coordinate_class(coordinate_float)

    # Get the degrees, without the minus sign
    degrees = re.sub("-", "", coordinate.to_string(LAT_LON_23_DEGREES))

    # Get the minutes
    minutes = coordinate.to_string(LAT_LON_23_MINUTES)

    # Get the seconds, rounded up to 3 decimals
    seconds = f"{float(coordinate.to_string(LAT_LON_23_SECONDS)):.3f}"

    # Get the hemisphere
    hemisphere = coordinate.to_string(LAT_LON_23_HEMISPHERE)

    # Join the strings together
    coordinate_as_string = f"""{degrees}°{minutes}'{seconds}"{hemisphere}"""

    return coordinate_as_string

#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
- LICENCE

The MIT License (MIT)

Copyright (c) 2016 Eleftherios Anagnostopoulos for Ericsson AB (EU FP7 CityPulse Project)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


- DESCRIPTION OF DOCUMENTS

-- MongoDB Database Documents:

address_document: {
    '_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}
}
bus_line_document: {
    '_id', 'bus_line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
}
bus_stop_document: {
    '_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}
}
bus_stop_waypoints_document: {
    '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[edge_object_id]]
}
bus_vehicle_document: {
    '_id', 'bus_vehicle_id', 'maximum_capacity',
    'routes': [{'starting_datetime', 'ending_datetime', 'timetable_id'}]
}
detailed_bus_stop_waypoints_document: {
    '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[edge_document]]
}
edge_document: {
    '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    'max_speed', 'road_type', 'way_id', 'traffic_density'
}
node_document: {
    '_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}
}
point_document: {
    '_id', 'osm_id', 'point': {'longitude', 'latitude'}
}
timetable_document: {
    '_id', 'timetable_id', 'bus_line_id', 'bus_vehicle_id',
    'timetable_entries': [{
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime', 'number_of_onboarding_passengers',
        'number_of_deboarding_passengers', 'number_of_current_passengers',
        'route': {
            'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
            'distances_from_starting_node', 'times_from_starting_node',
            'distances_from_previous_node', 'times_from_previous_node'
        }
    }],
    'travel_requests': [{
        '_id', 'client_id', 'bus_line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }]
}
traffic_event_document: {
    '_id', 'event_id', 'event_type', 'event_level', 'point': {'longitude', 'latitude'}, 'datetime'
}
travel_request_document: {
    '_id', 'client_id', 'bus_line_id',
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'departure_datetime', 'arrival_datetime',
    'starting_timetable_entry_index', 'ending_timetable_entry_index'
}
way_document: {
    '_id', 'osm_id', 'tags', 'references'
}

-- Route Generator Responses:

get_route_between_two_bus_stops: {
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'route': {
        'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        'distances_from_starting_node', 'times_from_starting_node',
        'distances_from_previous_node', 'times_from_previous_node'
    }
}
get_route_between_multiple_bus_stops: [{
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'route': {
        'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        'distances_from_starting_node', 'times_from_starting_node',
        'distances_from_previous_node', 'times_from_previous_node'
    }
}]
get_waypoints_between_two_bus_stops: {
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[{
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'
    }]]
}
get_waypoints_between_multiple_bus_stops: [{
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[{
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'
    }]]
}]
"""
import math
import numpy as np

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class Point(object):
    """
    A geographic point on a map represented by Latitude and Longitude.

    Longitude and Latitude are floating point values in degrees.
    """

    def __init__(self, longitude=0.0, latitude=0.0):
        self.longitude = float(longitude)
        self.latitude = float(latitude)

    def __str__(self):
        return str(self.__dict__)
        # return self.coordinates_to_string()

    def __repr__(self):
        return str(self.__dict__)
        # return self.coordinates_to_string()

    def coordinates(self):
        return self.longitude, self.latitude

    def longitude(self):
        return self.longitude

    def latitude(self):
        return self.latitude

    def coordinates_to_string(self):
        return '(' + str(self.longitude) + ', ' + str(self.latitude) + ')'

    def equal_to_coordinates(self, longitude, latitude):
        return self.longitude == longitude and self.latitude == latitude


def distance(point_one=None, point_two=None, longitude_one=None, latitude_one=None,
             longitude_two=None, latitude_two=None):
    """
    Calculate the great circle distance (in meters) between two geographic points
    (specified in decimal degrees).

    :type point_one: Point
    :type point_two: Point
    :type longitude_one: float
    :type latitude_one: float
    :type longitude_two: float
    :type latitude_two: float
    """
    if (point_one is None and (longitude_one is None or latitude_one in None)) \
            or (point_two is None and (longitude_two is None or latitude_two in None)):
        return -1

    if point_one is not None:
        if isinstance(point_one, Point):
            longitude_one, latitude_one = point_one.coordinates()
        else:
            longitude_one, latitude_one = point_one

    if point_two is not None:
        if isinstance(point_two, Point):
            longitude_two, latitude_two = point_two.coordinates()
        else:
            longitude_two, latitude_two = point_two

    # Radius of the earth in meters
    earth_radius = 6371000

    distance_longitude = (longitude_two - longitude_one) * math.pi / 180
    distance_latitude = (latitude_two - latitude_one) * math.pi / 180

    a = math.sin(distance_latitude / 2) ** 2 \
        + math.cos(latitude_one * math.pi / 180) \
        * math.cos(latitude_two * math.pi / 180) \
        * math.sin(distance_longitude / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_in_meters = earth_radius * c

    return distance_in_meters


def average(points):
    """
    Find the average value for the longitude and latitude values in a list of geographic points.

    :param points: [Point]
    :return: Point
    """
    tuples = [point.coordinates() for point in points]
    avg = [sum(y) / len(y) for y in zip(*tuples)]

    return Point(avg[0], avg[1])


def center(points):
    """
    Calculate the center of multiple geographic points.

    :param points: [Point]
    :return: Point
    """
    tuples = [point.coordinates() for point in points]
    _max = reduce(lambda x, y: (max(x[0], y[0]), max(x[1], y[1])), tuples)
    _min = reduce(lambda x, y: (min(x[0], y[0]), min(x[1], y[1])), tuples)
    _longitude = _max[0] - ((_max[0] - _min[0]) / 2)
    _latitude = _max[1] - ((_max[1] - _min[1]) / 2)

    return Point(longitude=_longitude, latitude=_latitude)


def closest_point_in_list(point, points):
    """
    Retrieve the point, from a list of points, which has the minimum distance from a given point.

    :param point: Point
    :param points: [Point]
    :return: Point
    """
    return points[np.argmin([distance(point, pointy) for pointy in points])]


def y2lat(y):
    """
    Translate a y-axis coordinate to longitude geographic coordinate, assuming
    a spherical Mercator projection.

    :param y: float
    :return: float
    """
    return 180.0 / math.pi * (2.0 * math.atan(math.exp(y * math.pi / 180.0)) - math.pi / 2.0)


def lat2y(latitude):
    """
    Translate a latitude coordinate to a projection on the y-axis, using
    spherical Mercator projection.

    :param latitude: float
    :return: float
    """
    return 180.0 / math.pi * (math.log(math.tan(math.pi / 4.0 + latitude * (math.pi / 180.0) / 2.0)))

"""
Copyright 2016 Eleftherios Anagnostopoulos for Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import math
import numpy as np


class Point(object):
    """
    A geographic point on a map represented by Latitude and Longitude.

    Longitude and Latitude are floating point values in degrees.
    """

    def __init__(self, longitude=0.0, latitude=0.0):
        self.longitude = float(longitude)
        self.latitude = float(latitude)

    def __str__(self):
        return self.coordinates_to_string()

    def __repr__(self):
        return self.coordinates_to_string()

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


def distance(point_one, point_two):
    """
    Calculate the great circle distance (in meters) between two geographic points (specified in decimal degrees).

    :param point_one: Point
    :param point_two: Point
    """
    if isinstance(point_one, Point):
        longitude_one, latitude_one = point_one.coordinates()
    else:
        longitude_one, latitude_one = point_one

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

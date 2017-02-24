#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
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
"""
import requests
import json
from bson import ObjectId
from src.common.parameters import route_generator_host, route_generator_port, route_generator_request_timeout

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class JSONResponseEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return o.__dict__


def get_route_between_two_bus_stops(starting_bus_stop=None, ending_bus_stop=None,
                                    starting_bus_stop_name=None, ending_bus_stop_name=None):
    """
    bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

    :param starting_bus_stop: bus_stop_document
    :param ending_bus_stop: bus_stop_document
    :param starting_bus_stop_name: string
    :param ending_bus_stop_name: string
    :return: {'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
              'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
              'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                        'distances_from_starting_node', 'times_from_starting_node',
                        'distances_from_previous_node', 'times_from_previous_node'}}
    """
    url = 'http://' + route_generator_host + ':' + route_generator_port + '/get_route_between_two_bus_stops'
    # headers = {'content-type': 'application/x-www-form-urlencoded'}
    headers = {'content-type': 'application/json'}
    data = {
        'starting_bus_stop': starting_bus_stop,
        'ending_bus_stop': ending_bus_stop,
        'starting_bus_stop_name': starting_bus_stop_name,
        'ending_bus_stop_name': ending_bus_stop_name
    }
    json_data = json.dumps(data, cls=JSONResponseEncoder)
    request = requests.post(url, data=json_data, headers=headers, timeout=route_generator_request_timeout)
    response = json.loads(request.text)
    return response


def get_route_between_multiple_bus_stops(bus_stops=None, bus_stop_names=None):
    """
    bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

    :param bus_stops: [bus_stop_document]
    :param bus_stop_names: [string]
    :return: [{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                         'distances_from_starting_node', 'times_from_starting_node',
                         'distances_from_previous_node', 'times_from_previous_node'}}]
    """
    url = 'http://' + route_generator_host + ':' + route_generator_port + '/get_route_between_multiple_bus_stops'
    # headers = {'content-type': 'application/x-www-form-urlencoded'}
    headers = {'content-type': 'application/json'}
    data = {
        'bus_stops': bus_stops,
        'bus_stop_names': bus_stop_names
    }
    json_data = json.dumps(data, cls=JSONResponseEncoder)
    request = requests.post(url, data=json_data, headers=headers, timeout=route_generator_request_timeout)
    response = json.loads(request.text)
    return response


def get_waypoints_between_two_bus_stops(starting_bus_stop=None, ending_bus_stop=None,
                                        starting_bus_stop_name=None, ending_bus_stop_name=None):
    """
    bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

    :param starting_bus_stop: bus_stop_document
    :param ending_bus_stop: bus_stop_document
    :param starting_bus_stop_name: string
    :param ending_bus_stop_name: string
    :return: {'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
              'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
              'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                              'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                              'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}
    """
    url = 'http://' + route_generator_host + ':' + route_generator_port + '/get_waypoints_between_two_bus_stops'
    # headers = {'content-type': 'application/x-www-form-urlencoded'}
    headers = {'content-type': 'application/json'}
    data = {
        'starting_bus_stop': starting_bus_stop,
        'ending_bus_stop': ending_bus_stop,
        'starting_bus_stop_name': starting_bus_stop_name,
        'ending_bus_stop_name': ending_bus_stop_name
    }
    json_data = json.dumps(data, cls=JSONResponseEncoder)
    request = requests.post(url, data=json_data, headers=headers, timeout=route_generator_request_timeout)
    response = json.loads(request.text)
    return response


def get_waypoints_between_multiple_bus_stops(bus_stops=None, bus_stop_names=None):
    """
    bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

    :param bus_stops: [bus_stop_document]
    :param bus_stop_names: [string]
    :return: [{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                               'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                               'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}]
    """
    url = 'http://' + route_generator_host + ':' + route_generator_port + '/get_waypoints_between_multiple_bus_stops'
    # headers = {'content-type': 'application/x-www-form-urlencoded'}
    headers = {'content-type': 'application/json'}
    data = {
        'bus_stops': bus_stops,
        'bus_stop_names': bus_stop_names
    }
    json_data = json.dumps(data, cls=JSONResponseEncoder)
    request = requests.post(url, data=json_data, headers=headers, timeout=route_generator_request_timeout)
    response = json.loads(request.text)
    return response

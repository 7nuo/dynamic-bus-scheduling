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
from src.route_generator.path_finder import find_path_between_two_nodes
from src.route_generator.multiple_paths_finder import find_waypoints_between_two_nodes
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port
from src.geospatial_data.point import distance, Point
from src.mongodb_database.mongodb_database_connection import MongodbDatabaseConnection

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class Router(object):
    def __init__(self):
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='Router', log_type='DEBUG', log_message='mongodb_database_connection: established')

    def get_bus_stop(self, name=None, provided_point=None, longitude=None, latitude=None):
        """
        Get a bus_stop_document.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param name: string
        :param provided_point: Point
        :param longitude: float
        :param latitude: float
        :return: bus_stop: bus_stop_document
        """
        bus_stop = None

        if name is not None:
            bus_stop = self.mongodb_database_connection.find_bus_stop_document(name=name)
        elif provided_point is not None:
            bus_stop_documents = self.mongodb_database_connection.find_bus_stop_documents()
            bus_stop = self.get_bus_stop_closest_to_point(
                bus_stop_documents=bus_stop_documents,
                provided_point=provided_point
            )
        elif longitude is not None and latitude is not None:
            point = Point(longitude=longitude, latitude=latitude)
            bus_stop_documents = self.mongodb_database_connection.find_bus_stop_documents()
            bus_stop = self.get_bus_stop_closest_to_point(
                bus_stop_documents=bus_stop_documents,
                provided_point=point
            )
        else:
            pass

        return bus_stop

    @staticmethod
    def get_bus_stop_closest_to_point(bus_stop_documents, provided_point):
        """
        Get the bus stop which is closest to a geographic point.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param bus_stop_documents: [bus_stop_document]
        :param provided_point: Point
        :return closest_bus_stop: bus_stop_document
        """
        minimum_distance = float('Inf')
        closest_bus_stop = None

        for bus_stop_document in bus_stop_documents:
            bus_stop_document_point = bus_stop_document.get('point')

            current_distance = distance(
                point_one=provided_point,
                longitude_two=bus_stop_document_point.get('longitude'),
                latitude_two=bus_stop_document_point.get('latitude')
            )
            if current_distance == 0:
                closest_bus_stop = bus_stop_document
                break
            elif current_distance < minimum_distance:
                minimum_distance = current_distance
                closest_bus_stop = bus_stop_document
            else:
                pass

        return closest_bus_stop

    def get_bus_stops(self, names):
        """
        Get multiple bus_stop_documents.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param names: [string]
        :return: bus_stops: [bus_stop_document]
        """
        bus_stops = []

        # for name in names:
        #     bus_stop = self.get_bus_stop(name=name)
        #     bus_stops.append(bus_stop)

        bus_stop_documents = self.mongodb_database_connection.find_bus_stop_documents(names=names)
        bus_stop_documents_dictionary = {}

        for bus_stop_document in bus_stop_documents:
            bus_stop_document_name = bus_stop_document.get('name')
            bus_stop_documents_dictionary[bus_stop_document_name] = bus_stop_document

        for name in names:
            bus_stop_document = bus_stop_documents_dictionary.get(name)
            bus_stops.append(bus_stop_document)

        return bus_stops

    def get_bus_stops_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the BusStops collection.

        :return: bus_stops_dictionary: {name -> {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}}
        """
        bus_stops_dictionary = self.mongodb_database_connection.get_bus_stops()
        return bus_stops_dictionary

    def get_bus_stops_list(self):
        """
        Retrieve a list containing all the documents of the BusStops collection.

        :return: bus_stops_list: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        """
        bus_stops_list = self.mongodb_database_connection.get_bus_stop_documents_list()
        return bus_stops_list

    def get_edges_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Edges collection.

        :return: {starting_node_osm_id -> [{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                            'max_speed', 'road_type', 'way_id', 'traffic_density'}]}
        """
        edges_dictionary = self.mongodb_database_connection.get_edges_dictionary()
        return edges_dictionary

    def get_edges_list(self):
        """
        Retrieve a list containing all the documents of the Edges collection.

        :return: edges_list: [{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                               'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                               'max_speed', 'road_type', 'way_id', 'traffic_density'}]
        """
        edges_list = self.mongodb_database_connection.get_edge_documents_list()
        return edges_list

    def get_points_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Points collection.

        :return points_dictionary: {osm_id -> {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}}
        """
        points_dictionary = self.mongodb_database_connection.get_points()
        return points_dictionary

    def get_route_between_two_bus_stops(self, starting_bus_stop=None, ending_bus_stop=None,
                                        starting_bus_stop_name=None, ending_bus_stop_name=None,
                                        edges_dictionary=None):
        """
        Find a route between two bus_stops.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param starting_bus_stop: bus_stop_document
        :param ending_bus_stop: bus_stop_document
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :param edges_dictionary: {starting_node_osm_id -> [edge_document]}
        :return response: {
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                              'distances_from_starting_node', 'times_from_starting_node',
                              'distances_from_previous_node', 'times_from_previous_node'}}
        """
        if starting_bus_stop is None and starting_bus_stop_name is not None:
            starting_bus_stop = self.get_bus_stop(name=starting_bus_stop_name)

        if ending_bus_stop is None and ending_bus_stop_name is not None:
            ending_bus_stop = self.get_bus_stop(name=ending_bus_stop_name)

        if edges_dictionary is None:
            edges_dictionary = self.get_edges_dictionary()

        route = find_path_between_two_nodes(
            start=starting_bus_stop,
            end=ending_bus_stop,
            edges_dictionary=edges_dictionary
        )
        response = {
            'starting_bus_stop': starting_bus_stop,
            'ending_bus_stop': ending_bus_stop,
            'route': route
        }
        return response

    def get_route_between_multiple_bus_stops(self, bus_stops=None, bus_stop_names=None):
        """
        Find a route between multiple bus_stop, based on their names.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: string
        :return response: [{
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                              'distances_from_starting_node', 'times_from_starting_node',
                              'distances_from_previous_node', 'times_from_previous_node'}}]
        """
        response = []
        edges_dictionary = self.get_edges_dictionary()

        if bus_stops is None and bus_stop_names is not None:
            bus_stops = self.get_bus_stops(names=bus_stop_names)

        for i in range(0, len(bus_stops) - 1):
            starting_bus_stop = bus_stops[i]
            ending_bus_stop = bus_stops[i + 1]

            intermediate_route = self.get_route_between_two_bus_stops(
                starting_bus_stop=starting_bus_stop,
                ending_bus_stop=ending_bus_stop,
                edges_dictionary=edges_dictionary
            )
            response.append(intermediate_route)

        return response

    def get_waypoints_between_two_bus_stops(self, starting_bus_stop=None, ending_bus_stop=None,
                                            starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Find the waypoints of all possible routes between two bus_stops, based on their names.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param starting_bus_stop: bus_stop_document
        :param ending_bus_stop: bus_stop_document
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return response: {
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                    'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                    'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}
        """
        if starting_bus_stop is None and starting_bus_stop_name is not None:
            starting_bus_stop = self.get_bus_stop(name=starting_bus_stop_name)

        if ending_bus_stop is None and ending_bus_stop_name is not None:
            ending_bus_stop = self.get_bus_stop(name=ending_bus_stop_name)

        edges_dictionary = self.get_edges_dictionary()

        waypoints = find_waypoints_between_two_nodes(
            starting_node_osm_id=starting_bus_stop.get('osm_id'),
            ending_node_osm_id=ending_bus_stop.get('osm_id'),
            edges_dictionary=edges_dictionary
        )
        response = {
            'starting_bus_stop': starting_bus_stop,
            'ending_bus_stop': ending_bus_stop,
            'waypoints': waypoints
        }
        return response

    def get_waypoints_between_multiple_bus_stops(self, bus_stops=None, bus_stop_names=None):
        """
        Find the waypoints of all possible routes between multiple bus_stops, based on their names.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: string
        :return response: [{
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                    'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                    'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}]
        """
        response = []

        if bus_stops is None and bus_stop_names is not None:
            bus_stops = self.get_bus_stops(names=bus_stop_names)

        edges_dictionary = self.get_edges_dictionary()

        for i in range(0, len(bus_stops) - 1):
            starting_bus_stop = bus_stops[i]
            ending_bus_stop = bus_stops[i + 1]

            waypoints = find_waypoints_between_two_nodes(
                starting_node_osm_id=starting_bus_stop.get('osm_id'),
                ending_node_osm_id=ending_bus_stop.get('osm_id'),
                edges_dictionary=edges_dictionary
            )
            intermediate_response = {
                'starting_bus_stop': starting_bus_stop,
                'ending_bus_stop': ending_bus_stop,
                'waypoints': waypoints
            }
            response.append(intermediate_response)

        return response

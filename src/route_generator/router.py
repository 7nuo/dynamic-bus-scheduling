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
from path_finder import find_path_between_two_nodes
from multiple_paths_finder import find_waypoints_between_two_nodes
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port, route_generator_edges_updater_timeout, \
    route_generator_edges_updater_max_operation_timeout
from src.geospatial_data.point import distance, Point
from src.mongodb_database.mongodb_database_connection import MongodbDatabaseConnection
from multiprocessing import Process
import time


class Router(object):
    def __init__(self):
        self.connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='Router', log_type='DEBUG', log_message='mongodb_database_connection: established')
        self.bus_stops_dictionary = {}
        self.edges_dictionary = {}
        self.points_dictionary = {}
        self.initialize_dictionaries()
        log(module_name='Router', log_type='DEBUG', log_message='initialize_dictionaries: ok')
        self.edges_updater_process = Process(target=self.update_edges_dictionary, args=())
        log(module_name='Router', log_type='DEBUG', log_message='initialize_edges_updater_process: ok')
        self.start_edges_updater_process()

    def initialize_dictionaries(self):
        self.bus_stops_dictionary = self.get_bus_stops_dictionary()
        self.edges_dictionary = self.get_edges_dictionary()
        self.points_dictionary = self.get_points_dictionary()

    def get_bus_stop_closest_to_coordinates(self, longitude, latitude):
        """
        Get the bus stop which is closest to a set of coordinates.

        :type longitude: float
        :type latitude: float
        :return bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        provided_point = Point(longitude=longitude, latitude=latitude)
        bus_stop = self.get_bus_stop_closest_to_point(provided_point=provided_point)
        return bus_stop

    def get_bus_stop_closest_to_point(self, provided_point):
        """
        Get the bus stop which is closest to a geographic point.

        :type provided_point: Point
        :return bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        minimum_distance = float('Inf')
        closest_bus_stop = None

        # bus_stops_dictionary: {name -> {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}}
        #
        for bus_stop in self.bus_stops_dictionary.values():
            bus_stop_point = bus_stop.get('point')

            current_distance = distance(
                point_one=provided_point,
                longitude_two=bus_stop_point.get('longitude'),
                latitude_two=bus_stop_point.get('latitude')
            )

            if current_distance == 0:
                closest_bus_stop = bus_stop
                break
            elif current_distance < minimum_distance:
                minimum_distance = current_distance
                closest_bus_stop = bus_stop
            else:
                pass

        return closest_bus_stop

    def get_bus_stop_from_coordinates(self, longitude, latitude):
        """
        Get the bus_stop which corresponds to a set of coordinates.

        :type longitude: float
        :type latitude: float
        :return bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        bus_stop = None

        # bus_stops_dictionary: {name -> {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}}
        #
        for current_bus_stop in self.bus_stops_dictionary.values():
            current_bus_stop_point = current_bus_stop.get('point')

            if (current_bus_stop_point.get('longitude') == longitude and
                        current_bus_stop_point.get('latitude') == latitude):
                bus_stop = current_bus_stop
                break

        return bus_stop

    def get_bus_stop_from_name(self, name):
        """
        Get the bus_stop which corresponds to a name.

        :type name: string
        :return bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        name = name.decode('utf-8')
        bus_stop = self.bus_stops_dictionary.get(name)
        return bus_stop

    def get_bus_stop_from_point(self, point):
        """
        Get the bus_stop which corresponds to a name.

        :type point: Point
        :return bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        bus_stop = self.get_bus_stop_from_coordinates(longitude=point.longitude, latitude=point.latitude)
        return bus_stop

    def get_bus_stops(self, names):
        """
        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param names: [string]
        :return: bus_stops: [bus_stop_document]
        """
        bus_stops = []

        for name in names:
            bus_stop = self.get_bus_stop_from_name(name=name)
            bus_stops.append(bus_stop)

        return bus_stops

    def get_bus_stops_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the BusStops collection.

        :return: bus_stops_dictionary: {name -> {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}}
        """
        bus_stops_dictionary = self.connection.get_bus_stop_documents_dictionary()
        return bus_stops_dictionary

    def get_bus_stops_list(self):
        """
        Retrieve a list containing all the documents of the BusStops collection.

        :return: bus_stops_list: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        """
        bus_stops_list = self.connection.get_bus_stop_documents_list()
        return bus_stops_list

    def get_edges_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Edges collection.

        :return: {starting_node_osm_id -> [{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                            'max_speed', 'road_type', 'way_id', 'traffic_density'}]}
        """
        edges_dictionary = self.connection.get_edge_documents_dictionary()
        return edges_dictionary

    def get_edges_list(self):
        """
        Retrieve a list containing all the documents of the Edges collection.

        :return: edges_list: [{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                               'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                               'max_speed', 'road_type', 'way_id', 'traffic_density'}]
        """
        edges_list = self.connection.get_edge_documents_list()
        return edges_list

    def get_points_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Points collection.

        :return points_dictionary: {osm_id -> {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}}
        """
        points_dictionary = self.connection.get_point_documents_dictionary()
        return points_dictionary

    def get_route_between_two_bus_stops(self, starting_bus_stop=None, ending_bus_stop=None,
                                        starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Find a route between two bus_stops.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param starting_bus_stop: bus_stop_document
        :param ending_bus_stop: bus_stop_document
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return response: {
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                              'distances_from_starting_node', 'times_from_starting_node',
                              'distances_from_previous_node', 'times_from_previous_node'}}
        """
        if starting_bus_stop is None and starting_bus_stop_name is not None:
            starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)

        if ending_bus_stop is None and ending_bus_stop_name is not None:
            ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

        route = find_path_between_two_nodes(
            starting_node_osm_id=starting_bus_stop.get('osm_id'),
            ending_node_osm_id=ending_bus_stop.get('osm_id'),
            edges_dictionary=self.edges_dictionary,
            points_dictionary=self.points_dictionary
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

        if bus_stops is None and bus_stop_names is not None:
            bus_stops = self.get_bus_stops(names=bus_stop_names)

        for i in range(0, len(bus_stops) - 1):
            starting_bus_stop = bus_stops[i]
            ending_bus_stop = bus_stops[i + 1]

            intermediate_route = self.get_route_between_two_bus_stops(
                starting_bus_stop=starting_bus_stop,
                ending_bus_stop=ending_bus_stop
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
            starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)

        if ending_bus_stop is None and ending_bus_stop_name is not None:
            ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

        waypoints = find_waypoints_between_two_nodes(
            starting_node_osm_id=starting_bus_stop.get('osm_id'),
            ending_node_osm_id=ending_bus_stop.get('osm_id'),
            edges_dictionary=self.edges_dictionary
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

        for i in range(0, len(bus_stop_names) - 1):
            starting_bus_stop = bus_stops[i]
            ending_bus_stop = bus_stops[i + 1]

            waypoints = find_waypoints_between_two_nodes(
                starting_node_osm_id=starting_bus_stop.get('osm_id'),
                ending_node_osm_id=ending_bus_stop.get('osm_id'),
                edges_dictionary=self.edges_dictionary
            )
            intermediate_response = {
                'starting_bus_stop': starting_bus_stop,
                'ending_bus_stop': ending_bus_stop,
                'waypoints': waypoints
            }
            response.append(intermediate_response)

        return response

    def start_edges_updater_process(self):
        self.edges_updater_process.start()
        log(module_name='Router', log_type='DEBUG', log_message='edges_updater_process: started')

    def terminate_edges_updater_process(self):
        self.edges_updater_process.terminate()
        self.edges_updater_process.join()
        log(module_name='Router', log_type='DEBUG', log_message='edges_updater_process: finished')

    def update_edges_dictionary(self):
        """
        Update the edges dictionary periodically, based on route_generator_edges_updater_timeout parameter.
        The function stops execution, after route_generator_edges_updater_max_operation_timeout seconds.

        :return: None
        """
        time_difference = 0
        initial_time = time.time()

        while time_difference < route_generator_edges_updater_max_operation_timeout:
            self.edges_dictionary = self.get_edges_dictionary()
            log(module_name='Router', log_type='DEBUG', log_message='edges_dictionary updated')
            time.sleep(route_generator_edges_updater_timeout)
            time_difference = time.time() - initial_time

        log(module_name='Router', log_type='DEBUG', log_message='edges_updater_process: finished')

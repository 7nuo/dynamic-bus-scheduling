#!/usr/local/bin/python
# -*- coding: utf-8 -*-
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
from path_finder import find_path_between_two_nodes
from multiple_paths_finder import find_waypoints_between_two_nodes
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port, route_generator_edges_updater_timeout, \
    route_generator_edges_updater_max_operation_timeout
from src.geospatial_data.point import distance, Point
from src.mongodb_database.mongo_connection import MongoConnection
from multiprocessing import Process
import time


class Router(object):
    def __init__(self):
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='Router', log_type='DEBUG', log_message='connection ok')
        self.bus_stops_dictionary = {}
        self.edges_dictionary = {}
        self.points_dictionary = {}
        self.initialize_dictionaries()
        self.edges_updater_process = Process(target=self.update_edges_dictionary, args=())
        self.edges_updater_process.start()
        log(module_name='Router', log_type='DEBUG', log_message='initialize_dictionaries ok')

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

        self.edges_updater_process.join()

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
        edges_dictionary = self.connection.get_edges_dictionary()
        return edges_dictionary

    def get_edges_list(self):
        """
        Retrieve a list containing all the documents of the Edges collection.

        :return: edges_list: [{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                               'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                               'max_speed', 'road_type', 'way_id', 'traffic_density'}]
        """
        edges_list = self.connection.get_edges_list()
        return edges_list

    def get_points_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Points collection.

        :return points_dictionary: {osm_id -> {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}}
        """
        points_dictionary = self.connection.get_points_dictionary()
        return points_dictionary

    def get_route_between_two_bus_stops(self, starting_bus_stop, ending_bus_stop):
        """
        Find a route between two bus_stops.

        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :return response: {
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                              'distances_from_starting_node', 'times_from_starting_node',
                              'distances_from_previous_node', 'times_from_previous_node'}}
        """
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

    def get_route_between_two_bus_stop_names(self, starting_bus_stop_name, ending_bus_stop_name):
        """
        Find a route between two bus_stops, based on their names.

        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return response: {
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                              'distances_from_starting_node', 'times_from_starting_node',
                              'distances_from_previous_node', 'times_from_previous_node'}}
        """
        starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
        ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

        response = self.get_route_between_two_bus_stops(
            starting_bus_stop=starting_bus_stop,
            ending_bus_stop=ending_bus_stop
        )
        return response

    def get_route_between_multiple_bus_stops(self, bus_stops):
        """
        Find a route between multiple bus_stop, based on their names.

        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :return response: [{
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                              'distances_from_starting_node', 'times_from_starting_node',
                              'distances_from_previous_node', 'times_from_previous_node'}}]
        """
        response = []

        for i in range(0, len(bus_stops) - 1):
            starting_bus_stop = bus_stops[i]
            ending_bus_stop = bus_stops[i + 1]

            intermediate_route = self.get_route_between_two_bus_stops(
                starting_bus_stop=starting_bus_stop,
                ending_bus_stop=ending_bus_stop
            )
            response.append(intermediate_route)

        return response

    def get_route_between_multiple_bus_stop_names(self, bus_stop_names):
        """
        Find a route between multiple bus_stop, based on their names.

        :param bus_stop_names: [string]
        :return response: [{
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                              'distances_from_starting_node', 'times_from_starting_node',
                              'distances_from_previous_node', 'times_from_previous_node'}}]
        """
        response = []

        for i in range(0, len(bus_stop_names) - 1):
            starting_bus_stop_name = bus_stop_names[i]
            ending_bus_stop_name = bus_stop_names[i + 1]

            intermediate_route = self.get_route_between_two_bus_stop_names(
                starting_bus_stop_name=starting_bus_stop_name,
                ending_bus_stop_name=ending_bus_stop_name
            )
            response.append(intermediate_route)

        return response

    def get_waypoints_between_two_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        """
        Find the waypoints of all possible routes between two bus_stops, based on their names.

        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return response: {
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                    'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                    'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}
        """
        starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
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

    def get_waypoints_between_multiple_bus_stops(self, bus_stop_names):
        """
        Find the waypoints of all possible routes between multiple bus_stops, based on their names.

        :param bus_stop_names: [string]
        :return response: [{
                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                    'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                    'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}]
        """
        response = []

        for i in range(0, len(bus_stop_names) - 1):
            starting_bus_stop_name = bus_stop_names[i]
            starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
            ending_bus_stop_name = bus_stop_names[i + 1]
            ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

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

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
from src.mongodb_database.mongo_connection import MongoConnection
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port
from src.route_generator.route_generator_client import get_waypoints_between_multiple_bus_stops


class LookAheadHandler(object):
    def __init__(self):
        self.bus_stops_dictionary = {}
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='look_ahead_handler', log_type='DEBUG', log_message='connection ok')

    def get_bus_line_from_multiple_bus_stops(self, bus_stops):
        pass

    def initialize_connection(self):
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='look_ahead_handler', log_type='DEBUG', log_message='connection ok')

    def retrieve_bus_stops_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the BusStops collection.

        bus_stops_dictionary: {name -> {'osm_id', 'point': {'longitude', 'latitude'}}}
        """
        self.bus_stops_dictionary = self.connection.get_bus_stops_dictionary()
        log(module_name='look_ahead_handler', log_type='DEBUG', log_message='bus_stops_dictionary ok')

    def generate_waypoints_between_multiple_bus_stops(self, bus_stop_names):
        """

        :param bus_stop_names: [string]
        :return:
        """
        route_generator_response = get_waypoints_between_multiple_bus_stops(bus_stop_names=bus_stop_names)
        # [{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #   'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #                   'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #                   'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}]

        for intermediate_response in route_generator_response:
            starting_bus_stop = intermediate_response.get('starting_bus_stop')
            ending_bus_stop = intermediate_response.get('ending_bus_stop')
            waypoints = intermediate_response.get('waypoints')
            lists_of_edge_object_ids = []

            for list_of_edges in waypoints:
                list_of_edge_object_ids = []

                for edge in list_of_edges:
                    edge_object_id = edge.get('_id')
                    list_of_edge_object_ids.append(edge_object_id)

                lists_of_edge_object_ids.append(list_of_edge_object_ids)

            # waypoints: [[edge_object_id]]
            waypoints = lists_of_edge_object_ids
            self.connection.insert_bus_stop_waypoints(starting_bus_stop=starting_bus_stop,
                                                      ending_bus_stop=ending_bus_stop,
                                                      waypoints=waypoints)

        # print self.connection.get_bus_stop_waypoints_detailed_edges(starting_bus_stop_name='Centralstationen',
        #                                                             ending_bus_stop_name='Stadshuset')

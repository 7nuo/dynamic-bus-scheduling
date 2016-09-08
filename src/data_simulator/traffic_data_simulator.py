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


class TrafficDataSimulator(object):
    def __init__(self):
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='traffic_data_simulator', log_type='DEBUG', log_message='mongodb_database_connection ok')

    def clear_traffic_density(self):
        self.connection.clear_traffic_density()

    def generate_traffic_between_bus_stop_names(self, starting_bus_stop_name, ending_bus_stop_name,
                                                waypoints_index, new_traffic_density):
        """

        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :param waypoints_index:
        :param new_traffic_density:
        :return:
        """
        # {'_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #  'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #  'waypoints': [[edge_object_id]]}

        bus_stop_waypoints = self.connection.get_waypoints_between_two_bus_stop_names(
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )

        edge_object_ids = bus_stop_waypoints.get('waypoints')[waypoints_index]

        for edge_object_id in edge_object_ids:
            self.connection.update_traffic_density(edge_object_id=edge_object_id,
                                                   new_traffic_density=new_traffic_density)

    def print_traffic_density_between_two_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        self.connection.print_traffic_density_between_two_bus_stops(
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )

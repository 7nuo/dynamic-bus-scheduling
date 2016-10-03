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
from src.mongodb_database.mongodb_database_connection import MongodbDatabaseConnection
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port
import random


class TrafficDataSimulator(object):
    def __init__(self):
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='traffic_data_simulator', log_type='DEBUG',
            log_message='mongodb_database_connection: established')

    def clear_traffic_density(self):
        self.mongodb_database_connection.clear_traffic_density()

    def generate_traffic_data_for_bus_line(self, bus_line=None, line_id=None):
        """
        Generate random traffic density values for the edge_documents which are included in a bus_line_document.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param bus_line: bus_line_document
        :param line_id: int
        :return: None
        """
        edge_object_ids_included_in_bus_line_document = \
            self.mongodb_database_connection.get_edge_object_ids_included_in_bus_line(
                bus_line=bus_line,
                line_id=line_id
            )

        self.generate_traffic_data_for_edge_object_ids(
            edge_object_ids=edge_object_ids_included_in_bus_line_document
        )

    def generate_traffic_data_between_bus_stops(self, starting_bus_stop=None, ending_bus_stop=None,
                                                starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Generate random traffic density values for the edges which connect two bus_stops.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return: None
        """
        bus_stop_waypoints_document = self.mongodb_database_connection.find_bus_stop_waypoints_document(
            starting_bus_stop=starting_bus_stop,
            ending_bus_stop=ending_bus_stop,
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )
        edge_object_ids_included_in_bus_stop_waypoints_document = \
            self.mongodb_database_connection.get_edge_object_ids_included_in_bus_stop_waypoints(
                bus_stop_waypoints=bus_stop_waypoints_document
            )
        self.generate_traffic_data_for_edge_object_ids(
            edge_object_ids=edge_object_ids_included_in_bus_stop_waypoints_document
        )

    def generate_traffic_data_for_edge_object_ids(self, edge_object_ids):
        """
        Generate random traffic density values and update the corresponding edge_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param edge_object_ids: [ObjectId]
        :return: None
        """
        number_of_edge_object_ids = len(edge_object_ids)
        number_of_produced_traffic_values = random.randint(0, number_of_edge_object_ids - 1)

        for i in range(0, number_of_produced_traffic_values):
            edge_object_ids_index = random.randint(0, number_of_edge_object_ids - 1)
            edge_object_id = edge_object_ids[edge_object_ids_index]
            new_traffic_density_value = random.uniform(0, 1)
            self.mongodb_database_connection.update_traffic_density(
                edge_object_id=edge_object_id,
                new_traffic_density_value=new_traffic_density_value
            )

    def print_traffic_density_between_two_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        self.mongodb_database_connection.print_traffic_density_documents(
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )

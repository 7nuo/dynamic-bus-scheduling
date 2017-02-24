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
import random
from src.mongodb_database.mongodb_database_connection import MongodbDatabaseConnection
from src.common.logger import log
from src.common.parameters import mongodb_host, mongodb_port

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class TrafficDataSimulator(object):
    def __init__(self):
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='traffic_data_simulator', log_type='DEBUG',
            log_message='mongodb_database_connection: established')

    def clear_traffic_density(self):
        self.mongodb_database_connection.clear_traffic_density()

    def generate_traffic_data_between_two_bus_stops(self, starting_bus_stop=None, ending_bus_stop=None,
                                                    starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Generate random traffic density values for the edges which connect two bus_stops.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param starting_bus_stop: bus_stop_document
        :param ending_bus_stop: bus_stop_document
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

    def generate_traffic_data_between_multiple_bus_stops(self, bus_stops=None, bus_stop_names=None):
        """
        Generate random traffic density values for the edges which connect multiple bus_stops.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param bus_stops: [bus_stop_documents]
        :param bus_stop_names: [string]
        :return: None
        """
        if bus_stops is not None:
            number_of_bus_stops = len(bus_stops)

            for i in range(0, number_of_bus_stops - 1):
                starting_bus_stop = bus_stops[i]
                ending_bus_stop = bus_stops[i + 1]
                self.generate_traffic_data_between_two_bus_stops(
                    starting_bus_stop=starting_bus_stop,
                    ending_bus_stop=ending_bus_stop
                )

        elif bus_stop_names is not None:
            number_of_bus_stop_names = len(bus_stop_names)

            for i in range(0, number_of_bus_stop_names - 1):
                starting_bus_stop_name = bus_stop_names[i]
                ending_bus_stop_name = bus_stop_names[i + 1]
                self.generate_traffic_data_between_two_bus_stops(
                    starting_bus_stop_name=starting_bus_stop_name,
                    ending_bus_stop_name=ending_bus_stop_name
                )

        else:
            pass

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

    def generate_traffic_data_for_bus_lines(self, bus_lines=None):
        """
        Generate random traffic density values for the edge_documents which are included in a bus_line_documents.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param bus_lines: [bus_line_document]
        :return: None
        """
        if bus_lines is None:
            bus_lines = self.mongodb_database_connection.find_bus_line_documents()

        for bus_line in bus_lines:
            self.generate_traffic_data_for_bus_line(bus_line=bus_line)

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

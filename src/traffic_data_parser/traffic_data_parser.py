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
from common.variables import mongodb_host, mongodb_port, traffic_data_parser_updater_timeout, \
    traffic_data_parser_updater_max_operation_timeout
from mongodb_database.mongodb_database_connection import MongodbDatabaseConnection
from src.common.logger import log
from src.geospatial_data.point import Point, distance
from multiprocessing import Process
import time


class TrafficDataParser(object):
    def __init__(self):
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        self.edge_documents = []
        self.traffic_event_documents = []
        self.traffic_data_updater_process = Process(target=self.update_traffic_data(), args=())
        self.traffic_data_updater_process.start()
        log(module_name='traffic_data_parser', log_type='DEBUG',
            log_message='mongodb_database_connection: established')

    def traffic_data_updater_process_handler(self):
        time_difference = 0
        initial_time = time.time()

        while time_difference < traffic_data_parser_updater_max_operation_timeout:
            self.update_traffic_data()
            log(module_name='TrafficDataParser', log_type='DEBUG', log_message='traffic_data updated')
            time.sleep(traffic_data_parser_updater_timeout)
            time_difference = time.time() - initial_time

        self.traffic_data_updater_process.join()

    def update_traffic_data(self):
        """
        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        traffic_event_document: {
            '_id', 'event_id', 'event_type', 'severity_level', 'longitude', 'latitude', 'date'
        }
        :return:
        """
        self.edge_documents = self.mongodb_database_connection.find_edge_documents()
        self.traffic_event_documents = self.mongodb_database_connection.find_traffic_event_documents()

        for traffic_event_document in self.traffic_event_documents:
            traffic_event_point = Point(
                longitude=traffic_event_document.get('longitude'),
                latitude=traffic_event_document.get('latitude')
            )
            new_traffic_density_value = self.get_new_traffic_density_value(
                severity_level=traffic_event_document.get('severity_level')
            )
            minimum_distance = float('Inf')
            edge_document_with_minimum_distance = None

            for edge_document in self.edge_documents:
                starting_node = edge_document.get('starting_node')
                starting_node_point_document = starting_node.get('point')
                starting_node_point = Point(
                    longitude=starting_node_point_document.get('longitude'),
                    latitude=starting_node_point_document.get('latitude')
                )
                ending_node = edge_document.get('ending_node')
                ending_node_point_document = ending_node.get('point')
                ending_node_point = Point(
                    longitude=ending_node_point_document.get('longitude'),
                    latitude=ending_node_point_document.get('latitude')
                )
                distance_of_starting_node = distance(
                    point_one=traffic_event_point,
                    point_two=starting_node_point
                )
                distance_of_ending_node = distance(
                    point_one=traffic_event_point,
                    point_two=ending_node_point
                )
                distance_of_edge_document = distance_of_starting_node + distance_of_ending_node

                if distance_of_edge_document < minimum_distance:
                    edge_document_with_minimum_distance = edge_document
                    minimum_distance = distance_of_edge_document

            self.mongodb_database_connection.update_traffic_density(
                edge_object_id=edge_document_with_minimum_distance.get('_id'),
                new_traffic_density_value=new_traffic_density_value
            )

    @staticmethod
    def get_new_traffic_density_value(severity_level):
        """

        :param severity_level:
        :return:
        """
        if severity_level == 1:
            new_traffic_density_value = 0.2
        elif severity_level == 2:
            new_traffic_density_value = 0.4
        elif severity_level == 3:
            new_traffic_density_value = 0.6
        elif severity_level == 4:
            new_traffic_density_value = 0.8
        else:
            new_traffic_density_value = 0.0

        return new_traffic_density_value

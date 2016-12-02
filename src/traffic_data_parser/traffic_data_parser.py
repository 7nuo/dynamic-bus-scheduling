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
from src.common.variables import mongodb_host, mongodb_port
from src.mongodb_database.mongodb_database_connection import MongodbDatabaseConnection
from src.common.logger import log
from src.geospatial_data.point import Point, distance

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class TrafficDataParser(object):
    def __init__(self):
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        self.edge_documents = []
        self.traffic_event_documents = []
        self.minimum_longitude = float('inf')
        self.maximum_longitude = float('-inf')
        self.minimum_latitude = float('inf')
        self.maximum_latitude = float('-inf')
        log(module_name='traffic_data_parser', log_type='DEBUG',
            log_message='mongodb_database_connection: established')

    def check_borders_of_traffic_event_document(self, traffic_event_document):
        """
        Check if a traffic_event_document corresponds to the operation area, by comparing their borders.
        If yes, then return True. Otherwise, False.

        traffic_event_document: {
            '_id', 'event_id', 'event_type', 'event_level', 'point': {'longitude', 'latitude'}, 'datetime'
        }
        :param traffic_event_document: traffic_event_document
        :return: included_in_borders: bool
        """
        included_in_borders = True
        traffic_event_point_document = traffic_event_document.get('point')
        traffic_event_longitude = traffic_event_point_document.get('longitude')
        traffic_event_latitude = traffic_event_point_document.get('latitude')

        if (traffic_event_longitude < self.minimum_longitude or traffic_event_longitude > self.maximum_longitude or
                    traffic_event_latitude < self.minimum_latitude or traffic_event_latitude > self.maximum_latitude):
            included_in_borders = False

        return included_in_borders

    @staticmethod
    def estimate_traffic_density_value(event_level):
        """
        Estimate the traffic_density_value based on the event_level.

        :param event_level: int
        :return: traffic_density_value: float
        """
        if event_level == 1:
            traffic_density_value = 0.2
        elif event_level == 2:
            traffic_density_value = 0.4
        elif event_level == 3:
            traffic_density_value = 0.6
        elif event_level == 4:
            traffic_density_value = 0.8
        else:
            traffic_density_value = 0.0

        return traffic_density_value

    @staticmethod
    def get_edge_document_with_minimum_distance(traffic_event_document, edge_documents):
        """
        Get the edge_document which corresponds to the nearest point of a traffic_event.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        traffic_event_document: {
            '_id', 'event_id', 'event_type', 'event_level', 'point': {'longitude', 'latitude'}, 'datetime'
        }
        :param traffic_event_document: traffic_event_document
        :param edge_documents: [edge_document]
        :return:
        """
        edge_document_with_minimum_distance = None
        minimum_distance = float('Inf')

        traffic_event_point_document = traffic_event_document.get('point')
        traffic_event_longitude = traffic_event_point_document.get('longitude')
        traffic_event_latitude = traffic_event_point_document.get('latitude')

        traffic_event_point = Point(
            longitude=traffic_event_longitude,
            latitude=traffic_event_latitude
        )
        for edge_document in edge_documents:
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

        return edge_document_with_minimum_distance

    def set_borders_of_operation_area(self, edge_documents):
        """
        Set the minimum and maximum values for longitude and latitude of the operation area.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param edge_documents: [edge_document]
        :return: None
        """
        for edge_document in edge_documents:
            starting_node = edge_document.get('starting_node')
            starting_node_point_document = starting_node.get('point')
            starting_node_longitude = starting_node_point_document.get('longitude')
            starting_node_latitude = starting_node_point_document.get('latitude')

            if starting_node_longitude < self.minimum_longitude:
                self.minimum_longitude = starting_node_longitude

            if starting_node_longitude > self.maximum_longitude:
                self.maximum_longitude = starting_node_longitude

            if starting_node_latitude < self.minimum_latitude:
                self.minimum_latitude = starting_node_latitude

            if starting_node_latitude > self.maximum_latitude:
                self.maximum_latitude = starting_node_latitude

            ending_node = edge_document.get('ending_node')
            ending_node_point_document = ending_node.get('point')
            ending_node_longitude = ending_node_point_document.get('longitude')
            ending_node_latitude = ending_node_point_document.get('latitude')

            if ending_node_longitude < self.minimum_longitude:
                self.minimum_longitude = ending_node_longitude

            if ending_node_longitude > self.maximum_longitude:
                self.maximum_longitude = ending_node_longitude

            if ending_node_latitude < self.minimum_latitude:
                self.minimum_latitude = ending_node_latitude

            if ending_node_latitude > self.maximum_latitude:
                self.maximum_latitude = ending_node_latitude

    def update_traffic_data(self):
        """
        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        traffic_event_document: {
            '_id', 'event_id', 'event_type', 'event_level', 'point': {'longitude', 'latitude'}, 'datetime'
        }
        :return: None
        """
        self.edge_documents = self.mongodb_database_connection.find_edge_documents()
        self.traffic_event_documents = self.mongodb_database_connection.find_traffic_event_documents()
        self.set_borders_of_operation_area(edge_documents=self.edge_documents)

        for traffic_event_document in self.traffic_event_documents:

            if self.check_borders_of_traffic_event_document(traffic_event_document=traffic_event_document):
                edge_document_with_minimum_distance = self.get_edge_document_with_minimum_distance(
                    traffic_event_document=traffic_event_document,
                    edge_documents=self.edge_documents
                )
                traffic_density_value = self.estimate_traffic_density_value(
                    event_level=traffic_event_document.get('event_level')
                )
                self.mongodb_database_connection.update_traffic_density(
                    edge_object_id=edge_document_with_minimum_distance.get('_id'),
                    new_traffic_density_value=traffic_density_value
                )
            else:
                print 'traffic_event_document: out_of_borders -', traffic_event_document

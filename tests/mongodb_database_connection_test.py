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
import time
from src.mongodb_database.mongodb_database_connection import MongodbDatabaseConnection
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port


class MongodbDatabaseConnectionTester(object):
    def __init__(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='initialize_mongodb_database_connection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='initialize_mongodb_database_connection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_all_collections(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_all_collections: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_all_collections()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_all_collections: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def print_address_documents(self, object_ids=None, names=None, node_ids=None, counter=None):
        """
        Print multiple address_documents.

        address_document: {'_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param names: [string]
        :param node_ids: [int]
        :param counter: int
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_address_documents')
        self.mongodb_database_connection.print_address_documents(
            object_ids=object_ids,
            names=names,
            node_ids=node_ids,
            counter=counter
        )

    def print_bus_line_documents(self, object_ids=None, line_ids=None, counter=None):
        """
        Print multiple bus_line_documents.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param object_ids: [ObjectId]
        :param line_ids: [int]
        :param counter: int
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_bus_line_documents')
        self.mongodb_database_connection.print_bus_line_documents(
            object_ids=object_ids,
            line_ids=line_ids,
            counter=counter
        )

    def print_bus_stop_documents(self, object_ids=None, osm_ids=None, names=None, counter=None):
        """
        Print multiple bus_stop_documents.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param names: [string]
        :param counter: int
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_bus_stop_documents')
        self.mongodb_database_connection.print_bus_stop_documents(
            object_ids=object_ids,
            osm_ids=osm_ids,
            names=names,
            counter=counter
        )

    def print_edge_documents(self, object_ids=None, starting_node_osm_id=None, ending_node_osm_id=None, counter=None):
        """
        Print multiple edge_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param object_ids: [ObjectId]
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :param counter: int
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_edge_documents')
        self.mongodb_database_connection.print_edge_documents(
            object_ids=object_ids,
            starting_node_osm_id=starting_node_osm_id,
            ending_node_osm_id=ending_node_osm_id,
            counter=counter
        )

    def print_node_documents(self, object_ids=None, osm_ids=None, counter=None):
        """
        Print multiple node_documents.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param counter: int
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_node_documents')
        self.mongodb_database_connection.print_node_documents(
            object_ids=object_ids,
            osm_ids=osm_ids,
            counter=counter
        )

    def print_point_documents(self, object_ids=None, osm_ids=None, counter=None):
        """
        Print multiple point_documents.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param counter: int
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_point_documents')
        self.mongodb_database_connection.print_point_documents(
            object_ids=object_ids,
            osm_ids=osm_ids,
            counter=counter
        )

    def print_travel_request_documents(self, object_ids=None, client_ids=None, line_ids=None,
                                       min_departure_datetime=None, max_departure_datetime=None,
                                       counter=None):
        """
        Print multiple travel_request_documents.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime: datetime
        :param counter: int
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_travel_request_documents')
        self.mongodb_database_connection.print_travel_request_documents(
            object_ids=object_ids,
            client_ids=client_ids,
            line_ids=line_ids,
            min_departure_datetime=min_departure_datetime,
            max_departure_datetime=max_departure_datetime,
            counter=counter
        )

    def print_way_documents(self, object_ids=None, osm_ids=None, counter=None):
        """
        Print multiple way_documents.

        way_document: {'_id', 'osm_id', 'tags', 'references'}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param counter: int
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_way_documents')
        self.mongodb_database_connection.print_way_documents(
            object_ids=object_ids,
            osm_ids=osm_ids,
            counter=counter
        )

    def print_bus_stop_waypoints_documents(self, object_ids=None, bus_stops=None, bus_stop_names=None, line_id=None):
        """
        Print multiple bus_stop_waypoints_documents.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param object_ids: [ObjectId]
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :param line_id: int
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_bus_stop_waypoints_documents')
        self.mongodb_database_connection.print_bus_stop_waypoints_documents(
            object_ids=object_ids,
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names,
            line_id=line_id
        )

    def print_detailed_bus_stop_waypoints_documents(self, object_ids=None, bus_stops=None,
                                                    bus_stop_names=None, line_id=None):
        """
        Print multiple detailed_bus_stop_waypoints_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        detailed_bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_document]]
        }
        :param object_ids: [ObjectId]
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :param line_id: int
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_detailed_bus_stop_waypoints_documents')
        self.mongodb_database_connection.print_detailed_bus_stop_waypoints_documents(
            object_ids=object_ids,
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names,
            line_id=line_id
        )

    def print_traffic_density_documents(self, bus_stops=None, bus_stop_names=None):
        """
        Print multiple traffic_density_documents.

        traffic_density_document: {
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'traffic_density_values': [[{'edge_object_id', 'traffic_density'}]]
        }
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :return: None
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_traffic_density_documents')
        self.mongodb_database_connection.print_traffic_density_documents(
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names
        )

if __name__ == '__main__':
    tester = MongodbDatabaseConnectionTester()
    # travel_requests_simulator_tester.clear_all_collections()
    # travel_requests_simulator_tester.print_address_documents()
    # travel_requests_simulator_tester.print_bus_line_documents()
    # travel_requests_simulator_tester.print_bus_stop_documents()
    # travel_requests_simulator_tester.print_edge_documents()
    # travel_requests_simulator_tester.print_node_documents()
    # travel_requests_simulator_tester.print_point_documents()
    # travel_requests_simulator_tester.print_travel_request_documents()
    # travel_requests_simulator_tester.print_way_documents()
    # travel_requests_simulator_tester.print_bus_stop_waypoints_documents()
    # travel_requests_simulator_tester.print_detailed_bus_stop_waypoints_documents()
    # travel_requests_simulator_tester.print_traffic_density_documents()

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
from src.mongodb_database.mongo_connection import MongoConnection
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port
import os


class MongodbDatabaseTester(object):
    def __init__(self):
        log(module_name='mongodb_database_test', log_type='INFO',
            log_message='initialize_database_connection: starting')
        self.start_time = time.time()
        self.mongo = MongoConnection(host=mongodb_host, port=mongodb_port)
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_test', log_type='INFO',
            log_message='initialize_database_connection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_all_collections(self):
        log(module_name='mongodb_database_test', log_type='INFO',
            log_message='clear_all_collections: starting')
        self.start_time = time.time()
        self.mongo.clear_all_collections()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_test', log_type='INFO',
            log_message='clear_all_collections: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def print_bus_line(self, line_id):
        log(module_name='mongodb_database_test', log_type='INFO', log_message='print_bus_line_document')
        self.mongo.print_bus_line_document(line_id=line_id)

    def print_bus_line_waypoints(self, line_id):
        log(module_name='mongodb_database_test', log_type='INFO', log_message='print_bus_stop_waypoints_documents')
        self.mongo.print_bus_stop_waypoints_documents(line_id=line_id)

    def print_detailed_bus_line_waypoints(self, line_id):
        log(module_name='mongodb_database_test', log_type='INFO', log_message='print_detailed_bus_stop_waypoints_documents')
        self.mongo.print_detailed_bus_stop_waypoints_documents(line_id=line_id)

    def print_bus_stops(self, counter):
        log(module_name='mongodb_database_test', log_type='INFO', log_message='print_bus_stop_documents')
        self.mongo.print_bus_stop_documents(counter=counter)

    def print_edges(self, counter):
        log(module_name='mongodb_database_test', log_type='INFO', log_message='print_edge_documents')
        self.mongo.print_edge_documents(counter=counter)

    def print_nodes(self, counter):
        log(module_name='mongodb_database_test', log_type='INFO', log_message='print_node_documents')
        self.mongo.print_node_documents(counter=counter)

    def print_travel_request_documents(self, counter):
        log(module_name='mongodb_database_test', log_type='INFO', log_message='print_travel_request_documents')
        self.mongo.print_travel_request_documents(counter=counter)


if __name__ == '__main__':
    tester = MongodbDatabaseTester()
    tester.mongo.test()
    # tester.clear_all_collections()
    # tester.print_node_documents(counter=200)
    # tester.print_bus_stop_documents(counter=200)
    # tester.print_edge_documents(counter=200)
    # tester.print_bus_line_document(line_id=1)
    # tester.print_bus_stop_waypoints_documents(line_id=1)
    # tester.print_detailed_bus_stop_waypoints_documents(line_id=1)
    # tester.print_travel_request_documents(counter=10000)

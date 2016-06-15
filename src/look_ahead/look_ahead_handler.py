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
        route_generator_response = get_waypoints_between_multiple_bus_stops(bus_stop_names=bus_stop_names)
        self.connection.insert_bus_stop_waypoints_documents(bus_stop_waypoints_documents=route_generator_response)

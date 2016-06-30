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
import random
from datetime import timedelta


class TravelRequestsSimulator(object):
    def __init__(self):
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='travel_requests_simulator', log_type='DEBUG', log_message='mongodb_database connection ok')

    def clear_travel_requests(self):
        self.connection.clear_travel_requests()
        # log(module_name='travel_requests_simulator', log_type='DEBUG', log_message='clear_travel_requests ok')

    def delete_travel_requests_based_on_bus_line_id(self, bus_line_id):
        self.connection.delete_travel_requests_based_on_bus_line_id(bus_line_id=bus_line_id)
        # log(module_name='travel_requests_simulator', log_type='DEBUG',
        #     log_message='delete_travel_requests_based_on_bus_line_id ok')

    def delete_travel_requests_based_on_departure_datetime(self, min_departure_datetime, max_departure_datetime):
        self.connection.delete_travel_requests_based_on_departure_datetime(
            min_departure_datetime=min_departure_datetime,
            max_departure_datetime=max_departure_datetime
        )
        # log(module_name='travel_requests_simulator', log_type='DEBUG',
        #     log_message='delete_travel_requests_based_on_departure_datetime ok')

    def generate_travel_requests(self, bus_line_id, initial_datetime, number_of_requests):
        # bus_line: {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        bus_line = self.connection.find_bus_line(line_id=bus_line_id)
        bus_stops = bus_line.get('bus_stops')
        number_of_bus_stops = len(bus_stops)

        weighted_datetimes = [
            (initial_datetime + timedelta(hours=0), 1),
            (initial_datetime + timedelta(hours=1), 1),
            (initial_datetime + timedelta(hours=2), 1),
            (initial_datetime + timedelta(hours=3), 1),
            (initial_datetime + timedelta(hours=4), 1),
            (initial_datetime + timedelta(hours=5), 1),
            (initial_datetime + timedelta(hours=6), 1),
            (initial_datetime + timedelta(hours=7), 1),
            (initial_datetime + timedelta(hours=8), 1),
            (initial_datetime + timedelta(hours=9), 1),
            (initial_datetime + timedelta(hours=10), 1),
            (initial_datetime + timedelta(hours=11), 1),
            (initial_datetime + timedelta(hours=12), 1),
            (initial_datetime + timedelta(hours=13), 1),
            (initial_datetime + timedelta(hours=14), 1),
            (initial_datetime + timedelta(hours=15), 1),
            (initial_datetime + timedelta(hours=16), 1),
            (initial_datetime + timedelta(hours=17), 1),
            (initial_datetime + timedelta(hours=18), 1),
            (initial_datetime + timedelta(hours=19), 1),
            (initial_datetime + timedelta(hours=20), 1),
            (initial_datetime + timedelta(hours=21), 1),
            (initial_datetime + timedelta(hours=22), 1),
            (initial_datetime + timedelta(hours=23), 1)
        ]
        datetime_population = [val for val, cnt in weighted_datetimes for i in range(cnt)]
        travel_request_documents = []

        for i in range(0, number_of_requests - 1):
            client_id = i
            starting_bus_stop_index = random.randint(0, number_of_bus_stops - 2)
            starting_bus_stop = bus_stops[starting_bus_stop_index]
            ending_bus_stop_index = random.randint(starting_bus_stop_index, number_of_bus_stops - 1)
            ending_bus_stop = bus_stops[ending_bus_stop_index]
            additional_departure_time_interval = random.randint(0, 59)
            departure_datetime = random.choice(datetime_population) + timedelta(
                minutes=additional_departure_time_interval)

            travel_request_document = {'client_id': client_id, 'bus_line_id': bus_line_id,
                                       'starting_bus_stop': starting_bus_stop, 'ending_bus_stop': ending_bus_stop,
                                       'departure_datetime': departure_datetime, 'arrival_datetime': None}

            travel_request_documents.append(travel_request_document)

        self.connection.insert_travel_request_documents(travel_request_documents=travel_request_documents)


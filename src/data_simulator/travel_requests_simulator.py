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
from datetime import timedelta


class TravelRequestsSimulator(object):
    def __init__(self):
        self.connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='travel_requests_simulator', log_type='DEBUG',
            log_message='mongodb_database_connection: established')

    def clear_travel_requests(self):
        """
        Clear all the documents of the TravelRequests collection.

        :return: None
        """
        self.connection.clear_travel_requests()
        log(module_name='travel_requests_simulator', log_type='DEBUG',
            log_message='clear_travel_requests ok')

    def delete_travel_requests_based_on_line_id(self, line_id):
        """
        Delete the travel_request documents with the selected line_id.

        travel_request_document: {'_id', 'client_id', 'line_id', 'starting_bus_stop_id',
                                  'ending_bus_stop_id', 'departure_datetime', 'arrival_datetime'}

        :param line_id: int
        :return: None
        """
        self.connection.delete_travel_request_documents(line_id=line_id)
        log(module_name='travel_requests_simulator', log_type='DEBUG',
            log_message='delete_travel_request_documents ok')

    def delete_travel_requests_based_on_departure_datetime(self, min_departure_datetime, max_departure_datetime):
        """
        Delete the travel_request documents with departure_datetime between
        min_departure_datetime and max_departure_datetime.

        travel_request_document: {'_id', 'client_id', 'line_id', 'starting_bus_stop_id',
                                  'ending_bus_stop_id', 'departure_datetime', 'arrival_datetime'}

        :param min_departure_datetime: datetime
        :param max_departure_datetime: datetime
        :return: None
        """
        self.connection.delete_travel_request_documents(
            min_departure_datetime=min_departure_datetime,
            max_departure_datetime=max_departure_datetime
        )
        log(module_name='travel_requests_simulator', log_type='DEBUG',
            log_message='delete_travel_request_documents ok')

    def generate_travel_requests(self, line_id, initial_datetime, number_of_requests):
        """
        Generate a specific number of travel_request documents, for the selected bus_line,
        for a 24hour period starting from a selected datetime, and store them at the
        corresponding collection of the System Database.

        :param line_id: int
        :param initial_datetime: datetime
        :param number_of_requests: int
        :return: None
        """
        # 1: The inputs: line_id, initial_datetime, and number_of_requests are provided to
        #    the Travel Requests Simulator, so as a specific number of travel_request documents
        #    to be generated, for the selected bus_line, for a 24hour period starting from
        #    the selected datetime.

        # 2: The Travel Requests Simulator retrieves from the System Database the bus_line which
        #    corresponds to the selected line_id.
        #
        # bus_line: {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        #
        bus_line = self.connection.find_bus_line_document(line_id=line_id)
        bus_stops = bus_line.get('bus_stops')
        number_of_bus_stops = len(bus_stops)

        # 3: The Travel Requests Simulator generates the travel_request documents, taking into consideration
        #    the variation of transportation demand during the hours of the day.
        #
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

        for i in range(0, number_of_requests):
            client_id = i
            starting_bus_stop_index = random.randint(0, number_of_bus_stops - 2)
            starting_bus_stop = bus_stops[starting_bus_stop_index]
            ending_bus_stop_index = random.randint(starting_bus_stop_index + 1, number_of_bus_stops - 1)
            ending_bus_stop = bus_stops[ending_bus_stop_index]
            additional_departure_time_interval = random.randint(0, 59)
            departure_datetime = (random.choice(datetime_population) +
                                  timedelta(minutes=additional_departure_time_interval))

            travel_request_document = {
                'client_id': client_id,
                'line_id': line_id,
                'starting_bus_stop': starting_bus_stop,
                'ending_bus_stop': ending_bus_stop,
                'departure_datetime': departure_datetime,
                'arrival_datetime': None
            }
            travel_request_documents.append(travel_request_document)

        # 4: The generated travel_request documents are stored at the
        #    TravelRequests collection of the System Database.
        #
        self.connection.insert_travel_request_documents(travel_request_documents=travel_request_documents)

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
import os

from common.variables import testing_osm_filename, requests_min_departure_datetime_testing_value, \
    testing_bus_stop_names, requests_max_departure_datetime_testing_value
from src.common.logger import log
from tests.look_ahead_test import LookAheadHandlerTester
from tests.mongodb_database_connection_test import MongodbDatabaseConnectionTester
from tests.osm_parser_test import OsmParserTester
from tests.traffic_data_simulator_test import TrafficDataSimulatorTester
from tests.travel_requests_simulator_test import TravelRequestsSimulatorTester


class ApplicationTester(object):
    def __init__(self):
        log(module_name='application_test', log_type='INFO',
            log_message='initialize_application_tester: starting')
        self.start_time = time.time()

        self.mongodb_database_connection_tester = self.initialize_mongodb_database_connection_tester()
        self.osm_parser_tester = self.initialize_osm_parser_tester()
        self.travel_requests_simulator_tester = self.initialize_travel_requests_simulator_tester()
        self.traffic_data_simulator_tester = self.initialize_traffic_data_simulator_tester()
        self.look_ahead_handler_tester = self.initialize_look_ahead_handler_tester()

        self.elapsed_time = time.time() - self.start_time
        log(module_name='application_test', log_type='INFO',
            log_message='initialize_application_tester: finished - elapsed time = '
                        + str(self.elapsed_time) + ' sec')

    @staticmethod
    def initialize_look_ahead_handler_tester():
        look_ahead_handler_tester = LookAheadHandlerTester()
        return look_ahead_handler_tester

    @staticmethod
    def initialize_mongodb_database_connection_tester():
        mongodb_database_connection_tester = MongodbDatabaseConnectionTester()
        return mongodb_database_connection_tester

    @staticmethod
    def initialize_osm_parser_tester():
        osm_parser_tester = OsmParserTester(
            osm_filename=os.path.join(os.path.dirname(__file__), testing_osm_filename)
        )
        return osm_parser_tester

    @staticmethod
    def initialize_traffic_data_simulator_tester():
        traffic_data_simulator_tester = TrafficDataSimulatorTester()
        return traffic_data_simulator_tester

    @staticmethod
    def initialize_travel_requests_simulator_tester():
        travel_requests_simulator_tester = TravelRequestsSimulatorTester()
        return travel_requests_simulator_tester


if __name__ == '__main__':
    application_tester = ApplicationTester()

    # application_tester.mongodb_database_connection_tester.clear_all_collections()
    #
    # application_tester.osm_parser_tester.test_parse_osm_file()
    # application_tester.osm_parser_tester.test_populate_all_collections()
    #
    # application_tester.look_ahead_handler_tester.test_generate_bus_line(
    #     line_id=1,
    #     bus_stop_names=testing_bus_stop_names
    # )
    #
    # application_tester.mongodb_database_connection_tester.print_bus_line_documents()
    #
    # application_tester.travel_requests_simulator_tester.test_generate_travel_request_documents(
    #     line_id=1,
    #     initial_datetime=requests_min_departure_datetime_testing_value,
    #     number_of_travel_request_documents=10000
    # )

    # application_tester.mongodb_database_connection_tester.print_travel_request_documents(
    #     line_ids=[1],
    #     min_departure_datetime=requests_min_departure_datetime_testing_value,
    #     max_departure_datetime=requests_max_departure_datetime_testing_value,
    #     counter=10
    # )

    # application_tester.look_ahead_handler_tester.test_generate_timetables_for_bus_line(
    #     line_id=1
    # )


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

from common.variables import testing_osm_filename
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
    def initialize_mongodb_database_connection_tester():
        # log(module_name='application_test', log_type='INFO',
        #     log_message='initialize_mongodb_database_connection_tester: starting')
        # start_time = time.time()
        mongodb_database_connection_tester = MongodbDatabaseConnectionTester()
        # elapsed_time = time.time() - start_time
        # log(module_name='application_test', log_type='INFO',
        #     log_message='initialize_mongodb_database_connection_tester: finished - elapsed time = '
        #                 + str(elapsed_time) + ' sec')
        return mongodb_database_connection_tester

    @staticmethod
    def initialize_osm_parser_tester():
        # log(module_name='application_test', log_type='INFO',
        #     log_message='initialize_osm_parser_tester: starting')
        # start_time = time.time()
        osm_parser_tester = OsmParserTester(
            osm_filename=os.path.join(os.path.dirname(__file__), testing_osm_filename)
        )
        # elapsed_time = time.time() - start_time
        # log(module_name='application_test', log_type='INFO',
        #     log_message='initialize_osm_parser_tester: finished - elapsed time = '
        #                 + str(elapsed_time) + ' sec')
        return osm_parser_tester

    @staticmethod
    def initialize_look_ahead_handler_tester():
        # log(module_name='application_test', log_type='INFO',
        #     log_message='initialize_look_ahead_handler_tester: starting')
        # start_time = time.time()
        look_ahead_handler_tester = LookAheadHandlerTester()
        # elapsed_time = time.time() - start_time
        # log(module_name='application_test', log_type='INFO',
        #     log_message='initialize_look_ahead_handler_tester: finished - elapsed time = '
        #                 + str(elapsed_time) + ' sec')
        return look_ahead_handler_tester

    @staticmethod
    def initialize_travel_requests_simulator_tester():
        # log(module_name='application_test', log_type='INFO',
        #     log_message='initialize_travel_requests_simulator_tester: starting')
        # start_time = time.time()
        travel_requests_simulator_tester = TravelRequestsSimulatorTester()
        # elapsed_time = time.time() - start_time
        # log(module_name='application_test', log_type='INFO',
        #     log_message='initialize_travel_requests_simulator_tester: finished - elapsed time = '
        #                 + str(elapsed_time) + ' sec')
        return travel_requests_simulator_tester

    @staticmethod
    def initialize_traffic_data_simulator_tester():
        # log(module_name='application_test', log_type='INFO',
        #     log_message='initialize_traffic_data_simulator_tester: starting')
        # start_time = time.time()
        traffic_data_simulator_tester = TrafficDataSimulatorTester()
        # elapsed_time = time.time() - start_time
        # log(module_name='application_test', log_type='INFO',
        #     log_message='initialize_traffic_data_simulator_tester: finished - elapsed time = '
        #                 + str(elapsed_time) + ' sec')
        return traffic_data_simulator_tester

    # def osm_parser_parse_osm_file(self):
    #     log(module_name='application_test', log_type='INFO',
    #         log_message='osm_parser_tester: parse_osm_file: starting')
    #     start_time = time.time()
    #     self.osm_parser_tester.parse_osm_file()
    #     elapsed_time = time.time() - start_time
    #     log(module_name='application_test', log_type='INFO',
    #         log_message='osm_parser_tester: parse_osm_file: finished - elapsed time = '
    #                     + str(elapsed_time) + ' sec')

    # def osm_parser_populate_all_connections(self):
    #     log(module_name='application_test', log_type='INFO',
    #         log_message='osm_parser_tester: populate_all_connections: starting')
    #     start_time = time.time()
    #     self.osm_parser_tester.populate_all_collections()
    #     elapsed_time = time.time() - start_time
    #     log(module_name='application_test', log_type='INFO',
    #         log_message='osm_parser_tester: populate_all_connections: finished - elapsed time = '
    #                     + str(elapsed_time) + ' sec')

    # def foo(self):
    #     log(module_name='application_test', log_type='INFO', log_message=': starting')
    #     start_time = time.time()
    #
    #     elapsed_time = time.time() - start_time
    #     log(module_name='application_test', log_type='INFO',
    #         log_message=': finished - elapsed time = ' + str(elapsed_time) + ' sec')


if __name__ == '__main__':
    application_tester = ApplicationTester()
    # application_tester.mongodb_database_connection_tester.clear_all_collections()
    # application_tester.osm_parser_parse_osm_file()
    # application_tester.osm_parser_populate_all_connections()

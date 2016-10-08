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
import time
import os

from common.variables import testing_osm_filename, testing_bus_stop_names, \
    travel_requests_min_departure_datetime_testing_value, travel_requests_max_departure_datetime_testing_value, \
    travel_requests_generator_min_number_of_documents, travel_requests_generator_max_number_of_documents
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

    def start_traffic_data_simulator_tester(self, bus_line=None, line_id=None):
        self.traffic_data_simulator_tester.test_generate_traffic_data_for_bus_line(
            bus_line=bus_line,
            line_id=line_id
        )


if __name__ == '__main__':
    application_tester = ApplicationTester()
    time.sleep(0.01)
    # Positive int or None
    printing_limit = 10

    while True:
        selection = raw_input(
            '\n0.  exit'
            '\n1.  (mongodb_database) clear_all_collections'
            '\n2.  (osm_parser) test_parse_osm_file'
            '\n3.  (osm_parser) test_populate_all_collections'
            '\n4.  (mongodb_database) print_collections'
            '\n4.  (look_ahead_handler) test_generate_bus_line'
            '\n5.  (mongodb_database) print_bus_line_documents'
            '\n6.  (travel_requests_simulator) test_generate_travel_request_documents'
            '\n7.  (mongodb_database) print_travel_request_documents'
            '\n8.  (look_ahead_handler) test_generate_timetables_for_bus_line'
            '\n9.  (look_ahead_handler) test_update_timetables_of_bus_line'
            '\n10. (look_ahead_handler) start_timetables_generator_process'
            '\n11. (look_ahead_handler) terminate_timetables_generator_process'
            '\n12. (look_ahead_handler) start_timetables_updater_process'
            '\n13. (look_ahead_handler) terminate_timetables_updater_process'
            '\n14. (travel_requests_simulator) start_travel_requests_generator_process'
            '\n15. (travel_requests_simulator) terminate_travel_requests_generator_process'
            '\n16. (traffic_data_simulator) start_traffic_data_generator_process'
            '\n17. (traffic_data_simulator) terminate_traffic_data_generator_process'
            '\nSelection: '
        )

        if selection == '0':
            break

        elif selection == '1':
            application_tester.mongodb_database_connection_tester.clear_all_collections()

        elif selection == '2':
            application_tester.osm_parser_tester.test_parse_osm_file()

        elif selection == '3':
            application_tester.osm_parser_tester.test_populate_all_collections()

        elif selection == '4':
            inner_selection = raw_input(
                '\n0.  back'
                '\n1.  print_address_documents'
                '\n2.  print_bus_stop_documents'
                '\n3.  print_edge_documents'
                '\n4.  print_node_documents'
                '\n5.  print_point_documents'
                '\n6.  print_way_documents'
                '\nSelection: '
            )
            if inner_selection == '0':
                pass

            elif inner_selection == '1':
                application_tester.mongodb_database_connection_tester.print_address_documents(counter=printing_limit)

            elif inner_selection == '2':
                application_tester.mongodb_database_connection_tester.print_bus_stop_documents(counter=printing_limit)

            elif inner_selection == '3':
                application_tester.mongodb_database_connection_tester.print_edge_documents(counter=printing_limit)

            elif inner_selection == '4':
                application_tester.mongodb_database_connection_tester.print_node_documents(counter=printing_limit)

            elif inner_selection == '5':
                application_tester.mongodb_database_connection_tester.print_point_documents(counter=printing_limit)

            elif inner_selection == '6':
                application_tester.mongodb_database_connection_tester.print_way_documents(counter=printing_limit)

            else:
                print 'Invalid input.'

        elif selection == '4':
            application_tester.look_ahead_handler_tester.test_generate_bus_line(
                line_id=1,
                bus_stop_names=testing_bus_stop_names
            )

        elif selection == '5':
            application_tester.mongodb_database_connection_tester.print_bus_line_documents()

        elif selection == '6':
            application_tester.travel_requests_simulator_tester.test_generate_travel_request_documents(
                line_id=1,
                initial_datetime=travel_requests_min_departure_datetime_testing_value,
                number_of_travel_request_documents=10000
            )

        elif selection == '7':
            application_tester.mongodb_database_connection_tester.print_travel_request_documents(
                line_ids=[1],
                min_departure_datetime=travel_requests_min_departure_datetime_testing_value,
                max_departure_datetime=travel_requests_max_departure_datetime_testing_value,
                counter=10
            )

        elif selection == '8':
            application_tester.look_ahead_handler_tester.test_generate_timetables_for_bus_line(line_id=1)

        elif selection == '9':
            application_tester.look_ahead_handler_tester.test_update_timetables_of_bus_line(line_id=1)

        elif selection == '10':
            application_tester.look_ahead_handler_tester.start_timetables_generator_process()

        elif selection == '11':
            application_tester.look_ahead_handler_tester.terminate_timetables_generator_process()

        elif selection == '12':
            application_tester.look_ahead_handler_tester.start_timetables_updater_process()

        elif selection == '13':
            application_tester.look_ahead_handler_tester.terminate_timetables_updater_process()

        elif selection == '14':
            application_tester.travel_requests_simulator_tester.start_travel_requests_generator_process(
                initial_datetime=travel_requests_min_departure_datetime_testing_value,
                min_number_of_travel_request_documents=travel_requests_generator_min_number_of_documents,
                max_number_of_travel_request_documents=travel_requests_generator_max_number_of_documents
            )

        elif selection == '15':
            application_tester.travel_requests_simulator_tester.terminate_travel_requests_generator_process()

        elif selection == '16':
            application_tester.traffic_data_simulator_tester.start_traffic_data_generator_process()

        elif selection == '17':
            application_tester.traffic_data_simulator_tester.terminate_traffic_data_generator_process()

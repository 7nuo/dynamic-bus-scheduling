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
from multiprocessing import Process
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.common.variables import testing_osm_filename, testing_bus_stop_names, \
    travel_requests_min_departure_datetime_testing_value, travel_requests_max_departure_datetime_testing_value, \
    travel_requests_generator_min_number_of_documents, travel_requests_generator_max_number_of_documents
from src.common.logger import log
from tests.look_ahead_test import LookAheadHandlerTester
from tests.mongodb_database_connection_test import MongodbDatabaseConnectionTester
from tests.osm_parser_test import OsmParserTester
from tests.traffic_data_simulator_test import TrafficDataSimulatorTester
from tests.travel_requests_simulator_test import TravelRequestsSimulatorTester
from tests.route_generator_test import test_get_route_between_two_bus_stops, test_get_route_between_multiple_bus_stops,\
    test_get_waypoints_between_two_bus_stops, test_get_waypoints_between_multiple_bus_stops


__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


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
    printing_limit = 10  # Positive int or None
    timetables_generator_process = None
    timetables_updater_process = None
    travel_requests_generator_process = None
    traffic_data_generator_process = None

    while True:
        time.sleep(0.01)
        selection = raw_input(
            '\n0.  exit'
            '\n1.  (mongodb_database) ---------- clear_collections'
            '\n2.  (osm_parser) ---------------- test_parse_osm_file'
            '\n3.  (osm_parser) ---------------- test_populate_all_collections'
            '\n4.  (mongodb_database) ---------- print_collections'
            '\n5.  (route_generator) ----------- test_get_route_between_two_bus_stops'
            '\n6.  (route_generator) ----------- test_get_route_between_multiple_bus_stops'
            '\n7.  (route_generator) ----------- test_get_waypoints_between_two_bus_stops'
            '\n8.  (route_generator) ----------- test_get_waypoints_between_multiple_bus_stops'
            '\n9.  (look_ahead_handler) -------- test_generate_bus_line'
            '\n10. (mongodb_database) ---------- print_bus_line_documents'
            '\n11. (mongodb_database) ---------- print_detailed_bus_stop_waypoints_documents'
            '\n12. (travel_requests_simulator) - test_generate_travel_request_documents'
            '\n13. (mongodb_database) ---------- print_travel_request_documents'
            '\n14. (look_ahead_handler) -------- test_generate_timetables_for_bus_line'
            '\n15. (mongodb_database) ---------- print_timetable_documents'
            '\n16. (traffic_data_simulator) ---- test_generate_traffic_data_between_multiple_stops'
            '\n17. (mongodb_database) ---------- print_traffic_density_documents'
            '\n18. (look_ahead_handler) -------- test_update_timetables_of_bus_line'
            '\n19. (look_ahead_handler) -------- start_timetables_generator_process'
            '\n20. (look_ahead_handler) -------- terminate_timetables_generator_process'
            '\n21. (look_ahead_handler) -------- start_timetables_updater_process'
            '\n22. (look_ahead_handler) -------- terminate_timetables_updater_process'
            '\n23. (travel_requests_simulator) - start_travel_requests_generator_process'
            '\n24. (travel_requests_simulator) - terminate_travel_requests_generator_process'
            '\n25. (traffic_data_simulator) ---- start_traffic_data_generator_process'
            '\n26. (traffic_data_simulator) ---- terminate_traffic_data_generator_process'
            '\nSelection: '
        )
        # 0. exit
        if selection == '0':
            break

        # 1. (mongodb_database) - clear_collections
        elif selection == '1':
            while True:
                inner_selection = raw_input(
                    '\n0.  back'
                    '\n1.  clear_all_collections'
                    '\n2.  clear_address_documents_collection'
                    '\n3.  clear_bus_line_documents_collection'
                    '\n4.  clear_bus_stop_documents_collection'
                    '\n5.  clear_bus_stop_waypoints_documents_collection'
                    '\n6.  clear_edge_documents_collection'
                    '\n7.  clear_node_documents_collection'
                    '\n8.  clear_point_documents_collection'
                    '\n9.  clear_timetable_documents_collection'
                    '\n10. clear_traffic_event_documents_collection'
                    '\n11. clear_travel_request_documents_collection'
                    '\n12. clear_way_documents_collection'
                    '\nSelection: '
                )

                # 0. back
                if inner_selection == '0':
                    break

                # 1. clear_all_collections
                elif inner_selection == '1':
                    application_tester.mongodb_database_connection_tester.clear_all_collections()

                # 2. clear_address_documents_collection
                elif inner_selection == '2':
                    application_tester.mongodb_database_connection_tester.clear_address_documents_collection()

                # 3. clear_bus_line_documents_collection
                elif inner_selection == '3':
                    application_tester.mongodb_database_connection_tester.clear_bus_line_documents_collection()

                # 4. clear_bus_stop_documents_collection
                elif inner_selection == '4':
                    application_tester.mongodb_database_connection_tester.clear_bus_stop_documents_collection()

                # 5. clear_bus_stop_waypoints_documents_collection
                elif inner_selection == '5':
                    application_tester.mongodb_database_connection_tester.\
                        clear_bus_stop_waypoints_documents_collection()

                # 6. clear_edge_documents_collection
                elif inner_selection == '6':
                    application_tester.mongodb_database_connection_tester.clear_edge_documents_collection()

                # 7. clear_node_documents_collection
                elif inner_selection == '7':
                    application_tester.mongodb_database_connection_tester.clear_node_documents_collection()

                # 8. clear_point_documents_collection
                elif inner_selection == '8':
                    application_tester.mongodb_database_connection_tester.clear_point_documents_collection()

                # 9. clear_timetable_documents_collection
                elif inner_selection == '9':
                    application_tester.mongodb_database_connection_tester.clear_timetable_documents_collection()

                # 10. clear_traffic_event_documents_collection
                elif inner_selection == '10':
                    application_tester.mongodb_database_connection_tester.clear_traffic_event_documents_collection()

                # 11. clear_travel_request_documents_collection
                elif inner_selection == '11':
                    application_tester.mongodb_database_connection_tester.clear_travel_request_documents_collection()

                # 12. clear_way_documents_collection
                elif inner_selection == '12':
                    application_tester.mongodb_database_connection_tester.clear_way_documents_collection()

                else:
                    pass

        # 2. (osm_parser) - test_parse_osm_file
        elif selection == '2':
            application_tester.osm_parser_tester.test_parse_osm_file()

        # 3. (osm_parser) - test_populate_all_collections
        elif selection == '3':
            application_tester.osm_parser_tester.test_populate_all_collections()

        # 4. (mongodb_database) - print_collections
        elif selection == '4':
            while True:
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
                # 0. back
                if inner_selection == '0':
                    break

                # 1. print_address_documents
                elif inner_selection == '1':
                    application_tester.mongodb_database_connection_tester.print_address_documents(
                        counter=printing_limit
                    )

                # 2. print_bus_stop_documents
                elif inner_selection == '2':
                    application_tester.mongodb_database_connection_tester.print_bus_stop_documents(
                        counter=printing_limit
                    )

                # 3. print_edge_documents
                elif inner_selection == '3':
                    application_tester.mongodb_database_connection_tester.print_edge_documents(
                        counter=printing_limit
                    )

                # 4. print_node_documents
                elif inner_selection == '4':
                    application_tester.mongodb_database_connection_tester.print_node_documents(
                        counter=printing_limit
                    )

                # 5. print_point_documents
                elif inner_selection == '5':
                    application_tester.mongodb_database_connection_tester.print_point_documents(
                        counter=printing_limit
                    )

                # 6. print_way_documents
                elif inner_selection == '6':
                    application_tester.mongodb_database_connection_tester.print_way_documents(
                        counter=printing_limit
                    )

                else:
                    pass

        # 5. (route_generator) - test_get_route_between_two_bus_stops
        elif selection == '5':
            test_get_route_between_two_bus_stops(
                starting_bus_stop_name=testing_bus_stop_names[0],
                ending_bus_stop_name=testing_bus_stop_names[1]
            )

        # 6. (route_generator) - test_get_route_between_multiple_bus_stops
        elif selection == '6':
            test_get_route_between_multiple_bus_stops(
                bus_stop_names=testing_bus_stop_names
            )

        # 7. (route_generator) - test_get_waypoints_between_two_bus_stops
        elif selection == '7':
            test_get_waypoints_between_two_bus_stops(
                starting_bus_stop_name=testing_bus_stop_names[0],
                ending_bus_stop_name=testing_bus_stop_names[1]
            )

        # 8. (route_generator) - test_get_waypoints_between_multiple_bus_stops
        elif selection == '8':
            test_get_waypoints_between_multiple_bus_stops(
                bus_stop_names=testing_bus_stop_names
            )

        # 9. (look_ahead_handler) - test_generate_bus_line
        elif selection == '9':
            application_tester.look_ahead_handler_tester.test_generate_bus_line(
                line_id=1,
                bus_stop_names=testing_bus_stop_names
            )

        # 10. (mongodb_database) - print_bus_line_documents
        elif selection == '10':
            application_tester.mongodb_database_connection_tester.print_bus_line_documents()

        # 11. (mongodb_database) - print_detailed_bus_stop_waypoints_documents
        elif selection == '11':
            application_tester.mongodb_database_connection_tester.print_detailed_bus_stop_waypoints_documents(
                bus_stop_names=testing_bus_stop_names
            )

        # 12. (travel_requests_simulator) - test_generate_travel_request_documents
        elif selection == '12':
            application_tester.travel_requests_simulator_tester.test_generate_travel_request_documents(
                line_id=1,
                initial_datetime=travel_requests_min_departure_datetime_testing_value,
                number_of_travel_request_documents=10000
            )

        # 13. (mongodb_database) - print_travel_request_documents
        elif selection == '13':
            application_tester.mongodb_database_connection_tester.print_travel_request_documents(
                line_ids=[1],
                min_departure_datetime=travel_requests_min_departure_datetime_testing_value,
                max_departure_datetime=travel_requests_max_departure_datetime_testing_value,
                counter=10
            )

        # 14. (look_ahead_handler) - test_generate_timetables_for_bus_line
        elif selection == '14':
            application_tester.look_ahead_handler_tester.test_generate_timetables_for_bus_line(line_id=1)

        # 15. (mongodb_database) - print_timetable_documents
        elif selection == '15':
            application_tester.mongodb_database_connection_tester.print_timetable_documents(
                line_ids=[1],
                counter=1,
                timetables_control=True,
                timetable_entries_control=True,
                travel_requests_control=True
            )

        # 16. (traffic_data_simulator) - test_generate_traffic_data_between_multiple_bus_stops
        elif selection == '16':
            application_tester.traffic_data_simulator_tester.test_generate_traffic_data_between_multiple_bus_stops(
                bus_stop_names=testing_bus_stop_names
            )

        # 17. (mongodb_database) - print_traffic_density_documents
        elif selection == '17':
            application_tester.mongodb_database_connection_tester.print_traffic_density_documents(
                bus_stop_names=testing_bus_stop_names
            )

        # 18. (look_ahead_handler) - test_update_timetables_of_bus_line
        elif selection == '18':
            application_tester.look_ahead_handler_tester.test_update_timetables_of_bus_line(line_id=1)

        # 19. (look_ahead_handler) - start_timetables_generator_process
        elif selection == '19':
            # application_tester.look_ahead_handler_tester.start_timetables_generator_process()
            timetables_generator_process = Process(
                target=application_tester.look_ahead_handler_tester.test_timetables_generator_process,
                args=()
            )
            timetables_generator_process.start()
            print '\nlook_ahead_handler: timetables_generator_process: terminated'

        # 20. (look_ahead_handler) - terminate_timetables_generator_process
        elif selection == '20':
            # application_tester.look_ahead_handler_tester.terminate_timetables_generator_process()
            if timetables_generator_process is not None:
                timetables_generator_process.terminate()
                timetables_generator_process.join()
                timetables_generator_process = None
                print '\nlook_ahead_handler: timetables_generator_process: terminated'
            else:
                print '\nlook_ahead_handler: timetables_generator_process: None'

        # 21. (look_ahead_handler) - start_timetables_updater_process
        elif selection == '21':
            # application_tester.look_ahead_handler_tester.start_timetables_updater_process()
            timetables_updater_process = Process(
                target=application_tester.look_ahead_handler_tester.test_timetables_updater_process,
                args=()
            )
            timetables_updater_process.start()
            print '\nlook_ahead_handler: timetables_updater_process: starting'

        # 22. (look_ahead_handler) - terminate_timetables_updater_process
        elif selection == '22':
            # application_tester.look_ahead_handler_tester.terminate_timetables_updater_process()
            if timetables_updater_process is not None:
                timetables_updater_process.terminate()
                timetables_updater_process.join()
                timetables_generator_process = None
                print '\nlook_ahead_handler: timetables_updater_process: terminated'
            else:
                print '\nlook_ahead_handler: timetables_updater_process: None'

        # 23. (travel_requests_simulator) - start_travel_requests_generator_process
        elif selection == '23':
            # application_tester.travel_requests_simulator_tester.start_travel_requests_generator_process(
            #     initial_datetime=travel_requests_min_departure_datetime_testing_value,
            #     min_number_of_travel_request_documents=travel_requests_generator_min_number_of_documents,
            #     max_number_of_travel_request_documents=travel_requests_generator_max_number_of_documents
            # )
            initial_datetime = travel_requests_min_departure_datetime_testing_value
            min_number_of_travel_request_documents = travel_requests_generator_min_number_of_documents
            max_number_of_travel_request_documents = travel_requests_generator_max_number_of_documents

            travel_requests_generator_process = Process(
                target=application_tester.travel_requests_simulator_tester.test_travel_requests_generator_process,
                args=(initial_datetime, min_number_of_travel_request_documents, max_number_of_travel_request_documents)
            )
            travel_requests_generator_process.start()
            print '\ntravel_requests_simulator: travel_requests_generator_process: starting'

        # 24. (travel_requests_simulator) - terminate_travel_requests_generator_process
        elif selection == '24':
            # application_tester.travel_requests_simulator_tester.terminate_travel_requests_generator_process()
            if travel_requests_generator_process is not None:
                travel_requests_generator_process.terminate()
                travel_requests_generator_process.join()
                traffic_requests_generator_process = None
                print '\ntravel_requests_simulator: travel_requests_generator_process: terminated'
            else:
                print '\ntravel_requests_simulator: travel_requests_generator_process: None'

        # 25. (traffic_data_simulator) - start_traffic_data_generator_process
        elif selection == '25':
            # application_tester.traffic_data_simulator_tester.start_traffic_data_generator_process()
            traffic_data_generator_process = Process(
                target=application_tester.traffic_data_simulator_tester.test_traffic_data_generator_process,
                args=()
            )
            traffic_data_generator_process.start()
            print '\ntraffic_data_simulator: traffic_data_generator_process: starting'

        # 26. (traffic_data_simulator) - terminate_traffic_data_generator_process
        elif selection == '26':
            # application_tester.traffic_data_simulator_tester.terminate_traffic_data_generator_process()
            if traffic_data_generator_process is not None:
                traffic_data_generator_process.terminate()
                traffic_data_generator_process.join()
                traffic_data_generator_process = None
                print '\ntraffic_data_simulator: traffic_data_generator_process: terminated'
            else:
                print '\ntraffic_data_simulator: traffic_data_generator_process: None'

        else:
            pass

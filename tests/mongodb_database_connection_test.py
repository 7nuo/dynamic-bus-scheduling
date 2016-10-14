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

    def clear_address_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_address_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_address_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_address_documents_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_bus_line_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_bus_line_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_bus_line_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_bus_line_documents_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_bus_stop_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_bus_stop_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_bus_stop_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_bus_stop_documents_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_bus_stop_waypoints_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_bus_stop_waypoints_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_bus_stop_waypoints_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_bus_stop_waypoints_documents_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_edge_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_edge_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_edge_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_edge_documents_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_node_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_node_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_node_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_node_documents_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_point_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_point_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_point_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_point_documents_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_timetable_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_timetable_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_timetable_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_timetable_documents_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_traffic_event_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_traffic_event_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_traffic_event_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_traffic_event_documents_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_travel_request_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_travel_request_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_travel_request_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_travel_request_documents_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_way_documents_collection(self):
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_way_documents_collection: starting')
        self.start_time = time.time()
        self.mongodb_database_connection.clear_way_documents_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='clear_way_documents_collection: finished - elapsed_time = ' +
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

    def print_timetable_documents(self, object_ids=None, line_ids=None, counter=None, timetables_control=True,
                                  timetable_entries_control=False, travel_requests_control=False):
        """
        Print multiple timetable_documents.

        timetable_document: {
            '_id', 'line_id',
            'timetable_entries': [{
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                'number_of_deboarding_passengers', 'number_of_current_passengers'}],
            'travel_requests': [{
                '_id', 'client_id', 'line_id',
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime',
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
        }
        :param object_ids: [ObjectId]
        :param line_ids: [int]
        :param counter: int
        :param timetables_control: bool
        :param timetable_entries_control: bool
        :param travel_requests_control: bool
        :return: timetable_documents: [timetable_document]
        """
        log(module_name='mongodb_database_connection_test', log_type='INFO',
            log_message='print_timetable_documents')
        self.mongodb_database_connection.print_timetable_documents(
            object_ids=object_ids,
            line_ids=line_ids,
            counter=counter,
            timetables_control=timetables_control,
            timetable_entries_control=timetable_entries_control,
            travel_requests_control=travel_requests_control
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

if __name__ == '__main__':
    mongodb_database_connection_tester = MongodbDatabaseConnectionTester()
    printing_limit = 10  # Positive int or None

    while True:
        time.sleep(0.01)
        selection = raw_input(
            '\n0.  exit'
            '\n1.  clear_collections'
            '\n2.  print_address_documents'
            '\n3.  print_bus_line_documents'
            '\n4.  print_bus_stop_documents'
            '\n5.  print_bus_stop_waypoints_documents'
            '\n6.  print_detailed_bus_stop_waypoints_documents'
            '\n7.  print_edge_documents'
            '\n8.  print_node_documents'
            '\n9.  print_point_documents'
            '\n10. print_timetable_documents'
            '\n11. print_traffic_density_documents'
            '\n12. print_travel_request_documents'
            '\n13. print_way_documents'
            '\nSelection: '
        )
        # 0. exit
        if selection == '0':
            break

        # 1. clear_collections
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
                    mongodb_database_connection_tester.clear_all_collections()

                # 2. clear_address_documents_collection
                elif inner_selection == '2':
                    mongodb_database_connection_tester.clear_address_documents_collection()

                # 3. clear_bus_line_documents_collection
                elif inner_selection == '3':
                    mongodb_database_connection_tester.clear_bus_line_documents_collection()

                # 4. clear_bus_stop_documents_collection
                elif inner_selection == '4':
                    mongodb_database_connection_tester.clear_bus_stop_documents_collection()

                # 5. clear_bus_stop_waypoints_documents_collection
                elif inner_selection == '5':
                    mongodb_database_connection_tester.clear_bus_stop_waypoints_documents_collection()

                # 6. clear_edge_documents_collection
                elif inner_selection == '6':
                    mongodb_database_connection_tester.clear_edge_documents_collection()

                # 7. clear_node_documents_collection
                elif inner_selection == '7':
                    mongodb_database_connection_tester.clear_node_documents_collection()

                # 8. clear_point_documents_collection
                elif inner_selection == '8':
                    mongodb_database_connection_tester.clear_point_documents_collection()

                # 9. clear_timetable_documents_collection
                elif inner_selection == '9':
                    mongodb_database_connection_tester.clear_timetable_documents_collection()

                # 10. clear_traffic_event_documents_collection
                elif inner_selection == '10':
                    mongodb_database_connection_tester.clear_traffic_event_documents_collection()

                # 11. clear_travel_request_documents_collection
                elif inner_selection == '11':
                    mongodb_database_connection_tester.clear_travel_request_documents_collection()

                # 12. clear_way_documents_collection
                elif inner_selection == '12':
                    mongodb_database_connection_tester.clear_way_documents_collection()

                else:
                    pass

        # 2. print_address_documents
        elif selection == '2':
            mongodb_database_connection_tester.print_address_documents()

        # 3. print_bus_line_documents
        elif selection == '3':
            mongodb_database_connection_tester.print_bus_line_documents()

        # 4. print_bus_stop_documents
        elif selection == '4':
            mongodb_database_connection_tester.print_bus_stop_documents()

        # 5. print_bus_stop_waypoints_documents
        elif selection == '5':
            mongodb_database_connection_tester.print_bus_stop_waypoints_documents()

        # 6. print_detailed_bus_stop_waypoints_documents
        elif selection == '6':
            mongodb_database_connection_tester.print_detailed_bus_stop_waypoints_documents()

        # 7. print_edge_documents
        elif selection == '7':
            mongodb_database_connection_tester.print_edge_documents()

        # 8. print_node_documents
        elif selection == '8':
            mongodb_database_connection_tester.print_node_documents()

        # 9. print_point_documents
        elif selection == '9':
            mongodb_database_connection_tester.print_point_documents()

        # 10. print_timetable_documents
        elif selection == '10':
            mongodb_database_connection_tester.print_timetable_documents()

        # 11. print_traffic_density_documents
        elif selection == '11':
            mongodb_database_connection_tester.print_traffic_density_documents()

        # 12. print_travel_request_documents
        elif selection == '12':
            mongodb_database_connection_tester.print_travel_request_documents()

        # 13. print_way_documents
        elif selection == '13':
            mongodb_database_connection_tester.print_way_documents()

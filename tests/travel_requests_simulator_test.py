#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
- LICENCE

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


- DESCRIPTION OF DOCUMENTS

-- MongoDB Database Documents:

address_document: {
    '_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}
}
bus_line_document: {
    '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
}
bus_stop_document: {
    '_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}
}
bus_stop_waypoints_document: {
    '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[edge_object_id]]
}
bus_vehicle_document: {
    '_id', 'bus_vehicle_id', 'maximum_capacity',
    'routes': [{'starting_datetime', 'ending_datetime', 'timetable_id'}]
}
detailed_bus_stop_waypoints_document: {
    '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[edge_document]]
}
edge_document: {
    '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    'max_speed', 'road_type', 'way_id', 'traffic_density'
}
node_document: {
    '_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}
}
point_document: {
    '_id', 'osm_id', 'point': {'longitude', 'latitude'}
}
timetable_document: {
    '_id', 'timetable_id', 'line_id', 'bus_vehicle_id',
    'timetable_entries': [{
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime', 'number_of_onboarding_passengers',
        'number_of_deboarding_passengers', 'number_of_current_passengers',
        'route': {
            'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
            'distances_from_starting_node', 'times_from_starting_node',
            'distances_from_previous_node', 'times_from_previous_node'
        }
    }],
    'travel_requests': [{
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }]
}
traffic_event_document: {
    '_id', 'event_id', 'event_type', 'event_level', 'point': {'longitude', 'latitude'}, 'datetime'
}
travel_request_document: {
    '_id', 'client_id', 'line_id',
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'departure_datetime', 'arrival_datetime',
    'starting_timetable_entry_index', 'ending_timetable_entry_index'
}
way_document: {
    '_id', 'osm_id', 'tags', 'references'
}

-- Route Generator Responses:

get_route_between_two_bus_stops: {
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'route': {
        'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        'distances_from_starting_node', 'times_from_starting_node',
        'distances_from_previous_node', 'times_from_previous_node'
    }
}
get_route_between_multiple_bus_stops: [{
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'route': {
        'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        'distances_from_starting_node', 'times_from_starting_node',
        'distances_from_previous_node', 'times_from_previous_node'
    }
}]
get_waypoints_between_two_bus_stops: {
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[{
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'
    }]]
}
get_waypoints_between_multiple_bus_stops: [{
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[{
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'
    }]]
}]
"""
import time
from multiprocessing import Process
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.data_simulator.travel_requests_simulator import TravelRequestsSimulator
from src.common.logger import log
from src.common.parameters import travel_requests_simulator_timeout, travel_requests_simulator_max_operation_timeout, \
    testing_travel_requests_min_departure_datetime, travel_requests_simulator_min_number_of_documents, \
    travel_requests_simulator_max_number_of_documents, testing_bus_line_id

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class TravelRequestsSimulatorTester(object):
    def __init__(self):
        self.module_name = 'travel_requests_simulator_tester'
        self.log_type = 'INFO'
        self.log_message = 'initialize_travel_requests_simulator: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.travel_requests_simulator = TravelRequestsSimulator()
        self.travel_requests_generator_process = None
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'initialize_travel_requests_simulator: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def start_travel_requests_generator_process(self, initial_datetime, min_number_of_travel_request_documents,
                                                max_number_of_travel_request_documents):
        """
        :param initial_datetime: datetime
        :param min_number_of_travel_request_documents: int
        :param max_number_of_travel_request_documents: int
        :return: None
        """
        if self.travel_requests_generator_process is None:
            self.travel_requests_generator_process = Process(
                target=self.test_travel_requests_generator_process,
                args=(initial_datetime, min_number_of_travel_request_documents, max_number_of_travel_request_documents)
            )
            self.travel_requests_generator_process.start()
            self.log_message = 'travel_requests_generator_process: starting'
        else:
            self.log_message = 'travel_requests_generator_process: already started'

        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def terminate_travel_requests_generator_process(self):
        if self.travel_requests_generator_process is not None:
            self.travel_requests_generator_process.terminate()
            self.travel_requests_generator_process.join()
            self.travel_requests_generator_process = None
            self.log_message = 'travel_requests_generator_process: terminated'
        else:
            self.log_message = 'travel_requests_generator_process: None'

        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_clear_travel_requests_collection(self):
        self.log_message = 'test_clear_travel_requests_collection: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.travel_requests_simulator.clear_travel_requests_collection()
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_clear_travel_requests_collection: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_delete_travel_request_documents(self, object_ids=None, client_ids=None, line_ids=None,
                                             min_departure_datetime=None, max_departure_datetime=None):
        """
        Delete multiple travel_request_documents.

        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :return: None
        """
        self.log_message = 'test_delete_travel_request_documents: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.travel_requests_simulator.delete_travel_request_documents(
            object_ids=object_ids,
            client_ids=client_ids,
            line_ids=line_ids,
            min_departure_datetime=min_departure_datetime,
            max_departure_datetime=max_departure_datetime
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_delete_travel_request_documents: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_generate_random_travel_request_documents(self, initial_datetime, min_number_of_travel_request_documents,
                                                      max_number_of_travel_request_documents):
        """
        Generate random number of travel_request_documents for each bus_line,
        for a 24hour period starting from a selected datetime, and store them at the
        corresponding collection of the System Database.

        :param initial_datetime: datetime
        :param min_number_of_travel_request_documents: int
        :param max_number_of_travel_request_documents: int
        :return: None
        """
        self.log_message = 'test_generate_random_travel_request_documents: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.travel_requests_simulator.generate_random_travel_request_documents(
            initial_datetime=initial_datetime,
            min_number_of_travel_request_documents=min_number_of_travel_request_documents,
            max_number_of_travel_request_documents=max_number_of_travel_request_documents
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_generate_random_travel_request_documents: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_generate_travel_request_documents(self, initial_datetime, number_of_travel_request_documents,
                                               bus_line=None, line_id=None):
        """
        Generate a specific number of travel_request_documents, for the selected bus_line,
        for a 24hour period starting from a selected datetime, and store them at the
        corresponding collection of the System Database.

        :param initial_datetime: datetime
        :param number_of_travel_request_documents: int
        :param bus_line: bus_line_document
        :param line_id: int
        :return: None
        """
        self.log_message = 'test_generate_travel_request_documents: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.travel_requests_simulator.generate_travel_request_documents(
            initial_datetime=initial_datetime,
            number_of_travel_request_documents=number_of_travel_request_documents,
            bus_line=bus_line,
            line_id=line_id
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_generate_travel_request_documents: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_travel_requests_generator_process(self, initial_datetime, min_number_of_travel_request_documents,
                                               max_number_of_travel_request_documents):
        """
        :param initial_datetime: datetime
        :param min_number_of_travel_request_documents: int
        :param max_number_of_travel_request_documents: int
        :return: None
        """
        time_difference = 0
        initial_time = time.time()

        while time_difference < travel_requests_simulator_max_operation_timeout:
            self.test_generate_random_travel_request_documents(
                initial_datetime=initial_datetime,
                min_number_of_travel_request_documents=min_number_of_travel_request_documents,
                max_number_of_travel_request_documents=max_number_of_travel_request_documents
            )
            time.sleep(travel_requests_simulator_timeout)
            time_difference = time.time() - initial_time


if __name__ == '__main__':
    travel_requests_simulator_tester = TravelRequestsSimulatorTester()
    number_of_travel_requests_documents = 1000

    while True:
        time.sleep(0.01)
        selection = raw_input(
            '\n0.  exit'
            '\n1.  test_generate_travel_request_documents'
            '\n2.  start_travel_requests_generator_process'
            '\n3.  terminate_travel_requests_generator_process'
            '\nSelection: '
        )

        # 0. exit
        if selection == '0':
            break

        # 1. test_generate_travel_request_documents
        elif selection == '1':
            travel_requests_simulator_tester.test_generate_travel_request_documents(
                line_id=testing_bus_line_id,
                initial_datetime=testing_travel_requests_min_departure_datetime,
                number_of_travel_request_documents=number_of_travel_requests_documents
            )

        # 2. start_travel_requests_generator_process
        elif selection == '2':
            travel_requests_simulator_tester.start_travel_requests_generator_process(
                initial_datetime=testing_travel_requests_min_departure_datetime,
                min_number_of_travel_request_documents=travel_requests_simulator_min_number_of_documents,
                max_number_of_travel_request_documents=travel_requests_simulator_max_number_of_documents
            )

        # 3. terminate_travel_requests_generator_process
        elif selection == '3':
            travel_requests_simulator_tester.terminate_travel_requests_generator_process()

        else:
            pass

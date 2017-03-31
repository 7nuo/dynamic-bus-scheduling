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
from src.common.logger import log
from src.common.parameters import testing_timetables_starting_datetime, testing_timetables_ending_datetime, \
    testing_travel_requests_min_departure_datetime, testing_travel_requests_max_departure_datetime, \
    look_ahead_timetables_generator_timeout, look_ahead_timetables_generator_max_operation_timeout, \
    look_ahead_timetables_updater_timeout, look_ahead_timetables_updater_max_operation_timeout, testing_bus_line_id, \
    testing_bus_stop_names
from src.look_ahead.look_ahead_handler import LookAheadHandler

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class LookAheadHandlerTester(object):
    def __init__(self):
        self.module_name = 'look_ahead_handler_tester'
        self.log_type = 'INFO'
        self.log_message = 'initialize_look_ahead_handler: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.look_ahead_handler = LookAheadHandler()
        self.timetables_generator_process = None
        self.timetables_updater_process = None
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'initialize_look_ahead_handler: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def start_timetables_generator_process(self):
        self.log_message = 'timetables_generator_process: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.timetables_generator_process = Process(target=self.test_timetables_generator_process, args=())
        self.timetables_generator_process.start()

    def start_timetables_updater_process(self):
        self.log_message = 'timetables_updater_process: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.timetables_updater_process = Process(target=self.test_timetables_updater_process, args=())
        self.timetables_updater_process.start()

    def terminate_timetables_generator_process(self):
        if self.timetables_generator_process is not None:
            self.timetables_generator_process.terminate()
            self.timetables_generator_process.join()
            self.timetables_generator_process = None
            self.log_message = 'timetables_generator_process: terminated'
        else:
            self.log_message = 'timetables_generator_process: None'

        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def terminate_timetables_updater_process(self):
        if self.timetables_updater_process is not None:
            self.timetables_updater_process.terminate()
            self.timetables_updater_process.join()
            self.timetables_updater_process = None
            self.log_message = 'timetables_updater_process: terminated'
        else:
            self.log_message = 'timetables_updater_process: None'

        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_generate_bus_line(self, bus_stop_names, line_id=None):
        self.log_message = 'test_generate_bus_line: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.look_ahead_handler.generate_bus_line(
            bus_stop_names=bus_stop_names,
            line_id=line_id
        )
        elapsed_time = time.time() - self.start_time

        self.log_message = 'test_generate_bus_line: finished - elapsed_time = ' + str(elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_generate_timetables_for_bus_line(self, bus_line=None, line_id=None):
        self.log_message = 'generate_timetables_for_bus_line: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.look_ahead_handler.generate_timetables_for_bus_line(
            timetables_starting_datetime=testing_timetables_starting_datetime,
            timetables_ending_datetime=testing_timetables_ending_datetime,
            requests_min_departure_datetime=testing_travel_requests_min_departure_datetime,
            requests_max_departure_datetime=testing_travel_requests_max_departure_datetime,
            bus_line=bus_line,
            line_id=line_id
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'generate_timetables_for_bus_line: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_generate_timetables_for_bus_lines(self):
        self.log_message = 'generate_timetables_for_bus_lines: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.look_ahead_handler.generate_timetables_for_bus_lines(
            timetables_starting_datetime=testing_timetables_starting_datetime,
            timetables_ending_datetime=testing_timetables_ending_datetime,
            requests_min_departure_datetime=testing_travel_requests_min_departure_datetime,
            requests_max_departure_datetime=testing_travel_requests_max_departure_datetime,
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'generate_timetables_for_bus_lines: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_timetables_generator_process(self):
        time_difference = 0
        initial_time = time.time()

        while time_difference < look_ahead_timetables_generator_max_operation_timeout:
            self.test_generate_timetables_for_bus_lines()
            time.sleep(look_ahead_timetables_generator_timeout)
            time_difference = time.time() - initial_time

    def test_timetables_updater_process(self):
        time_difference = 0
        initial_time = time.time()

        while time_difference < look_ahead_timetables_updater_max_operation_timeout:
            self.test_update_timetables_of_bus_lines()
            time.sleep(look_ahead_timetables_updater_timeout)
            time_difference = time.time() - initial_time

    def test_update_timetables_of_bus_line(self, bus_line=None, line_id=None):
        self.log_message = 'test_update_timetables_of_bus_line: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.look_ahead_handler.update_timetables_of_bus_line(bus_line=bus_line, line_id=line_id)
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_update_timetables_of_bus_line: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_update_timetables_of_bus_lines(self):
        self.log_message = 'test_update_timetables_of_bus_lines: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.look_ahead_handler.update_timetables_of_bus_lines()
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_update_timetables_of_bus_lines: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)


if __name__ == '__main__':
    look_ahead_handler_tester = LookAheadHandlerTester()

    while True:
        time.sleep(0.01)
        selection = raw_input(
            '\n0.  exit'
            '\n1.  test_generate_bus_line'
            '\n2.  test_generate_timetables_for_bus_line'
            '\n3.  test_update_timetables_of_bus_line'
            '\n4.  start_timetables_generator_process'
            '\n5.  terminate_timetables_generator_process'
            '\n6.  start_timetables_updater_process'
            '\n7.  terminate_timetables_updater_process'
            '\nSelection: '
        )
        # 0. exit
        if selection == '0':
            break

        # 1. test_generate_bus_line
        elif selection == '1':
            look_ahead_handler_tester.test_generate_bus_line(
                line_id=testing_bus_line_id,
                bus_stop_names=testing_bus_stop_names
            )

        # 2. test_generate_timetables_for_bus_line
        elif selection == '2':
            look_ahead_handler_tester.test_generate_timetables_for_bus_line(
                line_id=testing_bus_line_id
            )

        # 3. test update_timetables_of_bus_line
        elif selection == '3':
            look_ahead_handler_tester.test_update_timetables_of_bus_line(
                line_id=testing_bus_line_id
            )

        # 4. start_timetables_generator_process
        elif selection == '4':
            look_ahead_handler_tester.start_timetables_generator_process()

        # 5. terminate_timetables_generator_process
        elif selection == '5':
            look_ahead_handler_tester.terminate_timetables_generator_process()

        # 6. start_timetables_updater_process
        elif selection == '6':
            look_ahead_handler_tester.start_timetables_updater_process()

        # 7. terminate_timetables_updater_process
        elif selection == '7':
            look_ahead_handler_tester.terminate_timetables_updater_process()

        else:
            pass

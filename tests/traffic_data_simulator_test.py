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
    '_id', 'bus_line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
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
    '_id', 'timetable_id', 'bus_line_id', 'bus_vehicle_id',
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
        '_id', 'client_id', 'bus_line_id',
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
    '_id', 'client_id', 'bus_line_id',
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
from src.common.parameters import traffic_data_simulator_timeout, traffic_data_simulator_max_operation_timeout, \
    testing_bus_stop_names
from src.data_simulator.traffic_data_simulator import TrafficDataSimulator

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class TrafficDataSimulatorTester(object):
    def __init__(self):
        self.module_name = 'traffic_data_simulator_tester'
        self.log_type = 'INFO'
        self.log_message = 'initialize_traffic_data_simulator: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.traffic_data_simulator = TrafficDataSimulator()
        self.traffic_data_generator_process = None
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'initialize_traffic_data_simulator: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def start_traffic_data_generator_process(self):
        if self.traffic_data_generator_process is None:
            self.traffic_data_generator_process = Process(
                target=self.test_generate_traffic_data_for_bus_lines,
                args=()
            )
            self.traffic_data_generator_process.start()
            self.log_message = 'traffic_data_generator_process: starting'
        else:
            self.log_message = 'traffic_data_generator_process: already started'

        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def terminate_traffic_data_generator_process(self):
        if self.traffic_data_generator_process is not None:
            self.traffic_data_generator_process.terminate()
            self.traffic_data_generator_process.join()
            self.traffic_data_generator_process = None
            self.log_message = 'traffic_data_generator_process: terminated'
        else:
            'traffic_data_generator_process: None'

        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_clear_traffic_density(self):
        self.log_message = 'test_clear_traffic_density: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.traffic_data_simulator.clear_traffic_density()
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_clear_traffic_density: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_generate_traffic_data_between_two_bus_stops(self, starting_bus_stop=None, ending_bus_stop=None,
                                                         starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Generate random traffic density values for the edges which connect two bus_stops.

        :param starting_bus_stop: bus_stop_document
        :param ending_bus_stop: bus_stop_document
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return: None
        """
        self.log_message = 'test_generate_traffic_data_between_two_bus_stops: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.traffic_data_simulator.generate_traffic_data_between_two_bus_stops(
            starting_bus_stop=starting_bus_stop,
            ending_bus_stop=ending_bus_stop,
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_generate_traffic_data_between_two_bus_stops: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_generate_traffic_data_between_multiple_bus_stops(self, bus_stops=None, bus_stop_names=None):
        """
        Generate random traffic density values for the edges which connect multiple bus_stops.

        :param bus_stops: [bus_stop_document]
        :param bus_stop_names: [string]
        :return: None
        """
        self.log_message = 'test_generate_traffic_data_between_multiple_bus_stops: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.traffic_data_simulator.generate_traffic_data_between_multiple_bus_stops(
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_generate_traffic_data_between_multiple_bus_stops: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_generate_traffic_data_for_bus_line(self, bus_line=None, bus_line_id=None):
        """
        Generate random traffic density values for the edge_documents which are included in a bus_line_document.

        :param bus_line: bus_line_document
        :param bus_line_id: int
        :return: None
        """
        self.log_message = 'test_generate_traffic_data_for_bus_line: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.traffic_data_simulator.generate_traffic_data_for_bus_line(
            bus_line=bus_line,
            bus_line_id=bus_line_id
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_generate_traffic_data_for_bus_line: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_generate_traffic_data_for_bus_lines(self, bus_lines=None):
        """
        Generate random traffic density values for the edge_documents which are included in a bus_line_documents.

        :param bus_lines: [bus_line_document]
        :return: None
        """
        self.log_message = 'test_generate_traffic_data_for_bus_lines: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.traffic_data_simulator.generate_traffic_data_for_bus_lines(bus_lines=bus_lines)
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_generate_traffic_data_for_bus_lines: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_traffic_data_generator_process(self):
        time_difference = 0
        initial_time = time.time()

        while time_difference < traffic_data_simulator_max_operation_timeout:
            self.test_generate_traffic_data_for_bus_lines()
            time.sleep(traffic_data_simulator_timeout)
            time_difference = time.time() - initial_time

    def test_set_traffic_density_limits(self, lowest_traffic_density_value, highest_traffic_density_value):
        """
        Set the lowest and highest traffic density values.

        :param lowest_traffic_density_value: float: [0, 1]
        :param highest_traffic_density_value: float: [0, 1]
        :return: None
        """
        self.log_message = 'test_set_traffic_density_limits: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.traffic_data_simulator.set_traffic_density_limits(
            lowest_traffic_density_value=lowest_traffic_density_value,
            highest_traffic_density_value=highest_traffic_density_value
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_set_traffic_density_limits: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)


if __name__ == '__main__':
    traffic_data_simulator_tester = TrafficDataSimulatorTester()

    while True:
        time.sleep(0.01)
        selection = raw_input(
            '\n0.  exit'
            '\n1.  test_generate_traffic_data_between_multiple_bus_stops'
            '\n2.  start_traffic_data_generator_process'
            '\n3.  terminate_traffic_data_generator_process'
            '\nSelection: '
        )

        # 0. exit
        if selection == '0':
            break

        # 1. test_generate_traffic_data_between_multiple_bus_stops
        elif selection == '1':
            traffic_data_simulator_tester.test_generate_traffic_data_between_multiple_bus_stops(
                bus_stop_names=testing_bus_stop_names
            )

        # 2. start_traffic_data_generator_process
        elif selection == '2':
            traffic_data_simulator_tester.start_traffic_data_generator_process()

        # 3. terminate_traffic_data_generator_process
        elif selection == '3':
            traffic_data_simulator_tester.terminate_traffic_data_generator_process()

        else:
            pass


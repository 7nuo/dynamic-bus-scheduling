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
from src.common.logger import log
from src.common.variables import traffic_data_generator_timeout, traffic_data_generator_max_operation_timeout
from src.data_simulator.traffic_data_simulator import TrafficDataSimulator
from multiprocessing import Process


class TrafficDataSimulatorTester(object):
    def __init__(self):
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='initialize_traffic_data_simulator: starting')
        self.start_time = time.time()
        self.traffic_data_simulator = TrafficDataSimulator()
        self.traffic_data_generator_process = None
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='initialize_traffic_data_simulator: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def start_traffic_data_generator_process(self):
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='traffic_data_generator_process: starting')
        self.traffic_data_generator_process = Process(
            target=self.test_generate_traffic_data_for_bus_lines,
            args=()
        )
        self.traffic_data_generator_process.start()

    def terminate_traffic_data_generator_process(self):
        self.traffic_data_generator_process.terminate()
        self.traffic_data_generator_process.join()
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='traffic_data_generator_process: finished')

    def test_clear_traffic_density(self):
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='test_clear_traffic_density: starting')
        self.start_time = time.time()
        self.traffic_data_simulator.clear_traffic_density()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='test_clear_traffic_density: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')

    def test_generate_traffic_data_for_bus_line(self, bus_line=None, line_id=None):
        """
        Generate random traffic density values for the edge_documents which are included in a bus_line_document.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param bus_line: bus_line_document
        :param line_id: int
        :return: None
        """
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='test_generate_traffic_data_for_bus_line: starting')
        self.start_time = time.time()
        self.traffic_data_simulator.generate_traffic_data_for_bus_line(
            bus_line=bus_line,
            line_id=line_id
        )
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='test_generate_traffic_data_for_bus_line: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')

    def test_generate_traffic_data_for_bus_lines(self, bus_lines=None):
        """
        Generate random traffic density values for the edge_documents which are included in a bus_line_documents.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param bus_lines: [bus_line_document]
        :return: None
        """
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='test_generate_traffic_data_for_bus_lines: starting')
        self.start_time = time.time()
        self.traffic_data_simulator.generate_traffic_data_for_bus_lines(bus_lines=bus_lines)
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='test_generate_traffic_data_for_bus_lines: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')

    def test_generate_traffic_data_between_bus_stops(self, starting_bus_stop=None, ending_bus_stop=None,
                                                     starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Generate random traffic density values for the edges which connect two bus_stops.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return: None
        """
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='test_generate_traffic_data_between_bus_stops: starting')
        self.start_time = time.time()
        self.traffic_data_simulator.generate_traffic_data_between_bus_stops(
            starting_bus_stop=starting_bus_stop,
            ending_bus_stop=ending_bus_stop,
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='test_generate_traffic_data_between_bus_stops: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')

    def test_traffic_data_generator_process(self):
        time_difference = 0
        initial_time = time.time()

        while time_difference < traffic_data_generator_max_operation_timeout:
            self.test_generate_traffic_data_for_bus_lines()
            time.sleep(traffic_data_generator_timeout)
            time_difference = time.time() - initial_time

        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='traffic_data_generator_process: finished')

    # def print_traffic_density_between_two_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
    #     log(module_name='traffic_data_simulator_test', log_type='INFO',
    #         log_message='print_traffic_density_documents: starting')
    #     self.start_time = time.time()
    #     self.traffic_data_simulator.print_traffic_density_between_two_bus_stops(
    #         starting_bus_stop_name=starting_bus_stop_name,
    #         ending_bus_stop_name=ending_bus_stop_name,
    #     )
    #     self.elapsed_time = time.time() - self.start_time
    #     log(module_name='traffic_data_simulator_test', log_type='INFO',
    #         log_message='print_traffic_density_documents: finished - elapsed_time = ' +
    #                     str(self.elapsed_time) + ' sec')


if __name__ == '__main__':
    tester = TrafficDataSimulatorTester()

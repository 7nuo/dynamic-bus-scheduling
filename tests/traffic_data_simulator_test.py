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
from src.data_simulator.traffic_data_simulator import TrafficDataSimulator


class TrafficDataSimulatorTester(object):
    def __init__(self):
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='initialize_traffic_data_simulator: starting')
        self.start_time = time.time()
        self.traffic_data_simulator = TrafficDataSimulator()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='initialize_traffic_data_simulator: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_traffic_density(self):
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='clear_traffic_density: starting')
        self.start_time = time.time()
        self.traffic_data_simulator.clear_traffic_density()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='clear_traffic_density: finished - elapsed_time = ' + str(self.elapsed_time) + ' sec')

    def generate_traffic_between_bus_stop_names(self, starting_bus_stop_name, ending_bus_stop_name,
                                                waypoints_index, new_traffic_density):
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='generate_traffic_between_bus_stop_names: starting')
        self.start_time = time.time()
        self.traffic_data_simulator.generate_traffic_between_bus_stop_names(
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name,
            waypoints_index=waypoints_index,
            new_traffic_density=new_traffic_density
        )
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='generate_traffic_between_bus_stop_names: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def print_traffic_density_between_two_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='print_traffic_density_between_two_bus_stops: starting')
        self.start_time = time.time()
        self.traffic_data_simulator.print_traffic_density_between_two_bus_stops(
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name,
        )
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_simulator_test', log_type='INFO',
            log_message='print_traffic_density_between_two_bus_stops: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')


if __name__ == '__main__':
    # bus_stop_names = ['Centralstationen', 'Stadshuset', 'Skolgatan', 'Ekonomikum', 'Studentstaden', 'Rickomberga',
    #                   'Oslogatan', 'Reykjaviksgatan', 'Ekebyhus', 'Sernanders väg', 'Flogsta centrum',
    #                   'Sernanders väg', 'Ekebyhus', 'Reykjaviksgatan', 'Oslogatan', 'Rickomberga',
    #                   'Studentstaden', 'Ekonomikum','Skolgatan', 'Stadshuset', 'Centralstationen']

    tester = TrafficDataSimulatorTester()

    # tester.clear_traffic_density()

    # tester.print_traffic_density_between_two_bus_stops(
    #     starting_bus_stop_name='Ekebyhus',
    #     ending_bus_stop_name='Sernanders väg'
    # )

    # tester.generate_traffic_between_bus_stop_names(
    #     starting_bus_stop_name='Ekebyhus',
    #     ending_bus_stop_name='Sernanders väg',
    #     waypoints_index=0,
    #     new_traffic_density=0.99
    # )
    # tester.generate_traffic_between_bus_stop_names(
    #     starting_bus_stop_name='Ekebyhus',
    #     ending_bus_stop_name='Sernanders väg',
    #     waypoints_index=1,
    #     new_traffic_density=0.10
    # )
    # tester.print_traffic_density_between_two_bus_stops(
    #     starting_bus_stop_name='Ekebyhus',
    #     ending_bus_stop_name='Sernanders väg'
    # )

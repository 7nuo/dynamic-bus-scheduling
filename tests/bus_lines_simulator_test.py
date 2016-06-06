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
from src.data_simulator.bus_lines_simulator import BusLinesSimulator
from src.common.logger import log


if __name__ == '__main__':
    log(module_name='bus_lines_simulator_test', log_type='INFO', log_message='initialize_database_connection: starting')
    start_time = time.time()
    bus_lines_simulator = BusLinesSimulator()
    bus_lines_simulator.initialize_connection()
    elapsed_time = time.time() - start_time
    log(module_name='bus_lines_simulator_test', log_type='INFO',
        log_message='initialize_database_connection: finished - elapsed_time = ' + str(elapsed_time) + ' sec')

    log(module_name='bus_lines_simulator_test', log_type='INFO', log_message='retrieve_bus_stops_dictionary: starting')
    start_time = time.time()
    bus_lines_simulator.retrieve_bus_stops_dictionary()
    elapsed_time = time.time() - start_time
    log(module_name='bus_lines_simulator_test', log_type='INFO',
        log_message='retrieve_bus_stops_dictionary: finished - elapsed_time = ' + str(elapsed_time) + ' sec')

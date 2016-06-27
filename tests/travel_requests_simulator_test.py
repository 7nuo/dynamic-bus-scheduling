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
from src.data_simulator.travel_requests_simulator import TravelRequestsSimulator
from src.common.logger import log
import time


if __name__ == '__main__':
    log(module_name='travel_requests_simulator_test', log_type='INFO',
        log_message='initialize_travel_requests_simulator: starting')
    start_time = time.time()
    travel_requests_simulator = TravelRequestsSimulator()
    elapsed_time = time.time() - start_time
    log(module_name='travel_requests_simulator_test', log_type='INFO',
        log_message='initialize_travel_requests_simulator: finished - elapsed_time = ' + str(elapsed_time) + ' sec')

    log(module_name='travel_requests_simulator_test', log_type='INFO',
        log_message='generate_travel_requests: starting')
    start_time = time.time()
    travel_requests_simulator.generate_travel_requests()
    elapsed_time = time.time() - start_time
    log(module_name='travel_requests_simulator_test', log_type='INFO',
        log_message='generate_travel_requests: finished - elapsed_time = ' + str(elapsed_time) + ' sec')

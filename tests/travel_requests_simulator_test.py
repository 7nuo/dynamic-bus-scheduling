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
from datetime import datetime
import time


class TravelRequestsSimulatorTester(object):
    def __init__(self):
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='initialize_travel_requests_simulator: starting')
        self.start_time = time.time()
        self.travel_requests_simulator = TravelRequestsSimulator()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='initialize_travel_requests_simulator: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def clear_travel_requests(self):
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='clear_travel_requests: starting')
        self.start_time = time.time()
        self.travel_requests_simulator.clear_travel_requests()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='clear_travel_requests: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def delete_travel_requests_based_on_bus_line_id(self, bus_line_id):
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='delete_travel_requests_based_on_line_id: starting')
        self.start_time = time.time()
        self.travel_requests_simulator.delete_travel_requests_based_on_line_id(line_id=bus_line_id)
        self.elapsed_time = time.time() - self.start_time
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='delete_travel_requests_based_on_line_id: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def delete_travel_requests_based_on_departure_datetime(self, min_departure_datetime, max_departure_datetime):
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='delete_travel_requests_based_on_departure_datetime: starting')
        self.start_time = time.time()
        self.travel_requests_simulator.delete_travel_requests_based_on_departure_datetime(
            min_departure_datetime=min_departure_datetime,
            max_departure_datetime=max_departure_datetime
        )
        self.elapsed_time = time.time() - self.start_time
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='delete_travel_requests_based_on_departure_datetime: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def generate_travel_requests(self, bus_line_id, initial_datetime, number_of_requests):
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='generate_travel_requests: starting')
        self.start_time = time.time()
        self.travel_requests_simulator.generate_travel_requests(
            line_id=bus_line_id,
            initial_datetime=initial_datetime,
            number_of_requests=number_of_requests
        )
        self.elapsed_time = time.time() - self.start_time
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='generate_travel_requests: finished - elapsed_time = ' + str(self.elapsed_time) + ' sec')


if __name__ == '__main__':
    tester = TravelRequestsSimulatorTester()

    tester.clear_travel_requests()

    tester.generate_travel_requests(
        bus_line_id=1,
        initial_datetime=datetime(2016, 8, 26, 0, 0, 0, 00000),
        number_of_requests=10000
    )

    # tester.delete_travel_requests_based_on_line_id(bus_line_id=1)

    # tester.delete_travel_requests_based_on_departure_datetime(
    #     min_departure_datetime=datetime(2016, 6, 30, 0, 0, 0, 00000),
    #     max_departure_datetime=datetime(2016, 7, 1, 0, 0, 0, 00000)
    # )



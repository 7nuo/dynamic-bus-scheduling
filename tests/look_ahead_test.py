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
from src.look_ahead.look_ahead_handler import LookAheadHandler
from datetime import datetime


class LookAheadHandlerTester(object):
    def __init__(self):
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='initialize_look_ahead_handler: starting')
        self.start_time = time.time()
        self.look_ahead_handler = LookAheadHandler()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='initialize_look_ahead_handler: finished - elapsed_time = ' + str(self.elapsed_time) + ' sec')

    def generate_bus_line(self, line_id, bus_stop_names):
        log(module_name='look_ahead_handler_test', log_type='INFO', log_message='generate_bus_line: starting')
        self.start_time = time.time()
        self.look_ahead_handler.generate_bus_line(line_id=line_id, bus_stop_names=bus_stop_names)
        elapsed_time = time.time() - self.start_time
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='generate_bus_line: finished - elapsed_time = ' + str(elapsed_time) + ' sec')

    def generate_bus_line_timetable(self, line_id):
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='generate_bus_line_timetable: starting')
        self.start_time = time.time()
        self.look_ahead_handler.generate_bus_line_timetable(line_id=line_id)
        self.elapsed_time = time.time() - self.start_time
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='generate_bus_line_timetable: finished - elapsed_time = ' + str(self.elapsed_time) + ' sec')

    def test_look_ahead(self):
        self.look_ahead_handler.test_look_ahead(
            line_id=1,
            timetable_starting_datetime=datetime(2016, 7, 18, 0, 0, 0, 00000),
            timetable_ending_datetime=datetime(2016, 7, 19, 0, 0, 0, 00000),
            requests_min_departure_datetime=datetime(2016, 7, 18, 0, 0, 0, 00000),
            requests_max_departure_datetime=datetime(2016, 7, 19, 0, 0, 0, 00000),
            bus_capacity=100,
            minimum_number_of_passengers=10
        )


if __name__ == '__main__':
    bus_stop_names = ['Centralstationen', 'Stadshuset', 'Skolgatan', 'Ekonomikum', 'Studentstaden', 'Rickomberga',
                      'Oslogatan', 'Reykjaviksgatan', 'Ekebyhus', 'Sernanders väg', 'Flogsta centrum', 'Sernanders väg',
                      'Ekebyhus', 'Reykjaviksgatan', 'Oslogatan', 'Rickomberga', 'Studentstaden', 'Ekonomikum',
                      'Skolgatan', 'Stadshuset', 'Centralstationen']

    tester = LookAheadHandlerTester()
    # tester.generate_bus_line(line_id=1, bus_stop_names=bus_stop_names)
    # tester.generate_bus_line_timetable(line_id=1)
    tester.test_look_ahead()





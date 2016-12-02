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
from multiprocessing import Process
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.common.logger import log
from src.common.variables import timetables_starting_datetime_testing_value, timetables_ending_datetime_testing_value, \
    travel_requests_min_departure_datetime_testing_value, travel_requests_max_departure_datetime_testing_value, \
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

    def test_generate_bus_line(self, line_id, bus_stop_names):
        self.log_message = 'test_generate_bus_line: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.look_ahead_handler.generate_bus_line(
            line_id=line_id,
            bus_stop_names=bus_stop_names
        )
        elapsed_time = time.time() - self.start_time

        self.log_message = 'test_generate_bus_line: finished - elapsed_time = ' + str(elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_generate_timetables_for_bus_line(self, bus_line=None, line_id=None):
        self.log_message = 'generate_timetables_for_bus_line: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.look_ahead_handler.generate_timetables_for_bus_line(
            timetables_starting_datetime=timetables_starting_datetime_testing_value,
            timetables_ending_datetime=timetables_ending_datetime_testing_value,
            requests_min_departure_datetime=travel_requests_min_departure_datetime_testing_value,
            requests_max_departure_datetime=travel_requests_max_departure_datetime_testing_value,
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
            timetables_starting_datetime=timetables_starting_datetime_testing_value,
            timetables_ending_datetime=timetables_ending_datetime_testing_value,
            requests_min_departure_datetime=travel_requests_min_departure_datetime_testing_value,
            requests_max_departure_datetime=travel_requests_max_departure_datetime_testing_value,
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

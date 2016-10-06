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
from src.common.logger import log
from src.common.variables import timetables_starting_datetime_testing_value, timetables_ending_datetime_testing_value, \
    travel_requests_min_departure_datetime_testing_value, travel_requests_max_departure_datetime_testing_value, \
    look_ahead_timetables_generator_timeout, look_ahead_timetables_generator_max_operation_timeout, \
    look_ahead_timetables_updater_timeout, look_ahead_timetables_updater_max_operation_timeout
from src.look_ahead.look_ahead_handler import LookAheadHandler


class LookAheadHandlerTester(object):
    def __init__(self):
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='initialize_look_ahead_handler: starting')
        self.start_time = time.time()
        self.look_ahead_handler = LookAheadHandler()
        self.timetables_generator_process = None
        self.timetables_updater_process = None
        self.elapsed_time = time.time() - self.start_time
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='initialize_look_ahead_handler: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')

    def start_timetables_generator_process(self):
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='timetables_generator_process: starting')
        self.timetables_generator_process = Process(target=self.test_timetables_generator_process, args=())
        self.timetables_generator_process.start()

    def start_timetables_updater_process(self):
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='timetables_updater_process: starting')
        self.timetables_updater_process = Process(target=self.test_timetables_updater_process, args=())
        self.timetables_updater_process.start()

    def terminate_timetables_generator_process(self):
        self.timetables_generator_process.terminate()
        self.timetables_generator_process.join()
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='timetables_generator_process: finished')

    def terminate_timetables_updater_process(self):
        self.timetables_updater_process.terminate()
        self.timetables_updater_process.join()
        log(module_name='look_ahead_handler_test', log_type='DEBUG',
            log_message='timetables_updater_process: finished')

    def test_generate_bus_line(self, line_id, bus_stop_names):
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='test_generate_bus_line: starting')
        self.start_time = time.time()
        self.look_ahead_handler.generate_bus_line(
            line_id=line_id,
            bus_stop_names=bus_stop_names
        )
        elapsed_time = time.time() - self.start_time
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='test_generate_bus_line: finished - elapsed_time = '
                        + str(elapsed_time) + ' sec')

    def test_generate_timetables_for_bus_line(self, bus_line=None, line_id=None):
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='generate_timetables_for_bus_line: starting')
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
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='generate_timetables_for_bus_line: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')

    def test_generate_timetables_for_bus_lines(self):
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='generate_timetables_for_bus_lines: starting')
        self.start_time = time.time()
        self.look_ahead_handler.generate_timetables_for_bus_lines(
            timetables_starting_datetime=timetables_starting_datetime_testing_value,
            timetables_ending_datetime=timetables_ending_datetime_testing_value,
            requests_min_departure_datetime=travel_requests_min_departure_datetime_testing_value,
            requests_max_departure_datetime=travel_requests_max_departure_datetime_testing_value,
        )
        self.elapsed_time = time.time() - self.start_time
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='generate_timetables_for_bus_lines: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')

    def test_timetables_generator_process(self):
        time_difference = 0
        initial_time = time.time()

        while time_difference < look_ahead_timetables_generator_max_operation_timeout:
            self.test_generate_timetables_for_bus_lines()
            time.sleep(look_ahead_timetables_generator_timeout)
            time_difference = time.time() - initial_time

        log(module_name='look_ahead_handler_test', log_type='DEBUG',
            log_message='timetables_generator_process: finished')

    def test_timetables_updater_process(self):
        time_difference = 0
        initial_time = time.time()

        while time_difference < look_ahead_timetables_updater_max_operation_timeout:
            self.test_update_timetables_of_bus_lines()
            time.sleep(look_ahead_timetables_updater_timeout)
            time_difference = time.time() - initial_time

        log(module_name='look_ahead_handler_test', log_type='DEBUG',
            log_message='timetables_updater_process: finished')

    def test_update_timetables_of_bus_line(self, bus_line=None, line_id=None):
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='test_update_timetables_of_bus_line: starting')
        self.start_time = time.time()
        self.look_ahead_handler.update_timetables_of_bus_line(bus_line=bus_line, line_id=line_id)
        self.elapsed_time = time.time() - self.start_time
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='test_update_timetables_of_bus_line: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')

    def test_update_timetables_of_bus_lines(self):
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='test_update_timetables_of_bus_lines: starting')
        self.start_time = time.time()
        self.look_ahead_handler.update_timetables_of_bus_lines()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='look_ahead_handler_test', log_type='INFO',
            log_message='test_update_timetables_of_bus_lines: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')


if __name__ == '__main__':
    tester = LookAheadHandlerTester()
    # travel_requests_simulator_tester.test_generate_timetables_for_bus_line(line_id=1)
    # travel_requests_simulator_tester.test_generate_timetables_for_bus_lines()
    # travel_requests_simulator_tester.test_update_timetables_of_bus_line(line_id=1)
    # travel_requests_simulator_tester.test_update_timetables_of_bus_lines()

    # travel_requests_simulator_tester.start_timetables_generator_process()
    # travel_requests_simulator_tester.terminate_timetables_generator_process()

    # travel_requests_simulator_tester.start_timetables_updater_process()
    # travel_requests_simulator_tester.terminate_timetables_updater_process()

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
from src.common.variables import traffic_data_parser_timeout, traffic_data_parser_max_operation_timeout
from src.traffic_data_parser.traffic_data_parser import TrafficDataParser

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class TrafficDataParserTester(object):
    def __init__(self):
        log(module_name='traffic_data_parser_test', log_type='INFO',
            log_message='initialize_traffic_data_parser: starting')
        self.start_time = time.time()
        self.traffic_data_parser = TrafficDataParser()
        self.traffic_data_parser_process = None
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_parser_test', log_type='INFO',
            log_message='initialize_traffic_data_parser: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def handle_traffic_data_updater_process(self):
        time_difference = 0
        initial_time = time.time()

        while time_difference < traffic_data_parser_max_operation_timeout:
            self.test_update_traffic_data()
            time.sleep(traffic_data_parser_timeout)
            time_difference = time.time() - initial_time

    def start_traffic_data_parser_process(self):
        log(module_name='traffic_data_parser_test', log_type='INFO',
            log_message='traffic_data_parser_process: starting')
        self.traffic_data_parser_process = Process(target=self.handle_traffic_data_updater_process, args=())
        self.traffic_data_parser_process.start()

    def terminate_traffic_data_parser_process(self):
        if self.traffic_data_parser_process is not None:
            self.traffic_data_parser_process.terminate()
            self.traffic_data_parser_process.join()
        log(module_name='traffic_data_parser_test', log_type='INFO',
            log_message='traffic_data_parser_process: finished')

    def test_update_traffic_data(self):
        log(module_name='traffic_data_parser_test', log_type='INFO',
            log_message='update_traffic_data: starting')
        self.start_time = time.time()
        self.traffic_data_parser.update_traffic_data()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='traffic_data_parser_test', log_type='INFO',
            log_message='update_traffic_data: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

if __name__ == '__main__':
    traffic_data_parser_tester = TrafficDataParserTester()
    time.sleep(0.2)
    selection = ''

    while True:
        selection = raw_input(
            '\n0.  exit'
            '\n1.  update_traffic_data'
            '\n2.  start_traffic_data_parser_process'
            '\n3.  terminate_traffic_data_parser_process'
            '\nSelection: '
        )

        if selection == '0':
            break

        elif selection == '1':
            traffic_data_parser_tester.test_update_traffic_data()

        elif selection == '2':
            traffic_data_parser_tester.start_traffic_data_parser_process()

        elif selection == '3':
            traffic_data_parser_tester.terminate_traffic_data_parser_process()

        else:
            print 'Invalid input'

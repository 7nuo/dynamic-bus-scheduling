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


if __name__ == '__main__':
    bus_stop_names = ['Centralstationen', 'Stadshuset', 'Skolgatan', 'Ekonomikum', 'Studentstaden', 'Rickomberga',
                      'Oslogatan', 'Reykjaviksgatan', 'Ekebyhus', 'Sernanders väg', 'Flogsta centrum', 'Sernanders väg',
                      'Ekebyhus', 'Reykjaviksgatan', 'Oslogatan', 'Rickomberga', 'Studentstaden', 'Ekonomikum',
                      'Skolgatan', 'Stadshuset', 'Centralstationen']

    log(module_name='look_ahead_handler_test', log_type='INFO', log_message='initialize_look_ahead_handler: starting')
    start_time = time.time()
    look_ahead_handler = LookAheadHandler()
    elapsed_time = time.time() - start_time
    log(module_name='look_ahead_handler_test', log_type='INFO',
        log_message='initialize_look_ahead_handler: finished - elapsed_time = ' + str(elapsed_time) + ' sec')

    # log(module_name='look_ahead_handler_test', log_type='INFO', log_message='generate_bus_line: starting')
    # start_time = time.time()
    # look_ahead_handler.generate_bus_line(line_id=1, bus_stop_names=bus_stop_names)
    # elapsed_time = time.time() - start_time
    # log(module_name='look_ahead_handler_test', log_type='INFO',
    #     log_message='generate_bus_line: finished - elapsed_time = ' + str(elapsed_time) + ' sec')

    # log(module_name='look_ahead_handler_test', log_type='INFO', log_message='generate_bus_line_timetable: starting')
    # start_time = time.time()
    # look_ahead_handler.generate_bus_line_timetable(line_id=1)
    # elapsed_time = time.time() - start_time
    # log(module_name='look_ahead_handler_test', log_type='INFO',
    #     log_message='generate_bus_line_timetable: finished - elapsed_time = ' + str(elapsed_time) + ' sec')






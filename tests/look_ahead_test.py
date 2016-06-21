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
import requests
import json
import time
from src.common.logger import log
from src.look_ahead.look_ahead_handler import LookAheadHandler

host = 'http://127.0.0.1'
port = '2000'


class JSONResponseEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def get_route_between_multiple_bus_stops(bus_stop_names):
    url = host + ':' + port + '/get_route_between_multiple_bus_stop_names'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {'bus_stop_names': bus_stop_names}
    request = requests.post(url, data=data, headers=headers)
    response = json.loads(request.text)
    return response

    # response = [{'starting_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #              'ending_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #              'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
    #                        'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}}]

    # for intermediate_response in response:
    #     starting_bus_stop = intermediate_response.get('starting_bus_stop')
    #     intermediate_route = intermediate_response.get('route')
    #     total_time = intermediate_route.get('total_time')

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

    log(module_name='look_ahead_handler_test', log_type='INFO', log_message='generate_bus_line_timetable: starting')
    start_time = time.time()
    look_ahead_handler.generate_bus_line_timetable(line_id=1)
    elapsed_time = time.time() - start_time
    log(module_name='look_ahead_handler_test', log_type='INFO',
        log_message='generate_bus_line_timetable: finished - elapsed_time = ' + str(elapsed_time) + ' sec')






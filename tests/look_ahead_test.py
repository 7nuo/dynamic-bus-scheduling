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
from datetime import datetime, timedelta
import requests
import json
import time
from src.common.logger import log

host = 'http://127.0.0.1'
port = '2000'


class JSONResponseEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def get_route_between_multiple_bus_stops(bus_stop_names):
    url = host + ':' + port + '/get_route_between_multiple_bus_stops'
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
    starting_datetime = datetime(2016, 6, 10, 8, 0, 0, 00000)
    # ending_datetime = datetime(2016, 6, 10, 8, 0, 0, 00000) + timedelta(hours=1)
    current_datetime = starting_datetime

    bus_stop_names = ['Centralstationen', 'Stadshuset', 'Skolgatan', 'Ekonomikum', 'Studentstaden', 'Rickomberga',
                      'Oslogatan', 'Reykjaviksgatan', 'Ekebyhus', 'Sernanders väg', 'Flogsta centrum', 'Sernanders väg',
                      'Ekebyhus', 'Reykjaviksgatan', 'Oslogatan', 'Rickomberga', 'Studentstaden', 'Ekonomikum',
                      'Skolgatan', 'Stadshuset', 'Centralstationen']

    route_generator_response = get_route_between_multiple_bus_stops(bus_stop_names=bus_stop_names)
    times = []

    for intermediate_response in route_generator_response:
        starting_bus_stop = unicode(intermediate_response.get('starting_bus_stop').get('name')).encode('utf-8')
        ending_bus_stop = unicode(intermediate_response.get('ending_bus_stop').get('name')).encode('utf-8')
        # ending_bus_stop = unicode(intermediate_response.get('ending_bus_stop').get('name')).encode('utf-8')
        intermediate_route = intermediate_response.get('route')
        total_time = intermediate_route.get('total_time')

        times.append({'starting_bus_stop': starting_bus_stop,
                      'ending_bus_stop': ending_bus_stop,
                      'departure_datetime': current_datetime,
                      'arrival_datetime': current_datetime + timedelta(minutes=total_time/60)})

        current_datetime += timedelta(minutes=total_time//60+1)

    for time_entry in times:
        starting_bus_stop = str(time_entry.get('starting_bus_stop'))
        departure_datetime = str(time_entry.get('departure_datetime'))
        ending_bus_stop = str(time_entry.get('ending_bus_stop'))
        arrival_datetime = str(time_entry.get('arrival_datetime'))
        print 'starting_bus_stop: ' + starting_bus_stop + \
              ' - departure_datetime: ' + departure_datetime + \
              ' - ending_bus_stop: ' + ending_bus_stop + \
              ' - arrival_datetime: ' + arrival_datetime

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
from datetime import datetime

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]

mongodb_host = '127.0.0.1'
mongodb_port = 27017

route_generator_host = '127.0.0.1'
route_generator_port = '2000'
route_generator_request_timeout = 60
route_generator_edges_updater_timeout = 10
route_generator_edges_updater_max_operation_timeout = 600

traffic_data_generator_timeout = 100
traffic_data_generator_max_operation_timeout = 600
traffic_data_parser_timeout = 100
traffic_data_parser_max_operation_timeout = 600

look_ahead_timetables_generator_timeout = 100
look_ahead_timetables_generator_max_operation_timeout = 600

look_ahead_timetables_updater_timeout = 100
look_ahead_timetables_updater_max_operation_timeout = 600

travel_requests_generator_timeout = 100
travel_requests_generator_max_operation_timeout = 600
travel_requests_generator_min_number_of_documents = 10
travel_requests_generator_max_number_of_documents = 100

# Maximum amount of speed for roads without a predefined value
standard_speed = 50
# Road types that can be accessed by bus
bus_road_types = (
    'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary',
    'secondary_link', 'tertiary', 'tertiary_link', 'unclassified', 'residential', 'bus_road'
)

maximum_bus_capacity = 100
average_waiting_time_threshold = 60
individual_waiting_time_threshold = 200
minimum_number_of_passengers_in_timetable = 30

timetables_starting_datetime_testing_value = datetime(2016, 10, 20, 0, 0, 0, 00000)
timetables_ending_datetime_testing_value = datetime(2016, 10, 21, 0, 0, 0, 00000)

travel_requests_min_departure_datetime_testing_value = datetime(2016, 10, 20, 0, 0, 0, 00000)
travel_requests_max_departure_datetime_testing_value = datetime(2016, 10, 21, 0, 0, 0, 00000)

testing_osm_filename = '../resources/osm_files/uppsala.osm'

testing_bus_stop_names = [
    'Centralstationen', 'Stadshuset', 'Skolgatan', 'Ekonomikum', 'Rickomberga',
    'Oslogatan', 'Reykjaviksgatan', 'Ekebyhus', 'Sernanders väg', 'Flogsta centrum',
    'Sernanders väg', 'Ekebyhus', 'Reykjaviksgatan', 'Oslogatan', 'Rickomberga',
    'Ekonomikum', 'Skolgatan', 'Stadshuset', 'Centralstationen'
]

testing_bus_line_id = 1

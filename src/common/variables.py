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
from datetime import datetime


mongodb_host = '127.0.0.1'
mongodb_port = 27017

route_generator_host = '127.0.0.1'
route_generator_port = '2000'
route_generator_request_timeout = 30
route_generator_edges_updater_timeout = 100
route_generator_edges_updater_max_operation_timeout = 600

# Maximum amount of speed for roads without a predefined value
standard_speed = 50
# Road types that can be accessed by a bus
bus_road_types = ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary',
                  'secondary_link', 'tertiary', 'tertiary_link', 'unclassified', 'residential', 'bus_road')

maximum_bus_capacity = 100
average_waiting_time_threshold = 100
individual_waiting_time_threshold = 100
minimum_number_of_passengers_in_timetable = 20

timetables_starting_datetime_testing_value = datetime(2016, 8, 26, 0, 0, 0, 00000)
timetables_ending_datetime_testing_value = datetime(2016, 8, 27, 0, 0, 0, 00000)
requests_min_departure_datetime_testing_value = datetime(2016, 8, 26, 0, 0, 0, 00000)
requests_max_departure_datetime_testing_value = datetime(2016, 8, 27, 0, 0, 0, 00000)

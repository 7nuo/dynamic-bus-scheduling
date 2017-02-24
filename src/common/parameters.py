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

# ---------------------------------------- STANDARD PARAMETERS --------------------------------------------------------
# Maximum amount of speed for route connections without a specified value.
standard_speed = 50
# Road types that can be accessed by bus vehicles.
bus_road_types = (
    'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary',
    'secondary_link', 'tertiary', 'tertiary_link', 'unclassified', 'residential', 'bus_road'
)

# ---------------------------------------- SYSTEM DATABASE PARAMETERS -------------------------------------------------
# The name of the host where MongoDB is running.
mongodb_host = '127.0.0.1'
# The port where MongoDB is listening to.
mongodb_port = 27017

# ---------------------------------------- ROUTE GENERATOR PARAMETERS -------------------------------------------------
# The name of the host where the Route Generator is running.
route_generator_host = '127.0.0.1'
# The port where the Route Generator is listening to.
route_generator_port = '2000'
# A parameter representing the time interval (in seconds) during which
# a client is waiting for a response from the Route Generator.
route_generator_request_timeout = 60

# ---------------------------------------- TRAFFIC DATA SIMULATOR PARAMETERS ------------------------------------------
# A parameter representing the time interval (in seconds) during which the Traffic Data Simulator
# process is waiting, before new traffic density values are generated for the stored edge_documents.
traffic_data_simulator_timeout = 100
# A parameter representing the time interval (in seconds) during which the Traffic Data Simulator process is running.
traffic_data_simulator_max_operation_timeout = 600

# ---------------------------------------- TRAFFIC DATA PARSER PARAMETERS ---------------------------------------------
# A parameter representing the time interval (in seconds) during which the Traffic Data Parser
# process is waiting, before the traffic density values of stored edge_documents are updated,
# based on the traffic_jam_events which are retrieved from the CityPulse Data Bus.
traffic_data_parser_timeout = 100
# A parameter representing the time interval (in seconds) during which the Traffic Data Parser process running.
traffic_data_parser_max_operation_timeout = 600

# ---------------------------------------- TRAVEL REQUESTS SIMULATOR PARAMETERS ---------------------------------------
# A parameter representing the time interval (in seconds) during which the Travel Requests Simulator
# process is waiting, before new travel_requests are generated.
travel_requests_simulator_timeout = 100
# A parameter representing the time interval (in seconds) during which the Travel Requests Simulator process is running.
travel_requests_simulator_max_operation_timeout = 600
# The minimum number of travel_requests generated (each time) by the Travel Requests Simulator process.
travel_requests_simulator_min_number_of_documents = 10
# The maximum number of travel_requests generated (each time) by the Travel Requests Simulator process.
travel_requests_simulator_max_number_of_documents = 100

# A list containing 24 integer values, corresponding to a 24-hour period, used by the Travel Requests Simulator
# as comparison values (weights) for the distribution of generated travel_requests. Greater comparison values
# lead to more generated travel_requests during the corresponding hourly period.
#
# travel_requests_simulator_datetime_distribution_weights = [
#     00:00 - 00:59, 01:00 - 01:59, 02:00 - 02:59, 03:00 - 03:59, 04:00 - 04:59, 05:00 - 05:59,
#     06:00 - 06:59, 07:00 - 07:59, 08:00 - 08:59, 09:00 - 09:59, 10:00 - 10:59, 11:00 - 11:59,
#     12:00 - 12:59, 13:00 - 13:59, 14:00 - 14:59, 15:00 - 15:59, 16:00 - 16:59, 17:00 - 17:59,
#     18:00 - 18:59, 19:00 - 19:59, 20:00 - 20:59, 21:00 - 21:59, 22:00 - 22:59, 23:00 - 23:59
# ]
travel_requests_simulator_datetime_distribution_weights = [
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1
]

# ---------------------------------------- LOOK AHEAD PARAMETERS ------------------------------------------------------
# The maximum number of passengers that a bus vehicle can transport.
maximum_bus_capacity = 100
# A time parameter (in seconds) used in order to set limits to the average waiting time of passengers in all timetables.
# As long as the average waiting time of passengers in all timetables is greater than this threshold, the timetable
# generation algorithm will investigate the possibility of updating the generated timetables, so as to reduce the
# average waiting time of passengers. As a result, lower threshold values lead to more generated timetables.
average_waiting_time_threshold = 0
individual_waiting_time_threshold = 0
# The minimum number of passengers that could be served by a timetable. Lower values lead to more generated timetables.
minimum_number_of_passengers_in_timetable = 10

# A parameter representing the time interval (in seconds) during which the Look Ahead
# process is waiting, before the timetable generation algorithm is applied again.
look_ahead_timetables_generator_timeout = 100
# A parameter representing the time interval (in seconds) during which the timetable generation
# algorithm is applied by the the Look Ahead process.
look_ahead_timetables_generator_max_operation_timeout = 600

# A parameter representing the time interval (in seconds) during which the Look Ahead
# process is waiting, before the timetable update algorithm is applied again.
look_ahead_timetables_updater_timeout = 100
# A parameter representing the time interval (in seconds) during which the timetable update
# algorithm is applied by the Look Ahead process.
look_ahead_timetables_updater_max_operation_timeout = 600

# ---------------------------------------- TESTING PARAMETERS ---------------------------------------------------------
testing_osm_filename = '../resources/osm_files/uppsala.osm'

testing_bus_stop_names = [
    'Centralstationen', 'Stadshuset', 'Skolgatan', 'Ekonomikum', 'Rickomberga',
    'Oslogatan', 'Reykjaviksgatan', 'Ekebyhus', 'Sernanders väg', 'Flogsta centrum',
    'Sernanders väg', 'Ekebyhus', 'Reykjaviksgatan', 'Oslogatan', 'Rickomberga',
    'Ekonomikum', 'Skolgatan', 'Stadshuset', 'Centralstationen'
]

testing_bus_line_id = 1

now = datetime.now()
today = datetime(now.year, now.month, now.day, 0, 0, 0, 00000)
tomorrow = datetime(now.year, now.month, now.day+1, 0, 0, 0, 00000)

testing_travel_requests_min_departure_datetime = today
testing_travel_requests_max_departure_datetime = tomorrow

testing_timetables_starting_datetime = today
testing_timetables_ending_datetime = tomorrow

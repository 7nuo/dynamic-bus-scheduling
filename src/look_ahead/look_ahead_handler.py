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
from src.mongodb_database.mongo_connection import MongoConnection
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port, maximum_bus_capacity, average_waiting_time_threshold, \
    individual_waiting_time_threshold, minimum_number_of_passengers_in_timetable
from src.route_generator.route_generator_client import get_route_between_multiple_bus_stops, \
    get_waypoints_between_multiple_bus_stops
from datetime import datetime, timedelta, time
from src.look_ahead.timetable_generator import *


class LookAheadHandler(object):
    def __init__(self):
        self.bus_stops_dictionary = {}
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='look_ahead_handler', log_type='DEBUG', log_message='connection ok')

    def initialize_connection(self):
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='look_ahead_handler', log_type='DEBUG', log_message='connection ok')

    def retrieve_bus_stops_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the BusStops collection.

        bus_stops_dictionary: {name -> {'osm_id', 'point': {'longitude', 'latitude'}}}
        """
        self.bus_stops_dictionary = self.connection.get_bus_stops_dictionary()
        log(module_name='look_ahead_handler', log_type='DEBUG', log_message='bus_stops_dictionary ok')

    def generate_bus_line(self, line_id, bus_stop_names):
        """

        :param line_id: integer
        :param bus_stop_names: [string]
        :return:
        """
        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='get_waypoints_between_multiple_bus_stops (route_generator): starting')
        route_generator_response = get_waypoints_between_multiple_bus_stops(bus_stop_names=bus_stop_names)
        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='get_waypoints_between_multiple_bus_stops (route_generator): finished')
        # [{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #   'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #                   'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #                   'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}]

        bus_stops = []
        starting_bus_stop_controller = True

        for intermediate_response in route_generator_response:
            starting_bus_stop = intermediate_response.get('starting_bus_stop')
            ending_bus_stop = intermediate_response.get('ending_bus_stop')
            waypoints = intermediate_response.get('waypoints')
            lists_of_edge_object_ids = []

            for list_of_edges in waypoints:
                list_of_edge_object_ids = []

                for edge in list_of_edges:
                    edge_object_id = edge.get('_id')
                    list_of_edge_object_ids.append(edge_object_id)

                lists_of_edge_object_ids.append(list_of_edge_object_ids)

            # waypoints: [[edge_object_id]]
            waypoints = lists_of_edge_object_ids
            self.connection.insert_bus_stop_waypoints(starting_bus_stop=starting_bus_stop,
                                                      ending_bus_stop=ending_bus_stop,
                                                      waypoints=waypoints)

            if starting_bus_stop_controller:
                bus_stops.append(starting_bus_stop)
                starting_bus_stop_controller = False

            bus_stops.append(ending_bus_stop)

        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='bus_stop_waypoints (mongodb_database): ok')

        self.connection.insert_bus_line(line_id=line_id, bus_stops=bus_stops)

        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='bus_line (mongodb_database): ok')

    def generate_bus_line_timetables(self, line_id, timetables_starting_datetime, timetables_ending_datetime,
                                     requests_min_departure_datetime, requests_max_departure_datetime):

        """

        :param line_id:
        :param timetables_starting_datetime:
        :param timetables_ending_datetime:
        :param requests_min_departure_datetime:
        :param requests_max_departure_datetime:
        :return:
        """

        # 1: The input: line_id is provided to the function, so as timetables for the corresponding
        #    bus_line to be generated. The Look Ahead retrieves from the System Database the list
        #    of bus_stops which correspond to the selected bus_line.
        #
        # bus_line: {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        # bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        #
        bus_line = self.connection.find_bus_line(line_id=line_id)
        bus_stops = bus_line.get('bus_stops')

        # 2: The inputs: requests_min_departure_datetime and requests_max_departure_datetime are provided
        #    to the function, so as to evaluate travel_requests for the specific datetime period.
        #    The Look Ahead retrieves from the System Database the requests with
        #    departure_datetime between these values.
        #
        # travel_requests: [{'_id', 'travel_request_id, 'client_id', 'bus_line_id', 'starting_bus_stop',
        #                    'ending_bus_stop', 'departure_datetime', 'arrival_datetime'}]
        #
        travel_requests = self.connection.get_travel_requests_list_based_on_bus_line_id_and_departure_datetime(
            bus_line_id=line_id,
            min_departure_datetime=requests_min_departure_datetime,
            max_departure_datetime=requests_max_departure_datetime
        )

        # Initialize TimetableGenerator
        timetable_generator = TimetableGenerator(
            line_id=line_id,
            bus_stops=bus_stops,
            travel_requests=travel_requests
        )

        # The list of bus stops of a bus line might contain the same bus_stop_osm_ids more than once.
        # For this reason, each travel_request needs to be related with the correct index in the bus_stops list.
        correspond_travel_requests_to_bus_stops(
            travel_requests=timetable_generator.travel_requests,
            bus_stops=timetable_generator.bus_stops
        )

        # 3: Timetables are initialized, starting from the starting_datetime and ending at the ending_datetime.
        #
        timetable_generator.timetables = generate_initial_timetables(
            line_id=line_id,
            timetables_starting_datetime=timetables_starting_datetime,
            timetables_ending_datetime=timetables_ending_datetime,
            route_generator_response=timetable_generator.route_generator_response
        )

        # 4: Initial Clustering:
        #    Correspond each travel request to a timetable, so as to produce the
        #    minimum waiting time for each passenger.
        #
        # timetable_generator.correspond_travel_requests_to_timetables_local()
        correspond_travel_requests_to_timetables(
            travel_requests=timetable_generator.travel_requests,
            timetables=timetable_generator.timetables
        )

        handle_overcrowded_timetables(timetables=timetable_generator.timetables)

        adjust_departure_datetimes_of_timetables(timetables=timetable_generator.timetables)

        handle_timetables_with_average_waiting_time_above_threshold(timetables=timetable_generator.timetables)

        handle_travel_requests_of_timetables_with_waiting_time_above_threshold(
            timetables=timetable_generator.timetables
        )

        calculate_number_of_passengers_of_timetables(timetables=timetable_generator.timetables)

        adjust_departure_datetimes_of_timetables(timetables=timetable_generator.timetables)

        # divide_timetable(timetable=timetable_generator.timetables[4])

        print_timetables(timetables=timetable_generator.timetables)

        # 5: Timetables are being re-calculated, based on their corresponding travel requests.
        #    For a set of travel requests, related to a specific bus stop of a timetable,
        #    the new departure datetime corresponds to the mean value of the departure datetimes of the requests.
        #    (New Cluster Centroids)

        # timetable_generator.adjust_departure_datetimes_of_timetable()

        # self.adjust_departure_datetimes(timetables=timetables)

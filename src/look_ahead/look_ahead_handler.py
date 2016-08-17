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
from src.common.variables import mongodb_host, mongodb_port, bus_capacity
from src.route_generator.route_generator_client import get_route_between_multiple_bus_stops, \
    get_waypoints_between_multiple_bus_stops
from datetime import datetime, timedelta, time


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

    # def generate_bus_line_timetable(self, line_id):
    #     """
    #
    #     :param line_id: integer
    #     :return:
    #     """
    #     starting_datetime = datetime(2016, 7, 11, 0, 0, 0, 00000)
    #     current_datetime = starting_datetime
    #     timetable = []
    #
    #     # {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
    #     bus_line = self.connection.find_bus_line(line_id=line_id)
    #     bus_stops = bus_line.get('bus_stops')
    #
    #     # [{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #     #   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #     #   'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
    #     #             'distances_from_starting_node', 'times_from_starting_node',
    #     #             'distances_from_previous_node', 'times_from_previous_node'}}]
    #     route_generator_response = get_route_between_multiple_bus_stops(bus_stops=bus_stops)
    #
    #     for intermediate_response in route_generator_response:
    #         starting_bus_stop = unicode(intermediate_response.get('starting_bus_stop').get('name')).encode('utf-8')
    #         ending_bus_stop = unicode(intermediate_response.get('ending_bus_stop').get('name')).encode('utf-8')
    #         intermediate_route = intermediate_response.get('route')
    #         total_time = intermediate_route.get('total_time')
    #
    #         timetable.append({'starting_bus_stop': starting_bus_stop,
    #                           'ending_bus_stop': ending_bus_stop,
    #                           'departure_datetime': current_datetime,
    #                           'arrival_datetime': current_datetime + timedelta(minutes=total_time / 60)})
    #
    #         current_datetime += timedelta(minutes=total_time // 60 + 1)
    #
    #     for timetable_entry in timetable:
    #         starting_bus_stop = str(timetable_entry.get('starting_bus_stop'))
    #         departure_datetime = str(timetable_entry.get('departure_datetime'))
    #         ending_bus_stop = str(timetable_entry.get('ending_bus_stop'))
    #         arrival_datetime = str(timetable_entry.get('arrival_datetime'))
    #         print 'starting_bus_stop: ' + starting_bus_stop + \
    #               ' - departure_datetime: ' + departure_datetime + \
    #               ' - ending_bus_stop: ' + ending_bus_stop + \
    #               ' - arrival_datetime: ' + arrival_datetime

    # def generate_bus_line_timetables(self, line_id, timetable_starting_datetime, timetable_ending_datetime):
    #     """
    #
    #     :param line_id:
    #     :param timetable_starting_datetime:
    #     :param timetable_ending_datetime:
    #     :return: timetables: [[{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #                             'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #                             'departure_datetime', 'arrival_datetime', 'total_time', 'travel_requests',
    #                             'average_waiting_time', 'number_of_onboarding_passengers',
    #                             'number_of_deboarding_passengers', 'number_of_current_passengers'}]]
    #     """
    #     timetables = []
    #
    #     # 1: The list of bus stops corresponding to the provided bus_line_id is retrieved from the database.
    #     # bus_line: {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
    #     bus_line = self.connection.find_bus_line(line_id=line_id)
    #     bus_stops = bus_line.get('bus_stops')
    #
    #     # [{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #     #   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #     #   'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
    #     #             'distances_from_starting_node', 'times_from_starting_node',
    #     #             'distances_from_previous_node', 'times_from_previous_node'}}]
    #     route_generator_response = get_route_between_multiple_bus_stops(bus_stops=bus_stops)
    #     current_datetime = timetable_starting_datetime
    #
    #     while current_datetime < timetable_ending_datetime:
    #         timetable = []
    #
    #         for intermediate_response in route_generator_response:
    #             starting_bus_stop = intermediate_response.get('starting_bus_stop')
    #             ending_bus_stop = intermediate_response.get('ending_bus_stop')
    #             intermediate_route = intermediate_response.get('route')
    #             total_time = intermediate_route.get('total_time')
    #
    #             timetable_entry = {'starting_bus_stop': starting_bus_stop,
    #                                'ending_bus_stop': ending_bus_stop,
    #                                'departure_datetime': current_datetime,
    #                                'arrival_datetime': current_datetime + timedelta(minutes=total_time / 60),
    #                                'total_time': total_time,
    #                                'travel_requests': [],
    #                                'average_waiting_time': 0,
    #                                'number_of_onboarding_passengers': 0,
    #                                'number_of_deboarding_passengers': 0,
    #                                'number_of_current_passengers': 0}
    #
    #             timetable.append(timetable_entry)
    #             current_datetime += timedelta(minutes=total_time // 60 + 1)
    #
    #         timetables.append(timetable)
    #
    #     return timetables

    def generate_bus_line_timetables(self, line_id, timetables_starting_datetime, timetables_ending_datetime,
                                     requests_min_departure_datetime, requests_max_departure_datetime):

        # 1: The list of bus stops corresponding to the provided bus_line_id is retrieved from the database.
        #
        # bus_line: {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        bus_line = self.connection.find_bus_line(line_id=line_id)
        bus_stops = bus_line.get('bus_stops')

        # 2: The list of travel requests with departure datetime between the requests_min_departure_datetime
        #    and requests_max_departure_datetime is retrieved from the database.
        #
        # travel_requests_list: [{'_id', 'travel_request_id, 'client_id', 'bus_line_id', 'starting_bus_stop',
        #                         'ending_bus_stop', 'departure_datetime', 'arrival_datetime'}]
        travel_requests_list = self.connection.get_travel_requests_list_based_on_bus_line_id_and_departure_datetime(
            bus_line_id=line_id,
            min_departure_datetime=requests_min_departure_datetime,
            max_departure_datetime=requests_max_departure_datetime
        )

        # Initialize TimetableGenerator
        timetable_generator = TimetableGenerator(bus_stops=bus_stops, travel_requests=travel_requests_list)

        # The list of bus stops of a bus line might contain the same bus_stop_osm_ids more than once.
        # For this reason, each travel_request needs to be related with the correct index in the bus_stops list.
        timetable_generator.correspond_travel_requests_to_bus_stops()

        # 3: Timetables are initialized, starting from the starting_datetime and ending at the ending_datetime.
        #
        timetable_generator.generate_initial_timetables(timetables_starting_datetime=timetables_starting_datetime,
                                                        timetables_ending_datetime=timetables_ending_datetime)

        # 4: Initial Clustering:
        #    Correspond each travel request to a timetable, so as to produce the
        #    minimum waiting time for each passenger.
        #
        timetable_generator.correspond_travel_requests_to_timetables_local()

        # 5: Timetables are being re-calculated, based on their corresponding travel requests.
        #    For a set of travel requests, related to a specific bus stop of a timetable,
        #    the new departure datetime corresponds to the mean value of the departure datetimes of the requests.
        #    (New Cluster Centroids)

        # timetable_generator.adjust_departure_datetimes_of_timetable()

        # self.adjust_departure_datetimes(timetables=timetables)


class TimetableGenerator(object):
    def __init__(self, bus_stops, travel_requests):
        """
        Initialize the TimetableGenerator, send a request to the RouteGenerator, and receive the less time-consuming
        route which connects the provided bus stops.

        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}

        :param travel_requests: [{'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                                  'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                                  'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                                  'departure_datetime', 'arrival_datetime',
                                  'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

        timetables: [{
            'timetable_entries': [{
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                'number_of_deboarding_passengers', 'number_of_current_passengers'}],
            'travel_requests': [{
                '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime',
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
            'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        route_generator_response: [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                      'distances_from_starting_node', 'times_from_starting_node',
                      'distances_from_previous_node', 'times_from_previous_node'}}]

        :return: None
        """
        self.timetables = []
        self.bus_stops = bus_stops
        self.travel_requests = travel_requests
        self.route_generator_response = get_route_between_multiple_bus_stops(bus_stops=self.bus_stops)

    @staticmethod
    def add_ideal_departure_datetimes_of_travel_request(ideal_departure_datetimes_of_travel_requests,
                                                        ideal_departure_datetimes_of_travel_request):
        """

        :param ideal_departure_datetimes_of_travel_requests: [[departure_datetime]]
        :param ideal_departure_datetimes_of_travel_request: [departure_datetime]
        :return: None (Updates ideal_departure_datetimes)
        """
        for index in range(0, len(ideal_departure_datetimes_of_travel_request)):
            ideal_departure_datetime_of_travel_request = ideal_departure_datetimes_of_travel_request[index]
            ideal_departure_datetimes_of_travel_requests[index].append(ideal_departure_datetime_of_travel_request)

    def add_timetable(self, timetable):
        """
        Add a provided timetable to the self.timetables list, sorted by the 'starting_datetime' variable.

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: None
        """
        current_number_of_timetables = len(self.timetables)
        index = current_number_of_timetables

        for i in range(0, current_number_of_timetables):
            current_timetable = self.timetables[i]

            if timetable.get('starting_datetime') < current_timetable.get('starting_datetime'):
                index = i
                break

        self.timetables.insert(index, timetable)

    @staticmethod
    def add_travel_request_to_timetable(travel_request, timetable):
        """

        :param travel_request: {'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                                'departure_datetime', 'arrival_datetime',
                                'starting_timetable_entry_index', 'ending_timetable_entry_index'}

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: None (Updates timetable)
        """
        travel_requests_of_timetable = timetable.get('travel_requests')
        travel_requests_of_timetable.append(travel_request)

    def adjust_departure_datetimes_of_timetable(self, timetable):
        """

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: None (Updates timetable)
        """
        travel_requests = timetable.get('travel_requests')
        timetable_entries = timetable.get('timetable_entries')
        number_of_timetable_entries = len(timetable_entries)
        total_times = [timetable_entry.get('total_time') for timetable_entry in timetable_entries]
        ideal_departure_datetimes_of_travel_requests = [[]]

        for travel_request in travel_requests:
            ideal_departure_datetimes_of_travel_request = self.get_ideal_departure_datetimes_of_travel_request(
                travel_request=travel_request,
                number_of_timetable_entries=number_of_timetable_entries,
                total_times=total_times
            )
            self.add_ideal_departure_datetimes_of_travel_request(
                ideal_departure_datetimes_of_travel_requests=ideal_departure_datetimes_of_travel_requests,
                ideal_departure_datetimes_of_travel_request=ideal_departure_datetimes_of_travel_request
            )

        ideal_departure_datetimes = self.estimate_ideal_departure_datetimes(
            ideal_departure_datetimes_of_travel_requests=ideal_departure_datetimes_of_travel_requests
        )

        self.adjust_timetable_entries(timetable=timetable, ideal_departure_datetimes=ideal_departure_datetimes)

    def adjust_departure_datetimes_of_timetables(self, timetables):
        """

        :param timetables: [{
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        :return: None (Updates timetables)
        """
        for timetable in timetables:
            self.adjust_departure_datetimes_of_timetable(timetable=timetable)

    def adjust_departure_datetimes_of_timetables_local(self):
        """

        timetables: [{
            'timetable_entries': [{
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                'number_of_deboarding_passengers', 'number_of_current_passengers'}],
            'travel_requests': [{
                '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime',
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
            'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        :return: None (Updates self.timetables)
        """
        self.adjust_departure_datetimes_of_timetables(timetables=self.timetables)

    @staticmethod
    def adjust_starting_datetime_of_timetable(timetable):
        """

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: None (Updates timetable)
        """
        timetable_entries = timetable.get('timetable_entries')
        starting_timetable_entry = timetable_entries[0]
        departure_datetime_of_starting_timetable_entry = starting_timetable_entry.get('departure_datetime')
        timetable['starting_datetime'] = departure_datetime_of_starting_timetable_entry

    @staticmethod
    def adjust_ending_datetime_of_timetable(timetable):
        """

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: None (Updates timetable)
        """
        timetable_entries = timetable.get('timetable_entries')
        ending_timetable_entry = timetable_entries[len(timetable_entries) - 1]
        arrival_datetime_of_ending_timetable_entry = ending_timetable_entry.get('arrival_datetime')
        timetable['ending_datetime'] = arrival_datetime_of_ending_timetable_entry

    def adjust_timetable_entries(self, timetable, ideal_departure_datetimes):
        """

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :param ideal_departure_datetimes: [departure_datetime]
        :return: None (Updates timetable)
        """
        timetable_entries = timetable.get('timetable_entries')
        number_of_timetable_entries = len(timetable_entries)

        for i in range(0, number_of_timetable_entries):
            timetable_entry = timetable_entries[i]
            total_time = timetable_entry.get('total_time')
            ideal_starting_datetime = ideal_departure_datetimes[i]

            if i == 0:
                departure_datetime = self.ceil_datetime_minutes(starting_datetime=ideal_starting_datetime)
            else:
                previous_departure_datetime = timetable_entries[i - 1].get('departure_datetime')
                departure_datetime = self.ceil_datetime_minutes(
                    starting_datetime=previous_departure_datetime + timedelta(seconds=total_time)
                )

            arrival_datetime = departure_datetime + timedelta(seconds=total_time)
            timetable_entry['departure_datetime'] = departure_datetime
            timetable_entry['arrival_datetime'] = arrival_datetime

    def calculate_average_waiting_time_of_timetable(self, timetable):
        """
        Calculate the average waiting time of a timetable in seconds,
        and update the corresponding timetable entry.

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: average_waiting_time_in_seconds (float)
        """
        timetable_entries = timetable.get('timetable_entries')
        travel_requests = timetable.get('travel_requests')
        number_of_passengers = len(travel_requests)
        total_waiting_time_in_seconds = 0

        for travel_request in travel_requests:
            waiting_time_of_travel_request = self.calculate_waiting_time_of_travel_request(
                timetable_entries=timetable_entries,
                travel_request=travel_request
            )
            total_waiting_time_in_seconds += waiting_time_of_travel_request

        average_waiting_time_in_seconds = total_waiting_time_in_seconds / number_of_passengers
        timetable['average_waiting_time'] = average_waiting_time_in_seconds
        return average_waiting_time_in_seconds

    def calculate_average_waiting_time_of_timetables(self, timetables):
        """

        :param timetables: [{
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        :return:
        """
        for timetable in timetables:
            self.calculate_average_waiting_time_of_timetable(timetable=timetable)

    def calculate_average_waiting_time_of_timetables_local(self):
        """

        timetables: [{
            'timetable_entries': [{
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                'number_of_deboarding_passengers', 'number_of_current_passengers'}],
            'travel_requests': [{
                '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime',
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
            'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        :return:
        """
        self.calculate_average_waiting_time_of_timetables(timetables=self.timetables)

    @staticmethod
    def calculate_departure_datetime_differences_between_travel_request_and_timetables(travel_request, timetables):
        """
        Calculate the datetime difference between a travel request and a list of timetables.

        :param travel_request: {'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                                'departure_datetime', 'arrival_datetime',
                                'starting_timetable_entry_index', 'ending_timetable_entry_index'}

        :param timetables: [{
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        :return: departure_datetime_differences: [{
                     'timetable': {
                         'timetable_entries': [{
                             'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                             'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                             'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                             'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                         'travel_requests': [{
                             '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                             'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                             'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                             'departure_datetime', 'arrival_datetime',
                             'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                         'starting_datetime', 'ending_datetime', 'average_waiting_time'},
                     'departure_datetime_difference'}]
        """
        departure_datetime_differences = []
        # starting_timetable_entry_index corresponds to the timetable_entry from where the passenger departs from.
        starting_timetable_entry_index = travel_request.get('starting_timetable_entry_index')

        for timetable in timetables:
            timetable_entries = timetable.get('timetable_entries')
            corresponding_timetable_entry = timetable_entries[starting_timetable_entry_index]

            departure_datetime_of_travel_request = travel_request.get('departure_datetime')
            departure_datetime_of_timetable_entry = corresponding_timetable_entry.get('departure_datetime')
            departure_datetime_difference = abs(departure_datetime_of_travel_request -
                                                departure_datetime_of_timetable_entry)

            departure_datetime_difference_entry = {
                'timetable': timetable,
                'departure_datetime_difference': departure_datetime_difference
            }
            departure_datetime_differences.append(departure_datetime_difference_entry)

        return departure_datetime_differences

    @staticmethod
    def calculate_mean_departure_datetime(departure_datetimes):
        """

        :param departure_datetimes: [datetime]
        :return: mean_departure_datetime: datetime
        """
        total = 0
        number_of_departure_datetimes = len(departure_datetimes)

        for departure_datetime in departure_datetimes:
            total += (departure_datetime.hour * 3600) + (departure_datetime.minute * 60) + departure_datetime.second

        avg = total / number_of_departure_datetimes
        minutes, seconds = divmod(int(avg), 60)
        hours, minutes = divmod(minutes, 60)
        mean_departure_datetime = datetime.combine(departure_datetimes[0].date(), time(hours, minutes, seconds))
        return mean_departure_datetime

    @staticmethod
    def calculate_number_of_passengers_of_timetable(timetable):
        """

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: None (Updates timetable)
        """
        travel_requests = timetable.get('travel_requests')
        timetable_entries = timetable.get('timetable_entries')

        for travel_request in travel_requests:
            starting_timetable_entry_index = travel_request.get('starting_timetable_entry_index')
            starting_timetable_entry = timetable_entries[starting_timetable_entry_index]
            starting_timetable_entry['number_of_onboarding_passengers'] += 1

            ending_timetable_entry_index = travel_request.get('ending_timetable_entry_index')
            ending_timetable_entry = timetable_entries[ending_timetable_entry_index]
            ending_timetable_entry['number_of_deboarding_passengers'] += 1

        previous_number_of_current_passengers = 0
        previous_number_of_deboarding_passengers = 0

        for timetable_entry in timetable_entries:
            number_of_current_passengers = previous_number_of_current_passengers - \
                                           previous_number_of_deboarding_passengers + \
                                           timetable_entry.get('number_of_boarding_passengers')
            timetable_entry['number_of_current_passengers'] = number_of_current_passengers
            previous_number_of_current_passengers = number_of_current_passengers
            previous_number_of_deboarding_passengers = timetable_entry.get('number_of_deboarding_passengers')

    def calculate_number_of_passengers_of_timetables(self, timetables):
        """

        :param timetables: [{
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        :return: None (Updates timetables)
        """
        for timetable in timetables:
            self.calculate_number_of_passengers_of_timetable(timetable=timetable)

    def calculate_number_of_passengers_of_timetables_local(self):
        """

        timetables: [{
            'timetable_entries': [{
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                'number_of_deboarding_passengers', 'number_of_current_passengers'}],
            'travel_requests': [{
                '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime',
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
            'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        :return: None (Updates self.timetables)
        """
        self.calculate_number_of_passengers_of_timetables(timetables=self.timetables)

    def calculate_waiting_time_of_travel_request(self, timetable_entries, travel_request):
        """
        Calculate the waiting time of a travel request in seconds.

        :param timetable_entries: [{
                   'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                   'number_of_deboarding_passengers', 'number_of_current_passengers'}]

        :param travel_request: [{
                   '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                   'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'departure_datetime', 'arrival_datetime',
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

        :return: waiting_time_in_seconds (float)
        """
        departure_datetime_of_travel_request = travel_request.get('departure_datetime')
        corresponding_timetable_entry = timetable_entries.get('starting_timetable_entry_index')
        departure_datetime_of_timetable = corresponding_timetable_entry.get('departure_datetime')
        waiting_time_in_datetime = abs(departure_datetime_of_timetable - departure_datetime_of_travel_request)
        waiting_time_in_seconds = self.datetime_to_seconds(provided_datetime=waiting_time_in_datetime)
        return waiting_time_in_seconds

    def calculate_waiting_time_of_travel_requests_of_timetable(self, timetable):
        """
        Calculate the waiting time (in seconds) of each travel request of a timetable.

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: waiting_time_of_travel_requests: [{
                     'travel_request': {
                         '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                         'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'departure_datetime', 'arrival_datetime',
                         'starting_timetable_entry_index', 'ending_timetable_entry_index'},
                     'waiting_time'}]
        """
        timetable_entries = timetable.get('timetable_entries')
        travel_requests = timetable.get('travel_requests')
        waiting_time_of_travel_requests = []

        for travel_request in travel_requests:
            waiting_time = self.calculate_waiting_time_of_travel_request(
                timetable_entries=timetable_entries,
                travel_request=travel_request
            )
            dictionary_entry = {'travel_request': travel_request, 'waiting_time': waiting_time}
            waiting_time_of_travel_requests.append(dictionary_entry)

        return waiting_time_of_travel_requests

    @staticmethod
    def ceil_datetime_minutes(starting_datetime):
        """

        :param starting_datetime: datetime
        :return: ending_datetime: datetime
        """
        ending_datetime = starting_datetime - timedelta(microseconds=starting_datetime.microsecond) - \
                          timedelta(seconds=starting_datetime.second) + \
                          timedelta(minutes=1)
        return ending_datetime

    @staticmethod
    def check_number_of_passengers_of_timetable(timetable):
        """
        Check if the number of passengers of a timetable exceeds the bus vehicle capacity.

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: True, if timetable can be served by one bus, otherwise False.
        """
        returned_value = True

        for timetable_entry in timetable.get('timetable_entries'):
            if timetable_entry.get('number_of_current_passengers') > bus_capacity:
                returned_value = True
                break

        return returned_value

    def correspond_travel_requests_to_bus_stops(self):
        """
        The list of bus stops of a bus line might contain the same bus_stop_osm_ids more than once.
        For example, consider a bus line with bus stops [A, B, C, D, C, B, A].
        For this reason, a travel request from bus stop B to bus stop A needs to be related to
        bus_stops list indexes 5 and 6 respectively, not 2 and 6.
        This operation is achieved using this function, which adds the parameters 'starting_timetable_entry_index' and
        'ending_timetable_entry_index' to each travel_request.

        travel_requests: [{'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                           'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                           'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                           'departure_datetime', 'arrival_datetime',
                           'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

        :return: None (Updates self.travel_requests)
        """
        bus_stop_osm_ids = [bus_stop.get('osm_id') for bus_stop in self.bus_stops]

        for travel_request in self.travel_requests:
            starting_bus_stop_osm_id = travel_request.get('starting_bus_stop').get('osm_id')
            starting_timetable_entry_index = self.get_bus_stop_index(
                bus_stop_osm_id=starting_bus_stop_osm_id,
                bus_stop_osm_ids=bus_stop_osm_ids,
                start=0
            )
            travel_request['starting_timetable_entry_index'] = starting_timetable_entry_index

            ending_bus_stop_osm_id = travel_request.get('ending_bus_stop').get('osm_id')
            ending_timetable_entry_index = self.get_bus_stop_index(
                bus_stop_osm_id=ending_bus_stop_osm_id,
                bus_stop_osm_ids=bus_stop_osm_ids,
                start=starting_timetable_entry_index + 1
            )
            travel_request['ending_timetable_entry_index'] = ending_timetable_entry_index

    def correspond_travel_requests_to_timetables(self, travel_requests, timetables):
        """
        Correspond each travel request to a timetable, so as to produce
        the minimum waiting time for each passenger.

        :param travel_requests: [{'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                                  'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                                  'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                                  'departure_datetime', 'arrival_datetime',
                                  'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

        :param timetables: [{
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        :return: None (Updates timetables)
        """
        for travel_request in travel_requests:
            departure_datetime_differences = \
                self.calculate_departure_datetime_differences_between_travel_request_and_timetables(
                    travel_request=travel_request,
                    timetables=timetables
                )

            timetable_with_minimum_datetime_difference = self.get_timetable_with_minimum_departure_datetime_difference(
                departure_datetime_differences=departure_datetime_differences
            )

            self.add_travel_request_to_timetable(
                travel_request=travel_request,
                timetable=timetable_with_minimum_datetime_difference
            )

    def correspond_travel_requests_to_timetables_local(self):
        """
        Correspond each travel request of the TimetableGenerator to a timetable,
        so as to produce the minimum waiting time for the passenger.

        :return: None (Updates self.timetables)
        """
        self.correspond_travel_requests_to_timetables(
            travel_requests=self.travel_requests,
            timetables=self.timetables
        )

    @staticmethod
    def datetime_to_seconds(provided_datetime):
        """
        Convert a datetime to seconds.

        :param provided_datetime: datetime
        :return: seconds: float
        """
        seconds = provided_datetime.year * 31556926 + provided_datetime.month * 2629743.83 + \
                  provided_datetime.day * 86400 + provided_datetime.hour * 3600 + provided_datetime.minute * 60 + \
                  provided_datetime.second
        return seconds

    def estimate_ideal_departure_datetimes(self, ideal_departure_datetimes_of_travel_requests):
        """

        :param ideal_departure_datetimes_of_travel_requests: [[departure_datetime]]
        :return: ideal_departure_datetimes: [departure_datetime]
        """
        ideal_departure_datetimes = []

        for corresponding_departure_datetimes in ideal_departure_datetimes_of_travel_requests:
            ideal_departure_datetime = self.calculate_mean_departure_datetime(
                departure_datetimes=corresponding_departure_datetimes
            )
            ideal_departure_datetimes.append(ideal_departure_datetime)

        return ideal_departure_datetimes

    def generate_initial_timetables(self, timetables_starting_datetime, timetables_ending_datetime):
        """

        :param timetables_starting_datetime: datetime
        :param timetables_ending_datetime: datetime

        timetables: [{
            'timetable_entries': [{
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                'number_of_deboarding_passengers', 'number_of_current_passengers'}],
            'travel_requests': [{
                '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime',
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
            'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        :return: None (Updates self.timetables)
        """
        current_datetime = timetables_starting_datetime

        while current_datetime < timetables_ending_datetime:
            timetable = self.generate_new_timetable(timetable_starting_datetime=current_datetime)
            self.timetables.append(timetable)
            current_datetime = timetable.get('ending_datetime')

    def generate_new_timetable(self, timetable_starting_datetime):
        """
        Generate a timetable starting from a provided datetime.

        :param timetable_starting_datetime: datetime
        :return: timetable: {
                     'timetable_entries': [{
                         'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                         'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                     'travel_requests': [{
                         '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                         'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'departure_datetime', 'arrival_datetime',
                         'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                     'starting_datetime', 'ending_datetime', 'average_waiting_time'}
        """
        current_datetime = timetable_starting_datetime
        timetable = {'timetable_entries': [], 'travel_requests': [], 'average_waiting_time': 0}

        for intermediate_response in self.route_generator_response:
            starting_bus_stop = intermediate_response.get('starting_bus_stop')
            ending_bus_stop = intermediate_response.get('ending_bus_stop')
            intermediate_route = intermediate_response.get('route')
            total_time = intermediate_route.get('total_time')

            timetable_entry = {
                'starting_bus_stop': starting_bus_stop,
                'ending_bus_stop': ending_bus_stop,
                'departure_datetime': current_datetime,
                'arrival_datetime': current_datetime + timedelta(minutes=total_time / 60),
                'total_time': total_time,
                'number_of_onboarding_passengers': 0,
                'number_of_deboarding_passengers': 0,
                'number_of_current_passengers': 0
            }

            timetable['timetable_entries'].append(timetable_entry)
            current_datetime += timedelta(minutes=total_time // 60 + 1)

        self.adjust_starting_datetime_of_timetable(timetable=timetable)
        # first_timetable_entry = timetable.get('timetable_entries')[0]
        # timetable['starting_datetime'] = first_timetable_entry.get('departure_datetime')

        self.adjust_ending_datetime_of_timetable(timetable=timetable)
        # last_timetable_entry = timetable.get('timetable_entries')[len(timetable.get('timetable_entries')) - 1]
        # timetable['ending_datetime'] = last_timetable_entry.get('arrival_datetime')

        return timetable

    @staticmethod
    def get_bus_stop_index(bus_stop_osm_id, bus_stop_osm_ids, start):
        """

        :param bus_stop_osm_id:
        :param bus_stop_osm_ids:
        :param start:
        :return:
        """
        bus_stop_index = -1

        for i in range(start, len(bus_stop_osm_ids)):
            if bus_stop_osm_id == bus_stop_osm_ids[i]:
                bus_stop_index = i
                break

        return bus_stop_index

    @staticmethod
    def get_ideal_departure_datetimes_of_travel_request(travel_request, number_of_timetable_entries, total_times):
        """

        :param travel_request: {
                   '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                   'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'departure_datetime', 'arrival_datetime',
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}
        :param number_of_timetable_entries: int
        :param total_times: []
        :return: ideal_departure_datetimes: [departure_datetime]
        """
        ideal_departure_datetimes = []
        starting_timetable_entry_index = travel_request.get('starting_timetable_entry_index')
        departure_datetime = travel_request.get('departure_datetime')

        ideal_departure_datetimes[starting_timetable_entry_index] = departure_datetime

        # Estimate ideal departure_datetimes before departure_datetime
        index = starting_timetable_entry_index - 1
        ideal_departure_datetime = departure_datetime

        while index > -1:
            corresponding_total_time = total_times[index]
            ideal_departure_datetime -= corresponding_total_time
            ideal_departure_datetimes[index] = ideal_departure_datetime
            index -= 1

        # Estimate ideal departure_datetimes after departure_datetime
        index = starting_timetable_entry_index
        ideal_departure_datetime = departure_datetime

        while index < number_of_timetable_entries - 1:
            corresponding_total_time = total_times[index]
            ideal_departure_datetime += corresponding_total_time
            ideal_departure_datetimes[index] = ideal_departure_datetime
            index += 1

        return ideal_departure_datetimes

    def get_overcrowded_timetables(self, timetables):
        """
        Get the timetables with number of passengers which exceeds the bus vehicle capacity.

        :param timetables: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: overcrowded_timetables: [{
                     'timetable_entries': [{
                         'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                         'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                     'travel_requests': [{
                         '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                         'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'departure_datetime', 'arrival_datetime',
                         'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                     'starting_datetime', 'ending_datetime', 'average_waiting_time'}]
        """
        overcrowded_timetables = []

        for timetable in timetables:
            if not self.check_number_of_passengers_of_timetable(timetable=timetable):
                overcrowded_timetables.append(timetable)

        return overcrowded_timetables

    @staticmethod
    def get_timetable_with_minimum_departure_datetime_difference(departure_datetime_differences):
        """
        Get the timetable with the minimum departure_datetime difference.

        :param departure_datetime_differences: [{
                   'timetable': {
                       'timetable_entries': [{
                           'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                           'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                           'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                           'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                       'travel_requests': [{
                           '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                           'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                           'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                           'departure_datetime', 'arrival_datetime',
                           'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                       'starting_datetime', 'ending_datetime', 'average_waiting_time'},
                   'departure_datetime_difference'}]

        :return: 'timetable': {
                     'timetable_entries': [{
                         'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                         'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                     'travel_requests': [{
                         '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                         'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                         'departure_datetime', 'arrival_datetime',
                         'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                     'starting_datetime', 'ending_datetime', 'average_waiting_time'}
        """
        # minimum_datetime_difference is initialized with a big datetime value.
        min_departure_datetime_difference = timedelta(days=356)
        timetable_with_min_departure_datetime_difference = None

        for departure_datetime_difference_entry in departure_datetime_differences:
            timetable = departure_datetime_difference_entry.get('timetable')
            departure_datetime_difference = departure_datetime_difference_entry.get('departure_datetime_difference')

            if departure_datetime_difference < min_departure_datetime_difference:
                min_departure_datetime_difference = departure_datetime_difference
                timetable_with_min_departure_datetime_difference = timetable

        return timetable_with_min_departure_datetime_difference

    def handle_overcrowded_timetables(self):
        """

        timetables: [{
            'timetable_entries': [{
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                'number_of_deboarding_passengers', 'number_of_current_passengers'}],
            'travel_requests': [{
                '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime',
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
            'starting_datetime', 'ending_datetime', 'average_waiting_time'}]

        :return:
        """
        overcrowded_timetables = self.get_overcrowded_timetables(timetables=self.timetables)

        while len(overcrowded_timetables) > 0:

            for overcrowded_timetable in overcrowded_timetables:
                additional_timetable = self.split_timetable(timetable=overcrowded_timetable)
                self.add_timetable(timetable=additional_timetable)

            overcrowded_timetables = self.get_overcrowded_timetables(timetables=self.timetables)

    def retrieve_travel_requests_with_waiting_time_above_time_limit(self, timetable, waiting_time_limit):
        """

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :param waiting_time_limit: float (in seconds)

        waiting_time_of_travel_requests: [{
            'travel_request': {
                '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime',
                'starting_timetable_entry_index', 'ending_timetable_entry_index'},
            'waiting_time'}]

        :return: travel_requests_with_waiting_time_above_time_limit: [{
            'travel_request': {
                '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime',
                'starting_timetable_entry_index', 'ending_timetable_entry_index'},
            'waiting_time'}]
        """
        travel_requests_with_waiting_time_above_time_limit = []
        waiting_time_of_travel_requests = self.calculate_waiting_time_of_travel_requests_of_timetable(
            timetable=timetable
        )

        for dictionary_entry in waiting_time_of_travel_requests:
            waiting_time = dictionary_entry.get('waiting_time')

            if waiting_time > waiting_time_limit:
                travel_requests_with_waiting_time_above_time_limit.append(dictionary_entry)

        return travel_requests_with_waiting_time_above_time_limit

    def split_timetable(self, timetable):
        """

        :param timetable: {
                   'timetable_entries': [{
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                       'number_of_deboarding_passengers', 'number_of_current_passengers'}],
                   'travel_requests': [{
                       '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                       'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                       'departure_datetime', 'arrival_datetime',
                       'starting_timetable_entry_index', 'ending_timetable_entry_index'}],
                   'starting_datetime', 'ending_datetime', 'average_waiting_time'}

        :return: additional_timetable
        """
        additional_timetable = timetable.copy()
        travel_requests = list(timetable.get('travel_requests'))

        timetable['travel_requests'] = []
        additional_timetable['travel_requests'] = []

        timetables = [timetable, additional_timetable]
        self.correspond_travel_requests_to_timetables(travel_requests=travel_requests, timetables=timetables)
        self.adjust_departure_datetimes_of_timetables(timetables=timetables)

        return additional_timetable

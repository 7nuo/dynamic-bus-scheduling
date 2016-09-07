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
from src.look_ahead.timetable_generator import *
from src.look_ahead.timetable_updater import *


class LookAheadHandler(object):
    def __init__(self):
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='mongodb_database_connection: established')

    def generate_bus_line(self, line_id, bus_stop_names):
        """
        Generate a bus_line, consisted of a line_id and a list of bus_stops, and store it to the corresponding
        collection of the System Database. Moreover, identify all the possible waypoints between the bus_stops
        of the bus_line, and populate the BusStopWaypoints collection.

        :param line_id: int
        :param bus_stop_names: [string]
        :return: None
        """
        # 1: The inputs: line_id and bus_stop_names are provided to the function, so as as a bus_line
        #    with the corresponding line_id and bus_stops to be generated.

        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='get_waypoints_between_multiple_bus_stops (route_generator): starting')

        # 2: The Look Ahead sends a request to the Route Generator so as to select the corresponding bus_stops
        #    for the provided bus_stop_names, as well as to identify all the possible combinations
        #    of intermediate waypoints which connect these bus stops.
        #
        # route_generator_response: [{
        #     'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #     'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #     'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #                     'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #                     'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}]
        #
        route_generator_response = get_waypoints_between_multiple_bus_stops(bus_stop_names=bus_stop_names)

        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='get_waypoints_between_multiple_bus_stops (route_generator): finished')

        # 3: The Look Ahead processes the response of the Route Generator, extracting the bus_stops
        #    and all the possible combinations of their intermediate waypoints which connect them.
        #    These waypoints correspond to the edges which connect the geographic nodes of the
        #    operation area. So, a bus_route is represented as a list of edges. Multiple possible
        #    routes between bus_stops are represented as multiple lists of edges.
        #
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
            #
            waypoints = lists_of_edge_object_ids

            # 4: The Look Ahead populates the BusStopWaypoints collection, by storing all the possible waypoints
            #    for each combination of starting_bus_stop and ending_bus_stop oh the bus_line.
            #
            self.connection.insert_bus_stop_waypoints(
                starting_bus_stop=starting_bus_stop,
                ending_bus_stop=ending_bus_stop,
                waypoints=waypoints
            )

            if starting_bus_stop_controller:
                bus_stops.append(starting_bus_stop)
                starting_bus_stop_controller = False

            bus_stops.append(ending_bus_stop)

        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='insert_bus_stop_waypoints (mongodb_database): ok')

        # 5: The Look Ahead stores the generated bus_line, which is consisted of the line_id and
        #    the list of its bus_stops, to the corresponding collection of the System Database.
        #
        self.connection.insert_bus_line(line_id=line_id, bus_stops=bus_stops)

        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='insert_bus_line (mongodb_database): ok')

    def generate_timetables_for_bus_line(self, bus_line, timetables_starting_datetime, timetables_ending_datetime,
                                         requests_min_departure_datetime, requests_max_departure_datetime):
        """
        Generate timetables for a bus_line, for a selected datetime period,
        evaluating travel_requests of a specific datetime period.

        :param bus_line: {
                   '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        :param timetables_starting_datetime: datetime
        :param timetables_ending_datetime: datetime
        :param requests_min_departure_datetime: datetime
        :param requests_max_departure_datetime: datetime
        :return: None
        """

        # 1: The input: bus_line is provided to the function, so as timetables for the corresponding bus_line
        # to be generated. The Look Ahead retrieves the list of bus_stops which correspond to the selected bus_line.
        #
        # bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        #
        line_id = bus_line.get('line_id')
        bus_stops = bus_line.get('bus_stops')

        # 2: The inputs: timetable_starting_datetime and timetable_ending_datetime are provided to the function,
        #    so as timetables to be generated for the specific datetime period.

        # 3: The inputs: requests_min_departure_datetime and requests_max_departure_datetime are provided
        #    to the function, so as to evaluate travel_requests for the specific datetime period.
        #    The Look Ahead retrieves from the System Database the requests with
        #    departure_datetime between these values.
        #
        # travel_requests: [{'_id', 'client_id', 'bus_line_id',
        #                    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #                    'departure_datetime', 'arrival_datetime',
        #                    'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
        #
        travel_requests = self.connection.get_travel_requests_list_based_on_bus_line_id_and_departure_datetime(
            line_id=line_id,
            min_departure_datetime=requests_min_departure_datetime,
            max_departure_datetime=requests_max_departure_datetime
        )

        # 4: (TimetableGenerator is initialized) The Look Ahead sends a request to the Route Generator so as
        #    to identify the less time-consuming bus_route between the the bus_stops of the bus_line,
        #    while taking into consideration the current levels of traffic density.
        #
        timetable_generator = TimetableGenerator(
            line_id=line_id,
            bus_stops=bus_stops,
            travel_requests=travel_requests
        )

        # The list of bus_stops of a bus_line might contain the same bus_stop_osm_ids more than once.
        # For this reason, each travel_request needs to be related with the correct index in the bus_stops list.
        # So, the values 'starting_timetable_entry_index' and 'ending_timetable_entry_index' are estimated.
        correspond_travel_requests_to_bus_stops(
            travel_requests=timetable_generator.travel_requests,
            bus_stops=timetable_generator.bus_stops
        )

        # 5: Based on the response of the Route Generator, which includes details about the followed bus_route,
        #    and using only one bus vehicle, the Look Ahead generates some initial timetables which cover the
        #    whole datetime period from timetables_starting_datetime to timetables_ending_datetime.
        #    Initially, the list of travel requests of these timetables is empty, and the departure_datetime and
        #    arrival_datetime values of the timetable_entries are based exclusively on the details of the bus_route.
        #    In the next steps of the algorithm, these timetables are used in the initial clustering
        #    of the travel requests.
        #
        timetable_generator.timetables = generate_initial_timetables(
            line_id=line_id,
            timetables_starting_datetime=timetables_starting_datetime,
            timetables_ending_datetime=timetables_ending_datetime,
            route_generator_response=timetable_generator.route_generator_response
        )

        # 6: (Initial Clustering) Each one of the retrieved travel_requests is corresponded to the timetable
        #    which produces the minimum_individual_waiting_time for the passenger. The waiting time is calculated
        #    as the difference between the departure_datetime of the travel_request and the departure_datetime of
        #    the timetable_entry from where the passenger departs from (identified by the
        #    'starting_timetable_entry_index' value).
        #
        correspond_travel_requests_to_timetables(
            travel_requests=timetable_generator.travel_requests,
            timetables=timetable_generator.timetables
        )

        # 7: (Handling of Undercrowded Timetables) After the initial clustering step, there might be timetables
        #    where the number of travel_requests is lower than the input: minimum_number_of_passengers_in_timetable.
        #    This is usual during night hours, where transportation demand is not so high. These timetables are
        #    removed from the list of generated timetables and each one of their travel_requests is corresponded
        #    to one of the remaining timetables, based on the individual_waiting_time of the passenger.
        #
        handle_undercrowded_timetables(timetables=timetable_generator.timetables)

        # 8: (Handling of Overcrowded Timetables) In addition, there might be timetables where the
        #    number_of_current_passengers is higher than the input: maximum_bus_capacity, which indicates that
        #    each one of these timetables cannot be served by one bus vehicle. For this reason, each one of these
        #    timetables should be divided into two timetables, and the corresponding travel_requests are partitioned.
        #    The whole procedure is repeated until there is no timetable where the number_of_current_passengers
        #    exceeds the maximum_bus_capacity.
        #
        #    The first step is to calculate the number_of_current_passengers in each one of the timetable_entries.
        #
        calculate_number_of_passengers_of_timetables(timetables=timetable_generator.timetables)
        handle_overcrowded_timetables(timetables=timetable_generator.timetables)

        # 9: (Adjust Departure Datetimes) At this point of processing, the number of travel_requests in each timetable
        #    is higher than the minimum_number_of_passengers_in_timetable and lower than the maximum_bus_capacity.
        #    So, the departure_datetime and arrival_datetime values of each timetable_entry are re-estimated,
        #    taking into consideration the departure_datetime values of the corresponding travel_requests.
        #    In each timetable and for each travel_request, the ideal departure_datetimes from all bus_stops
        #    (not only the bus stop from where the passenger desires to depart) are estimated. Then, the ideal
        #    departure_datetimes of the timetable, for each bus stop, correspond to the mean values of the ideal
        #    departure_datetimes of the corresponding travel_requests. Finally, starting from the initial bus_stop
        #    and combining the ideal departure_datetimes of each bus_stop and the required traveling time between
        #    bus_stops, included in the response of the Route Generator, the departure_datetimes of the
        #    timetable_entries are finalized.
        adjust_departure_datetimes_of_timetables(timetables=timetable_generator.timetables)

        # 10: (Individual Waiting Time) For each timetable, the individual_waiting_time of each passenger is calculated.
        #     For each one of the travel_requests where individual_waiting_time is higher than the
        #     input: individual_waiting_time_threshold, alternative existing timetables are investigated, based on the
        #     new individual_waiting_time, the average_waiting_time and the number_of_current_passengers of each
        #     timetable. For the travel_requests which cannot be served by the other existing timetables, if their
        #     number is greater or equal than the mini_number_of_passengers_in_timetable, then a new timetable is
        #     generated with departure_datetimes based on the ideal departure_datetimes of the
        #     aforementioned passengers.
        #
        handle_travel_requests_of_timetables_with_waiting_time_above_threshold(
            timetables=timetable_generator.timetables
        )
        calculate_number_of_passengers_of_timetables(timetables=timetable_generator.timetables)
        adjust_departure_datetimes_of_timetables(timetables=timetable_generator.timetables)

        # 11: (Average Waiting Time) For each timetable, the average_waiting_time of passengers is calculated.
        #     If the average waiting time is higher than the input: average-waiting-time-threshold, then the
        #     possibility of dividing the timetable is investigated. If the two new timetables have lower
        #     average_waiting_time than the initial one and both have more travel_requests than the
        #     minimum_number_of_passengers_in_timetable, then the initial timetable is divided, its travel_requests
        #     are partitioned, and the departure_datetime and arrival_datetime values of the timetable_entries of
        #     the new timetables, are estimated based on the departure_datetime values of the partitioned requests.
        #
        handle_timetables_with_average_waiting_time_above_threshold(timetables=timetable_generator.timetables)
        calculate_number_of_passengers_of_timetables(timetables=timetable_generator.timetables)
        adjust_departure_datetimes_of_timetables(timetables=timetable_generator.timetables)

        print_timetables(timetables=timetable_generator.timetables)

        # self.connection.insert_timetables(timetables=timetable_generator.timetables)

    def generate_timetables_for_bus_line_id(self, line_id, timetables_starting_datetime, timetables_ending_datetime,
                                            requests_min_departure_datetime, requests_max_departure_datetime):
        """
        Generate timetables for a bus_line, for a selected datetime period,
        evaluating travel_requests of a specific datetime period.

        :param line_id: int
        :param timetables_starting_datetime: datetime
        :param timetables_ending_datetime: datetime
        :param requests_min_departure_datetime: datetime
        :param requests_max_departure_datetime: datetime
        :return: None
        """

        # 1: The input: line_id is provided to the function, so as timetables for the corresponding
        #    bus_line to be generated. The Look Ahead retrieves from the System Database the bus_line
        #    which corresponds to the selected line_id.
        #
        # bus_line: {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        # bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        #
        bus_line = self.connection.find_bus_line(line_id=line_id)
        self.generate_timetables_for_bus_line(
            bus_line=bus_line,
            timetables_starting_datetime=timetables_starting_datetime,
            timetables_ending_datetime=timetables_ending_datetime,
            requests_min_departure_datetime=requests_min_departure_datetime,
            requests_max_departure_datetime=requests_max_departure_datetime
        )

    def generate_timetables_for_bus_lines(self, timetables_starting_datetime, timetables_ending_datetime,
                                          requests_min_departure_datetime, requests_max_departure_datetime):
        """
        Generate timetables for all bus_lines, for a selected datetime period,
        evaluating travel_requests of a specific datetime period.

        :param timetables_starting_datetime: datetime
        :param timetables_ending_datetime: datetime
        :param requests_min_departure_datetime: datetime
        :param requests_max_departure_datetime: datetime
        :return: None
        """
        bus_lines = self.connection.get_bus_lines_list()

        for bus_line in bus_lines:
            self.generate_timetables_for_bus_line(
                bus_line=bus_line,
                timetables_starting_datetime=timetables_starting_datetime,
                timetables_ending_datetime=timetables_ending_datetime,
                requests_min_departure_datetime=requests_min_departure_datetime,
                requests_max_departure_datetime=requests_max_departure_datetime
            )

    def update_timetables_of_bus_line(self, bus_line):
        """
        Update the timetables of a bus_line, taking into consideration the current levels of traffic_density.

        :param bus_line: {
                   '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        :return: None
        """
        line_id = bus_line.get('line_id')
        bus_stops = bus_line.get('bus_stops')
        timetables = self.connection.get_timetables_of_bus_line_list(line_id=line_id)

        timetable_updater = TimetableUpdater(bus_stops=bus_stops, timetables=timetables)

        update_timetables(
            timetables=timetable_updater.timetables,
            route_generator_response=timetable_updater.route_generator_response
        )
        # self.connection.insert_timetables(timetables=timetable_updater.timetables)

    def update_timetables_of_bus_line_id(self, line_id):
        """
        Update the timetables of a bus_line, taking into consideration the current levels of traffic_density.

        :param line_id: int
        :return: None
        """
        bus_line = self.connection.find_bus_line(line_id=line_id)
        self.update_timetables_of_bus_line(bus_line=bus_line)

    def update_timetables_of_bus_lines(self):
        """
        Update the timetables of all bus_lines, taking into consideration the current levels of traffic_density.

        :return: None
        """
        bus_lines = self.connection.get_bus_lines_list()

        for bus_line in bus_lines:
            self.update_timetables_of_bus_line(bus_line=bus_line)

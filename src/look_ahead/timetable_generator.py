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
        self.route_generator_response = get_route_between_multiple_bus_stops(bus_stops=bus_stops)


def add_ideal_departure_datetimes_of_travel_request(ideal_departure_datetimes_of_travel_request,
                                                    ideal_departure_datetimes_of_travel_requests):
    """
    Add each one of the items in the ideal_departure_datetimes_of_travel_request list, to the corresponding list
    of the ideal_departure_datetimes_of_travel_requests double list.

    :param ideal_departure_datetimes_of_travel_request: [departure_datetime]
    :param ideal_departure_datetimes_of_travel_requests: [[departure_datetime]]
    :return: None (Updates ideal_departure_datetimes)
    """
    for index in range(0, len(ideal_departure_datetimes_of_travel_request)):
        ideal_departure_datetime_of_travel_request = ideal_departure_datetimes_of_travel_request[index]
        ideal_departure_datetimes_of_travel_requests[index].append(ideal_departure_datetime_of_travel_request)


def add_timetable_to_timetables_sorted_by_starting_datetime(timetable, timetables):
    """
    Add a provided timetable to the timetables list, sorted by its starting_datetime.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :param timetables: [timetable]
    :return: None (Updates timetables)
    """
    number_of_timetables = len(timetables)
    index = number_of_timetables

    for i in range(0, number_of_timetables):
        current_timetable = timetables[i]

        starting_datetime_of_timetable = get_starting_datetime_of_timetable(timetable=timetable)
        starting_datetime_of_current_timetable = get_starting_datetime_of_timetable(timetable=current_timetable)

        if starting_datetime_of_timetable < starting_datetime_of_current_timetable:
            index = i
            break

    timetables.insert(index, timetable)


def add_travel_request_to_timetable(travel_request, timetable):
    """
    Add a travel_request to the list of travel_requests of a timetable.

    :param travel_request: {'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                            'departure_datetime', 'arrival_datetime',
                            'starting_timetable_entry_index', 'ending_timetable_entry_index'}

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :return: None (Updates timetable)
    """
    travel_requests_of_timetable = timetable.get('travel_requests')
    travel_requests_of_timetable.append(travel_request)


def adjust_departure_datetimes_of_timetable(timetable):
    """
    Adjust the departure datetimes of a timetable, taking into consideration
    the departure datetimes of its corresponding travel requests.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :return: None (Updates timetable)
    """
    ideal_departure_datetimes_of_travel_requests = [[]]
    travel_requests = timetable.get('travel_requests')
    timetable_entries = timetable.get('timetable_entries')
    # number_of_timetable_entries = len(timetable_entries)
    total_times = [timetable_entry.get('total_time') for timetable_entry in timetable_entries]

    for travel_request in travel_requests:
        ideal_departure_datetimes_of_travel_request = estimate_ideal_departure_datetimes_of_travel_request(
            travel_request=travel_request,
            total_times=total_times
        )
        add_ideal_departure_datetimes_of_travel_request(
            ideal_departure_datetimes_of_travel_request=ideal_departure_datetimes_of_travel_request,
            ideal_departure_datetimes_of_travel_requests=ideal_departure_datetimes_of_travel_requests
        )

    ideal_departure_datetimes = estimate_ideal_departure_datetimes(
        ideal_departure_datetimes_of_travel_requests=ideal_departure_datetimes_of_travel_requests
    )

    adjust_timetable_entries(timetable=timetable, ideal_departure_datetimes=ideal_departure_datetimes)


def adjust_departure_datetimes_of_timetables(timetables):
    """
    Adjust the departure datetimes of each one of the timetables, taking into consideration
    the departure datetimes of its corresponding travel requests.

    :param timetables: [{
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]

    :return: None (Updates timetables)
    """
    for timetable in timetables:
        adjust_departure_datetimes_of_timetable(timetable=timetable)


def adjust_timetable_entries(timetable, ideal_departure_datetimes):
    """
    Adjust the timetable entries, combining the ideal departure datetimes and
    the required traveling time from one bus stop to another.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

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
            departure_datetime = ceil_datetime_minutes(starting_datetime=ideal_starting_datetime)
        else:
            previous_departure_datetime = timetable_entries[i - 1].get('departure_datetime')
            departure_datetime = ceil_datetime_minutes(
                starting_datetime=previous_departure_datetime + timedelta(seconds=total_time)
            )

        arrival_datetime = departure_datetime + timedelta(seconds=total_time)
        timetable_entry['departure_datetime'] = departure_datetime
        timetable_entry['arrival_datetime'] = arrival_datetime


def calculate_average_waiting_time_of_timetable_in_seconds(timetable):
    """
    Calculate the average waiting time of a timetable in seconds.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :return: average_waiting_time_in_seconds (float)
    """
    timetable_entries = timetable.get('timetable_entries')
    travel_requests = timetable.get('travel_requests')
    number_of_passengers = len(travel_requests)
    total_waiting_time_in_seconds = 0

    for travel_request in travel_requests:
        waiting_time_of_travel_request_in_seconds = calculate_waiting_time_of_travel_request_in_seconds(
            timetable_entries=timetable_entries,
            travel_request=travel_request
        )
        total_waiting_time_in_seconds += waiting_time_of_travel_request_in_seconds

    average_waiting_time_in_seconds = total_waiting_time_in_seconds / number_of_passengers
    return average_waiting_time_in_seconds


def calculate_average_waiting_time_of_timetables_in_seconds(timetables):
    """
    Calculate the average waiting time of a list of timetables in seconds.

    :param timetables: [{
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]

    :return: average_waiting_time_in_seconds (float)
    """
    total_waiting_time_in_seconds = 0
    number_of_timetables = len(timetables)

    for timetable in timetables:
        total_waiting_time_in_seconds += calculate_average_waiting_time_of_timetable_in_seconds(timetable=timetable)

    average_waiting_time_in_seconds = total_waiting_time_in_seconds / number_of_timetables
    return average_waiting_time_in_seconds


def calculate_departure_datetime_differences_between_travel_request_and_timetables(travel_request, timetables):
    """
    Calculate the datetime difference between a travel request and a list of timetables.

    :param travel_request: {'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                            'departure_datetime', 'arrival_datetime',
                            'starting_timetable_entry_index', 'ending_timetable_entry_index'}

    :param timetables: [{
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]

    :return: departure_datetime_differences: [{
                 'timetable': {
                     '_id',
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
                         'starting_timetable_entry_index', 'ending_timetable_entry_index'}]},
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


def calculate_mean_departure_datetime(departure_datetimes):
    """
    Calculate the mean value of a list of departure_datetime values.

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


def calculate_number_of_passengers_of_timetable(timetable):
    """
    Calculate the number of onboarding, deboarding, and current passengers for each timetable entry,
    and update the corresponding values.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

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
        number_of_current_passengers = (previous_number_of_current_passengers -
                                        previous_number_of_deboarding_passengers +
                                        timetable_entry.get('number_of_boarding_passengers'))

        timetable_entry['number_of_current_passengers'] = number_of_current_passengers
        previous_number_of_current_passengers = number_of_current_passengers
        previous_number_of_deboarding_passengers = timetable_entry.get('number_of_deboarding_passengers')


def calculate_number_of_passengers_of_timetables(timetables):
    """
    Calculate the number of onboarding, deboarding, and current passengers for each timetable entry,
    and update the corresponding values in each one of timetables.

    :param timetables: [{
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]

    :return: None (Updates timetables)
    """
    for timetable in timetables:
        calculate_number_of_passengers_of_timetable(timetable=timetable)


def calculate_waiting_time_of_travel_request_in_seconds(timetable_entries, travel_request):
    """
    Calculate the waiting time (in seconds) of a travel request.

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
    waiting_time_in_seconds = datetime_to_seconds(provided_datetime=waiting_time_in_datetime)
    return waiting_time_in_seconds


def calculate_waiting_time_of_travel_requests_of_timetable(timetable):
    """
    Calculate the waiting time (in seconds) of each travel request of a timetable.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

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
        waiting_time = calculate_waiting_time_of_travel_request_in_seconds(
            timetable_entries=timetable_entries,
            travel_request=travel_request
        )
        dictionary_entry = {'travel_request': travel_request, 'waiting_time': waiting_time}
        waiting_time_of_travel_requests.append(dictionary_entry)

    return waiting_time_of_travel_requests


def ceil_datetime_minutes(starting_datetime):
    """
    Ceil the minutes of a datetime.

    :param starting_datetime: datetime
    :return: ending_datetime: datetime
    """
    ending_datetime = (starting_datetime - timedelta(microseconds=starting_datetime.microsecond) -
                       timedelta(seconds=starting_datetime.second) + timedelta(minutes=1))
    return ending_datetime


def check_number_of_passengers_of_timetable(timetable):
    """
    Check if the number of passengers of a timetable exceeds the bus vehicle capacity.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :return: True, if timetable can be served by one bus, otherwise False.
    """
    returned_value = True

    for timetable_entry in timetable.get('timetable_entries'):
        if timetable_entry.get('number_of_current_passengers') > maximum_bus_capacity:
            returned_value = False
            break

    return returned_value


def correspond_travel_requests_to_bus_stops(travel_requests, bus_stops):
    """
    The list of bus stops of a bus line might contain the same bus_stop_osm_ids more than once.
    For example, consider a bus line with bus stops [A, B, C, D, C, B, A].
    For this reason, a travel request from bus stop B to bus stop A needs to be related to
    bus_stops list indexes 5 and 6 respectively, not 2 and 6.
    This operation is achieved using this function, which adds the parameters 'starting_timetable_entry_index' and
    'ending_timetable_entry_index' to each travel_request.

    :param travel_requests: [{'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                              'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                              'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                              'departure_datetime', 'arrival_datetime',
                              'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

    :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]

    :return: None (Updates travel_requests)
    """
    bus_stop_osm_ids = [bus_stop.get('osm_id') for bus_stop in bus_stops]

    for travel_request in travel_requests:
        starting_bus_stop_osm_id = travel_request.get('starting_bus_stop').get('osm_id')
        starting_timetable_entry_index = get_bus_stop_index(
            bus_stop_osm_id=starting_bus_stop_osm_id,
            bus_stop_osm_ids=bus_stop_osm_ids,
            start=0
        )
        travel_request['starting_timetable_entry_index'] = starting_timetable_entry_index

        ending_bus_stop_osm_id = travel_request.get('ending_bus_stop').get('osm_id')
        ending_timetable_entry_index = get_bus_stop_index(
            bus_stop_osm_id=ending_bus_stop_osm_id,
            bus_stop_osm_ids=bus_stop_osm_ids,
            start=starting_timetable_entry_index + 1
        )
        travel_request['ending_timetable_entry_index'] = ending_timetable_entry_index


def correspond_travel_requests_to_timetables(travel_requests, timetables):
    """
    Correspond each travel request to a timetable, so as to produce
    the minimum waiting time for each passenger.

    :param travel_requests: [{'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                              'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                              'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                              'departure_datetime', 'arrival_datetime',
                              'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

    :param timetables: [{
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]

    :return: None (Updates timetables)
    """
    for travel_request in travel_requests:
        departure_datetime_differences = \
            calculate_departure_datetime_differences_between_travel_request_and_timetables(
                travel_request=travel_request,
                timetables=timetables
            )

        timetable_with_minimum_datetime_difference = get_timetable_with_minimum_departure_datetime_difference(
            departure_datetime_differences=departure_datetime_differences
        )

        add_travel_request_to_timetable(
            travel_request=travel_request,
            timetable=timetable_with_minimum_datetime_difference
        )


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


def estimate_ideal_departure_datetimes(ideal_departure_datetimes_of_travel_requests):
    """
    Process the ideal_departure_datetimes_of_travel_requests double list, which contains a list
    of ideal departure datetimes for each one of the timetable entries, calculate the mean value of each list,
    and return a list containing all of them.

    :param ideal_departure_datetimes_of_travel_requests: [[departure_datetime]]
    :return: ideal_departure_datetimes: [departure_datetime]
    """
    ideal_departure_datetimes = []

    for corresponding_departure_datetimes in ideal_departure_datetimes_of_travel_requests:
        ideal_departure_datetime = calculate_mean_departure_datetime(
            departure_datetimes=corresponding_departure_datetimes
        )
        ideal_departure_datetimes.append(ideal_departure_datetime)

    return ideal_departure_datetimes


def estimate_ideal_departure_datetimes_of_travel_request(travel_request, total_times):
    """
    Estimate the ideal departure datetime of a travel request, from all timetable entries.
    Initially, only the departure datetime from the corresponding starting timetable entry is known.
    Using the required traveling times from bus stop to bus stop (total_times), it is possible to
    estimate the ideal departure datetimes from all timetable entries.

    :param travel_request: {
               '_id', 'travel_request_id, 'client_id', 'bus_line_id',
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'departure_datetime', 'arrival_datetime',
               'starting_timetable_entry_index', 'ending_timetable_entry_index'}
    :param total_times: [float] (in seconds)
    :return: ideal_departure_datetimes: [departure_datetime]
    """
    ideal_departure_datetimes = []
    number_of_timetable_entries = len(total_times)

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


def generate_initial_timetables(timetables_starting_datetime, timetables_ending_datetime):
    """

    :param timetables_starting_datetime: datetime
    :param timetables_ending_datetime: datetime

    :return timetables: [{
                '_id',
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
                    'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]
    """
    timetables = []
    current_datetime = timetables_starting_datetime

    while current_datetime < timetables_ending_datetime:
        timetable = generate_new_timetable(timetable_starting_datetime=current_datetime)
        timetables.append(timetable)
        current_datetime = timetable.get('ending_datetime')

    return timetables


def generate_new_timetable(timetable_starting_datetime, route_generator_response):
    """
    Generate a timetable starting from a provided datetime.

    :param timetable_starting_datetime: datetime

    :param route_generator_response: [{
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                         'distances_from_starting_node', 'times_from_starting_node',
                         'distances_from_previous_node', 'times_from_previous_node'}}]

    :return: timetable: {
                 '_id',
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
                     'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}
    """
    current_datetime = timetable_starting_datetime
    timetable = {'timetable_entries': [], 'travel_requests': [], 'average_waiting_time': 0}

    for intermediate_response in route_generator_response:
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

    return timetable


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


def get_ending_datetime_of_timetable(timetable):
    """
    Get the ending_datetime of a timetable, which corresponds to
    the arrival_datetime of the last timetable entry.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :return: None (Updates timetable)
    """
    timetable_entries = timetable.get('timetable_entries')
    ending_timetable_entry = timetable_entries[len(timetable_entries) - 1]
    ending_datetime_of_timetable = ending_timetable_entry.get('arrival_datetime')
    return ending_datetime_of_timetable


def get_overcrowded_timetables(timetables):
    """
    Get the timetables with number of passengers which exceeds the bus vehicle capacity.

    :param timetables: [{
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]

    :return: overcrowded_timetables (list)
    """
    overcrowded_timetables = []

    for timetable in timetables:
        if not check_number_of_passengers_of_timetable(timetable=timetable):
            overcrowded_timetables.append(timetable)

    return overcrowded_timetables


def get_starting_datetime_of_timetable(timetable):
    """
    Get the starting_datetime of a timetable, which corresponds to
    the departure_datetime of the first timetable entry.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :return: starting_datetime_of_timetable: datetime
    """
    timetable_entries = timetable.get('timetable_entries')
    starting_timetable_entry = timetable_entries[0]
    starting_datetime_of_timetable = starting_timetable_entry.get('departure_datetime')
    return starting_datetime_of_timetable


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


def handle_overcrowded_timetables(timetables):
    """

    :param timetables: [{
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]

    :return:
    """
    overcrowded_timetables = get_overcrowded_timetables(timetables=timetables)

    while len(overcrowded_timetables) > 0:

        for overcrowded_timetable in overcrowded_timetables:
            additional_timetable = split_timetable(timetable=overcrowded_timetable)
            add_timetable_to_timetables_sorted_by_starting_datetime(timetable=additional_timetable)

        overcrowded_timetables = get_overcrowded_timetables(timetables=timetables)


def retrieve_travel_requests_with_waiting_time_above_time_limit(timetable, waiting_time_limit):
    """

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

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
    waiting_time_of_travel_requests = calculate_waiting_time_of_travel_requests_of_timetable(
        timetable=timetable
    )

    for dictionary_entry in waiting_time_of_travel_requests:
        waiting_time = dictionary_entry.get('waiting_time')

        if waiting_time > waiting_time_limit:
            travel_requests_with_waiting_time_above_time_limit.append(dictionary_entry)

    return travel_requests_with_waiting_time_above_time_limit


def split_timetable(timetable):
    """
    Create a copy of the initial timetable, split the requests of the initial timetable into the two timetables,
    adjust the departure_datetimes of both timetables, and return the new timetable.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :return: additional_timetable
    """
    additional_timetable = timetable.copy()
    travel_requests = list(timetable.get('travel_requests'))

    timetable['travel_requests'] = []
    additional_timetable['travel_requests'] = []

    timetables = [timetable, additional_timetable]
    split_travel_requests_in_timetables(travel_requests=travel_requests, timetables=timetables)
    adjust_departure_datetimes_of_timetables(timetables=timetables)

    return additional_timetable


def split_travel_requests_in_timetables(travel_requests, timetables):
    """
    Split a list of travel_requests in two timetables, and update their corresponding entries.

    :param travel_requests: [{'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                              'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                              'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                              'departure_datetime', 'arrival_datetime',
                              'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

    :param timetables: [{
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]

    :return: None (Updates timetables)
    """
    travel_requests_lists = split_travel_requests_by_departure_datetime(travel_requests=travel_requests)
    timetables[0]['travel_requests'] = travel_requests_lists[0]
    timetables[1]['travel_requests'] = travel_requests_lists[1]


def split_travel_requests_by_departure_datetime(travel_requests):
    """
    Split a list of travel_requests into two lists, based on their departure_datetime values,
    and return a double list containing both of them.

    :param travel_requests: [{
               '_id', 'travel_request_id, 'client_id', 'bus_line_id',
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'departure_datetime', 'arrival_datetime',
               'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

    :return: travel_requests_lists: [[{
                 '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                 'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                 'departure_datetime', 'arrival_datetime',
                 'starting_timetable_entry_index', 'ending_timetable_entry_index'}]]
    """
    travel_requests_lists = [[]]

    starting_timetable_entry_dictionary = get_starting_timetable_entry_dictionary(
        travel_requests=travel_requests
    )

    for corresponding_travel_requests_list in starting_timetable_entry_dictionary.itervalues():
        double_list = split_travel_requests_list(travel_requests=corresponding_travel_requests_list)
        travel_requests_lists[0].extend(double_list[0])
        travel_requests_lists[1].extend(double_list[1])

    return travel_requests_lists


def get_starting_timetable_entry_dictionary(travel_requests):
    """
    Create a dictionary containing the starting_timetable_entry_index as key,
    and a list of corresponding_travel_requests as value.

    :param travel_requests: [{
               '_id', 'travel_request_id, 'client_id', 'bus_line_id',
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'departure_datetime', 'arrival_datetime',
               'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

    :return: starting_timetable_entry_dictionary: {starting_timetable_entry_index: corresponding_travel_requests}
    """
    starting_timetable_entry_dictionary = {}

    for travel_request in travel_requests:
        starting_timetable_entry_index = travel_request.get('starting_timetable_entry_index')

        if starting_timetable_entry_index not in starting_timetable_entry_dictionary:
            starting_timetable_entry_dictionary[starting_timetable_entry_index] = []

        corresponding_travel_requests = starting_timetable_entry_dictionary.get(starting_timetable_entry_index)

        add_travel_request_sorted_by_departure_datetime(
            travel_request=travel_request,
            travel_requests=corresponding_travel_requests
        )

    return starting_timetable_entry_dictionary


def split_travel_requests_list(travel_requests):
    """
    Split a list of travel_requests into two lists, and return a double list containing both of them.

    :param travel_requests: [{
               '_id', 'travel_request_id, 'client_id', 'bus_line_id',
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'departure_datetime', 'arrival_datetime',
               'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

    :return: travel_requests_lists: [[{
                 '_id', 'travel_request_id, 'client_id', 'bus_line_id',
                 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                 'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                 'departure_datetime', 'arrival_datetime',
                 'starting_timetable_entry_index', 'ending_timetable_entry_index'}]]
    """
    travel_requests_lists = []
    number_of_travel_requests = len(travel_requests)
    half_number_of_travel_requests = number_of_travel_requests / 2

    travel_requests_lists[0] = travel_requests[0:half_number_of_travel_requests]
    travel_requests_lists[1] = travel_requests[half_number_of_travel_requests, number_of_travel_requests]

    return travel_requests_lists


def add_travel_request_sorted_by_departure_datetime(travel_request, travel_requests):
    """
    Add a travel_request to the corresponding index position of the travel_requests list,
    so as to keep the list sorted by the departure_datetime value.

    :param travel_request: {
               '_id', 'travel_request_id, 'client_id', 'bus_line_id',
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'departure_datetime', 'arrival_datetime',
               'starting_timetable_entry_index', 'ending_timetable_entry_index'}

    :param travel_requests: [{
               '_id', 'travel_request_id, 'client_id', 'bus_line_id',
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'departure_datetime', 'arrival_datetime',
               'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

    :return: None (Updates travel_requests)
    """
    departure_datetime_of_travel_request = travel_request.get('departure_datetime')
    insertion_index = 0

    for current_travel_request in travel_requests:
        current_departure_datetime = current_travel_request.get('departure_datetime')

        if departure_datetime_of_travel_request < current_departure_datetime:
            break
        else:
            insertion_index += 1

    travel_requests.insert(insertion_index, travel_request)


def check_average_waiting_time_of_timetable(timetable):
    """

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :return:
    """
    travel_requests = timetable.get('travel_requests')
    number_of_travel_requests = len(travel_requests)

    average_waiting_time_in_seconds = calculate_average_waiting_time_of_timetable_in_seconds(timetable=timetable)

    if average_waiting_time_in_seconds > average_waiting_time_threshold \
            and 2 * number_of_travel_requests > minimum_number_of_passengers_in_timetable:
        print 'hello'


def check_individual_waiting_of_timetable(timetable):
    """

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :return:
    """
    travel_requests_with_waiting_time_above_threshold = []
    timetable_entries = timetable.get('timetable_entries')
    travel_requests = timetable.get('travel_requests')

    for travel_request in travel_requests:
        waiting_time_of_travel_request = calculate_waiting_time_of_travel_request_in_seconds(
            timetable_entries=timetable_entries,
            travel_request=travel_request
        )

        if waiting_time_of_travel_request > individual_waiting_time_threshold:
            waiting_time_entry = {'travel_request': travel_request, 'waiting_time': waiting_time_of_travel_request}
            travel_requests_with_waiting_time_above_threshold.append(waiting_time_entry)

    number_of_travel_requests_with_waiting_time_above_threshold = len(
        travel_requests_with_waiting_time_above_threshold
    )

    if number_of_travel_requests_with_waiting_time_above_threshold >= minimum_number_of_passengers_in_timetable:
        print 'hello'


def generate_new_timetable_for_travel_requests(timetable, travel_requests):
    """
    Create a copy of the initial timetable, set the travel_requests, adjust the departure_datetimes
    based on the travel_requests, and return the new timetable.

    :param timetable: {
               '_id',
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
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :param travel_requests: [{
               '_id', 'travel_request_id, 'client_id', 'bus_line_id',
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'departure_datetime', 'arrival_datetime',
               'starting_timetable_entry_index', 'ending_timetable_entry_index'}]

    :return: additional_timetable
    """
    additional_timetable = timetable.copy()
    additional_timetable['travel_requests'] = travel_requests
    adjust_departure_datetimes_of_timetable(timetable=additional_timetable)
    return additional_timetable

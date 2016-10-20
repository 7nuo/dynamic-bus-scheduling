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
from src.common.variables import maximum_bus_capacity, average_waiting_time_threshold, \
    individual_waiting_time_threshold, minimum_number_of_passengers_in_timetable
from src.route_generator.route_generator_client import get_route_between_multiple_bus_stops
from datetime import datetime, timedelta, time


class TimetableGenerator(object):
    def __init__(self, line_id, bus_stops, travel_requests):
        """
        Initialize the TimetableGenerator, send a request to the RouteGenerator and receive the less time-consuming
        route which connects the provided bus stops.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        timetable_document: {
            '_id', 'line_id',
            'timetable_entries': [{
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                'number_of_deboarding_passengers', 'number_of_current_passengers'}],
            'travel_requests': [{
                '_id', 'client_id', 'line_id',
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime',
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
        }
        route_generator_response: [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                      'distances_from_starting_node', 'times_from_starting_node',
                      'distances_from_previous_node', 'times_from_previous_node'}
        }]
        :param line_id: int
        :param bus_stops: [bus_stop_document]
        :param travel_requests: [travel_request_document]
        :return: None
        """
        self.timetables = []
        self.line_id = line_id
        self.bus_stops = bus_stops
        self.travel_requests = travel_requests
        self.route_generator_response = get_route_between_multiple_bus_stops(bus_stops=bus_stops)


def add_ideal_departure_datetimes_of_travel_request(ideal_departure_datetimes_of_travel_request,
                                                    ideal_departure_datetimes_of_travel_requests):
    """
    Add each one of the items in the ideal_departure_datetimes_of_travel_request list, to the
    corresponding list of the ideal_departure_datetimes_of_travel_requests double list.

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

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    number_of_timetables = len(timetables)
    insertion_index = number_of_timetables

    for i in range(0, number_of_timetables):
        current_timetable = timetables[i]
        starting_datetime_of_new_timetable = get_starting_datetime_of_timetable(timetable=timetable)
        starting_datetime_of_current_timetable = get_starting_datetime_of_timetable(timetable=current_timetable)

        if starting_datetime_of_new_timetable < starting_datetime_of_current_timetable:
            insertion_index = i
            break

    timetables.insert(insertion_index, timetable)


def add_travel_request_sorted_by_departure_datetime(travel_request, travel_requests):
    """
    Add a travel_request to the corresponding index position of the travel_requests list,
    so as to keep the list sorted by the departure_datetime value.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    :param travel_request: travel_request_document
    :param travel_requests: [travel_request_document]
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


def add_travel_request_to_timetable_with_adjustments(travel_request, timetable):
    """
    Add a travel_request to the list of travel_requests of a timetable, adjusting the timetable_entries.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param travel_request: travel_request_document
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    add_travel_request_to_timetable_without_adjustments(travel_request=travel_request, timetable=timetable)
    adjust_departure_datetimes_of_timetable(timetable=timetable)
    calculate_number_of_passengers_of_timetable(timetable=timetable)


def add_travel_request_to_timetable_without_adjustments(travel_request, timetable):
    """
    Add a travel_request to the list of travel_requests of a timetable, without adjusting the timetable_entries.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param travel_request: travel_request_document
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    travel_requests = timetable.get('travel_requests')
    travel_requests.append(travel_request)


def adjust_departure_datetimes_of_timetable(timetable):
    """
    Adjust the departure datetimes of a timetable, taking into consideration
    the departure datetimes of its corresponding travel requests.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    travel_requests = timetable.get('travel_requests')
    timetable_entries = timetable.get('timetable_entries')
    total_times = [timetable_entry.get('total_time') for timetable_entry in timetable_entries]

    ideal_departure_datetimes_of_travel_requests = [
        [timetable_entry.get('departure_datetime')] for timetable_entry in timetable_entries
    ]

    for travel_request in travel_requests:
        if travel_request == 'ending_bus_stop':
            print travel_requests
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

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    for timetable in timetables:
        adjust_departure_datetimes_of_timetable(timetable=timetable)


def adjust_timetable_entries(timetable, ideal_departure_datetimes):
    """
    Adjust the timetable entries, combining the ideal departure datetimes and
    the required traveling time from one bus stop to another.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :param ideal_departure_datetimes: [datetime]
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


def calculate_average_number_of_travel_requests_in_timetables(timetables):
    """
    Calculate the average number of travel_requests in timetables.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: average_number_of_travel_requests: float
    """
    average_number_of_travel_requests = 0
    number_of_timetables = len(timetables)

    if number_of_timetables > 0:
        total_number_of_travel_requests = calculate_total_number_of_travel_requests_in_timetables(
            timetables=timetables
        )
        average_number_of_travel_requests = total_number_of_travel_requests / number_of_timetables

    return average_number_of_travel_requests


def calculate_average_waiting_time_of_timetable_in_seconds(timetable):
    """
    Calculate the average waiting time of a timetable in seconds.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: average_waiting_time_in_seconds (float)
    """
    timetable_entries = timetable.get('timetable_entries')
    travel_requests = timetable.get('travel_requests')
    number_of_passengers = len(travel_requests)
    total_waiting_time_in_seconds = 0

    for travel_request in travel_requests:
        waiting_time_of_travel_request_in_seconds = calculate_waiting_time_of_travel_request_in_seconds(
            travel_request=travel_request,
            timetable_entries=timetable_entries
        )
        total_waiting_time_in_seconds += waiting_time_of_travel_request_in_seconds

    average_waiting_time_in_seconds = total_waiting_time_in_seconds / number_of_passengers
    return average_waiting_time_in_seconds


def calculate_average_waiting_time_of_timetables_in_seconds(timetables):
    """
    Calculate the average waiting time of a list of timetables in seconds.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: average_waiting_time_in_seconds (float)
    """
    average_waiting_time_in_seconds = -1
    total_waiting_time_in_seconds = 0
    number_of_timetables = len(timetables)

    if number_of_timetables > 0:
        for timetable in timetables:
            total_waiting_time_in_seconds += calculate_average_waiting_time_of_timetable_in_seconds(
                timetable=timetable
            )
        average_waiting_time_in_seconds = total_waiting_time_in_seconds / number_of_timetables

    return average_waiting_time_in_seconds


def calculate_departure_datetime_differences_between_travel_request_and_timetables(travel_request, timetables):
    """
    Calculate the datetime difference between a travel request and a list of timetables.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param travel_request: timetable_document
    :param timetables: [timetable_document]
    :return: departure_datetime_differences: [{
                 'timetable': timetable_document, 'departure_datetime_difference': float (in seconds)}]
    """
    departure_datetime_differences = []
    # starting_timetable_entry_index corresponds to the timetable_entry from where the passenger departs from.
    starting_timetable_entry_index = travel_request.get('starting_timetable_entry_index')

    for timetable in timetables:
        timetable_entries = timetable.get('timetable_entries')
        corresponding_timetable_entry = timetable_entries[starting_timetable_entry_index]

        departure_datetime_of_travel_request_in_seconds = datetime_to_seconds(
            provided_datetime=travel_request.get('departure_datetime')
        )
        departure_datetime_of_timetable_entry_in_seconds = datetime_to_seconds(
            provided_datetime=corresponding_timetable_entry.get('departure_datetime')
        )
        departure_datetime_difference = abs(departure_datetime_of_travel_request_in_seconds -
                                            departure_datetime_of_timetable_entry_in_seconds)

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

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    clear_number_of_passengers_of_timetable(timetable=timetable)
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
                                        timetable_entry.get('number_of_onboarding_passengers'))

        timetable_entry['number_of_current_passengers'] = number_of_current_passengers
        previous_number_of_current_passengers = number_of_current_passengers
        previous_number_of_deboarding_passengers = timetable_entry.get('number_of_deboarding_passengers')


def calculate_number_of_passengers_of_timetables(timetables):
    """
    Calculate the number of onboarding, deboarding, and current passengers for each timetable entry,
    and update the corresponding values in each one of timetables.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    for timetable in timetables:
        calculate_number_of_passengers_of_timetable(timetable=timetable)


def calculate_total_number_of_travel_requests_in_timetables(timetables):
    """
    Calculate the total number of travel_requests in timetables.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: total_number_of_travel_requests: int
    """
    total_number_of_travel_requests = 0

    for timetable in timetables:
        travel_requests = timetable.get('travel_requests')
        number_of_travel_requests_of_timetable = len(travel_requests)
        total_number_of_travel_requests += number_of_travel_requests_of_timetable

    return total_number_of_travel_requests


def calculate_waiting_time_of_travel_request_in_seconds(travel_request, timetable_entries):
    """
    Calculate the waiting time (in seconds) of a travel request.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    :param travel_request: travel_request_document

    :param timetable_entries: [{
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
               'number_of_deboarding_passengers', 'number_of_current_passengers'}]

    :return: waiting_time_in_seconds (float)
    """
    departure_datetime_of_travel_request = travel_request.get('departure_datetime')
    departure_datetime_of_travel_request_in_seconds = datetime_to_seconds(
        provided_datetime=departure_datetime_of_travel_request
    )
    starting_timetable_entry_index = travel_request.get('starting_timetable_entry_index')
    corresponding_timetable_entry = timetable_entries[starting_timetable_entry_index]
    departure_datetime_of_timetable = corresponding_timetable_entry.get('departure_datetime')
    departure_datetime_of_timetable_in_seconds = datetime_to_seconds(
        provided_datetime=departure_datetime_of_timetable
    )
    waiting_time_in_seconds = abs(departure_datetime_of_timetable_in_seconds -
                                  departure_datetime_of_travel_request_in_seconds)

    return waiting_time_in_seconds


def calculate_waiting_time_of_travel_requests_of_timetable(timetable):
    """
    Calculate the waiting time (in seconds) of each travel request of a timetable.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: waiting_time_of_travel_requests: [{
                 'travel_request': travel_request_document, 'waiting_time': float (in seconds)}]
    """
    timetable_entries = timetable.get('timetable_entries')
    travel_requests = timetable.get('travel_requests')
    waiting_time_of_travel_requests = []

    for travel_request in travel_requests:
        waiting_time = calculate_waiting_time_of_travel_request_in_seconds(
            travel_request=travel_request,
            timetable_entries=timetable_entries
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


def check_average_waiting_time_of_timetable(timetable):
    """
    Check if the average_waiting_time_of_timetable exceeds the average_waiting_time_threshold.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: False if the average_waiting_time_of_timetable exceeds the average_waiting_time_threshold. Otherwise True.
    """
    check = True
    average_waiting_time_in_seconds = calculate_average_waiting_time_of_timetable_in_seconds(timetable=timetable)

    if average_waiting_time_in_seconds > average_waiting_time_threshold:
        check = False

    return check


def check_number_of_passengers_of_timetable(timetable):
    """
    Check if the number of passengers of a timetable exceeds the bus vehicle capacity.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: True, if timetable can be served by one bus, otherwise False.
    """
    check = True
    timetable_entries = timetable.get('timetable_entries')

    for timetable_entry in timetable_entries:
        if timetable_entry.get('number_of_current_passengers') > maximum_bus_capacity:
            check = False
            break

    return check


def clear_number_of_passengers_of_timetable(timetable):
    """
    Clear the number of passengers of a timetable.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    timetable_entries = timetable.get('timetable_entries')

    for timetable_entry in timetable_entries:
        timetable_entry['number_of_onboarding_passengers'] = 0
        timetable_entry['number_of_deboarding_passengers'] = 0
        timetable_entry['number_of_current_passengers'] = 0


def clear_travel_requests_of_timetable(timetable):
    """
    Clear the travel_requests of a timetable.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    timetable['travel_requests'] = []
    clear_number_of_passengers_of_timetable(timetable=timetable)


def clear_travel_requests_of_timetables(timetables):
    """
    Clear the travel_requests of multiple timetables.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    for timetable in timetables:
        clear_travel_requests_of_timetable(timetable=timetable)


def correspond_travel_requests_to_bus_stops(travel_requests, bus_stops):
    """
    The list of bus stops of a bus line might contain the same bus_stop_osm_ids more than once.
    For example, consider a bus line with bus stops [A, B, C, D, C, B, A].
    For this reason, a travel request from bus stop B to bus stop A needs to be related to
    bus_stops list indexes 5 and 6 respectively, not 2 and 6.
    This operation is achieved using this function, which adds the parameters 'starting_timetable_entry_index' and
    'ending_timetable_entry_index' to each travel_request.
    
    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

    :param travel_requests: [travel_request_document]
    :param bus_stops: [bus_stop_document]
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
        ) - 1
        travel_request['ending_timetable_entry_index'] = ending_timetable_entry_index


def correspond_travel_requests_to_timetables(travel_requests, timetables):
    """
    Correspond each travel request to a timetable, so as to produce
    the minimum waiting time for each passenger.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param travel_requests: [travel_request_document]
    :param timetables: [timetable_document]
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

        add_travel_request_to_timetable_without_adjustments(
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


def divide_timetable(timetable):
    """
    Create a copy of the initial timetable, split the requests of the initial timetable into the two timetables,
    adjust the departure_datetimes of both timetables, and return the new timetable.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: additional_timetable
    """
    additional_timetable = generate_additional_timetable(timetable=timetable)
    travel_requests = list(timetable.get('travel_requests'))
    timetable['travel_requests'] = []

    timetables = [timetable, additional_timetable]
    partition_travel_requests_in_timetables(travel_requests=travel_requests, timetables=timetables)
    adjust_departure_datetimes_of_timetables(timetables=timetables)
    calculate_number_of_passengers_of_timetables(timetables=timetables)

    # timetable['travel_requests'] = []
    # additional_timetable['travel_requests'] = []
    # correspond_travel_requests_to_timetables(travel_requests=travel_requests, timetables=timetables)
    # adjust_departure_datetimes_of_timetables(timetables=timetables)
    # calculate_number_of_passengers_of_timetables(timetables=timetables)

    return additional_timetable


def divide_timetable_based_on_average_waiting_time(timetable):
    """
    Check if a timetable should be divided, based on the number of travel requests and the average_waiting_time
    of the old and the two new timetables.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: additional_timetable if the timetable was divided, otherwise None.
    """
    initial_travel_requests = list(timetable.get('travel_requests'))

    if len(initial_travel_requests) < 2 * minimum_number_of_passengers_in_timetable:
        return None

    initial_timetable_entries = list(timetable.get('timetable_entries'))
    initial_average_waiting_time = calculate_average_waiting_time_of_timetable_in_seconds(timetable=timetable)

    additional_timetable = divide_timetable(timetable=timetable)
    new_average_waiting_time = calculate_average_waiting_time_of_timetable_in_seconds(timetable=timetable)
    additional_timetable_average_waiting_time = calculate_average_waiting_time_of_timetable_in_seconds(
        timetable=additional_timetable
    )

    # if (new_average_waiting_time + additional_timetable_average_waiting_time) / 2 > initial_average_waiting_time:
    #     timetable['timetable_entries'] = initial_timetable_entries
    #     timetable['travel_requests'] = initial_travel_requests
    #     return None

    if (new_average_waiting_time > initial_average_waiting_time or
                additional_timetable_average_waiting_time > initial_average_waiting_time):
        timetable['timetable_entries'] = initial_timetable_entries
        timetable['travel_requests'] = initial_travel_requests
        return None

    adjust_departure_datetimes_of_timetables(timetables=[timetable, additional_timetable])
    return additional_timetable


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

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    :param travel_request: travel_request_document
    :param total_times: [float] (in seconds)
    :return: ideal_departure_datetimes: [departure_datetime]
    """
    number_of_timetable_entries = len(total_times)
    ideal_departure_datetimes = [None for i in range(number_of_timetable_entries)]

    starting_timetable_entry_index = travel_request.get('starting_timetable_entry_index')
    departure_datetime = travel_request.get('departure_datetime')

    ideal_departure_datetimes[starting_timetable_entry_index] = departure_datetime

    # Estimate ideal departure_datetimes before departure_datetime
    index = starting_timetable_entry_index - 1
    ideal_departure_datetime = departure_datetime

    while index > -1:
        corresponding_total_time = total_times[index]
        ideal_departure_datetime -= timedelta(seconds=corresponding_total_time)
        ideal_departure_datetimes[index] = ideal_departure_datetime
        index -= 1

    # Estimate ideal departure_datetimes after departure_datetime
    index = starting_timetable_entry_index
    ideal_departure_datetime = departure_datetime

    while index < number_of_timetable_entries:
        corresponding_total_time = total_times[index]
        ideal_departure_datetime += timedelta(seconds=corresponding_total_time)
        ideal_departure_datetimes[index] = ideal_departure_datetime
        index += 1

    for i in ideal_departure_datetimes:
        if i is None:
            print ideal_departure_datetimes

    return ideal_departure_datetimes


def generate_additional_timetable(timetable):
    """
    Generate an additional timetable, copying the timetable_entries of an existing one.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: additional_timetable
    """
    line_id = timetable.get('line_id')
    timetable_entries = timetable.get('timetable_entries')
    additional_timetable = {'line_id': line_id, 'timetable_entries': [], 'travel_requests': []}

    for timetable_entry in timetable_entries:
        additional_timetable_entry = {
            'starting_bus_stop': timetable_entry.get('starting_bus_stop'),
            'ending_bus_stop': timetable_entry.get('ending_bus_stop'),
            'departure_datetime': timetable_entry.get('departure_datetime'),
            'arrival_datetime': timetable_entry.get('arrival_datetime'),
            'total_time': timetable_entry.get('total_time'),
            'number_of_onboarding_passengers': 0,
            'number_of_deboarding_passengers': 0,
            'number_of_current_passengers': 0
        }
        additional_timetable['timetable_entries'].append(additional_timetable_entry)

    return additional_timetable


def generate_additional_timetables(timetables):
    """

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: additional_timetables
    """
    additional_timetables = []

    for timetable in timetables:
        additional_timetable = generate_additional_timetable(timetable=timetable)
        additional_timetables.append(additional_timetable)

    return additional_timetables


def generate_initial_timetables(line_id, timetables_starting_datetime, timetables_ending_datetime,
                                route_generator_response):
    """

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param line_id: int
    :param timetables_starting_datetime: datetime
    :param timetables_ending_datetime: datetime

    :param route_generator_response: [{
           'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
           'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
           'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                     'distances_from_starting_node', 'times_from_starting_node',
                     'distances_from_previous_node', 'times_from_previous_node'}}]

    :return timetables: [timetable_document]
    """
    timetables = []
    current_datetime = timetables_starting_datetime

    while current_datetime < timetables_ending_datetime:
        timetable = generate_new_timetable(
            line_id=line_id,
            timetable_starting_datetime=current_datetime,
            route_generator_response=route_generator_response
        )
        timetables.append(timetable)
        current_datetime = get_ending_datetime_of_timetable(timetable=timetable)

    return timetables


def generate_new_timetable(line_id, timetable_starting_datetime, route_generator_response):
    """
    Generate a timetable starting from a provided datetime.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param line_id: int
    :param timetable_starting_datetime: datetime

    :param route_generator_response: [{
           'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
           'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
           'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                     'distances_from_starting_node', 'times_from_starting_node',
                     'distances_from_previous_node', 'times_from_previous_node'}}]

    :return: timetable: timetable_document
    """
    current_datetime = timetable_starting_datetime
    timetable = {'line_id': line_id, 'timetable_entries': [], 'travel_requests': []}

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


def generate_new_timetable_for_travel_requests(timetable, travel_requests):
    """
    Create a copy of the initial timetable, set the travel_requests, adjust the departure_datetimes
    based on the travel_requests, calculate the number of passengers, and return the new timetable.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    :param timetable: timetable_document
    :param travel_requests: [travel_request_document]
    :return: additional_timetable
    """
    additional_timetable = generate_additional_timetable(timetable=timetable)
    additional_timetable['travel_requests'] = travel_requests
    adjust_departure_datetimes_of_timetable(timetable=additional_timetable)
    calculate_number_of_passengers_of_timetable(timetable=additional_timetable)
    return additional_timetable


def get_bus_stop_index(bus_stop_osm_id, bus_stop_osm_ids, start):
    """

    :param bus_stop_osm_id: int
    :param bus_stop_osm_ids: [int]
    :param start: int
    :return: bus_stop_index: int
    """
    bus_stop_index = -1

    for i in range(start, len(bus_stop_osm_ids)):
        if bus_stop_osm_ids[i] == bus_stop_osm_id:
            bus_stop_index = i
            break

    return bus_stop_index


def get_ending_datetime_of_timetable(timetable):
    """
    Get the ending_datetime of a timetable, which corresponds to
    the arrival_datetime of the last timetable entry.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    timetable_entries = timetable.get('timetable_entries')
    ending_timetable_entry = timetable_entries[len(timetable_entries) - 1]
    ending_datetime_of_timetable = ending_timetable_entry.get('arrival_datetime')
    return ending_datetime_of_timetable


def get_overcrowded_timetables(timetables):
    """
    Get the timetables with number of passengers which exceeds the bus vehicle capacity.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: overcrowded_timetables: [timetable_document]
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

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :return: starting_datetime_of_timetable: datetime
    """
    timetable_entries = timetable.get('timetable_entries')
    starting_timetable_entry = timetable_entries[0]
    starting_datetime_of_timetable = starting_timetable_entry.get('departure_datetime')
    return starting_datetime_of_timetable


def get_starting_datetimes_of_timetables(timetables):
    """
    Retrieve a list containing the starting_datetimes of timetables.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: starting_datetimes: datetime
    """
    starting_datetimes = []

    for timetable in timetables:
        starting_datetime = get_starting_datetime_of_timetable(timetable=timetable)
        starting_datetimes.append(starting_datetime)

    return starting_datetimes


def get_starting_timetable_entry_dictionary(travel_requests):
    """
    Create a dictionary containing the starting_timetable_entry_index as key,
    and a list of corresponding_travel_requests as value.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    :param travel_requests: [travel_request_document]
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


def get_timetable_with_minimum_departure_datetime_difference(departure_datetime_differences):
    """
    Get the timetable with the minimum departure_datetime difference.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param departure_datetime_differences: [{
                 'timetable': timetable_document, 'departure_datetime_difference': float (in seconds)}]

    :return: timetable_with_min_departure_datetime_difference: timetable_document
    """
    # minimum_datetime_difference is initialized with a big datetime value.
    min_departure_datetime_difference = 356 * 86400
    timetable_with_min_departure_datetime_difference = None

    for departure_datetime_difference_entry in departure_datetime_differences:
        timetable = departure_datetime_difference_entry.get('timetable')
        departure_datetime_difference = departure_datetime_difference_entry.get('departure_datetime_difference')

        if departure_datetime_difference < min_departure_datetime_difference:
            min_departure_datetime_difference = departure_datetime_difference
            timetable_with_min_departure_datetime_difference = timetable

    return timetable_with_min_departure_datetime_difference


def get_timetables_with_average_waiting_time_above_threshold(timetables):
    """
    Retrieve a list containing the timetables_with_average_waiting_time_above_threshold.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: timetables_with_average_waiting_time_above_threshold: timetable_document
    """
    timetables_with_average_waiting_time_above_threshold = []

    for timetable in timetables:
        if not check_average_waiting_time_of_timetable(timetable=timetable):
            timetables_with_average_waiting_time_above_threshold.append(timetable)

    return timetables_with_average_waiting_time_above_threshold


def get_travel_requests_of_timetable_with_waiting_time_above_threshold(timetable):
    """

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    waiting_time_of_travel_requests: [{
        'travel_request': travel_request_document, 'waiting_time': float (in seconds)
    }]
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document

    :return: travel_requests_with_waiting_time_above_threshold: [{
                 'travel_request': travel_request_document, 'waiting_time': float (in seconds)}]
    """
    travel_requests_with_waiting_time_above_threshold = []
    waiting_time_of_travel_requests = calculate_waiting_time_of_travel_requests_of_timetable(
        timetable=timetable
    )
    for dictionary_entry in waiting_time_of_travel_requests:
        waiting_time = dictionary_entry.get('waiting_time')

        if waiting_time > individual_waiting_time_threshold:
            travel_requests_with_waiting_time_above_threshold.append(dictionary_entry)

    return travel_requests_with_waiting_time_above_threshold


def handle_timetables_with_average_waiting_time_above_threshold(timetables):
    """

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    control = True

    while control:
        control = False
        timetables_with_average_waiting_time_above_threshold = get_timetables_with_average_waiting_time_above_threshold(
            timetables=timetables
        )
        for timetable in timetables_with_average_waiting_time_above_threshold:
            additional_timetable = divide_timetable_based_on_average_waiting_time(timetable=timetable)

            if additional_timetable is not None:
                add_timetable_to_timetables_sorted_by_starting_datetime(
                    timetable=additional_timetable,
                    timetables=timetables
                )
                control = True


def handle_overcrowded_timetables(timetables):
    """
    There might be timetables with number_of_current_passengers higher than the input: maximum_bus_capacity,
    which indicates that each one of these timetables cannot be served by one bus vehicle.
    For this reason, each one of these timetables is divided into two timetables
    and the corresponding travel requests are partitioned.
    The whole procedure is repeated until there is no timetable where the number of passengers
    exceeds the maximum_bus_capacity.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    overcrowded_timetables = get_overcrowded_timetables(timetables=timetables)

    while len(overcrowded_timetables) > 0:

        for overcrowded_timetable in overcrowded_timetables:
            additional_timetable = divide_timetable(timetable=overcrowded_timetable)

            add_timetable_to_timetables_sorted_by_starting_datetime(
                timetable=additional_timetable,
                timetables=timetables
            )

        overcrowded_timetables = get_overcrowded_timetables(timetables=timetables)


def partition_travel_requests_by_departure_datetime(travel_requests):
    """
    Split a list of travel_requests into two lists, based on their departure_datetime values,
    and return a double list containing both of them.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    :param travel_requests: [travel_request_document]

    :return: travel_requests_for_timetables: {
             'travel_requests_for_first_timetable': [travel_request_document],
             'travel_requests_for_second_timetable': [travel_request_document]}
    """
    travel_requests_for_first_timetable = []
    travel_requests_for_second_timetable = []

    starting_timetable_entry_dictionary = get_starting_timetable_entry_dictionary(
        travel_requests=travel_requests
    )

    for corresponding_travel_requests_list in starting_timetable_entry_dictionary.itervalues():
        # travel_requests_lists: {'first_list': travel_requests, 'second_list': travel_requests}
        #
        travel_requests_lists = partition_travel_requests_list(travel_requests=corresponding_travel_requests_list)
        first_list = travel_requests_lists.get('first_list')
        second_list = travel_requests_lists.get('second_list')
        travel_requests_for_first_timetable.extend(first_list)
        travel_requests_for_second_timetable.extend(second_list)

    travel_requests_for_timetables = {
        'travel_requests_for_first_timetable': travel_requests_for_first_timetable,
        'travel_requests_for_second_timetable': travel_requests_for_second_timetable
    }

    return travel_requests_for_timetables


def partition_travel_requests_in_timetables(travel_requests, timetables):
    """
    Partition a list of travel_requests in two timetables, and update their corresponding entries.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param travel_requests: [travel_request_document]
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    # travel_requests_for_timetables: {
    #     'travel_requests_for_first_timetable': [travel_request_document],
    #     'travel_requests_for_second_timetable': [travel_request_document]}
    #
    travel_requests_for_timetables = partition_travel_requests_by_departure_datetime(travel_requests=travel_requests)
    travel_requests_for_first_timetable = travel_requests_for_timetables.get('travel_requests_for_first_timetable')
    travel_requests_for_second_timetable = travel_requests_for_timetables.get('travel_requests_for_second_timetable')

    timetables[0]['travel_requests'] = travel_requests_for_first_timetable
    timetables[1]['travel_requests'] = travel_requests_for_second_timetable


def partition_travel_requests_list(travel_requests):
    """
    Partition a list of travel_requests into two lists, and return a dictionary containing both of them.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    :param travel_requests: [travel_request_document]
    :return: travel_requests_lists: {'first_list': [travel_request_document], 'second_list': [travel_request_document]}
    """
    number_of_travel_requests = len(travel_requests)
    # half_number_of_travel_requests = number_of_travel_requests / 2
    #
    # first_list_of_travel_requests = travel_requests[0:half_number_of_travel_requests]
    # second_list_of_travel_requests = travel_requests[half_number_of_travel_requests:number_of_travel_requests]

    first_list_of_travel_requests = []
    second_list_of_travel_requests = []

    if number_of_travel_requests == 0:
        pass
    elif number_of_travel_requests == 1:
        first_list_of_travel_requests.append(travel_requests[0])
    else:
        first_list_of_travel_requests.append(travel_requests[0])
        second_list_of_travel_requests.append(travel_requests[number_of_travel_requests - 1])

        departure_datetimes = [travel_request.get('departure_datetime') for travel_request in travel_requests]
        first_list_of_departure_datetimes = [departure_datetimes[0]]
        second_list_of_departure_datetimes = [departure_datetimes[number_of_travel_requests - 1]]

        for i in range(1, number_of_travel_requests - 1):
            travel_request = travel_requests[i]
            departure_datetime = departure_datetimes[i]

            mean_of_first_list_of_departure_datetimes = calculate_mean_departure_datetime(
                departure_datetimes=first_list_of_departure_datetimes
            )
            mean_of_second_list_of_departure_datetimes = calculate_mean_departure_datetime(
                departure_datetimes=second_list_of_departure_datetimes
            )
            difference_with_first_list_of_departure_datetimes = abs(
                departure_datetime - mean_of_first_list_of_departure_datetimes
            )
            difference_with_second_list_departure_datetimes = abs(
                departure_datetime - mean_of_second_list_of_departure_datetimes
            )

            if difference_with_first_list_of_departure_datetimes < difference_with_second_list_departure_datetimes:
                first_list_of_travel_requests.append(travel_request)
                first_list_of_departure_datetimes.append(departure_datetime)
            else:
                second_list_of_travel_requests.append(travel_request)
                second_list_of_departure_datetimes.append(departure_datetime)

    travel_requests_lists = {
        'first_list': first_list_of_travel_requests,
        'second_list': second_list_of_travel_requests
    }
    return travel_requests_lists


def handle_travel_requests_of_timetable_with_waiting_time_above_threshold(timetable, timetables):
    """

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    travel_requests_with_waiting_time_above_threshold: [{
        'travel_request': travel_request_document, 'waiting_time': float (in seconds)
    }]
    departure_datetime_differences: [{
        'timetable': timetable_document, 'departure_datetime_difference': float (in seconds)
    }]
    :param timetable: timetable_document
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    travel_requests_with_waiting_time_above_threshold = \
        get_travel_requests_of_timetable_with_waiting_time_above_threshold(timetable=timetable)

    for dictionary_entry in travel_requests_with_waiting_time_above_threshold:
        travel_request = dictionary_entry.get('travel_request')
        waiting_time = dictionary_entry.get('waiting_time')

        departure_datetime_differences = \
            calculate_departure_datetime_differences_between_travel_request_and_timetables(
                travel_request=travel_request,
                timetables=timetables
            )

        for departure_datetime_difference_entry in departure_datetime_differences:
            current_timetable = departure_datetime_difference_entry.get('timetable')
            departure_datetime_difference = departure_datetime_difference_entry.get('departure_datetime_difference')

            if (departure_datetime_difference > waiting_time or
                        departure_datetime_difference > average_waiting_time_threshold or
                        departure_datetime_difference > individual_waiting_time_threshold or
                        len(current_timetable.get('travel_requests')) >= maximum_bus_capacity):
                departure_datetime_differences.remove(departure_datetime_difference_entry)

        if len(departure_datetime_differences) > 0:
            timetable_with_minimum_departure_datetime_difference = \
                get_timetable_with_minimum_departure_datetime_difference(
                    departure_datetime_differences=departure_datetime_differences
                )

            add_travel_request_to_timetable_without_adjustments(
                travel_request=travel_request,
                timetable=timetable_with_minimum_departure_datetime_difference
            )
            remove_travel_request_from_timetable_without_adjustments(travel_request=travel_request, timetable=timetable)
            travel_requests_with_waiting_time_above_threshold.remove(dictionary_entry)

    calculate_number_of_passengers_of_timetable(timetable=timetable)
    adjust_departure_datetimes_of_timetable(timetable=timetable)

    average_waiting_time_of_timetable = calculate_average_waiting_time_of_timetable_in_seconds(timetable=timetable)
    remaining_travel_requests = [travel_request_entry.get('travel_request') for travel_request_entry in
                                 travel_requests_with_waiting_time_above_threshold]

    if len(remaining_travel_requests) >= minimum_number_of_passengers_in_timetable:

        additional_timetable = generate_new_timetable_for_travel_requests(
            timetable=timetable,
            travel_requests=remaining_travel_requests
        )
        average_waiting_time_of_additional_timetable = calculate_average_waiting_time_of_timetable_in_seconds(
            timetable=additional_timetable
        )

        if average_waiting_time_of_additional_timetable < average_waiting_time_of_timetable:
            add_timetable_to_timetables_sorted_by_starting_datetime(
                timetable=additional_timetable, timetables=timetables
            )
            remove_travel_requests_from_timetable_without_adjustments(
                travel_requests=remaining_travel_requests,
                timetable=timetable
            )
        else:
            del additional_timetable


def handle_undercrowded_timetable(timetable, timetables):
    """

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    travel_requests = timetable.get('travel_requests')

    for travel_request in travel_requests:
        departure_datetime_differences = \
            calculate_departure_datetime_differences_between_travel_request_and_timetables(
                travel_request=travel_request,
                timetables=timetables
            )

        timetable_with_minimum_departure_datetime_difference = \
            get_timetable_with_minimum_departure_datetime_difference(
                departure_datetime_differences=departure_datetime_differences
            )

        add_travel_request_to_timetable_without_adjustments(
            travel_request=travel_request,
            timetable=timetable_with_minimum_departure_datetime_difference
        )

        # travel_requests.remove(travel_request)

        remove_travel_request_from_timetable_without_adjustments(
            travel_request=travel_request,
            timetable=timetable
        )


def handle_undercrowded_timetables(timetables):
    """

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    travel_requests_of_undercrowded_timetables = []
    undercrowded_timetables = get_undercrowded_timetables(timetables=timetables)

    for undercrowded_timetable in undercrowded_timetables:
        travel_requests_of_undercrowded_timetable = list(undercrowded_timetable.get('travel_requests'))
        travel_requests_of_undercrowded_timetables.extend(travel_requests_of_undercrowded_timetable)
        timetables.remove(undercrowded_timetable)
        del undercrowded_timetable

    return travel_requests_of_undercrowded_timetables


def get_undercrowded_timetables(timetables):
    """
    Retrieve a list containing the timetables where the number of travel_requests
    is less than the minimum_number_of_passengers_in_timetable.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: undercrowded_timetables: [timetable_document]
    """
    undercrowded_timetables = []

    for timetable in timetables:
        travel_requests = timetable.get('travel_requests')

        if len(travel_requests) < minimum_number_of_passengers_in_timetable:
            undercrowded_timetables.append(timetable)

    return undercrowded_timetables


def handle_travel_requests_of_timetables_with_waiting_time_above_threshold(timetables):
    """

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    for timetable in timetables:
        handle_travel_requests_of_timetable_with_waiting_time_above_threshold(
            timetable=timetable,
            timetables=timetables
        )

    # adjust_departure_datetimes_of_timetables(timetables=timetables)
    # calculate_number_of_passengers_of_timetables(timetables=timetables)


def print_timetable(timetable, timetable_entries_control=False, travel_requests_control=False):
    """
    Print a timetable_document.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
    :param timetable_entries_control: bool
    :param travel_requests_control: bool
    :return: None
    """
    timetable_entries = timetable.get('timetable_entries')
    travel_requests = timetable.get('travel_requests')
    starting_datetime = get_starting_datetime_of_timetable(timetable=timetable)
    ending_datetime = get_ending_datetime_of_timetable(timetable=timetable)
    average_waiting_time = calculate_average_waiting_time_of_timetable_in_seconds(timetable=timetable)

    print '\n-- Printing Timetable--'
    print 'starting_datetime:', starting_datetime, \
        '- ending_datetime:', ending_datetime, \
        '- number_of_travel_requests:', len(travel_requests), \
        '- average_waiting_time:', average_waiting_time

    if timetable_entries_control:
        print '- Timetable Entries:'

        for timetable_entry in timetable_entries:
            print 'starting_bus_stop:', timetable_entry.get('starting_bus_stop').get('name'), \
                '- ending_bus_stop:', timetable_entry.get('ending_bus_stop').get('name'), \
                '- departure_datetime:', timetable_entry.get('departure_datetime'), \
                '- arrival_datetime:', timetable_entry.get('arrival_datetime'), \
                '- total_time:', timetable_entry.get('total_time'), \
                '- number_of_onboarding_passengers:', timetable_entry.get('number_of_onboarding_passengers'), \
                '- number_of_deboarding_passengers:', timetable_entry.get('number_of_deboarding_passengers'), \
                '- number_of_current_passengers:', timetable_entry.get('number_of_current_passengers')

    if travel_requests_control:
        print '- Travel Requests:'

        for travel_request in travel_requests:
            print 'starting_bus_stop:', travel_request.get('starting_bus_stop').get('name'), \
                '- ending_bus_stop:', travel_request.get('ending_bus_stop').get('name'), \
                '- departure_datetime:', travel_request.get('departure_datetime'), \
                '- starting_timetable_entry_index:', travel_request.get('starting_timetable_entry_index'), \
                '- ending_timetable_entry_index:', travel_request.get('ending_timetable_entry_index')


def print_timetables(timetables, timetables_control=False, timetable_entries_control=False,
                     travel_requests_control=False):
    """
    Print multiple timetable_documents.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :param timetables_control: bool
    :param timetable_entries_control: bool
    :param travel_requests_control: bool
    :return: None
    """
    sort_timetables_by_starting_datetime(timetables=timetables)

    number_of_timetables = len(timetables)
    total_number_of_passengers_in_timetables = calculate_total_number_of_travel_requests_in_timetables(
        timetables=timetables
    )
    average_number_of_passengers_in_timetables = calculate_average_number_of_travel_requests_in_timetables(
        timetables=timetables
    )
    average_waiting_time = calculate_average_waiting_time_of_timetables_in_seconds(timetables=timetables)

    print 'number_of_timetables:', number_of_timetables, \
        '- total_number_of_passengers_in_timetables:', total_number_of_passengers_in_timetables, \
        '- average_number_of_passengers_in_timetables:', average_number_of_passengers_in_timetables, \
        '- average_waiting_time:', average_waiting_time

    if timetables_control:
        for timetable in timetables:
            print_timetable(
                timetable=timetable,
                timetable_entries_control=timetable_entries_control,
                travel_requests_control=travel_requests_control
            )


def remove_travel_request_from_timetable_with_adjustments(travel_request, timetable):
    """
    Remove a travel_request from the list of travel_requests of a timetable, adjusting the timetable_entries.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param travel_request: travel_request_document
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    remove_travel_request_from_timetable_without_adjustments(travel_request=travel_request, timetable=timetable)
    adjust_departure_datetimes_of_timetable(timetable=timetable)
    calculate_number_of_passengers_of_timetable(timetable=timetable)


def remove_travel_request_from_timetable_without_adjustments(travel_request, timetable):
    """
    Remove a travel_request from the list of travel_requests of a timetable, without adjusting the timetable_entries.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param travel_request: travel_request_document
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    travel_requests = timetable.get('travel_requests')

    if travel_request in travel_requests:
        travel_requests.remove(travel_request)


def remove_travel_requests_from_timetable_without_adjustments(travel_requests, timetable):
    """
    Remove a list of travel_requests from the list of travel_requests of a timetable,
    without adjusting the timetable_entries.

    travel_request_document: {
        '_id', 'client_id', 'line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }
    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param travel_requests: [travel_request_document]
    :param timetable: timetable_document
    :return: None (Updates timetable)
    """
    travel_requests_of_timetable = timetable.get('travel_requests')

    for travel_request in travel_requests:
        if travel_request in travel_requests_of_timetable:
            travel_requests_of_timetable.remove(travel_request)


def sort_timetables_by_starting_datetime(timetables):
    """
    Sort timetables by their starting_datetime.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers'}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_document]
    :return: None (Updates timetables)
    """
    starting_datetimes = get_starting_datetimes_of_timetables(timetables=timetables)
    quicksort(list_to_be_sorted=timetables, comparison_list=starting_datetimes, low=0, high=len(timetables)-1)


def quicksort(list_to_be_sorted, comparison_list, low, high):
    if low < high:
        p = partition(list_to_be_sorted=list_to_be_sorted, comparison_list=comparison_list, low=low, high=high)
        quicksort(list_to_be_sorted=list_to_be_sorted, comparison_list=comparison_list, low=low, high=p-1)
        quicksort(list_to_be_sorted=list_to_be_sorted, comparison_list=comparison_list, low=p+1, high=high)


def partition(list_to_be_sorted, comparison_list, low, high):
    pivot = comparison_list[high]
    i = low

    for j in range(low, high):
        if comparison_list[j] <= pivot:
            swap(l=list_to_be_sorted, first=i, second=j)
            swap(l=comparison_list, first=i, second=j)
            i += 1

    swap(l=list_to_be_sorted, first=i, second=high)
    swap(l=comparison_list, first=i, second=high)
    return i


def swap(l, first, second):
    temp = l[first]
    l[first] = l[second]
    l[second] = temp

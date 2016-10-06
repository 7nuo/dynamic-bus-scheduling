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
from src.look_ahead.timetable_generator import ceil_datetime_minutes
from src.route_generator.route_generator_client import get_route_between_multiple_bus_stops
from datetime import timedelta


class TimetableUpdater(object):
    def __init__(self, bus_stops, timetables):
        """
        Initialize the TimetableUpdater, send a request to the RouteGenerator and receive the less time-consuming
        route which connects the provided bus stops.

        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}

        :param timetables: [{
               '_id', 'line_id',
               'timetable_entries': [{
                   'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                   'number_of_deboarding_passengers', 'number_of_current_passengers'}],
               'travel_requests': [{
                   '_id', 'client_id', 'bus_line_id',
                   'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'departure_datetime', 'arrival_datetime',
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]

        route_generator_response: [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                      'distances_from_starting_node', 'times_from_starting_node',
                      'distances_from_previous_node', 'times_from_previous_node'}}]

        :return: None
        """
        self.bus_stops = bus_stops
        self.timetables = timetables
        self.route_generator_response = get_route_between_multiple_bus_stops(bus_stops=bus_stops)


def update_timetable(timetable, route_generator_response):
    """
    Update the timetable_entries of the timetable, taking into consideration the route_generator_response.

    :param timetable: {
               '_id', 'line_id',
               'timetable_entries': [{
                   'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                   'number_of_deboarding_passengers', 'number_of_current_passengers'}],
               'travel_requests': [{
                   '_id', 'client_id', 'bus_line_id',
                   'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'departure_datetime', 'arrival_datetime',
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

    :param route_generator_response: [{
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                         'distances_from_starting_node', 'times_from_starting_node',
                         'distances_from_previous_node', 'times_from_previous_node'}}]

    :return: None (Updates timetable)
    """
    timetable_entries = timetable.get('timetable_entries')
    number_of_timetable_entries = len(timetable_entries)
    total_times = []

    for intermediate_response in route_generator_response:
        intermediate_route = intermediate_response.get('route')
        total_time = intermediate_route.get('total_time')
        total_times.append(total_time)

    for i in range(0, number_of_timetable_entries):
        timetable_entry = timetable_entries[i]
        total_time = total_times[i]
        departure_datetime = timetable_entry.get('departure_datetime')

        if i > 0:
            previous_timetable_entry = timetable_entries[i - 1]
            previous_arrival_datetime = previous_timetable_entry.get('arrival_datetime')
            departure_datetime_based_on_previous_arrival_datetime = ceil_datetime_minutes(
                starting_datetime=previous_arrival_datetime
            )
            if departure_datetime_based_on_previous_arrival_datetime > departure_datetime:
                departure_datetime = departure_datetime_based_on_previous_arrival_datetime
                timetable_entry['departure_datetime'] = departure_datetime

        arrival_datetime = departure_datetime + timedelta(seconds=total_time)
        timetable_entry['arrival_datetime'] = arrival_datetime


def update_timetables(timetables, route_generator_response):
    """

    :param timetables: [{
               '_id', 'line_id',
               'timetable_entries': [{
                   'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'departure_datetime', 'arrival_datetime', 'total_time', 'number_of_onboarding_passengers',
                   'number_of_deboarding_passengers', 'number_of_current_passengers'}],
               'travel_requests': [{
                   '_id', 'client_id', 'bus_line_id',
                   'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                   'departure_datetime', 'arrival_datetime',
                   'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}]

    :param route_generator_response: [{
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                         'distances_from_starting_node', 'times_from_starting_node',
                         'distances_from_previous_node', 'times_from_previous_node'}}]

    :return: None (Updates timetables)
    """
    for timetable in timetables:
        update_timetable(timetable=timetable, route_generator_response=route_generator_response)

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
from datetime import timedelta
from src.look_ahead.timetable_generator import adjust_timetable_entries, ceil_datetime_minutes
from src.route_generator.route_generator_client import get_route_between_multiple_bus_stops

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class TimetableUpdater(object):
    def __init__(self, bus_stops, timetables, travel_requests):
        """
        Initialize the TimetableUpdater and send a request to the Route Generator in order to
        identify the less time-consuming route which connects the provided bus_stops.

        bus_stop_document: {
            '_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}
        }
        timetable_document: {
            '_id', 'line_id',
            'timetable_entries': [{
                'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                'departure_datetime', 'arrival_datetime', 'number_of_onboarding_passengers',
                'number_of_deboarding_passengers', 'number_of_current_passengers',
                'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                          'distances_from_starting_node', 'times_from_starting_node',
                          'distances_from_previous_node', 'times_from_previous_node'}}],
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
        route_generator_response: [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                      'distances_from_starting_node', 'times_from_starting_node',
                      'distances_from_previous_node', 'times_from_previous_node'}
        }]
        :param bus_stops: [bus_stop_document]
        :param timetables: [timetable_document]
        :param travel_requests: [travel_request_document]
        :return: None
        """
        self.bus_stops = bus_stops
        self.timetables = timetables
        self.travel_requests = travel_requests
        self.route_generator_response = get_route_between_multiple_bus_stops(bus_stops=bus_stops)


def update_entries_of_timetable(timetable, route_generator_response):
    """
    Update the timetable_entries of a timetable, taking into consideration the route_generator_response.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers',
            'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                      'distances_from_starting_node', 'times_from_starting_node',
                      'distances_from_previous_node', 'times_from_previous_node'}}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetable: timetable_document
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
    ideal_departure_datetimes = [timetable_entry.get('departure_datetime') for timetable_entry in timetable_entries]
    intermediate_routes = [intermediate_response.get('route') for intermediate_response in route_generator_response]
    # total_times = [intermediate_route.get('total_time') for intermediate_route in intermediate_routes]

    for i in range(0, number_of_timetable_entries):
        timetable_entry = timetable_entries[i]
        intermediate_route = intermediate_routes[i]
        timetable_entry['route'] = intermediate_route
        # total_time = timetable_entry.get('route').get('total_time')
        # # total_time = total_times[i]
        # departure_datetime = timetable_entry.get('departure_datetime')
        #
        # if i > 0:
        #     previous_timetable_entry = timetable_entries[i - 1]
        #     previous_arrival_datetime = previous_timetable_entry.get('arrival_datetime')
        #     # departure_datetime_based_on_previous_arrival_datetime = previous_arrival_datetime
        #     departure_datetime_based_on_previous_arrival_datetime = ceil_datetime_minutes(
        #         starting_datetime=previous_arrival_datetime
        #     )
        #     if departure_datetime_based_on_previous_arrival_datetime > departure_datetime:
        #         departure_datetime = departure_datetime_based_on_previous_arrival_datetime
        #         timetable_entry['departure_datetime'] = departure_datetime
        #
        # arrival_datetime = departure_datetime + timedelta(seconds=total_time)
        # timetable_entry['arrival_datetime'] = arrival_datetime

    adjust_timetable_entries(
        timetable=timetable,
        ideal_departure_datetimes=ideal_departure_datetimes
    )


def update_entries_of_timetables(timetables, route_generator_response):
    """
    Update the timetable_entries of a list of timetables, taking into consideration the route_generator_response.

    timetable_document: {
        '_id', 'line_id',
        'timetable_entries': [{
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime', 'number_of_onboarding_passengers',
            'number_of_deboarding_passengers', 'number_of_current_passengers',
            'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                      'distances_from_starting_node', 'times_from_starting_node',
                      'distances_from_previous_node', 'times_from_previous_node'}}],
        'travel_requests': [{
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'}]
    }
    :param timetables: [timetable_documents]
    :param route_generator_response: [{
               'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
               'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                         'distances_from_starting_node', 'times_from_starting_node',
                         'distances_from_previous_node', 'times_from_previous_node'}}]

    :return: None (Updates timetables)
    """
    for timetable in timetables:
        update_entries_of_timetable(timetable=timetable, route_generator_response=route_generator_response)

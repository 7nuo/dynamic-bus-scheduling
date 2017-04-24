#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
- LICENCE

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


- DESCRIPTION OF DOCUMENTS

-- MongoDB Database Documents:

address_document: {
    '_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}
}
bus_line_document: {
    '_id', 'bus_line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
}
bus_stop_document: {
    '_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}
}
bus_stop_waypoints_document: {
    '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[edge_object_id]]
}
bus_vehicle_document: {
    '_id', 'bus_vehicle_id', 'maximum_capacity',
    'routes': [{'starting_datetime', 'ending_datetime', 'timetable_id'}]
}
detailed_bus_stop_waypoints_document: {
    '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[edge_document]]
}
edge_document: {
    '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    'max_speed', 'road_type', 'way_id', 'traffic_density'
}
node_document: {
    '_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}
}
point_document: {
    '_id', 'osm_id', 'point': {'longitude', 'latitude'}
}
timetable_document: {
    '_id', 'timetable_id', 'bus_line_id', 'bus_vehicle_id',
    'timetable_entries': [{
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime', 'number_of_onboarding_passengers',
        'number_of_deboarding_passengers', 'number_of_current_passengers',
        'route': {
            'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
            'distances_from_starting_node', 'times_from_starting_node',
            'distances_from_previous_node', 'times_from_previous_node'
        }
    }],
    'travel_requests': [{
        '_id', 'client_id', 'bus_line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }]
}
traffic_event_document: {
    '_id', 'event_id', 'event_type', 'event_level', 'point': {'longitude', 'latitude'}, 'datetime'
}
travel_request_document: {
    '_id', 'client_id', 'bus_line_id',
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'departure_datetime', 'arrival_datetime',
    'starting_timetable_entry_index', 'ending_timetable_entry_index'
}
way_document: {
    '_id', 'osm_id', 'tags', 'references'
}

-- Route Generator Responses:

get_route_between_two_bus_stops: {
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'route': {
        'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        'distances_from_starting_node', 'times_from_starting_node',
        'distances_from_previous_node', 'times_from_previous_node'
    }
}
get_route_between_multiple_bus_stops: [{
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'route': {
        'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        'distances_from_starting_node', 'times_from_starting_node',
        'distances_from_previous_node', 'times_from_previous_node'
    }
}]
get_waypoints_between_two_bus_stops: {
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[{
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'
    }]]
}
get_waypoints_between_multiple_bus_stops: [{
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[{
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'
    }]]
}]
"""
import random
from datetime import timedelta
from src.mongodb_database.mongodb_database_connection import MongodbDatabaseConnection
from src.common.logger import log
from src.common.parameters import mongodb_host, mongodb_port, travel_requests_simulator_datetime_distribution_weights

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class TravelRequestsSimulator(object):
    def __init__(self):
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='travel_requests_simulator', log_type='DEBUG',
            log_message='mongodb_database_connection: established')

    def clear_travel_requests_collection(self):
        """
        Clear all the documents of the TravelRequests collection.

        :return: None
        """
        self.mongodb_database_connection.clear_travel_request_documents_collection()
        log(module_name='travel_requests_simulator', log_type='DEBUG',
            log_message='clear_travel_request_documents_collection: ok')

    def delete_travel_request_documents(self, object_ids=None, client_ids=None, bus_line_ids=None,
                                        min_departure_datetime=None, max_departure_datetime=None):
        """
        Delete multiple travel_request_documents.

        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param bus_line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :return: None
        """
        self.mongodb_database_connection.delete_travel_request_documents(
            object_ids=object_ids,
            client_ids=client_ids,
            bus_line_ids=bus_line_ids,
            min_departure_datetime=min_departure_datetime,
            max_departure_datetime=max_departure_datetime
        )
        log(module_name='travel_requests_simulator', log_type='DEBUG',
            log_message='delete_travel_request_documents: ok')

    def generate_random_travel_request_documents(self, initial_datetime, min_number_of_travel_request_documents,
                                                 max_number_of_travel_request_documents):
        """
        Generate random number of travel_request_documents for each bus_line,
        for a 24hour period starting from a selected datetime, and store them at the
        corresponding collection of the System Database.

        :param initial_datetime: datetime
        :param min_number_of_travel_request_documents: int
        :param max_number_of_travel_request_documents: int
        :return: None
        """
        bus_lines = self.mongodb_database_connection.find_bus_line_documents()

        for bus_line in bus_lines:
            number_of_travel_request_documents = random.randint(
                min_number_of_travel_request_documents,
                max_number_of_travel_request_documents
            )
            self.generate_travel_request_documents(
                initial_datetime=initial_datetime,
                number_of_travel_request_documents=number_of_travel_request_documents,
                bus_line=bus_line
            )

    def generate_travel_request_documents(self, initial_datetime, number_of_travel_request_documents,
                                          bus_line=None, bus_line_id=None):
        """
        Generate a specific number of travel_request_documents, for the selected bus_line,
        for a 24hour period starting from a selected datetime, and store them at the
        corresponding collection of the System Database.

        :param initial_datetime: datetime
        :param number_of_travel_request_documents: int
        :param bus_line: bus_line_document
        :param bus_line_id: int
        :return: None
        """
        # 1: The inputs: initial_datetime, number_of_travel_request_documents, and (bus_line or bus_line_id)
        #    are provided to the Travel Requests Simulator, so as a specific number of travel_request_documents
        #    to be generated, for the selected bus_line, for a 24hour period starting from
        #    the selected datetime.
        #
        # 2: If the provided bus_line is None, then the Travel Requests Simulator retrieves from the System Database
        #    the bus_line which corresponds to the provided bus_line_id.
        #
        if bus_line is None and bus_line_id is None:
            return None
        elif bus_line is None:
            bus_line = self.mongodb_database_connection.find_bus_line_document(bus_line_id=bus_line_id)
        else:
            pass

        bus_stops = bus_line.get('bus_stops')
        number_of_bus_stops = len(bus_stops)

        # 3: The Travel Requests Simulator generates the travel_request_documents, taking into consideration
        #    the variation of transportation demand during the hours of the day.
        #
        # distribution_weighted_datetimes = [
        #     (initial_datetime + timedelta(hours=0), 1),
        #     (initial_datetime + timedelta(hours=1), 1),
        #     (initial_datetime + timedelta(hours=2), 1),
        #     (initial_datetime + timedelta(hours=3), 1),
        #     (initial_datetime + timedelta(hours=4), 1),
        #     (initial_datetime + timedelta(hours=5), 1),
        #     (initial_datetime + timedelta(hours=6), 1),
        #     (initial_datetime + timedelta(hours=7), 1),
        #     (initial_datetime + timedelta(hours=8), 1),
        #     (initial_datetime + timedelta(hours=9), 1),
        #     (initial_datetime + timedelta(hours=10), 1),
        #     (initial_datetime + timedelta(hours=11), 1),
        #     (initial_datetime + timedelta(hours=12), 1),
        #     (initial_datetime + timedelta(hours=13), 1),
        #     (initial_datetime + timedelta(hours=14), 1),
        #     (initial_datetime + timedelta(hours=15), 1),
        #     (initial_datetime + timedelta(hours=16), 1),
        #     (initial_datetime + timedelta(hours=17), 1),
        #     (initial_datetime + timedelta(hours=18), 1),
        #     (initial_datetime + timedelta(hours=19), 1),
        #     (initial_datetime + timedelta(hours=20), 1),
        #     (initial_datetime + timedelta(hours=21), 1),
        #     (initial_datetime + timedelta(hours=22), 1),
        #     (initial_datetime + timedelta(hours=23), 1)
        # ]
        distribution_weighted_datetimes = [
            (initial_datetime + timedelta(hours=i),
             travel_requests_simulator_datetime_distribution_weights[i]) for i in range(0, 24)
        ]
        datetime_population = [val for val, cnt in distribution_weighted_datetimes for i in range(cnt)]
        travel_request_documents = []
        maximum_client_id = self.mongodb_database_connection.get_maximum_or_minimum(collection='travel_request')

        for i in range(0, number_of_travel_request_documents):
            client_id = maximum_client_id + 1
            maximum_client_id = client_id
            starting_bus_stop_index = random.randint(0, number_of_bus_stops - 2)
            starting_bus_stop = bus_stops[starting_bus_stop_index]
            ending_bus_stop_index = random.randint(starting_bus_stop_index + 1, number_of_bus_stops - 1)
            ending_bus_stop = bus_stops[ending_bus_stop_index]
            additional_departure_time_interval = random.randint(0, 59)
            departure_datetime = (random.choice(datetime_population) +
                                  timedelta(minutes=additional_departure_time_interval))

            travel_request_document = {
                'client_id': client_id,
                'bus_line_id': bus_line_id,
                'starting_bus_stop': starting_bus_stop,
                'ending_bus_stop': ending_bus_stop,
                'departure_datetime': departure_datetime,
                'arrival_datetime': None,
                'starting_timetable_entry_index': None,
                'ending_timetable_entry_index': None
            }
            travel_request_documents.append(travel_request_document)

        # 4: The generated travel_request_documents are stored at the
        #    TravelRequests collection of the System Database.
        #
        self.mongodb_database_connection.insert_travel_request_documents(
            travel_request_documents=travel_request_documents
        )

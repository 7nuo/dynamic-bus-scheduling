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
from src.mongodb_database.mongodb_database_connection import MongodbDatabaseConnection
from src.common.logger import log
from src.common.parameters import mongodb_host, mongodb_port

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class BusVehicleHandler(object):
    def __init__(self):
        self.module_name = 'bus_vehicle_handler'
        self.log_type = 'DEBUG'
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        self.log_message = 'mongodb_database_connection: established'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def clear_bus_vehicle_documents_collection(self):
        """
        Delete all the documents of the BusVehicleDocuments collection.

        :return: number_of_deleted_documents: int
        """
        number_of_deleted_documents = self.mongodb_database_connection.clear_bus_vehicle_documents_collection()
        self.log_message = 'clear_bus_vehicle_documents_collection: number_of_deleted_documents: ' + \
                           str(number_of_deleted_documents)
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return number_of_deleted_documents

    def delete_bus_vehicle_document(self, object_id=None, bus_vehicle_id=None):
        """
        Delete a bus_vehicle_document.

        :param object_id: ObjectId
        :param bus_vehicle_id: int
        :return: True if the document was successfully deleted, otherwise False.
        """
        deleted = self.delete_bus_vehicle_document(
            object_id=object_id,
            bus_vehicle_id=bus_vehicle_id
        )
        self.log_message = 'delete_bus_vehicle_document: ' + str(deleted)
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return deleted

    def delete_bus_vehicle_documents(self, object_ids=None, bus_vehicle_ids=None):
        """
        Delete multiple bus_vehicle_documents.

        :param object_ids: [ObjectId]
        :param bus_vehicle_ids: [int]
        :return: number_of_deleted_documents: int
        """
        number_of_deleted_documents = self.mongodb_database_connection.delete_bus_vehicle_documents(
            object_ids=object_ids,
            bus_vehicle_ids=bus_vehicle_ids
        )
        self.log_message = 'delete_bus_vehicle_documents: number_of_deleted_documents: ' + \
                           str(number_of_deleted_documents)
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return number_of_deleted_documents

    def generate_bus_vehicle_document(self, maximum_capacity):
        """
        Generate a new bus_vehicle_document.

        :param maximum_capacity: int
        :return: new_object_id: ObjectId
        """
        maximum_bus_vehicle_id = self.mongodb_database_connection.get_maximum_or_minimum(collection='bus_vehicle')
        bus_vehicle_id = maximum_bus_vehicle_id + 1

        bus_vehicle_document = {
            'bus_vehicle_id': bus_vehicle_id,
            'maximum_capacity': maximum_capacity,
            'routes': []
        }
        new_object_id = self.insert_bus_vehicle_document(bus_vehicle_document=bus_vehicle_document)
        return new_object_id

    def generate_bus_vehicle_documents(self, maximum_capacity, number_of_bus_vehicle_documents):
        """
        Generate multiple bus_vehicle_documents.

        :param maximum_capacity: int
        :param number_of_bus_vehicle_documents: int
        :return: new_object_ids: [ObjectIds]
        """
        bus_vehicle_documents = []
        maximum_bus_vehicle_id = self.mongodb_database_connection.get_maximum_or_minimum(collection='bus_vehicle')

        for i in range(0, number_of_bus_vehicle_documents):
            bus_vehicle_id = maximum_bus_vehicle_id + 1
            maximum_bus_vehicle_id = bus_vehicle_id

            bus_vehicle_document = {
                'bus_vehicle_id': bus_vehicle_id,
                'maximum_capacity': maximum_capacity,
                'routes': []
            }
            bus_vehicle_documents.append(bus_vehicle_document)

        new_object_ids = self.insert_bus_vehicle_documents(bus_vehicle_documents=bus_vehicle_documents)
        return new_object_ids

    def insert_bus_vehicle_document(self, bus_vehicle_document=None, bus_vehicle_id=None,
                                    maximum_capacity=None, routes=None):
        """
        Insert a new bus_vehicle_document or update, if it already exists in the database.

        :param bus_vehicle_document
        :param bus_vehicle_id: int
        :param maximum_capacity: int
        :param routes: [{'starting_datetime', 'ending_datetime', 'timetable_id'}]
        :return: new_object_id: ObjectId
        """
        new_object_id = self.mongodb_database_connection.insert_bus_vehicle_document(
            bus_vehicle_document=bus_vehicle_document,
            bus_vehicle_id=bus_vehicle_id,
            maximum_capacity=maximum_capacity,
            routes=routes
        )
        self.log_message = 'insert_bus_vehicle_document: new_object_id: ' + str(new_object_id)
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return new_object_id

    def insert_bus_vehicle_documents(self, bus_vehicle_documents, insert_many=False):
        """
        Insert multiple bus_vehicle_documents or update existing ones.

        :param bus_vehicle_documents:
        :param insert_many: bool
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = self.mongodb_database_connection.insert_bus_vehicle_documents(
            bus_vehicle_documents=bus_vehicle_documents,
            insert_many=insert_many
        )
        self.log_message = 'insert_bus_vehicle_documents: new_object_ids: ' + str(new_object_ids)
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return new_object_ids

    def print_bus_vehicle_document(self, object_id=None, bus_vehicle_id=None):
        """
        Print a bus_vehicle_document.

        :param object_id: ObjectId
        :param bus_vehicle_id: int
        :return: None
        """
        self.mongodb_database_connection.print_bus_vehicle_document(
            object_id=object_id,
            bus_vehicle_id=bus_vehicle_id
        )

    def print_bus_vehicle_documents(self, object_ids=None, bus_vehicle_ids=None, counter=None):
        """
        Print multiple bus_vehicle_documents.

        :param object_ids: [ObjectId]
        :param bus_vehicle_ids: [int]
        :param counter: int
        :return: None
        """
        self.mongodb_database_connection.print_bus_vehicle_documents(
            object_ids=object_ids,
            bus_vehicle_ids=bus_vehicle_ids,
            counter=counter
        )

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
    '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
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
    '_id', 'timetable_id', 'line_id', 'bus_vehicle_id',
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
        '_id', 'client_id', 'line_id',
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
    '_id', 'client_id', 'line_id',
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
import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.common.logger import log
from src.look_ahead.bus_vehicle_handler import BusVehicleHandler

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class BusVehicleHandlerTester(object):
    def __init__(self):
        self.module_name = 'bus_vehicle_handler_tester'
        self.log_type = 'INFO'
        self.log_message = 'initialize_bus_vehicle_handler: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.bus_vehicle_handler = BusVehicleHandler()
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'initialize_bus_vehicle_handler: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_clear_bus_vehicle_documents_collection(self):
        """
        Delete all the documents of the BusVehicleDocuments collection.

        :return: number_of_deleted_documents: int
        """
        self.log_message = 'test_clear_bus_vehicle_documents_collection: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        number_of_deleted_documents = self.bus_vehicle_handler.clear_bus_vehicle_documents_collection()
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_clear_bus_vehicle_documents_collection: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return number_of_deleted_documents

    def test_delete_bus_vehicle_document(self, object_id=None, bus_vehicle_id=None):
        """
        Delete a bus_vehicle_document.

        :param object_id: ObjectId
        :param bus_vehicle_id: int
        :return: True if the document was successfully deleted, otherwise False.
        """
        self.log_message = 'test_delete_bus_vehicle_document: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        deleted = self.bus_vehicle_handler.delete_bus_vehicle_document(
            object_id=object_id,
            bus_vehicle_id=bus_vehicle_id
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_delete_bus_vehicle_document: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return deleted

    def test_delete_bus_vehicle_documents(self, object_ids=None, bus_vehicle_ids=None):
        """
        Delete multiple bus_vehicle_documents.

        :param object_ids: [ObjectId]
        :param bus_vehicle_ids: [int]
        :return: number_of_deleted_documents: int
        """
        self.log_message = 'test_delete_bus_vehicle_documents: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        number_of_deleted_documents = self.bus_vehicle_handler.delete_bus_vehicle_documents(
            object_ids=object_ids,
            bus_vehicle_ids=bus_vehicle_ids
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_delete_bus_vehicle_documents: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return number_of_deleted_documents

    def test_generate_bus_vehicle_document(self, maximum_capacity):
        """
        Generate a new bus_vehicle_document.

        :param maximum_capacity: int
        :return: new_object_id: ObjectId
        """
        self.log_message = 'test_generate_bus_vehicle_document: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        new_object_id = self.bus_vehicle_handler.generate_bus_vehicle_document(
            maximum_capacity=maximum_capacity
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_generate_bus_vehicle_document: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return new_object_id

    def test_generate_bus_vehicle_documents(self, maximum_capacity, number_of_bus_vehicle_documents):
        """
        Generate multiple bus_vehicle_documents.

        :param maximum_capacity: int
        :param number_of_bus_vehicle_documents: int
        :return: new_object_ids: [ObjectIds]
        """
        self.log_message = 'test_generate_bus_vehicle_documents: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        new_object_ids = self.bus_vehicle_handler.generate_bus_vehicle_documents(
            maximum_capacity=maximum_capacity,
            number_of_bus_vehicle_documents=number_of_bus_vehicle_documents
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_generate_bus_vehicle_documents: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return new_object_ids

    def test_insert_bus_vehicle_document(self, bus_vehicle_document=None, bus_vehicle_id=None,
                                         maximum_capacity=None, routes=None):
        """
        Insert a new bus_vehicle_document or update, if it already exists in the database.

        :param bus_vehicle_document
        :param bus_vehicle_id: int
        :param maximum_capacity: int
        :param routes: [{'starting_datetime', 'ending_datetime', 'timetable_id'}]
        :return: new_object_id: ObjectId
        """
        self.log_message = 'test_insert_bus_vehicle_document: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        new_object_id = self.bus_vehicle_handler.insert_bus_vehicle_document(
            bus_vehicle_document=bus_vehicle_document,
            bus_vehicle_id=bus_vehicle_id,
            maximum_capacity=maximum_capacity,
            routes=routes
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_insert_bus_vehicle_document: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return new_object_id

    def test_insert_bus_vehicle_documents(self, bus_vehicle_documents, insert_many=False):
        """
        Insert multiple bus_vehicle_documents or update existing ones.

        :param bus_vehicle_documents:
        :param insert_many: bool
        :return: new_object_ids: [ObjectId]
        """
        self.log_message = 'test_insert_bus_vehicle_documents: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        new_object_ids = self.bus_vehicle_handler.insert_bus_vehicle_documents(
            bus_vehicle_documents=bus_vehicle_documents,
            insert_many=insert_many
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_insert_bus_vehicle_documents: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        return new_object_ids

    def test_print_bus_vehicle_document(self, object_id=None, bus_vehicle_id=None):
        """
        Print a bus_vehicle_document.

        :param object_id: ObjectId
        :param bus_vehicle_id: int
        :return: None
        """
        self.log_message = 'test_print_bus_vehicle_document: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.bus_vehicle_handler.print_bus_vehicle_document(
            object_id=object_id,
            bus_vehicle_id=bus_vehicle_id
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_print_bus_vehicle_document: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_print_bus_vehicle_documents(self, object_ids=None, bus_vehicle_ids=None, counter=None):
        """
        Print multiple bus_vehicle_documents.

        :param object_ids: [ObjectId]
        :param bus_vehicle_ids: [int]
        :param counter: int
        :return: None
        """
        self.log_message = 'test_print_bus_vehicle_documents: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.bus_vehicle_handler.print_bus_vehicle_documents(
            object_ids=object_ids,
            bus_vehicle_ids=bus_vehicle_ids,
            counter=counter
        )
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_print_bus_vehicle_documents: finished - elapsed_time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)


if __name__ == '__main__':
    bus_vehicle_handler_tester = BusVehicleHandlerTester()

    while True:
        time.sleep(0.01)
        selection = raw_input(
            '\n0. exit'
            '\n1. test_clear_bus_vehicle_documents_collection'
            '\n2. test_delete_bus_vehicle_document'
            '\n3. test_delete_bus_vehicle_documents'
            '\n4. test_generate_bus_vehicle_document'
            '\n5. test_generate_bus_vehicle_documents'
            '\n6. test_insert_bus_vehicle_document'
            '\n7. test_insert_bus_vehicle_documents'
            '\n8. test_print_bus_vehicle_document'
            '\n9. test_print_bus_vehicle_documents'
            '\nSelection: '
        )
        # 0. exit
        if selection == '0':
            break

        # 1. test_clear_bus_vehicle_documents_collection
        elif selection == '1':
            bus_vehicle_handler_tester.test_clear_bus_vehicle_documents_collection()

        # 2. test_delete_bus_vehicle_document
        elif selection == '2':
            bus_vehicle_id = int(
                raw_input(
                    '\n2. test_delete_bus_vehicle_document'
                    '\nbus_vehicle_id: '
                )
            )
            bus_vehicle_handler_tester.test_delete_bus_vehicle_document(
                object_id=None,
                bus_vehicle_id=bus_vehicle_id
            )

        # 3. test_delete_bus_vehicle_documents
        elif selection == '3':
            bus_vehicle_ids = []
            bus_vehicle_handler_tester.test_delete_bus_vehicle_documents(
                object_ids=None,
                bus_vehicle_ids=bus_vehicle_ids
            )

        # 4. test_generate_bus_vehicle_document
        elif selection == '4':
            maximum_capacity = int(
                raw_input(
                    '\n4. test_generate_bus_vehicle_document'
                    '\nmaximum_capacity: '
                )
            )
            bus_vehicle_handler_tester.test_generate_bus_vehicle_document(
                maximum_capacity=maximum_capacity
            )

        # 5. test_generate_bus_vehicle_documents
        elif selection == '5':
            maximum_capacity = int(
                raw_input(
                    '\n5. test_generate_bus_vehicle_documents'
                    '\nmaximum_capacity: '
                )
            )
            number_of_bus_vehicle_documents = int(
                raw_input(
                    '\nnumber_of_bus_vehicle_documents: '
                )
            )
            bus_vehicle_handler_tester.test_generate_bus_vehicle_documents(
                maximum_capacity=maximum_capacity,
                number_of_bus_vehicle_documents=number_of_bus_vehicle_documents
            )

        # 6. test_insert_bus_vehicle_document
        elif selection == '6':
            pass

        # 7. test_insert_bus_vehicle_documents
        elif selection == '7':
            pass

        # 8. test_print_bus_vehicle_document
        elif selection == '8':
            bus_vehicle_id = int(
                raw_input(
                    '\n8. test_print_bus_vehicle_document'
                    '\nbus_vehicle_id: '
                )
            )
            bus_vehicle_handler_tester.test_print_bus_vehicle_document(
                object_id=None,
                bus_vehicle_id=bus_vehicle_id
            )

        # 9. test_print_bus_vehicle_documents
        elif selection == '9':
            bus_vehicle_handler_tester.test_print_bus_vehicle_documents()

        else:
            pass

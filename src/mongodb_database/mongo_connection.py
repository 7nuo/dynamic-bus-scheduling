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
from bson import ObjectId
from pymongo import MongoClient


class MongoConnection(object):
    def __init__(self, host, port):
        self.mongo_client = MongoClient(host, port)
        self.db = self.mongo_client.monad
        self.nodes_collection = self.db.Nodes
        self.points_collection = self.db.Points
        self.ways_collection = self.db.Ways
        self.bus_stops_collection = self.db.BusStops
        self.edges_collection = self.db.Edges
        self.address_book_collection = self.db.AddressBook
        self.bus_lines_collection = self.db.BusLines
        self.bus_stop_waypoints_collection = self.db.BusStopWaypoints
        self.travel_requests_collection = self.db.TravelRequests
        self.timetables_collection = self.db.Timetables

    def clear_all_collections(self):
        self.clear_nodes()
        self.clear_points()
        self.clear_ways()
        self.clear_bus_stops()
        self.clear_edges()
        self.clear_address_book()
        self.clear_bus_lines()
        self.clear_bus_stop_waypoints()
        self.clear_travel_requests()
        self.clear_timetables()

    def clear_address_book(self):
        """
        Delete all the documents of the AddressBook collection.

        :return: The number of deleted documents.
        """
        result = self.address_book_collection.delete_many({})
        return result.deleted_count

    def clear_bus_lines(self):
        """
        Delete all the documents of the BusLines collection.

        :return: The number of deleted documents.
        """
        result = self.bus_lines_collection.delete_many({})
        return result.deleted_count

    def clear_bus_stop_waypoints(self):
        """
        Delete all the documents of the BusStopWaypoints collection.

        :return: The number of deleted documents.
        """
        result = self.bus_stop_waypoints_collection.delete_many({})
        return result.deleted_count

    def clear_bus_stops(self):
        """
        Delete all the documents of the BusStops collection.

        :return: The number of deleted documents.
        """
        result = self.bus_stops_collection.delete_many({})
        return result.deleted_count

    def clear_edges(self):
        """
        Delete all the documents of the Edges collection.

        :return: The number of deleted documents.
        """
        result = self.edges_collection.delete_many({})
        return result.deleted_count

    def clear_nodes(self):
        """
        Delete all the documents of the Nodes collection.

        :return: The number of deleted documents.
        """
        result = self.nodes_collection.delete_many({})
        return result.deleted_count

    def clear_points(self):
        """
        Delete all the documents of the Points collection.

        :return: The number of deleted documents.
        """
        result = self.points_collection.delete_many({})
        return result.deleted_count

    def clear_timetables(self):
        """
        Delete all the documents of the Timetables collection.

        :return: The number of deleted documents.
        """
        result = self.timetables_collection.delete_many({})
        return result.deleted_count

    def clear_traffic_density(self):
        """
        Set the traffic_density values of all edge documents to 0.
        """
        key = {}
        data = {'$set': {'traffic_density': 0}}
        self.edges_collection.update_many(key, data, upsert=False)

    def clear_travel_requests(self):
        """
        Delete all the documents of the TravelRequests collection.

        :return: The number of deleted documents.
        """
        result = self.travel_requests_collection.delete_many({})
        return result.deleted_count

    def clear_ways(self):
        """
        Delete all the documents of the Ways collection.

        :return The number of deleted documents.
        """
        result = self.ways_collection.delete_many({})
        return result.deleted_count

    def delete_address_document(self, object_id=None, name=None):
        """
        Delete an address_document.

        address_document: {'_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param name: string
        :return: True if the address_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.address_book_collection.delete_one({'_id': ObjectId(object_id)})
        elif name is not None:
            result = self.address_book_collection.delete_one({'name': name})
        else:
            return False

        return result.deleted_count == 1

    def delete_address_documents(self, object_ids=None, names=None):
        """
        Delete multiple address_documents.

        address_document: {'_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param names: [string]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.address_book_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif names is not None:
            result = self.address_book_collection.delete_many({'name': {'$in': names}})
        else:
            return 0

        return result.deleted_count

    def delete_bus_line_document(self, object_id=None, line_id=None):
        """
        Delete a bus_line_document.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param object_id: ObjectId
        :param line_id: int
        :return: True if the bus_line_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.bus_lines_collection.delete_one({'_id': ObjectId(object_id)})
        elif line_id is not None:
            result = self.bus_lines_collection.delete_one({'line_id': line_id})
        else:
            return False

        return result.deleted_count == 1

    def delete_bus_line_documents(self, object_ids=None, line_ids=None):
        """
        Delete multiple bus_line_document.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param object_ids: [ObjectId]
        :param line_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.bus_lines_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif line_ids is not None:
            result = self.bus_lines_collection.delete_many({'line_id': {'$in': line_ids}})
        else:
            return 0

        return result.deleted_count

    def delete_bus_stop_document(self, object_id=None, osm_id=None):
        """
        Delete a bus_stop_document.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param osm_id: int
        :return: True if the bus_stop_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.bus_stops_collection.delete_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            result = self.bus_stops_collection.delete_one({'osm_id': osm_id})
        else:
            return False

        return result.deleted_count == 1

    def delete_bus_stop_documents(self, object_ids=None, osm_ids=None):
        """
        Delete multiple bus_stop_documents.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.bus_stops_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            result = self.bus_stops_collection.delete_many({'osm_id': {'$in': osm_ids}})
        else:
            return 0

        return result.deleted_count

    def delete_bus_stop_waypoints_document(self, object_id=None, starting_bus_stop=None, ending_bus_stop=None,
                                           starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Delete a bus_stop_waypoints_document.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param object_id: ObjectId
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return: True if the bus_stop_waypoints_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.bus_stop_waypoints_collection.delete_one({'_id': ObjectId(object_id)})
        elif starting_bus_stop is not None and ending_bus_stop is not None:
            result = self.bus_stop_waypoints_collection.delete_one({
                'starting_bus_stop._id': starting_bus_stop.get('_id'),
                'ending_bus_stop._id': ending_bus_stop.get('_id')
            })
        elif starting_bus_stop_name is not None and ending_bus_stop_name is not None:
            result = self.bus_stop_waypoints_collection.delete_one({
                'starting_bus_stop.name': starting_bus_stop_name,
                'ending_bus_stop.name': ending_bus_stop_name
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_bus_stop_waypoints_documents(self, object_ids):
        """
        Delete multiple bus_stop_waypoints_documents.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param object_ids: [ObjectId]
        :return: The number of deleted documents
        """
        processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
        result = self.bus_stop_waypoints_collection.delete_many({'_id': {'$in': processed_object_ids}})
        return result.deleted_count

    def delete_edge_document(self, object_id=None, starting_node_osm_id=None, ending_node_osm_id=None):
        """
        Delete an edge_document.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param object_id: ObjectId
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :return: True if the document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.edges_collection.delete_one({'_id': ObjectId(object_id)})
        elif starting_node_osm_id is not None and ending_node_osm_id is not None:
            result = self.edges_collection.delete_one({
                'starting_node.osm_id': starting_node_osm_id,
                'ending_node.osm_id': ending_node_osm_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_edge_documents(self, object_ids=None, starting_node_osm_id=None, ending_node_osm_id=None):
        """
        Delete multiple edge_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param object_ids: [ObjectId]
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.edges_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif starting_node_osm_id is not None:
            result = self.edges_collection.delete_many({'starting_node.osm_id': starting_node_osm_id})
        elif ending_node_osm_id is not None:
            result = self.edges_collection.delete_many({'ending_node.osm_id': ending_node_osm_id})
        else:
            return 0

        return result.deleted_count

    def delete_node_document(self, object_id=None, osm_id=None):
        """
        Delete a node_document.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param osm_id: int
        :return: True if node_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.nodes_collection.delete_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            result = self.nodes_collection.delete_one({'osm_id': osm_id})
        else:
            return False

        return result.deleted_count == 1

    def delete_node_documents(self, object_ids=None, osm_ids=None):
        """
        Delete multiple node_documents.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.nodes_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            result = self.nodes_collection.delete_many({'osm_id': {'$in': osm_ids}})
        else:
            return 0

        return result.deleted_count

    def delete_point_document(self, object_id=None, osm_id=None):
        """
        Delete a point_document.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param osm_id: int
        :return: True if the point_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.points_collection.delete_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            result = self.points_collection.delete_one({'osm_id': osm_id})
        else:
            return False

        return result.deleted_count == 1

    def delete_point_documents(self, object_ids=None, osm_ids=None):
        """
        Delete multiple point_document.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.points_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            result = self.points_collection.delete_many({'osm_id': {'$in': osm_ids}})
        else:
            return 0

        return result.deleted_count

    def delete_timetable_document(self, object_id):
        """
        Delete a timetable_document.

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
        :param object_id: ObjectId
        :return: True if the document was successfully deleted, otherwise False.
        """
        result = self.timetables_collection.delete_one({'_id': ObjectId(object_id)})
        return result.deleted_count == 1

    def delete_timetable_documents(self, object_ids=None, line_id=None):
        """
        Delete multiple timetable_documents.

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
        :param object_ids: [ObjectId]
        :param line_id: int
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.timetables_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif line_id is not None:
            result = self.timetables_collection.delete_many({'line_id': line_id})
        else:
            return 0

        return result.deleted_count

    def delete_travel_request_document(self, object_id):
        """
        Delete a travel_request_document.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime'
        }
        :param object_id: ObjectId
        :return: True if the travel_request_document was successfully deleted, otherwise False.
        """
        result = self.travel_requests_collection.delete_one({'_id': ObjectId(object_id)})
        return result.deleted_count == 1

    def delete_travel_request_documents(self, object_ids=None, line_ids=None, min_departure_datetime=None,
                                        max_departure_datetime=None):
        """
        Delete multiple travel_request_documents.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime'
        }
        :param object_ids: [ObjectId]
        :param line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.travel_requests_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif line_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            result = self.travel_requests_collection.delete_many({
                'line_id': {'$in': line_ids},
                'departure_time': {'$gt': min_departure_datetime},
                'departure_time': {'$lt': max_departure_datetime}
            })
        elif line_ids is not None:
            result = self.travel_requests_collection.delete_many({'line_id': {'$in': line_ids}})
        elif min_departure_datetime is not None and max_departure_datetime is not None:
            result = self.travel_requests_collection.delete_many({
                'departure_time': {'$gt': min_departure_datetime},
                'departure_time': {'$lt': max_departure_datetime}
            })
        else:
            return 0

        return result.deleted_count

    def delete_way_document(self, object_id=None, osm_id=None):
        """
        Delete a way_document.

        way_document: {'_id', 'osm_id', 'tags', 'references'}

        :param object_id: ObjectId
        :param osm_id: int
        :return: True if the way_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.ways_collection.delete_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            result = self.ways_collection.delete_one({'osm_id': osm_id})
        else:
            return False

        return result.deleted_count == 1

    def delete_way_documents(self, object_ids=None, osm_ids=None):
        """
        Delete multiple way_documents.

        way_document: {'_id', 'osm_id', 'tags', 'references'}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.ways_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            result = self.ways_collection.delete_many({'osm_id': {'$in': osm_ids}})
        else:
            return 0

        return result.deleted_count

    def find_address_document(self, object_id=None, name=None, node_id=None, longitude=None, latitude=None):
        """
        Retrieve an address_document.

        address_document: {'_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param name: string
        :param node_id: int
        :param longitude: float
        :param latitude: float
        :return: address_document
        """
        if object_id is not None:
            address_document = self.address_book_collection.find_one({'_id': ObjectId(object_id)})
        elif name is not None:
            address_document = self.address_book_collection.find_one({'name': name})
        elif node_id is not None:
            address_document = self.address_book_collection.find_one({'node_id': node_id})
        elif longitude is not None and latitude is not None:
            address_document = self.address_book_collection.find_one({
                'point': {'longitude': longitude, 'latitude': latitude}
            })
        else:
            return None

        return address_document

    def find_address_documents(self, object_ids=None, names=None, node_ids=None):
        """
        Retrieve multiple address_documents.

        address_document: {'_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param names: [string]
        :param node_ids: [int]
        :return: address_documents: [address_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            address_documents_cursor = self.address_book_collection.find({'_id': {'$in': processed_object_ids}})
        elif names is not None:
            address_documents_cursor = self.address_book_collection.find({'name': {'$in': names}})
        elif node_ids is not None:
            address_documents_cursor = self.address_book_collection.find({'node_id': {'$in': node_ids}})
        else:
            return None

        address_documents = list(address_documents_cursor)
        return address_documents

    def find_bus_line_document(self, object_id=None, line_id=None):
        """
        Retrieve a bus_line_document.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param object_id: ObjectId
        :param line_id: int
        :return: bus_line_document
        """
        if object_id is not None:
            bus_line_document = self.bus_lines_collection.find_one({'_id': ObjectId(object_id)})
        elif line_id is not None:
            bus_line_document = self.bus_lines_collection.find_one({'line_id': line_id})
        else:
            return None

        return bus_line_document

    def find_bus_line_documents(self, object_ids=None, line_ids=None):
        """
        Retrieve multiple bus_line_documents.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param object_ids: [ObjectId]
        :param line_ids: [int]
        :return: bus_line_documents: [bus_line_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            bus_line_documents_cursor = self.bus_lines_collection.find({'_id': {'$in': processed_object_ids}})
        elif line_ids is not None:
            bus_line_documents_cursor = self.bus_lines_collection.find({'line_id': {'$in': line_ids}})
        else:
            return None

        bus_line_documents = list(bus_line_documents_cursor)
        return bus_line_documents

    def find_bus_stop_document(self, object_id=None, osm_id=None, name=None, longitude=None, latitude=None):
        """
        Retrieve a bus_stop_document.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param osm_id: int
        :param name: string
        :param longitude: float
        :param latitude: float
        :return: bus_stop_document
        """
        if object_id is not None:
            bus_stop_document = self.bus_stops_collection.find_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            bus_stop_document = self.bus_stops_collection.find_one({'osm_id': osm_id})
        elif name is not None:
            bus_stop_document = self.bus_stops_collection.find_one({'name': name})
        elif longitude is not None and latitude is not None:
            bus_stop_document = self.bus_stops_collection.find_one({
                'point': {'longitude': longitude, 'latitude': latitude}
            })
        else:
            return None

        return bus_stop_document

    def find_bus_stop_documents(self, object_ids=None, osm_ids=None, names=None):
        """
        Retrieve multiple bus_stop_documents.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param names: [string]
        :return: bus_stop_documents: [bus_stop_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            bus_stop_documents_cursor = self.bus_stops_collection.find({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            bus_stop_documents_cursor = self.bus_stops_collection.find({'osm_id': {'$in': osm_ids}})
        elif names is not None:
            bus_stop_documents_cursor = self.bus_stops_collection.find({'name': {'$in': names}})
        else:
            return None

        bus_stop_documents = list(bus_stop_documents_cursor)
        return bus_stop_documents

    def find_bus_stop_waypoints_document(self, object_id=None, starting_bus_stop=None, ending_bus_stop=None,
                                         starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Retrieve a bus_stop_waypoints_document.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param object_id: ObjectId
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return: bus_stop_waypoints_document
        """
        if object_id is not None:
            bus_stop_waypoints_document = self.bus_stop_waypoints_collection.find_one({'_id': ObjectId(object_id)})
        elif starting_bus_stop is not None and ending_bus_stop is not None:
            bus_stop_waypoints_document = self.bus_stop_waypoints_collection.find_one({
                'starting_bus_stop._id': starting_bus_stop.get('_id'),
                'ending_bus_stop._id': ending_bus_stop.get('_id')
            })
        elif starting_bus_stop_name is not None and ending_bus_stop_name is not None:
            bus_stop_waypoints_document = self.bus_stop_waypoints_collection.find_one({
                'starting_bus_stop.name': starting_bus_stop_name,
                'ending_bus_stop.name': ending_bus_stop_name
            })
        else:
            return None

        return bus_stop_waypoints_document

    def find_detailed_bus_stop_waypoints_document(self, object_id=None, starting_bus_stop=None, ending_bus_stop=None,
                                                  starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Retrieve a detailed_bus_stop_waypoints_document.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        detailed_bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_document]]
        }
        :param object_id: ObjectId
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return: detailed_bus_stop_waypoints_document
        """
        bus_stop_waypoints_document = self.find_bus_stop_waypoints_document(
            object_id=object_id,
            starting_bus_stop=starting_bus_stop,
            ending_bus_stop=ending_bus_stop,
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )
        detailed_bus_stop_waypoints_document = self.get_detailed_waypoints_from_waypoints(
            bus_stop_waypoints=bus_stop_waypoints_document
        )
        return detailed_bus_stop_waypoints_document

    def find_edge_document(self, object_id=None, starting_node_osm_id=None, ending_node_osm_id=None):
        """
        Retrieve an edge_document.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param object_id: ObjectId
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :return: edge_document
        """
        if object_id is not None:
            edge_document = self.edges_collection.find_one({'_id': ObjectId(object_id)})
        elif starting_node_osm_id is not None and ending_node_osm_id is not None:
            edge_document = self.edges_collection.find_one({
                'starting_node.osm_id': starting_node_osm_id,
                'ending_node.oms_id': ending_node_osm_id}
            )
        else:
            return None

        return edge_document

    def find_edge_documents(self, object_ids=None, starting_node_osm_id=None, ending_node_osm_id=None):
        """
        Retrieve multiple edge_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param object_ids: [ObjectId]
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :return: edge_documents: [edge_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            edge_documents_cursor = self.edges_collection.find({'_id': {'$in': processed_object_ids}})
        elif starting_node_osm_id is not None:
            edge_documents_cursor = self.edges_collection.find({'starting_node.osm_id': starting_node_osm_id})
        elif ending_node_osm_id is not None:
            edge_documents_cursor = self.edges_collection.find({'ending_node.oms_id': ending_node_osm_id})
        else:
            return None

        edge_documents = list(edge_documents_cursor)
        return edge_documents

    def find_node_document(self, object_id=None, osm_id=None, longitude=None, latitude=None):
        """
        Retrieve a node_document.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param osm_id: int
        :param longitude: float
        :param latitude: float
        :return: node_document
        """
        if object_id is not None:
            node_document = self.nodes_collection.find_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            node_document = self.nodes_collection.find_one({'osm_id': osm_id})
        elif longitude is not None and latitude is not None:
            node_document = self.nodes_collection.find_one({
                'point': {'longitude': longitude, 'latitude': latitude}
            })
        else:
            return None

        return node_document

    def find_node_documents(self, object_ids=None, osm_ids=None):
        """
        Retrieve multiple node_documents.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: node_documents: [node_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            node_documents_cursor = self.nodes_collection.find({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            node_documents_cursor = self.nodes_collection.find({'osm_id': {'$in': osm_ids}})
        else:
            return None

        node_documents = list(node_documents_cursor)
        return node_documents

    def find_point_document(self, object_id=None, osm_id=None, longitude=None, latitude=None):
        """
        Retrieve a point_document.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param osm_id: int
        :param longitude: float
        :param latitude: float
        :return: point_document
        """
        if object_id is not None:
            point_document = self.points_collection.find_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            point_document = self.points_collection.find_one({'osm_id': osm_id})
        elif longitude is not None and latitude is not None:
            point_document = self.points_collection.find_one({
                'point': {'longitude': longitude, 'latitude': latitude}
            })
        else:
            return None

        return point_document

    def find_point_documents(self, object_ids=None, osm_ids=None):
        """
        Retrieve multiple point_documents.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: point_documents: [point_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            point_documents_cursor = self.points_collection.find({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            point_documents_cursor = self.points_collection.find({'osm_id': {'$in': osm_ids}})
        else:
            return None

        point_documents = list(point_documents_cursor)
        return point_documents

    def find_timetable_document(self, object_id):
        """
        Retrieve a timetable_document.

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
        :param object_id: ObjectId
        :return: timetable_document
        """
        timetable_document = self.timetables_collection.find_one({'_id': ObjectId(object_id)})
        return timetable_document

    def find_timetable_documents(self, object_ids=None, line_ids=None):
        """
        Retrieve multiple timetable_documents.

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
        :param object_ids: [ObjectId]
        :param line_ids: [int]
        :return: timetable_documents: [timetable_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            timetable_documents_cursor = self.timetables_collection.find({'_id': {'$in': processed_object_ids}})
        elif line_ids is not None:
            timetable_documents_cursor = self.timetables_collection.find({'line_id': {'$in': line_ids}})
        else:
            return None

        timetable_documents = list(timetable_documents_cursor)
        return timetable_documents

    def find_travel_request_document(self, object_id):
        """
        Retrieve a travel_request_document.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime'
        }
        :param object_id: ObjectId
        :return: travel_request_document
        """
        travel_request_document = self.travel_requests_collection.find_one({'_id': ObjectId(object_id)})
        return travel_request_document

    def find_travel_request_documents(self, object_ids=None, line_ids=None, min_departure_datetime=None,
                                      max_departure_datetime=None):
        """
        Retrieve multiple travel_request_documents.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime'
        }
        :param object_ids: [ObjectId]
        :param line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :return: travel_request_documents: [travel_request_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            travel_requests_cursor = self.travel_requests_collection.find({'_id': {'$in': processed_object_ids}})
        elif line_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            travel_requests_cursor = self.travel_requests_collection.find({
                'line_id': {'$in': line_ids},
                'departure_time': {'$gt': min_departure_datetime},
                'departure_time': {'$lt': max_departure_datetime}
            })
        elif line_ids is not None:
            travel_requests_cursor = self.travel_requests_collection.find({'line_id': {'$in': line_ids}})
        elif min_departure_datetime is not None and max_departure_datetime is not None:
            travel_requests_cursor = self.travel_requests_collection.find({
                'departure_time': {'$gt': min_departure_datetime},
                'departure_time': {'$lt': max_departure_datetime}
            })
        else:
            return None

        travel_requests = list(travel_requests_cursor)
        return travel_requests

    def find_way_document(self, object_id=None, osm_id=None):
        """
        Retrieve a way_document.

        way_document: {'_id', 'osm_id', 'tags', 'references'}

        :param object_id: ObjectId
        :param osm_id: int
        :return: way_document
        """
        if object_id is not None:
            way_document = self.ways_collection.find_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            way_document = self.ways_collection.find_one({'osm_id': osm_id})
        else:
            return None

        return way_document

    def find_way_documents(self, object_ids=None, osm_ids=None):
        """
        Retrieve multiple way_documents.

        way_document: {'_id', 'osm_id', 'tags', 'references'}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: way_documents: [way_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            way_documents_cursor = self.ways_collection.find({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            way_documents_cursor = self.ways_collection.find({'osm_id': {'$in': osm_ids}})
        else:
            return None

        way_documents = list(way_documents_cursor)
        return way_documents

    def get_bus_line_documents_cursor(self):
        """
        Retrieve a cursor of all bus_line_documents.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :return: bus_line_documents_cursor
        """
        bus_line_documents_cursor = self.bus_lines_collection.find({})
        return bus_line_documents_cursor

    def get_bus_line_documents_dictionary(self):
        """
        Retrieve a dictionary containing all the bus_line_documents.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :return: bus_line_documents_dictionary: {line_id -> bus_line_document}
        """
        bus_line_documents_dictionary = {}
        bus_line_documents_cursor = self.get_bus_line_documents_cursor()

        for bus_line_document in bus_line_documents_cursor:
            line_id = bus_line_document.get('line_id')
            bus_line_documents_dictionary[line_id] = bus_line_document

        return bus_line_documents_dictionary

    def get_bus_line_documents_list(self):
        """
        Retrieve a list containing all the bus_line_documents.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :return: bus_line_documents_list: [bus_line_document]
        """
        bus_line_documents_cursor = self.get_bus_line_documents_cursor()
        bus_line_documents_list = list(bus_line_documents_cursor)
        return bus_line_documents_list

    def get_bus_stop_documents_cursor(self):
        """
        Retrieve a cursor of all bus_stop_documents.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :return: bus_stop_documents_cursor
        """
        bus_stop_documents_cursor = self.bus_stops_collection.find({})
        return bus_stop_documents_cursor

    def get_bus_stop_documents_dictionary(self):
        """
        Retrieve a dictionary containing all the bus_stop_documents.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :return: bus_stop_documents_dictionary: {name -> bus_stop_document}
        """
        bus_stop_documents_dictionary = {}
        bus_stop_documents_cursor = self.get_bus_stop_documents_cursor()

        for bus_stop_document in bus_stop_documents_cursor:
            name = bus_stop_document.get('name')

            if name not in bus_stop_documents_dictionary:
                bus_stop_documents_dictionary[name] = bus_stop_document

        return bus_stop_documents_dictionary

    def get_bus_stop_documents_list(self):
        """
        Retrieve a list containing all the bus_stop_documents.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :return: bus_stop_documents_list: [bus_stop_document]
        """
        bus_stop_documents_cursor = self.get_bus_stop_documents_cursor()
        bus_stop_documents_list = list(bus_stop_documents_cursor)
        return bus_stop_documents_list

    def get_edge_documents_cursor(self):
        """
        Retrieve a cursor of all the edge_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :return: edge_documents_cursor
        """
        edge_documents_cursor = self.edges_collection.find({})
        return edge_documents_cursor

    def get_edges_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Edges collection.

        edge_document: {'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                        'max_speed', 'road_type', 'way_id', 'traffic_density'}

        :return: edges_dictionary: {starting_node_osm_id -> [edge_document]}
        """
        edges_dictionary = {}
        edges_cursor = self.get_edge_documents_cursor()

        for edge_document in edges_cursor:
            starting_node_osm_id = edge_document.get('starting_node').get('osm_id')

            if starting_node_osm_id in edges_dictionary:
                edges_dictionary[starting_node_osm_id].append(edge_document)
            else:
                edges_dictionary[starting_node_osm_id] = [edge_document]

        return edges_dictionary

    def get_edges_list(self):
        """
        Retrieve a list containing all the documents of the Edges collection.

        edge_document: {'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                        'max_speed', 'road_type', 'way_id', 'traffic_density'}

        :return: edges_list: [edge_document]
        """
        edges_list = list(self.get_edge_documents_cursor())
        return edges_list

    def get_edges_cursor_from_starting_node_osm_id(self, starting_node_osm_id):
        """
        Retrieve a cursor of the edge documents, based on the osm_id of the starting node.

        edge_document: {'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                        'max_speed', 'road_type', 'way_id', 'traffic_density'}

        :param starting_node_osm_id: osm_id (int)
        :return: edges_cursor -> edge_document
        """
        edges_cursor = self.edges_collection.find({'starting_node.osm_id': starting_node_osm_id})
        return edges_cursor

    def get_edges_list_from_starting_node_osm_id(self, starting_node_osm_id):
        """
        Retrieve a list containing the edge documents, based on the osm_id of the starting node.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param starting_node_osm_id: osm_id (int)
        :return: edges_list: [edge_document]
        """
        edges_cursor = self.edges_collection.find({'starting_node.osm_id': starting_node_osm_id})
        edges_list = list(edges_cursor)
        return edges_list

    def get_edges_list_of_bus_line(self, line_id):
        """
        Get a list containing all the edge_documents which are contained in the waypoints of a bus_line.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param line_id: int
        :return: edges_list: [edge_document]
        """
        edge_object_ids_list = []
        bus_line = self.find_bus_line_document(line_id=line_id)
        bus_stops = bus_line.get('bus_stops')
        number_of_bus_stops = len(bus_stops)

        for i in range(0, number_of_bus_stops - 1):
            starting_bus_stop = bus_stops[i]
            ending_bus_stop = bus_stops[i + 1]

            bus_stop_waypoints = self.find_bus_stop_waypoints_document(
                starting_bus_stop=starting_bus_stop,
                ending_bus_stop=ending_bus_stop
            )
            edge_object_ids = self.get_edge_object_ids_list_of_bus_stop_waypoints(
                bus_stop_waypoints=bus_stop_waypoints
            )
            for edge_object_id in edge_object_ids:
                if edge_object_id not in edge_object_ids_list:
                    edge_object_ids_list.append(edge_object_id)

        edges_list = self.get_edges_list_from_edge_object_ids_list(
            edge_object_ids_list=edge_object_ids_list
        )
        return edges_list

    def get_edges_list_of_bus_stop_waypoints(self, bus_stop_waypoints):
        """
        Get a list containing all the edge_documents which are included in a bus_stop_waypoints document.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param bus_stop_waypoints: bus_stop_waypoints_document
        :return: edges_list: [edge_document]
        """

        list_of_all_edge_object_ids = self.get_edge_object_ids_list_of_bus_stop_waypoints(
            bus_stop_waypoints=bus_stop_waypoints
        )
        edges_list = self.get_edges_list_from_edge_object_ids_list(
            edge_object_ids_list=list_of_all_edge_object_ids
        )
        return edges_list

    def get_edges_list_from_edge_object_ids_list(self, edge_object_ids_list):
        """
        Get a list of edge_documents, based on their object_ids.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param edge_object_ids_list: [edge_object_id]
        :return: edges_list: [edge_document]
        """
        edges_list = []

        for edge_object_id in edge_object_ids_list:
            edge = self.find_edge_document(edge_object_id=edge_object_id)
            edges_list.append(edge)

        return edges_list

    @staticmethod
    def get_edge_object_ids_list_of_bus_stop_waypoints(bus_stop_waypoints):
        """
        Get a list containing all the object_ids of the edge_documents,
        which are included in a bus_stop_waypoints document.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param bus_stop_waypoints: bus_stop_waypoints_document
        :return: list_of_all_edge_object_ids: [edge_object_id]
        """
        list_of_all_edge_object_ids = []
        lists_of_edge_object_ids = bus_stop_waypoints.get('waypoints')

        for list_of_edge_object_ids in lists_of_edge_object_ids:
            for edge_object_id in list_of_edge_object_ids:
                if edge_object_id not in list_of_all_edge_object_ids:
                    list_of_all_edge_object_ids.append(edge_object_id)

        return list_of_all_edge_object_ids

    def get_ending_nodes_of_edges_dictionary(self):
        """
        Retrieve a dictionary containing all the ending_nodes which are included in the Edges collection.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :return: ending_nodes_dictionary: {ending_node_osm_id -> [edge_document]}
        """
        ending_nodes_dictionary = {}
        edges_cursor = self.get_edge_documents_cursor()

        for edges_document in edges_cursor:
            ending_node_osm_id = edges_document.get('ending_node').get('osm_id')

            if ending_node_osm_id in ending_nodes_dictionary:
                ending_nodes_dictionary[ending_node_osm_id].append(edges_document)
            else:
                ending_nodes_dictionary[ending_node_osm_id] = [edges_document]

        return ending_nodes_dictionary

    def get_nodes(self):
        """
        Retrieve all the documents of the Nodes collection.

        :return: Cursor -> {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}
        """
        cursor = self.nodes_collection.find({})
        return cursor

    def get_points(self):
        """
        Retrieve all the documents of the Points collection.

        :return: Cursor -> {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}
        """
        cursor = self.points_collection.find({})
        return cursor

    def get_points_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Points collection.

        :return points_dictionary: {osm_id -> {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}}
        """
        points_dictionary = {}
        points_cursor = self.get_points()
        # Cursor -> {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        for point_document in points_cursor:
            osm_id = point_document.get('osm_id')
            points_dictionary[osm_id] = point_document

        return points_dictionary

    def get_timetables_of_bus_line(self, line_id):
        """
        Retrieve a cursor containing all the documents of the Timetables collection,
        with a specific 'line_id' entry.

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
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

        :param line_id: int
        :return: Cursor -> timetable document
        """
        timetables_cursor = self.timetables_collection.find({'line_id': line_id})
        return timetables_cursor

    def get_timetables_of_bus_line_list(self, line_id):
        """
        Retrieve a list containing all the documents of the Timetables collection,
        with a specific 'line_id' entry.

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
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

        :param line_id: int
        :return: timetables_list: [timetable document]
        """
        timetables_cursor = self.get_timetables_of_bus_line(line_id=line_id)
        timetables_list = list(timetables_cursor)
        return timetables_list

    def get_traffic_density_between_two_bus_stop_names(self, starting_bus_stop_name, ending_bus_stop_name):
        """

        :param starting_bus_stop_name:
        :param ending_bus_stop_name:
        :return: {'_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                  'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                  'waypoints': [[{'edge_object_id', 'traffic_density'}]]}
        """
        bus_stop_waypoints = self.find_bus_stop_waypoints_document(
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )
        # {'_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #  'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #  'waypoints': [[edge_object_id]]}

        lists_of_edge_object_ids = bus_stop_waypoints.get('waypoints')
        lists_of_edge_traffic = []

        for list_of_edge_object_ids in lists_of_edge_object_ids:
            list_of_edge_object_ids = [ObjectId(i) for i in list_of_edge_object_ids]
            list_of_detailed_edges = [self.edges_collection.find_one({'_id': i}) for i in list_of_edge_object_ids]
            list_of_edge_traffic = [{'edge_object_id': i.get('_id'), 'traffic_density': i.get('traffic_density')}
                                    for i in list_of_detailed_edges]
            lists_of_edge_traffic.append(list_of_edge_traffic)

        bus_stop_waypoints['waypoints'] = lists_of_edge_traffic
        return bus_stop_waypoints

    def get_travel_requests_cursor(self):
        """
        Retrieve a cursor of all the documents of the TravelRequests collection.

        :return: Cursor -> {'_id', 'client_id', 'line_id', 'starting_bus_stop',
                            'ending_bus_stop', 'departure_datetime', 'arrival_datetime'}
        """
        cursor = self.travel_requests_collection.find({})
        return cursor

    def get_travel_requests_list(self):
        """
        Retrieve a list containing all the documents of the TravelRequests collection.

        :return: [{'_id', 'client_id', 'line_id', 'starting_bus_stop',
                   'ending_bus_stop', 'departure_datetime', 'arrival_datetime'}]
        """
        travel_requests_list = list(self.get_travel_requests_cursor())
        return travel_requests_list

    def get_travel_requests_cursor_based_on_line_id(self, line_id):
        """
        Retrieve a cursor of all the documents of the TravelRequests collection, based on the line_id entry.

        :param line_id: int
        :return: Cursor -> {'_id', 'client_id', 'line_id', 'starting_bus_stop',
                            'ending_bus_stop', 'departure_datetime', 'arrival_datetime'}
        """
        cursor = self.travel_requests_collection.find({'line_id': line_id})
        return cursor

    def get_travel_requests_cursor_based_on_departure_datetime(self, min_departure_datetime, max_departure_datetime):
        """
        Retrieve a cursor of all the documents of the TravelRequests collection,
        based on the departure_datetime entry.

        :param min_departure_datetime: datetime
        :param max_departure_datetime: datetime
        :return: Cursor -> {'_id', 'client_id', 'line_id', 'starting_bus_stop',
                            'ending_bus_stop', 'departure_datetime', 'arrival_datetime'}
        """
        # cursor = self.travel_requests_collection.find(
        #     {'departure_datetime': {'$and': [
        #         {'$gt': min_departure_datetime},
        #         {'$lt': max_departure_datetime}
        #     ]}})
        cursor = self.travel_requests_collection.find({
            'departure_time': {'$gt': min_departure_datetime},
            'departure_time': {'$lt': max_departure_datetime}
        })
        return cursor

    def get_travel_requests_cursor_based_on_line_id_and_departure_datetime(
            self, line_id, min_departure_datetime, max_departure_datetime):
        """
        Retrieve a cursor of all the documents of the TravelRequests collection,
        based on the line_id and departure_datetime entries.

        :param line_id: int
        :param min_departure_datetime: datetime
        :param max_departure_datetime: datetime
        :return: Cursor -> {'_id', 'client_id', 'line_id', 'starting_bus_stop',
                            'ending_bus_stop', 'departure_datetime', 'arrival_datetime'}
        """
        # cursor = self.travel_requests_collection.find({'$and': [
        #     {'line_id': line_id},
        #     {'departure_datetime': {'$and': [
        #         {'$gt': min_departure_datetime},
        #         {'$lt': max_departure_datetime}
        #     ]}}
        # ]})
        cursor = self.travel_requests_collection.find({
            'line_id': line_id,
            'departure_datetime': {'$gt': min_departure_datetime},
            'departure_datetime': {'$lt': max_departure_datetime}
        })
        return cursor

    def get_travel_requests_list_based_on_line_id_and_departure_datetime(
            self, line_id, min_departure_datetime, max_departure_datetime):
        """
        Retrieve a list containing all the documents of the TravelRequests collection,
        based on the line_id and departure_datetime entries.

        :param line_id: int
        :param min_departure_datetime: datetime
        :param max_departure_datetime: datetime
        :return: [{'_id', 'client_id', 'line_id', 'starting_bus_stop',
                   'ending_bus_stop', 'departure_datetime', 'arrival_datetime'}]
        """
        cursor = self.get_travel_requests_cursor_based_on_line_id_and_departure_datetime(
            line_id=line_id,
            min_departure_datetime=min_departure_datetime,
            max_departure_datetime=max_departure_datetime
        )
        return list(cursor)

    def has_edges(self, node_osm_id):
        """
        Check if a node exists in the Edges collection as a starting node.

        :param node_osm_id: int
        :return: True if exists, otherwise False.
        """
        return self.edges_collection.find_one({'starting_node.osm_id': node_osm_id}) is not None

    def in_edges(self, node_osm_id):
        """
        Check if a node exists in the Edges collection, either as a starting or an ending node.

        :param node_osm_id: int
        :return: True if exists, otherwise False.
        """
        return self.edges_collection.find_one({'$or': [{'starting_node.osm_id': node_osm_id},
                                                       {'ending_node.osm_id': node_osm_id}]}) is not None

    def insert_address(self, name, node_id, point):
        """
        Insert an address document to the AddressBook collection.

        :param name: string
        :param node_id: int
        :param point: Point
        :return: The ObjectId of the inserted document.
        """
        document = {'name': name, 'node_id': node_id,
                    'point': {'longitude': point.longitude, 'latitude': point.latitude}}

        result = self.address_book_collection.insert_one(document)
        return result.inserted_id

    def insert_addresses(self, address_book):
        """
        Insert a list of address documents to the AddressBook collection.

        :param address_book: [{'name', 'node_id', 'point': {'longitude', 'latitude'}}]
        :return: [ObjectId]
        """
        result = self.address_book_collection.insert_many(address_book)
        return result.inserted_ids

    def insert_bus_line(self, line_id, bus_stops):
        """
        Insert a bus_line document to the BusLines collection, or update the bus_stops
        if the document already exists in the database.

        :param line_id: int
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :return: The ObjectId if a new document was inserted.
        """
        # document = {'line_id': line_id, 'bus_stops': bus_stops}
        # result = self.bus_lines_collection.insert_one(document)
        key = {'line_id': line_id}
        data = {'$set': {'bus_stops': bus_stops}}
        result = self.bus_lines_collection.update_one(key, data, upsert=True)
        return result.upserted_id

    def insert_bus_lines(self, bus_lines):
        """
        Insert a list of bus_line documents to the BusLines collection.

        :param bus_lines: [{'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}]
        :return: [ObjectId]
        """
        result = self.bus_lines_collection.insert_many(bus_lines)
        return result.inserted_ids

    def insert_bus_stop(self, osm_id, name, point):
        """
        Insert a bus_stop document to the BusStops collection.

        :param osm_id: int
        :param name: string
        :param point: Point
        :return: The ObjectId of the inserted document.
        """
        document = {'osm_id': osm_id, 'name': name,
                    'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        result = self.bus_stops_collection.insert_one(document)
        return result.inserted_id

    def insert_bus_stops(self, bus_stops):
        """
        Insert a list of bus_stop documents to the BusStops collection.

        :param bus_stops: [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :return: [ObjectId]
        """
        result = self.bus_stops_collection.insert_many(bus_stops)
        return result.inserted_ids

    def insert_bus_stop_waypoints(self, starting_bus_stop, ending_bus_stop, waypoints):
        """
        Insert a new document to the BusStopWaypoints collection, or update the waypoints
        if the document already exists in the database.

        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param waypoints: [[edge_object_id]]
        :return: The ObjectId, if a new document was inserted.
        """
        key = {'starting_bus_stop': starting_bus_stop, 'ending_bus_stop': ending_bus_stop}
        data = {'$set': {'waypoints': waypoints}}
        result = self.bus_stop_waypoints_collection.update_one(key, data, upsert=True)
        return result.upserted_id

    def insert_edge(self, starting_node, ending_node, max_speed, road_type, way_id, traffic_density):
        """
        Insert an edge document to the Edges collection.

        :param starting_node: {'osm_id', 'point': {'longitude', 'latitude'}}
        :param ending_node: {'osm_id', 'point': {'longitude', 'latitude'}}
        :param max_speed: float or int
        :param road_type: string
        :param way_id: osm_id: int
        :param traffic_density: A value between 0 and 1 indicating the density of traffic: float
        :return: The Object Id of the inserted document.
        """
        document = {'starting_node': starting_node, 'ending_node': ending_node, 'max_speed': max_speed,
                    'road_type': road_type, 'way_id': way_id, 'traffic_density': traffic_density}
        result = self.edges_collection.insert_one(document)
        return result.inserted_id

    def insert_edges(self, edge_documents):
        """
        Insert a list of edge documents to the Edges collection.

        :param edge_documents: [{'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                 'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                 'max_speed', 'road_type', 'way_id', 'traffic_density'}]
        :return: [ObjectId]
        """
        result = self.edges_collection.insert_many(edge_documents)
        return result.inserted_ids

    def insert_node(self, osm_id, tags, point):
        """
        Insert a node document to the Nodes collection.

        :param osm_id: int
        :param tags: {}
        :param point: Point
        :return: The ObjectId of the inserted document.
        """
        document = {'osm_id': osm_id, 'tags': tags,
                    'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        result = self.nodes_collection.insert_one(document)
        return result.inserted_id

    def insert_nodes(self, node_documents):
        """
        Insert a list of node documents to the Nodes dictionary.

        :param node_documents: [{'osm_id', 'tags', 'point': {'longitude', 'latitude'}}]
        :return: [ObjectId]
        """
        result = self.nodes_collection.insert_many(node_documents)
        return result.inserted_ids

    def insert_point(self, osm_id, point):
        """
        Insert a point document to the Points collection.

        :param osm_id: int
        :param point: Point
        :return: The ObjectId of the inserted document.
        """
        document = {'osm_id': osm_id, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        result = self.points_collection.insert_one(document)
        return result.inserted_id

    def insert_points(self, point_documents):
        """
        Insert a list of point documents to the Points collection.

        :param point_documents: [{'osm_id', 'point': {'longitude', 'latitude'}}]
        :return: [ObjectId]
        """
        result = self.points_collection.insert_many(point_documents)
        return result.inserted_ids

    def insert_timetable(self, timetable):
        """
        Insert a new document to the Timetables collection, or update the
        corresponding document if it already exists in the database.

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
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

        :param timetable: timetable_document
        :return: The ObjectId, if a new document was inserted.
        """
        key = {'_id': timetable.get('_id')}
        data = {'$set': {
            'line_id': timetable.get('line_id'),
            'timetable_entries': timetable.get('timetable_entries'),
            'travel_requests': timetable.get('travel_requests')
        }}
        result = self.timetables_collection.update_one(key, data, upsert=True)
        return result.upserted_id

    def insert_timetables(self, timetables):
        """
        Insert multiple new documents to the Timetables collection, or update the
        corresponding documents if they already exist in the database.

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
                'starting_timetable_entry_index', 'ending_timetable_entry_index'}]}

        :param timetables: [timetable_document]
        :return: None
        """
        for timetable in timetables:
            self.insert_timetable(timetable=timetable)

    def insert_travel_request(self, client_id, line_id, starting_bus_stop, ending_bus_stop,
                              departure_datetime, arrival_datetime):
        """
        Insert a new document to the TravelRequests collection.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime'
        }
        :param client_id: int
        :param line_id: int
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param departure_datetime: datetime
        :param arrival_datetime: datetime
        :return: The ObjectId of the inserted document.
        """
        document = {'client_id': client_id, 'line_id': line_id,
                    'starting_bus_stop': starting_bus_stop, 'ending_bus_stop': ending_bus_stop,
                    'departure_datetime': departure_datetime, 'arrival_datetime': arrival_datetime}
        result = self.travel_requests_collection.insert_one(document)
        return result.inserted_id

    def insert_travel_request_documents(self, travel_request_documents):
        """
        Insert multiple documents to the TravelRequests collection.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime'
        }
        :param travel_request_documents: [{'client_id', 'line_id', 'starting_bus_stop', 'ending_bus_stop',
                                           'departure_datetime', 'arrival_datetime'}]
        :return: [ObjectId]
        """
        result = self.travel_requests_collection.insert_many(travel_request_documents)
        return result.inserted_ids

    def insert_way(self, osm_id, tags, references):
        """
        Insert a way document to the Ways collection.

        :param osm_id: int
        :param tags: {}
        :param references: [osm_id]
        :return: The ObjectId of the inserted document.
        """
        document = {'osm_id': osm_id, 'tags': tags, 'references': references}
        result = self.ways_collection.insert_one(document)
        return result.inserted_id

    def insert_ways(self, way_documents):
        """
        Insert a list of way documents to the Ways dictionary.

        :param way_documents: [{'osm_id', 'tags', 'references'}]
        :return: [ObjectId]
        """
        result = self.ways_collection.insert_many(way_documents)
        return result.inserted_ids

    def update_traffic_density(self, edge_object_id, new_traffic_density):
        """
        Update the traffic_density value of an edge document.
        edge_document: {'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                        'max_speed', 'road_type', 'way_id', 'traffic_density'}

        :param edge_object_id: ObjectId of edge document
        :param new_traffic_density: float [0, 1]
        :return: True if an edge_document was updated, otherwise False.
        """
        key = {'_id': ObjectId(edge_object_id)}
        data = {'$set': {'traffic_density': new_traffic_density}}
        result = self.edges_collection.update_one(key, data, upsert=False)
        return result.modified_count == 1

    def print_bus_stops(self, counter):
        """
        Print up to a specific number of bus_stop documents.

        :param counter: int
        """
        documents_cursor = self.get_bus_stop_documents_cursor()
        i = 0

        # Cursor -> {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        for document in documents_cursor:
            if i < counter:
                print document
                i += 1
            else:
                break

        print 'Total number of bus_stop documents: ' + str(documents_cursor.count())

    def print_edges(self, counter):
        """
        Print up to a specific number of edge documents.

        :param counter: int
        """
        documents_cursor = self.get_edge_documents_cursor()
        i = 0

        # Cursor -> {'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #            'max_speed', 'road_type', 'way_id', 'traffic_density'}
        for document in documents_cursor:
            if i < counter:
                print document
                i += 1
            else:
                break

        print 'Total number of edge documents: ' + str(documents_cursor.count())

    def print_nodes(self, counter):
        """
        Print up to a specific number of node documents.

        :param counter: int
        """
        documents_cursor = self.get_nodes()
        i = 0

        # Cursor -> {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}
        for document in documents_cursor:
            if i < counter:
                print document
                i += 1
            else:
                break

        print 'Total number of node documents: ' + str(documents_cursor.count())

    def print_bus_line(self, line_id):
        """
        Print a bus_line document based on the line_id.

        :param line_id: int
        """
        document = self.find_bus_line_document(line_id=line_id)
        print document

        bus_stops = document.get('bus_stops')
        for bus_stop in bus_stops:
            print bus_stop

    def print_bus_lines(self, counter):
        """
        Print up to a specific number of bus_line documents.

        :param counter: int
        """
        documents_cursor = self.get_bus_line_documents_cursor()
        i = 0

        # Cursor -> {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        for document in documents_cursor:
            if i < counter:
                print document
                i += 1
            else:
                break

        print 'Total number of bus_line documents: ' + str(documents_cursor.count())

    def print_bus_line_waypoints(self, line_id):
        """
        :param line_id: int
        """
        # {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        bus_line_document = self.find_bus_line_document(line_id=line_id)
        bus_stops = bus_line_document.get('bus_stops')

        bus_stop_names = [bus_stop.get('name') for bus_stop in bus_stops]
        self.print_waypoints_between_multiple_bus_stops(bus_stop_names=bus_stop_names)

    def print_detailed_bus_line_waypoints(self, line_id):
        """
        :param line_id: int
        """
        # {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        bus_line_document = self.find_bus_line_document(line_id=line_id)
        bus_stops = bus_line_document.get('bus_stops')

        bus_stop_names = [bus_stop.get('name') for bus_stop in bus_stops]
        self.print_detailed_waypoints_between_multiple_bus_stops(bus_stop_names=bus_stop_names)

    def print_waypoints_between_two_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        """
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        """
        bus_stop_waypoints = self.find_bus_stop_waypoints_document(
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )
        # {'_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #  'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #  'waypoints': [[edge_object_id]]}

        starting_bus_stop = bus_stop_waypoints.get('starting_bus_stop')
        ending_bus_stop = bus_stop_waypoints.get('ending_bus_stop')
        waypoints = bus_stop_waypoints.get('waypoints')

        print '\nstarting_bus_stop: ' + str(starting_bus_stop) + \
              '\nending_bus_stop: ' + str(ending_bus_stop)

        for alternative_waypoints in waypoints:
            print 'alternative_waypoints: ' + str(alternative_waypoints)

    def print_detailed_waypoints_between_two_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        """
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        """
        bus_stop_waypoints = self.find_detailed_bus_stop_waypoints_document(
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )
        # {'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #  'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #  'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #                  'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #                  'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}

        starting_bus_stop = bus_stop_waypoints.get('starting_bus_stop')
        ending_bus_stop = bus_stop_waypoints.get('ending_bus_stop')
        waypoints = bus_stop_waypoints.get('waypoints')

        print '\nstarting_bus_stop: ' + str(starting_bus_stop) + \
              '\nending_bus_stop: ' + str(ending_bus_stop)

        for alternative_waypoints in waypoints:
            print 'alternative_waypoints: ' + str(alternative_waypoints)

    def print_waypoints_between_multiple_bus_stops(self, bus_stop_names):
        """
        :param bus_stop_names: [string]
        """
        for i in range(0, len(bus_stop_names) - 1):
            starting_bus_stop_name = bus_stop_names[i]
            ending_bus_stop_name = bus_stop_names[i + 1]

            self.print_waypoints_between_two_bus_stops(
                starting_bus_stop_name=starting_bus_stop_name,
                ending_bus_stop_name=ending_bus_stop_name
            )

    def print_detailed_waypoints_between_multiple_bus_stops(self, bus_stop_names):
        """
        :param bus_stop_names: [string]
        """
        for i in range(0, len(bus_stop_names) - 1):
            starting_bus_stop_name = bus_stop_names[i]
            ending_bus_stop_name = bus_stop_names[i + 1]

            self.print_detailed_waypoints_between_two_bus_stops(
                starting_bus_stop_name=starting_bus_stop_name,
                ending_bus_stop_name=ending_bus_stop_name
            )

    def print_traffic_density_between_two_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        """

        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return:
        """
        bus_stop_waypoints = self.get_traffic_density_between_two_bus_stop_names(
            starting_bus_stop_name=starting_bus_stop_name,
            ending_bus_stop_name=ending_bus_stop_name
        )
        # {'_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #  'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #  'waypoints': [[{'edge_object_id', 'traffic_density'}]]}

        starting_bus_stop = bus_stop_waypoints.get('starting_bus_stop')
        ending_bus_stop = bus_stop_waypoints.get('ending_bus_stop')
        waypoints = bus_stop_waypoints.get('waypoints')

        print '\nstarting_bus_stop: ' + str(starting_bus_stop) + \
              '\nending_bus_stop: ' + str(ending_bus_stop)

        for alternative_waypoints in waypoints:
            print 'alternative_waypoints: ' + str(alternative_waypoints)

    def print_travel_request_documents(self, counter):
        """
        :param counter: int
        """
        file_writer = open('../src/travel_requests.txt', 'w')
        documents_cursor = self.get_travel_requests_cursor()
        i = 0

        # Cursor -> {'_id', 'client_id', 'line_id', 'starting_bus_stop',
        #            'ending_bus_stop', 'departure_datetime', 'arrival_datetime'}
        for document in documents_cursor:
            if i < counter:
                # print document
                file_writer.write(str(document) + '\n')
                i += 1
            else:
                break

        # print 'Total number of travel_request documents: ' + str(documents_cursor.count())
        file_writer.write('Total number of travel_request documents: ' + str(documents_cursor.count()))
        file_writer.close()

    def get_detailed_waypoints_from_waypoints(self, bus_stop_waypoints):
        """
        Convert a bus_stop_waypoints_document to a detailed_bus_stop_waypoints document.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        detailed_bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_document]]
        }
        :param bus_stop_waypoints: bus_stop_waypoints_document
        :return: detailed_bus_stop_waypoints: detailed_bus_stop_waypoints_document
        """
        lists_of_edge_object_ids = bus_stop_waypoints.get('waypoints')
        lists_of_detailed_edges = []

        for list_of_edge_object_ids in lists_of_edge_object_ids:
            list_of_detailed_edge_object_ids = [ObjectId(i) for i in list_of_edge_object_ids]
            list_of_detailed_edges = [
                self.edges_collection.find_one({'_id': i}) for i in list_of_detailed_edge_object_ids
                ]
            lists_of_detailed_edges.append(list_of_detailed_edges)

        detailed_bus_stop_waypoints = bus_stop_waypoints
        detailed_bus_stop_waypoints['waypoints'] = lists_of_detailed_edges
        return detailed_bus_stop_waypoints

    def test(self):
        bus_line = self.find_bus_line_document(line_id=1)
        bus_stops = bus_line.get('bus_stops')
        bus_stop_ids = [ObjectId(bus_stop.get('_id')) for bus_stop in bus_stops]
        collected_bus_stops = list(self.bus_stops_collection.find({'_id': {'$in': bus_stop_ids}}))

        print bus_stops
        print collected_bus_stops

        print len(bus_stops)
        print len(collected_bus_stops)

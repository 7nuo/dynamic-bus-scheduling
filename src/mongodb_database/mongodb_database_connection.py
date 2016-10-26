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
from bson import ObjectId
from pymongo import MongoClient
from src.look_ahead.timetable_generator import print_timetables

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class MongodbDatabaseConnection(object):
    """
    Database: dynamic_bus_scheduling

    Collections:
        - AddressDocuments
        - BusLineDocuments
        - BusStopDocuments
        - BusStopWaypointsDocuments
        - EdgeDocuments
        - NodeDocuments
        - PointDocuments
        - TimetableDocuments
        - TrafficEventDocuments
        - TravelRequestDocuments
        - WayDocuments

    Description of collection documents:

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
    traffic_event_document: {
        '_id', 'event_id', 'event_type', 'severity_level', 'longitude', 'latitude', 'date'
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
    """
    def __init__(self, host, port):
        self.mongo_client = MongoClient(host, port)
        self.db = self.mongo_client.dynamic_bus_scheduling
        self.address_documents_collection = self.db.AddressDocuments
        self.bus_line_documents_collection = self.db.BusLineDocuments
        self.bus_stop_documents_collection = self.db.BusStopDocuments
        self.bus_stop_waypoints_documents_collection = self.db.BusStopWaypointsDocuments
        self.edge_documents_collection = self.db.EdgeDocuments
        self.node_documents_collection = self.db.NodeDocuments
        self.point_documents_collection = self.db.PointDocuments
        self.timetable_documents_collection = self.db.TimetableDocuments
        self.traffic_event_documents_collection = self.db.TrafficEventDocuments
        self.travel_request_documents_collection = self.db.TravelRequestDocuments
        self.way_documents_collection = self.db.WayDocuments

    def clear_all_collections(self):
        self.clear_address_documents_collection()
        self.clear_bus_line_documents_collection()
        self.clear_bus_stop_documents_collection()
        self.clear_bus_stop_waypoints_documents_collection()
        self.clear_edge_documents_collection()
        self.clear_node_documents_collection()
        self.clear_point_documents_collection()
        self.clear_timetable_documents_collection()
        self.clear_traffic_event_documents_collection()
        self.clear_travel_request_documents_collection()
        self.clear_way_documents_collection()

    def clear_address_documents_collection(self):
        """
        Delete all the documents of the AddressBook collection.

        :return: The number of deleted documents.
        """
        result = self.address_documents_collection.delete_many({})
        return result.deleted_count

    def clear_bus_line_documents_collection(self):
        """
        Delete all the documents of the BusLines collection.

        :return: The number of deleted documents.
        """
        result = self.bus_line_documents_collection.delete_many({})
        return result.deleted_count

    def clear_bus_stop_documents_collection(self):
        """
        Delete all the documents of the BusStops collection.

        :return: The number of deleted documents.
        """
        result = self.bus_stop_documents_collection.delete_many({})
        return result.deleted_count

    def clear_bus_stop_waypoints_documents_collection(self):
        """
        Delete all the documents of the BusStopWaypoints collection.

        :return: The number of deleted documents.
        """
        result = self.bus_stop_waypoints_documents_collection.delete_many({})
        return result.deleted_count

    def clear_edge_documents_collection(self):
        """
        Delete all the documents of the Edges collection.

        :return: The number of deleted documents.
        """
        result = self.edge_documents_collection.delete_many({})
        return result.deleted_count

    def clear_node_documents_collection(self):
        """
        Delete all the documents of the Nodes collection.

        :return: The number of deleted documents.
        """
        result = self.node_documents_collection.delete_many({})
        return result.deleted_count

    def clear_point_documents_collection(self):
        """
        Delete all the documents of the Points collection.

        :return: The number of deleted documents.
        """
        result = self.point_documents_collection.delete_many({})
        return result.deleted_count

    def clear_timetable_documents_collection(self):
        """
        Delete all the documents of the Timetables collection.

        :return: The number of deleted documents.
        """
        result = self.timetable_documents_collection.delete_many({})
        return result.deleted_count

    def clear_traffic_density(self):
        """
        Set the traffic_density values of all edge documents to 0.
        """
        key = {}
        data = {'$set': {'traffic_density': 0}}
        self.edge_documents_collection.update_many(key, data, upsert=False)

    def clear_traffic_event_documents_collection(self):
        """
        Delete all the documents of the TrafficEvents collection.

        :return: The number of deleted documents.
        """
        result = self.traffic_event_documents_collection.delete_many({})
        return result.deleted_count

    def clear_travel_request_documents_collection(self):
        """
        Delete all the documents of the TravelRequests collection.

        :return: The number of deleted documents.
        """
        result = self.travel_request_documents_collection.delete_many({})
        return result.deleted_count

    def clear_way_documents_collection(self):
        """
        Delete all the documents of the Ways collection.

        :return The number of deleted documents.
        """
        result = self.way_documents_collection.delete_many({})
        return result.deleted_count

    def convert_bus_stop_waypoints_document_to_detailed_bus_stop_waypoints_document(self, bus_stop_waypoints_document):
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
        :param bus_stop_waypoints_document
        :return: detailed_bus_stop_waypoints_document
        """
        lists_of_edge_object_ids = bus_stop_waypoints_document.get('waypoints')
        lists_of_detailed_edges = []

        for list_of_edge_object_ids in lists_of_edge_object_ids:
            list_of_detailed_edge_object_ids = [ObjectId(i) for i in list_of_edge_object_ids]
            list_of_detailed_edges = [
                self.edge_documents_collection.find_one({'_id': i}) for i in list_of_detailed_edge_object_ids
                ]
            lists_of_detailed_edges.append(list_of_detailed_edges)

        detailed_bus_stop_waypoints_document = bus_stop_waypoints_document
        detailed_bus_stop_waypoints_document['waypoints'] = lists_of_detailed_edges
        return detailed_bus_stop_waypoints_document

    def delete_address_document(self, object_id=None, name=None):
        """
        Delete an address_document.

        address_document: {'_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param name: string
        :return: True if the address_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.address_documents_collection.delete_one({'_id': ObjectId(object_id)})
        elif name is not None:
            result = self.address_documents_collection.delete_one({'name': name})
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
            result = self.address_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif names is not None:
            result = self.address_documents_collection.delete_many({'name': {'$in': names}})
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
            result = self.bus_line_documents_collection.delete_one({'_id': ObjectId(object_id)})
        elif line_id is not None:
            result = self.bus_line_documents_collection.delete_one({'line_id': line_id})
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
            result = self.bus_line_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif line_ids is not None:
            result = self.bus_line_documents_collection.delete_many({'line_id': {'$in': line_ids}})
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
            result = self.bus_stop_documents_collection.delete_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            result = self.bus_stop_documents_collection.delete_one({'osm_id': osm_id})
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
            result = self.bus_stop_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            result = self.bus_stop_documents_collection.delete_many({'osm_id': {'$in': osm_ids}})
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
            result = self.bus_stop_waypoints_documents_collection.delete_one({'_id': ObjectId(object_id)})
        elif starting_bus_stop is not None and ending_bus_stop is not None:
            result = self.bus_stop_waypoints_documents_collection.delete_one({
                'starting_bus_stop._id': starting_bus_stop.get('_id'),
                'ending_bus_stop._id': ending_bus_stop.get('_id')
            })
        elif starting_bus_stop_name is not None and ending_bus_stop_name is not None:
            result = self.bus_stop_waypoints_documents_collection.delete_one({
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
        result = self.bus_stop_waypoints_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
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
            result = self.edge_documents_collection.delete_one({'_id': ObjectId(object_id)})
        elif starting_node_osm_id is not None and ending_node_osm_id is not None:
            result = self.edge_documents_collection.delete_one({
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
            result = self.edge_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif starting_node_osm_id is not None:
            result = self.edge_documents_collection.delete_many({'starting_node.osm_id': starting_node_osm_id})
        elif ending_node_osm_id is not None:
            result = self.edge_documents_collection.delete_many({'ending_node.osm_id': ending_node_osm_id})
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
            result = self.node_documents_collection.delete_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            result = self.node_documents_collection.delete_one({'osm_id': osm_id})
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
            result = self.node_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            result = self.node_documents_collection.delete_many({'osm_id': {'$in': osm_ids}})
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
            result = self.point_documents_collection.delete_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            result = self.point_documents_collection.delete_one({'osm_id': osm_id})
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
            result = self.point_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            result = self.point_documents_collection.delete_many({'osm_id': {'$in': osm_ids}})
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
        result = self.timetable_documents_collection.delete_one({'_id': ObjectId(object_id)})
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
            result = self.timetable_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif line_id is not None:
            result = self.timetable_documents_collection.delete_many({'line_id': line_id})
        else:
            return 0

        return result.deleted_count

    def delete_traffic_event_document(self, object_id=None, event_id=None):
        """
        Delete a traffic_event_document.

        traffic_event_document: {
            '_id', 'event_id', 'event_type', 'severity_level', 'longitude', 'latitude', 'date'
        }
        :param object_id: ObjectId
        :param event_id: string
        :return: True if the traffic_event_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.traffic_event_documents_collection.delete_one({'_id': ObjectId(object_id)})
        elif event_id is not None:
            result = self.traffic_event_documents_collection.delete_one({'event_id': event_id})
        else:
            return False

        return result.deleted_count == 1

    def delete_traffic_event_documents(self, object_ids=None, event_ids=None):
        """
        Delete multiple traffic_event_documents.

        traffic_event_document: {
            '_id', 'event_id', 'event_type', 'severity_level', 'longitude', 'latitude', 'date'
        }
        :param object_ids: [ObjectId]
        :param event_ids: [string]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.traffic_event_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif event_ids is not None:
            result = self.traffic_event_documents_collection.delete_many({'event_id': {'$in': event_ids}})
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
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :param object_id: ObjectId
        :return: True if the travel_request_document was successfully deleted, otherwise False.
        """
        result = self.travel_request_documents_collection.delete_one({'_id': ObjectId(object_id)})
        return result.deleted_count == 1

    def delete_travel_request_documents(self, object_ids=None, client_ids=None, line_ids=None,
                                        min_departure_datetime=None, max_departure_datetime=None):
        """
        Delete multiple travel_request_documents.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.travel_request_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif client_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            result = self.travel_request_documents_collection.delete_many({
                'client_id': {'$in': client_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif line_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            result = self.travel_request_documents_collection.delete_many({
                'line_id': {'$in': line_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif client_ids is not None:
            result = self.travel_request_documents_collection.delete_many({'client_id': {'$in': client_ids}})
        elif line_ids is not None:
            result = self.travel_request_documents_collection.delete_many({'line_id': {'$in': line_ids}})
        elif min_departure_datetime is not None and max_departure_datetime is not None:
            result = self.travel_request_documents_collection.delete_many({
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
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
            result = self.way_documents_collection.delete_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            result = self.way_documents_collection.delete_one({'osm_id': osm_id})
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
            result = self.way_documents_collection.delete_many({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            result = self.way_documents_collection.delete_many({'osm_id': {'$in': osm_ids}})
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
            address_document = self.address_documents_collection.find_one({'_id': ObjectId(object_id)})
        elif name is not None:
            address_document = self.address_documents_collection.find_one({'name': name})
        elif node_id is not None:
            address_document = self.address_documents_collection.find_one({'node_id': node_id})
        elif longitude is not None and latitude is not None:
            address_document = self.address_documents_collection.find_one({
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
            address_documents_cursor = self.address_documents_collection.find({'_id': {'$in': processed_object_ids}})
        elif names is not None:
            address_documents_cursor = self.address_documents_collection.find({'name': {'$in': names}})
        elif node_ids is not None:
            address_documents_cursor = self.address_documents_collection.find({'node_id': {'$in': node_ids}})
        else:
            address_documents_cursor = self.address_documents_collection.find({})

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
            bus_line_document = self.bus_line_documents_collection.find_one({'_id': ObjectId(object_id)})
        elif line_id is not None:
            bus_line_document = self.bus_line_documents_collection.find_one({'line_id': line_id})
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
            bus_line_documents_cursor = self.bus_line_documents_collection.find({'_id': {'$in': processed_object_ids}})
        elif line_ids is not None:
            bus_line_documents_cursor = self.bus_line_documents_collection.find({'line_id': {'$in': line_ids}})
        else:
            bus_line_documents_cursor = self.bus_line_documents_collection.find({})

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
            bus_stop_document = self.bus_stop_documents_collection.find_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({'osm_id': osm_id})
        elif name is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({'name': name})
        elif longitude is not None and latitude is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({
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
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({'osm_id': {'$in': osm_ids}})
        elif names is not None:
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({'name': {'$in': names}})
        else:
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({})

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
            bus_stop_waypoints_document = self.bus_stop_waypoints_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif starting_bus_stop is not None and ending_bus_stop is not None:
            bus_stop_waypoints_document = self.bus_stop_waypoints_documents_collection.find_one({
                'starting_bus_stop._id': starting_bus_stop.get('_id'),
                'ending_bus_stop._id': ending_bus_stop.get('_id')
            })
        elif starting_bus_stop_name is not None and ending_bus_stop_name is not None:
            bus_stop_waypoints_document = self.bus_stop_waypoints_documents_collection.find_one({
                'starting_bus_stop.name': starting_bus_stop_name,
                'ending_bus_stop.name': ending_bus_stop_name
            })
        else:
            return None

        return bus_stop_waypoints_document

    def find_bus_stop_waypoints_documents(self, object_ids=None, bus_stops=None, bus_stop_names=None, line_id=None):
        """
        Retrieve multiple bus_stop_waypoints_documents.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param object_ids: [ObjectId]
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :param line_id: int
        :return: bus_stop_waypoints_documents: [bus_stop_waypoints_document]
        """
        bus_stop_waypoints_documents = []

        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            bus_stop_waypoints_documents_cursor = self.bus_stop_waypoints_documents_collection.find(
                {'_id': {'$in': processed_object_ids}}
            )
            bus_stop_waypoints_documents.extend(list(bus_stop_waypoints_documents_cursor))

        elif bus_stops is not None:
            number_of_bus_stops = len(bus_stops)

            for i in range(0, number_of_bus_stops - 1):
                starting_bus_stop = bus_stops[i]
                ending_bus_stop = bus_stops[i + 1]
                bus_stop_waypoints_document = self.find_bus_stop_waypoints_document(
                    starting_bus_stop=starting_bus_stop,
                    ending_bus_stop=ending_bus_stop
                )
                bus_stop_waypoints_documents.append(bus_stop_waypoints_document)

        elif bus_stop_names is not None:
            number_of_bus_stop_names = len(bus_stop_names)

            for i in range(0, number_of_bus_stop_names - 1):
                starting_bus_stop_name = bus_stop_names[i]
                ending_bus_stop_name = bus_stop_names[i + 1]
                bus_stop_waypoints_document = self.find_bus_stop_waypoints_document(
                    starting_bus_stop_name=starting_bus_stop_name,
                    ending_bus_stop_name=ending_bus_stop_name
                )
                bus_stop_waypoints_documents.append(bus_stop_waypoints_document)

        elif line_id is not None:
            bus_line_document = self.find_bus_line_document(line_id=line_id)

            if bus_line_document is not None:
                retrieved_bus_stops = bus_line_document.get('bus_stops')
                number_of_retrieved_bus_stops = len(retrieved_bus_stops)

                for i in range(0, number_of_retrieved_bus_stops - 1):
                    starting_bus_stop = retrieved_bus_stops[i]
                    ending_bus_stop = retrieved_bus_stops[i + 1]
                    bus_stop_waypoints_document = self.find_bus_stop_waypoints_document(
                        starting_bus_stop=starting_bus_stop,
                        ending_bus_stop=ending_bus_stop
                    )
                    bus_stop_waypoints_documents.append(bus_stop_waypoints_document)

        else:
            bus_stop_waypoints_documents_cursor = self.bus_stop_waypoints_documents_collection.find({})
            bus_stop_waypoints_documents.extend(list(bus_stop_waypoints_documents_cursor))

        return bus_stop_waypoints_documents

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
        detailed_bus_stop_waypoints_document = \
            self.convert_bus_stop_waypoints_document_to_detailed_bus_stop_waypoints_document(
                bus_stop_waypoints_document=bus_stop_waypoints_document
            )
        return detailed_bus_stop_waypoints_document

    def find_detailed_bus_stop_waypoints_documents(self, object_ids=None, bus_stops=None,
                                                   bus_stop_names=None, line_id=None):
        """
        Retrieve multiple detailed_bus_stop_waypoints_documents.

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
        :param object_ids: [ObjectId]
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :param line_id: int
        :return: detailed_bus_stop_waypoints_documents: [detailed_bus_stop_waypoints_document]
        """
        detailed_bus_stop_waypoints_documents = []
        bus_stop_waypoints_documents = self.find_bus_stop_waypoints_documents(
            object_ids=object_ids,
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names,
            line_id=line_id
        )
        for bus_stop_waypoints_document in bus_stop_waypoints_documents:
            detailed_bus_stop_waypoints_document = \
                self.convert_bus_stop_waypoints_document_to_detailed_bus_stop_waypoints_document(
                    bus_stop_waypoints_document=bus_stop_waypoints_document
                )
            detailed_bus_stop_waypoints_documents.append(detailed_bus_stop_waypoints_document)

        return detailed_bus_stop_waypoints_documents

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
            edge_document = self.edge_documents_collection.find_one({'_id': ObjectId(object_id)})
        elif starting_node_osm_id is not None and ending_node_osm_id is not None:
            edge_document = self.edge_documents_collection.find_one({
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
            edge_documents_cursor = self.edge_documents_collection.find({'_id': {'$in': processed_object_ids}})
        elif starting_node_osm_id is not None:
            edge_documents_cursor = self.edge_documents_collection.find({'starting_node.osm_id': starting_node_osm_id})
        elif ending_node_osm_id is not None:
            edge_documents_cursor = self.edge_documents_collection.find({'ending_node.oms_id': ending_node_osm_id})
        else:
            edge_documents_cursor = self.edge_documents_collection.find({})

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
            node_document = self.node_documents_collection.find_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            node_document = self.node_documents_collection.find_one({'osm_id': osm_id})
        elif longitude is not None and latitude is not None:
            node_document = self.node_documents_collection.find_one({
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
            node_documents_cursor = self.node_documents_collection.find({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            node_documents_cursor = self.node_documents_collection.find({'osm_id': {'$in': osm_ids}})
        else:
            node_documents_cursor = self.node_documents_collection.find({})

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
            point_document = self.point_documents_collection.find_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            point_document = self.point_documents_collection.find_one({'osm_id': osm_id})
        elif longitude is not None and latitude is not None:
            point_document = self.point_documents_collection.find_one({
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
            point_documents_cursor = self.point_documents_collection.find({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            point_documents_cursor = self.point_documents_collection.find({'osm_id': {'$in': osm_ids}})
        else:
            point_documents_cursor = self.point_documents_collection.find({})

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
        timetable_document = self.timetable_documents_collection.find_one({'_id': ObjectId(object_id)})
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
            timetable_documents_cursor = self.timetable_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif line_ids is not None:
            timetable_documents_cursor = self.timetable_documents_collection.find({'line_id': {'$in': line_ids}})
        else:
            timetable_documents_cursor = self.timetable_documents_collection.find({})

        timetable_documents = list(timetable_documents_cursor)
        return timetable_documents

    def find_traffic_event_document(self, object_id=None, event_id=None):
        """
        Retrieve a traffic_event_document.

        traffic_event_document: {
            '_id', 'event_id', 'event_type', 'severity_level', 'longitude', 'latitude', 'date'
        }
        :param object_id: ObjectId
        :param event_id: string
        :return: traffic_event_document
        """
        if object_id is not None:
            traffic_event_document = self.traffic_event_documents_collection.find_one({'_id': ObjectId(object_id)})
        elif event_id is not None:
            traffic_event_document = self.traffic_event_documents_collection.find_one({'event_id': event_id})
        else:
            return None

        return traffic_event_document

    def find_traffic_event_documents(self, object_ids=None, event_ids=None):
        """
        Retrieve a traffic_event_document.

        traffic_event_document: {
            '_id', 'event_id', 'event_type', 'severity_level', 'longitude', 'latitude', 'date'
        }
        :param object_ids: [ObjectId]
        :param event_ids: [string]
        :return: traffic_event_documents: [traffic_event_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            traffic_event_documents_cursor = self.traffic_event_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif event_ids is not None:
            traffic_event_documents_cursor = self.traffic_event_documents_collection.find({
                'event_id': {'$in': event_ids}
            })
        else:
            traffic_event_documents_cursor = self.traffic_event_documents_collection.find({})

        traffic_event_documents = list(traffic_event_documents_cursor)
        return traffic_event_documents

    def find_travel_request_document(self, object_id):
        """
        Retrieve a travel_request_document.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :param object_id: ObjectId
        :return: travel_request_document
        """
        travel_request_document = self.travel_request_documents_collection.find_one({'_id': ObjectId(object_id)})
        return travel_request_document

    def find_travel_request_documents(self, object_ids=None, client_ids=None, line_ids=None,
                                      min_departure_datetime=None, max_departure_datetime=None):
        """
        Retrieve multiple travel_request_documents.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :return: travel_request_documents: [travel_request_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            travel_requests_cursor = self.travel_request_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif client_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'client_id': {'$in': client_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif line_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'line_id': {'$in': line_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif client_ids is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({'client_id': {'$in': client_ids}})
        elif line_ids is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({'line_id': {'$in': line_ids}})
        elif min_departure_datetime is not None and max_departure_datetime is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        else:
            travel_requests_cursor = self.travel_request_documents_collection.find({})

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
            way_document = self.way_documents_collection.find_one({'_id': ObjectId(object_id)})
        elif osm_id is not None:
            way_document = self.way_documents_collection.find_one({'osm_id': osm_id})
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
            way_documents_cursor = self.way_documents_collection.find({'_id': {'$in': processed_object_ids}})
        elif osm_ids is not None:
            way_documents_cursor = self.way_documents_collection.find({'osm_id': {'$in': osm_ids}})
        else:
            way_documents_cursor = self.way_documents_collection.find({})

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
        bus_line_documents_cursor = self.bus_line_documents_collection.find({})
        return bus_line_documents_cursor

    def get_bus_lines(self):
        """
        Retrieve a dictionary containing all the bus_line_documents.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :return: bus_lines: {line_id -> bus_line_document}
        """
        bus_lines = {}
        bus_line_documents_cursor = self.get_bus_line_documents_cursor()

        for bus_line_document in bus_line_documents_cursor:
            line_id = bus_line_document.get('line_id')
            bus_lines[line_id] = bus_line_document

        return bus_lines

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
        bus_stop_documents_cursor = self.bus_stop_documents_collection.find({})
        return bus_stop_documents_cursor

    def get_bus_stops(self):
        """
        Retrieve a dictionary containing all the bus_stop_documents.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :return: bus_stops: {name -> bus_stop_document}
        """
        bus_stops = {}
        bus_stop_documents_cursor = self.get_bus_stop_documents_cursor()

        for bus_stop_document in bus_stop_documents_cursor:
            name = bus_stop_document.get('name')

            if name not in bus_stops:
                bus_stops[name] = bus_stop_document

        return bus_stops

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
        edge_documents_cursor = self.edge_documents_collection.find({})
        return edge_documents_cursor

    def get_edges_dictionary(self):
        """
        Retrieve a dictionary containing all the edge_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :return: edges: {starting_node_osm_id -> [edge_document]}
        """
        edges = {}
        edge_documents_cursor = self.get_edge_documents_cursor()

        for edge_document in edge_documents_cursor:
            starting_node_osm_id = edge_document.get('starting_node').get('osm_id')

            if starting_node_osm_id in edges:
                edges[starting_node_osm_id].append(edge_document)
            else:
                edges[starting_node_osm_id] = [edge_document]

        return edges

    def get_edge_documents_list(self):
        """
        Retrieve a list containing all the edge_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :return: edge_documents_list: [edge_document]
        """
        edge_documents_cursor = self.get_edge_documents_cursor()
        edge_documents_list = list(edge_documents_cursor)
        return edge_documents_list

    def get_edge_documents_included_in_bus_line(self, bus_line=None, line_id=None):
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
        :param bus_line: bus_line_document
        :param line_id: int
        :return: edge_documents: [edge_document]
        """
        edge_object_ids = self.get_edge_object_ids_included_in_bus_line(
            bus_line=bus_line,
            line_id=line_id
        )
        edge_documents = self.find_edge_documents(object_ids=edge_object_ids)
        return edge_documents

    def get_edge_documents_included_in_bus_stop_waypoints(self, bus_stop_waypoints):
        """
        Get a list containing all the edge_documents which are included in a bus_stop_waypoints document.

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
        :param bus_stop_waypoints: bus_stop_waypoints_document
        :return: edge_documents: [edge_document]
        """

        edge_object_ids = self.get_edge_object_ids_included_in_bus_stop_waypoints(
            bus_stop_waypoints=bus_stop_waypoints
        )
        edge_documents = self.find_edge_documents(object_ids=edge_object_ids)
        return edge_documents

    def get_edge_object_ids_included_in_bus_line(self, bus_line=None, line_id=None):
        """
        Get a list containing the object_ids of the edge_documents,
        which are included in the waypoints of a bus_line.

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
        :param bus_line: bus_line_document
        :param line_id: int
        :return: edge_object_ids: [edge_object_id]
        """
        edge_object_ids = []

        if bus_line is None and line_id is None:
            return edge_object_ids
        elif bus_line is None:
            bus_line = self.find_bus_line_document(line_id=line_id)
        else:
            pass

        bus_stops = bus_line.get('bus_stops')
        number_of_bus_stops = len(bus_stops)

        for i in range(0, number_of_bus_stops - 1):
            starting_bus_stop = bus_stops[i]
            ending_bus_stop = bus_stops[i + 1]

            bus_stop_waypoints = self.find_bus_stop_waypoints_document(
                starting_bus_stop=starting_bus_stop,
                ending_bus_stop=ending_bus_stop
            )
            edge_object_ids_included_in_bus_stop_waypoints = self.get_edge_object_ids_included_in_bus_stop_waypoints(
                bus_stop_waypoints=bus_stop_waypoints
            )
            for edge_object_id in edge_object_ids_included_in_bus_stop_waypoints:
                if edge_object_id not in edge_object_ids:
                    edge_object_ids.append(edge_object_id)

        return edge_object_ids

    @staticmethod
    def get_edge_object_ids_included_in_bus_stop_waypoints(bus_stop_waypoints):
        """
        Get a list containing all the object_ids of the edge_documents,
        which are included in a bus_stop_waypoints document.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param bus_stop_waypoints: bus_stop_waypoints_document
        :return: edge_object_ids: [edge_object_id]
        """
        edge_object_ids = []
        lists_of_edge_object_ids = bus_stop_waypoints.get('waypoints')

        for list_of_edge_object_ids in lists_of_edge_object_ids:
            for edge_object_id in list_of_edge_object_ids:
                if edge_object_id not in edge_object_ids:
                    edge_object_ids.append(edge_object_id)

        return edge_object_ids

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

    def get_node_documents_cursor(self):
        """
        Retrieve a cursor of all node_documents.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :return: node_documents_cursor
        """
        node_documents_cursor = self.node_documents_collection.find({})
        return node_documents_cursor

    def get_node_documents_list(self):
        """
        Retrieve a list containing all the node_documents.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :return: node_documents_list: [node_document]
        """
        node_documents_cursor = self.node_documents_collection.find({})
        node_documents_list = list(node_documents_cursor)
        return node_documents_list

    def get_point_documents_cursor(self):
        """
        Retrieve a cursor of all point_documents.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :return: point_documents_cursor
        """
        point_documents_cursor = self.point_documents_collection.find({})
        return point_documents_cursor

    def get_points(self):
        """
        Retrieve a dictionary containing all the point_documents.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :return pointss: {osm_id -> point_document}
        """
        pointss = {}
        point_documents_cursor = self.get_point_documents_cursor()

        for point_document in point_documents_cursor:
            osm_id = point_document.get('osm_id')
            pointss[osm_id] = point_document

        return pointss

    def get_point_documents_list(self):
        """
        Retrieve a list containing all the point_documents.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :return: point_documents_list: [point_document]
        """
        point_documents_cursor = self.point_documents_collection.find({})
        point_documents_list = list(point_documents_cursor)
        return point_documents_list

    def get_timetable_documents_cursor(self):
        """
        Retrieve a cursor of all timetable_documents.

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
        :return: timetable_documents_cursor
        """
        timetable_documents_cursor = self.timetable_documents_collection.find({})
        return timetable_documents_cursor

    def get_timetable_documents_list(self):
        """
        Retrieve a list containing all the timetable_documents.

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
        :return: timetable_documents_list: [timetable_document]
        """
        timetable_documents_cursor = self.timetable_documents_collection.find({})
        timetable_documents_list = list(timetable_documents_cursor)
        return timetable_documents_list

    def get_traffic_density_documents(self, bus_stops=None, bus_stop_names=None):
        """
        Get multiple traffic_density_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        detailed_bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_document]]
        }
        traffic_density_document: {
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'traffic_density_values': [[{'edge_object_id', 'traffic_density'}]]
        }
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :return: traffic_density_documents: [traffic_density_document]
        """
        traffic_density_documents = []

        detailed_bus_stop_waypoints_documents = self.find_detailed_bus_stop_waypoints_documents(
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names
        )
        for detailed_bus_stop_waypoints_document in detailed_bus_stop_waypoints_documents:
            starting_bus_stop = detailed_bus_stop_waypoints_document.get('starting_bus_stop')
            ending_bus_stop = detailed_bus_stop_waypoints_document.get('ending_bus_stop')
            lists_of_edge_documents = detailed_bus_stop_waypoints_document.get('waypoints')
            traffic_density_values = []

            for list_of_edge_documents in lists_of_edge_documents:
                traffic_density_values_entry = [
                    {'edge_object_id': edge_document.get('_id'),
                     'traffic_density': edge_document.get('traffic_density')}
                    for edge_document in list_of_edge_documents
                ]
                traffic_density_values.append(traffic_density_values_entry)

            traffic_density_document = {
                'starting_bus_stop': starting_bus_stop,
                'ending_bus_stop': ending_bus_stop,
                'traffic_density_values': traffic_density_values
            }
            traffic_density_documents.append(traffic_density_document)

        return traffic_density_documents

    def get_travel_request_documents_cursor(self):
        """
        Retrieve a cursor of all travel_request_documents.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :return: travel_request_documents_cursor
        """
        travel_request_documents_cursor = self.travel_request_documents_collection.find({})
        return travel_request_documents_cursor

    def get_travel_request_documents_list(self):
        """
        Retrieve a list containing all the travel_request_documents.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :return: travel_request_documents_list: [travel_request_document]
        """
        travel_request_documents_cursor = self.get_travel_request_documents_cursor()
        travel_request_documents_list = list(travel_request_documents_cursor)
        return travel_request_documents_list

    def has_edges(self, node_osm_id):
        """
        Check if a node exists in the Edges collection as a starting node.

        :param node_osm_id: int
        :return: True if exists, otherwise False.
        """
        return self.edge_documents_collection.find_one({'starting_node.osm_id': node_osm_id}) is not None

    def in_edges(self, node_osm_id):
        """
        Check if a node exists in the Edges collection, either as a starting or an ending node.

        :param node_osm_id: int
        :return: True if exists, otherwise False.
        """
        return self.edge_documents_collection.find_one({'$or': [{'starting_node.osm_id': node_osm_id},
                                                                {'ending_node.osm_id': node_osm_id}]}) is not None

    def insert_address_document(self, address_document=None, name=None, node_id=None, point=None):
        """
        Insert an address_document.

        address_document: {'_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}}

        :param address_document
        :param name: string
        :param node_id: int
        :param point: Point
        :return: new_object_id: ObjectId
        """
        if address_document is None:
            address_document = {
                'name': name,
                'node_id': node_id,
                'point': {'longitude': point.longitude, 'latitude': point.latitude}
            }

        result = self.address_documents_collection.insert_one(address_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_address_documents(self, address_documents):
        """
        Insert multiple address_documents.

        address_document: {'_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}}

        :param address_documents: [address_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if address_documents:
            result = self.address_documents_collection.insert_many(address_documents)
            new_object_ids = result.inserted_ids

        return new_object_ids

    def insert_bus_line_document(self, bus_line_document=None, line_id=None, bus_stops=None):
        """
        Insert a new bus_line_document or update, if it already exists in the database.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param bus_line_document
        :param line_id: int
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :return: new_object_id: ObjectId
        """
        if bus_line_document is not None:
            key = {'_id': ObjectId(bus_line_document.get('_id'))}
            data = {
                '$set': {
                    'line_id': bus_line_document.get('line_id'),
                    'bus_stops': bus_line_document.get('bus_stops')
                }
            }
            result = self.bus_line_documents_collection.update_one(key, data, upsert=True)
            new_object_id = result.upserted_id
        else:
            bus_line_document = {'line_id': line_id, 'bus_stops': bus_stops}
            result = self.bus_line_documents_collection.insert_one(bus_line_document)
            new_object_id = result.inserted_id

        return new_object_id

    def insert_bus_line_documents(self, bus_line_documents):
        """
        Insert a list of bus_line_documents or update, if it already exists in the database.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param bus_line_documents: [bus_line_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        for bus_line_document in bus_line_documents:
            new_object_id = self.insert_bus_line_document(bus_line_document=bus_line_document)
            new_object_ids.append(new_object_id)

        return new_object_ids

    def insert_bus_stop_document(self, bus_stop_document=None, osm_id=None, name=None, point=None):
        """
        Insert a bus_stop_document.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param bus_stop_document
        :param osm_id: int
        :param name: string
        :param point: Point
        :return: new_object_id: ObjectId
        """
        if bus_stop_document is None:
            bus_stop_document = {
                'osm_id': osm_id,
                'name': name,
                'point': {'longitude': point.longitude, 'latitude': point.latitude}
            }

        result = self.bus_stop_documents_collection.insert_one(bus_stop_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_bus_stop_documents(self, bus_stop_documents):
        """
        Insert multiple bus_stop documents.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param bus_stop_documents: [bus_stop_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if bus_stop_documents:
            result = self.bus_stop_documents_collection.insert_many(bus_stop_documents)
            new_object_ids = result.inserted_ids

        return new_object_ids

    def insert_bus_stop_waypoints_document(self, bus_stop_waypoints_document=None, starting_bus_stop=None,
                                           ending_bus_stop=None, waypoints=None):
        """
        Insert a new document to the BusStopWaypoints collection, or update the waypoints
        if the document already exists in the database.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param bus_stop_waypoints_document
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param waypoints: [[edge_object_id]]
        :return: new_object_id: ObjectId
        """
        if bus_stop_waypoints_document is not None:
            key = {'_id': ObjectId(bus_stop_waypoints_document.get('_id'))}
            data = {
                '$set': {
                    'starting_bus_stop': starting_bus_stop,
                    'ending_bus_stop': ending_bus_stop,
                    'waypoints': waypoints
                }
            }
            result = self.bus_stop_waypoints_documents_collection.update_one(key, data, upsert=True)
            new_object_id = result.upserted_id
        else:
            bus_stop_waypoints_document = {
                'starting_bus_stop': starting_bus_stop,
                'ending_bus_stop': ending_bus_stop,
                'waypoints': waypoints
            }
            result = self.bus_stop_waypoints_documents_collection.insert_one(bus_stop_waypoints_document)
            new_object_id = result.inserted_id

        return new_object_id

    def insert_edge_document(self, edge_document=None, starting_node=None, ending_node=None, max_speed=None,
                             road_type=None, way_id=None, traffic_density=None):
        """
        Insert an edge_document.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param edge_document
        :param starting_node: {'osm_id', 'point': {'longitude', 'latitude'}}
        :param ending_node: {'osm_id', 'point': {'longitude', 'latitude'}}
        :param max_speed: float or int
        :param road_type: string
        :param way_id: osm_id: int
        :param traffic_density: A value between 0 and 1 indicating the density of traffic: float
        :return: new_object_id: ObjectId
        """
        if edge_document is None:
            edge_document = {
                'starting_node': starting_node, 'ending_node': ending_node, 'max_speed': max_speed,
                'road_type': road_type, 'way_id': way_id, 'traffic_density': traffic_density
            }

        result = self.edge_documents_collection.insert_one(edge_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_edge_documents(self, edge_documents):
        """
        Insert multiple edge_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param edge_documents: [edge_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if edge_documents:
            result = self.edge_documents_collection.insert_many(edge_documents)
            new_object_ids = result.inserted_ids

        return new_object_ids

    def insert_node_document(self, node_document=None, osm_id=None, tags=None, point=None):
        """
        Insert a node_document.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :param node_document
        :param osm_id: int
        :param tags: dict
        :param point: Point
        :return: new_object_id: ObjectId
        """
        if node_document is None:
            node_document = {
                'osm_id': osm_id, 'tags': tags,
                'point': {'longitude': point.longitude, 'latitude': point.latitude}
            }

        result = self.node_documents_collection.insert_one(node_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_node_documents(self, node_documents):
        """
        Insert multiple node_documents.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :param node_documents: [node_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if node_documents:
            result = self.node_documents_collection.insert_many(node_documents)
            new_object_ids = result.inserted_ids

        return new_object_ids

    def insert_point_document(self, point_document=None, osm_id=None, point=None):
        """
        Insert a point_document.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :param point_document
        :param osm_id: int
        :param point: Point
        :return: new_object_id: ObjectId
        """
        if point_document is None:
            point_document = {
                'osm_id': osm_id,
                'point': {'longitude': point.longitude, 'latitude': point.latitude}
            }

        result = self.point_documents_collection.insert_one(point_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_point_documents(self, point_documents):
        """
        Insert multiple point_documents.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :param point_documents: [point_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if point_documents:
            result = self.point_documents_collection.insert_many(point_documents)
            new_object_ids = result.inserted_ids

        return new_object_ids

    def insert_timetable_document(self, timetable):
        """
        Insert a new timetable_document or update, if it already exists in the database.

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
        :return: new_object_id: ObjectId
        """
        key = {'_id': ObjectId(timetable.get('_id'))}
        data = {'$set': {
            'line_id': timetable.get('line_id'),
            'timetable_entries': timetable.get('timetable_entries'),
            'travel_requests': timetable.get('travel_requests')
        }}
        result = self.timetable_documents_collection.update_one(key, data, upsert=True)
        new_object_id = result.upserted_id
        return new_object_id

    def insert_timetable_documents(self, timetable_documents):
        """
        Insert multiple new timetable_documents or update, if they already exist in the database.

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
        :param timetable_documents: [timetable_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        for timetable in timetable_documents:
            new_object_id = self.insert_timetable_document(timetable=timetable)
            new_object_ids.append(new_object_id)

        return new_object_ids

    def insert_traffic_event_document(self, traffic_event_document):
        """
        Insert a new traffic_event_document or update, if it already exists in the database.

        traffic_event_document: {
            '_id', 'event_id', 'event_type', 'severity_level', 'longitude', 'latitude', 'date'
        }
        :param traffic_event_document
        :return: new_object_id: ObjectId
        """
        key = {'event_id': traffic_event_document.get('event_id')}
        data = {'$set': {
            'event_type': traffic_event_document.get('event_type'),
            'severity_level': traffic_event_document.get('severity_level'),
            'longitude': traffic_event_document.get('longitude'),
            'latitude': traffic_event_document.get('latitude'),
            'date': traffic_event_document.get('date')
        }}
        result = self.traffic_event_documents_collection.update_one(key, data, upsert=True)
        new_object_id = result.upserted_id
        return new_object_id

    def insert_traffic_event_documents(self, traffic_event_documents):
        """
        Insert multiple new traffic_event_documents or update, if they already exist in the database.

        traffic_event_document: {
            '_id', 'event_id', 'event_type', 'severity_level', 'longitude', 'latitude', 'date'
        }
        :param traffic_event_documents: [traffic_event_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        for traffic_event_document in traffic_event_documents:
            new_object_id = self.insert_traffic_event_document(
                traffic_event_document=traffic_event_document
            )
            new_object_ids.append(new_object_id)

        return new_object_ids

    def insert_travel_request_document(self, travel_request_document=None, client_id=None, line_id=None,
                                       starting_bus_stop=None, ending_bus_stop=None,
                                       departure_datetime=None, arrival_datetime=None,
                                       starting_timetable_entry_index=None, ending_timetable_entry_index=None):
        """
        Insert a travel_request_document.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :param travel_request_document
        :param client_id: int
        :param line_id: int
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param departure_datetime: datetime
        :param arrival_datetime: datetime
        :param starting_timetable_entry_index: int
        :param ending_timetable_entry_index: int
        :return: new_object_id: ObjectId
        """
        if travel_request_document is None:
            travel_request_document = {
                'client_id': client_id,
                'line_id': line_id,
                'starting_bus_stop': starting_bus_stop,
                'ending_bus_stop': ending_bus_stop,
                'departure_datetime': departure_datetime,
                'arrival_datetime': arrival_datetime,
                'starting_timetable_entry_index': starting_timetable_entry_index,
                'ending_timetable_entry_index': ending_timetable_entry_index
            }

        result = self.travel_request_documents_collection.insert_one(travel_request_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_travel_request_documents(self, travel_request_documents):
        """
        Insert multiple travel_request_documents.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :param travel_request_documents: [travel_request_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if travel_request_documents:
            result = self.travel_request_documents_collection.insert_many(travel_request_documents)
            new_object_ids = result.inserted_ids

        return new_object_ids

    def insert_way_document(self, way_document=None, osm_id=None, tags=None, references=None):
        """
        Insert a way_document.

        way_document: {'_id', 'osm_id', 'tags', 'references'}

        :param way_document
        :param osm_id: int
        :param tags: dict
        :param references: [osm_id]
        :return: new_object_id: ObjectId
        """
        if way_document is None:
            way_document = {'osm_id': osm_id, 'tags': tags, 'references': references}

        result = self.way_documents_collection.insert_one(way_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_way_documents(self, way_documents):
        """
        Insert multiple way_documents.

        way_document: {'_id', 'osm_id', 'tags', 'references'}

        :param way_documents: [way_documents]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if way_documents:
            result = self.way_documents_collection.insert_many(way_documents)
            new_object_ids = result.inserted_ids

        return new_object_ids

    def print_address_document(self, object_id=None, name=None, node_id=None, longitude=None, latitude=None):
        """
        Print an address_document.

        address_document: {'_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param name: string
        :param node_id: int
        :param longitude: float
        :param latitude: float
        :return: None
        """
        address_document = self.find_address_document(
            object_id=object_id, name=name, node_id=node_id, longitude=longitude, latitude=latitude
        )
        print address_document

    def print_address_documents(self, object_ids=None, names=None, node_ids=None, counter=None):
        """
        Print multiple address_documents.

        address_document: {'_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param names: [string]
        :param node_ids: [int]
        :param counter: int
        :return: None
        """
        address_documents_list = self.find_address_documents(
            object_ids=object_ids,
            names=names,
            node_ids=node_ids
        )
        number_of_address_documents = len(address_documents_list)

        if counter is not None:
            if number_of_address_documents < counter:
                counter = number_of_address_documents

            for i in range(0, counter):
                address_document = address_documents_list[i]
                print address_document

        else:
            for address_document in address_documents_list:
                print address_document

        print 'number_of_address_documents:', number_of_address_documents

    def print_bus_line_document(self, object_id=None, line_id=None):
        """
        Print a bus_line_document.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param object_id: ObjectId
        :param line_id: int
        :return: bus_line_document
        """
        bus_line_document = self.find_bus_line_document(object_id=object_id, line_id=line_id)
        print bus_line_document

    def print_bus_line_documents(self, object_ids=None, line_ids=None, counter=None):
        """
        Print multiple bus_line_documents.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param object_ids: [ObjectId]
        :param line_ids: [int]
        :param counter: int
        :return: None
        """
        bus_line_documents_list = self.find_bus_line_documents(
            object_ids=object_ids,
            line_ids=line_ids
        )
        number_of_bus_line_documents = len(bus_line_documents_list)

        if counter is not None:
            if number_of_bus_line_documents < counter:
                counter = number_of_bus_line_documents

            for i in range(0, counter):
                bus_line_document = bus_line_documents_list[i]
                print bus_line_document

        else:
            for bus_line_document in bus_line_documents_list:
                print bus_line_document

        print 'number_of_bus_line_documents:', number_of_bus_line_documents

    def print_bus_stop_document(self, object_id=None, osm_id=None, name=None, longitude=None, latitude=None):
        """
        Retrieve a bus_stop_document.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param osm_id: int
        :param name: string
        :param longitude: float
        :param latitude: float
        :return: None
        """
        bus_stop_document = self.find_bus_stop_document(
            object_id=object_id, osm_id=osm_id, name=name, longitude=longitude, latitude=latitude
        )
        print bus_stop_document

    def print_bus_stop_documents(self, object_ids=None, osm_ids=None, names=None, counter=None):
        """
        Print multiple bus_stop_documents.

        bus_stop_document: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param names: [string]
        :param counter: int
        :return: None
        """
        bus_stop_documents_list = self.find_bus_stop_documents(
            object_ids=object_ids,
            osm_ids=osm_ids,
            names=names
        )
        number_of_bus_stop_documents = len(bus_stop_documents_list)

        if counter is not None:
            if number_of_bus_stop_documents < counter:
                counter = number_of_bus_stop_documents

            for i in range(0, counter):
                bus_stop_document = bus_stop_documents_list[i]
                print bus_stop_document

        else:
            for bus_stop_document in bus_stop_documents_list:
                print bus_stop_document

        print 'number_of_bus_stop_documents:', number_of_bus_stop_documents

    def print_edge_document(self, object_id=None, starting_node_osm_id=None, ending_node_osm_id=None):
        """
        Print an edge_document.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param object_id: ObjectId
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :return: None
        """
        edge_document = self.find_edge_document(
            object_id=object_id, starting_node_osm_id=starting_node_osm_id, ending_node_osm_id=ending_node_osm_id
        )
        print edge_document

    def print_edge_documents(self, object_ids=None, starting_node_osm_id=None, ending_node_osm_id=None, counter=None):
        """
        Print multiple edge_documents.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param object_ids: [ObjectId]
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :param counter: int
        :return: None
        """
        edge_documents_list = self.find_edge_documents(
            object_ids=object_ids,
            starting_node_osm_id=starting_node_osm_id,
            ending_node_osm_id=ending_node_osm_id
        )
        number_of_edge_documents = len(edge_documents_list)

        if counter is not None:
            if number_of_edge_documents < counter:
                counter = number_of_edge_documents

            for i in range(0, counter):
                edge_document = edge_documents_list[i]
                print edge_document

        else:
            for edge_document in edge_documents_list:
                print edge_document

        print 'number_of_edge_documents:', number_of_edge_documents

    def print_node_document(self, object_id=None, osm_id=None, longitude=None, latitude=None):
        """
        Print a node_document.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param osm_id: int
        :param longitude: float
        :param latitude: float
        :return: None
        """
        node_document = self.find_node_document(
            object_id=object_id, osm_id=osm_id, longitude=longitude, latitude=latitude
        )
        print node_document

    def print_node_documents(self, object_ids=None, osm_ids=None, counter=None):
        """
        Print multiple node_documents.

        node_document: {'_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param counter: int
        :return: None
        """
        node_documents_list = self.find_node_documents(
            object_ids=object_ids,
            osm_ids=osm_ids
        )
        number_of_node_documents = len(node_documents_list)

        if counter is not None:
            if number_of_node_documents < counter:
                counter = number_of_node_documents

            for i in range(0, counter):
                node_document = node_documents_list[i]
                print node_document

        else:
            for node_document in node_documents_list:
                print node_document

        print 'number_of_node_documents:', number_of_node_documents

    def print_point_document(self, object_id=None, osm_id=None, longitude=None, latitude=None):
        """
        Print a point_document.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :param object_id: ObjectId
        :param osm_id: int
        :param longitude: float
        :param latitude: float
        :return: None
        """
        point_document = self.find_point_document(
            object_id=object_id, osm_id=osm_id, longitude=longitude, latitude=latitude
        )
        print point_document

    def print_point_documents(self, object_ids=None, osm_ids=None, counter=None):
        """
        Print multiple point_documents.

        point_document: {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param counter: int
        :return: None
        """
        point_documents_list = self.find_point_documents(
            object_ids=object_ids,
            osm_ids=osm_ids
        )
        number_of_point_documents = len(point_documents_list)

        if counter is not None:
            if number_of_point_documents < counter:
                counter = number_of_point_documents

            for i in range(0, counter):
                point_document = point_documents_list[i]
                print point_document

        else:
            for point_document in point_documents_list:
                print point_document

        print 'number_of_point_documents:', number_of_point_documents

    def print_travel_request_document(self, object_id):
        """
        Print a travel_request_document.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :param object_id: ObjectId
        :return: None
        """
        travel_request_document = self.find_travel_request_document(object_id=object_id)
        print travel_request_document

    def print_travel_request_documents(self, object_ids=None, client_ids=None, line_ids=None,
                                       min_departure_datetime=None, max_departure_datetime=None,
                                       counter=None):
        """
        Print multiple travel_request_documents.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime: datetime
        :param counter: int
        :return: None
        """
        travel_request_documents_list = self.find_travel_request_documents(
            object_ids=object_ids,
            client_ids=client_ids,
            line_ids=line_ids,
            min_departure_datetime=min_departure_datetime,
            max_departure_datetime=max_departure_datetime
        )
        number_of_travel_request_documents = len(travel_request_documents_list)

        if counter is not None:
            if number_of_travel_request_documents < counter:
                counter = number_of_travel_request_documents

            for i in range(0, counter):
                travel_request_document = travel_request_documents_list[i]
                print travel_request_document

        else:
            for travel_request_document in travel_request_documents_list:
                print travel_request_document

        print 'number_of_travel_request_documents:', number_of_travel_request_documents

    def print_way_document(self, object_id=None, osm_id=None):
        """
        Print a way_document.

        way_document: {'_id', 'osm_id', 'tags', 'references'}

        :param object_id: ObjectId
        :param osm_id: int
        :return: None
        """
        way_document = self.find_way_document(object_id=object_id, osm_id=osm_id)
        print way_document

    def print_way_documents(self, object_ids=None, osm_ids=None, counter=None):
        """
        Print multiple way_documents.

        way_document: {'_id', 'osm_id', 'tags', 'references'}

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param counter: int
        :return: None
        """
        way_documents_list = self.find_way_documents(
            object_ids=object_ids,
            osm_ids=osm_ids
        )
        number_of_way_documents = len(way_documents_list)

        if counter is not None:
            if number_of_way_documents < counter:
                counter = number_of_way_documents

            for i in range(0, counter):
                way_document = way_documents_list[i]
                print way_document

        else:
            for way_document in way_documents_list:
                print way_document

        print 'number_of_way_documents:', number_of_way_documents

    def print_bus_stop_waypoints_document(self, bus_stop_waypoints_document=None, object_id=None,
                                          starting_bus_stop=None, ending_bus_stop=None,
                                          starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Print a bus_stop_waypoints_document.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param bus_stop_waypoints_document
        :param object_id: ObjectId
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return: None
        """
        if bus_stop_waypoints_document is None:
            bus_stop_waypoints_document = self.find_bus_stop_waypoints_document(
                object_id=object_id,
                starting_bus_stop=starting_bus_stop,
                ending_bus_stop=ending_bus_stop,
                starting_bus_stop_name=starting_bus_stop_name,
                ending_bus_stop_name=ending_bus_stop_name
            )
        # print bus_stop_waypoints_document

        if bus_stop_waypoints_document is not None:
            starting_bus_stop = bus_stop_waypoints_document.get('starting_bus_stop')
            ending_bus_stop = bus_stop_waypoints_document.get('ending_bus_stop')
            waypoints = bus_stop_waypoints_document.get('waypoints')

            print '\nstarting_bus_stop:', starting_bus_stop
            print 'ending_bus_stop:', ending_bus_stop

            for alternative_waypoints in waypoints:
                print 'alternative_waypoints:', alternative_waypoints

    def print_bus_stop_waypoints_documents(self, object_ids=None, bus_stops=None, bus_stop_names=None, line_id=None):
        """
        Print multiple bus_stop_waypoints_documents.

        bus_stop_waypoints_document: {
            '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'waypoints': [[edge_object_id]]
        }
        :param object_ids: [ObjectId]
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :param line_id: int
        :return: None
        """
        bus_stop_waypoints_documents = self.find_bus_stop_waypoints_documents(
            object_ids=object_ids,
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names,
            line_id=line_id
        )
        for bus_stop_waypoints_document in bus_stop_waypoints_documents:
            if bus_stop_waypoints_document is not None:
                self.print_bus_stop_waypoints_document(
                    bus_stop_waypoints_document=bus_stop_waypoints_document
                )

    def print_detailed_bus_stop_waypoints_document(self, detailed_bus_stop_waypoints_document=None, object_id=None,
                                                   starting_bus_stop=None, ending_bus_stop=None,
                                                   starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Print a detailed_bus_stop_waypoints_document.

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
        :param detailed_bus_stop_waypoints_document
        :param object_id: ObjectId
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return: None
        """
        if detailed_bus_stop_waypoints_document is None:
            detailed_bus_stop_waypoints_document = self.find_detailed_bus_stop_waypoints_document(
                object_id=object_id,
                starting_bus_stop=starting_bus_stop,
                ending_bus_stop=ending_bus_stop,
                starting_bus_stop_name=starting_bus_stop_name,
                ending_bus_stop_name=ending_bus_stop_name
            )
        if detailed_bus_stop_waypoints_document is not None:
            starting_bus_stop = detailed_bus_stop_waypoints_document.get('starting_bus_stop')
            ending_bus_stop = detailed_bus_stop_waypoints_document.get('ending_bus_stop')
            waypoints = detailed_bus_stop_waypoints_document.get('waypoints')

            print '\nstarting_bus_stop:', starting_bus_stop
            print 'ending_bus_stop:', ending_bus_stop

            for alternative_waypoints in waypoints:
                print 'alternative_waypoints:', alternative_waypoints

    def print_detailed_bus_stop_waypoints_documents(self, object_ids=None, bus_stops=None,
                                                    bus_stop_names=None, line_id=None):
        """
        Print multiple detailed_bus_stop_waypoints_documents.

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
        :param object_ids: [ObjectId]
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :param line_id: int
        :return: None
        """
        detailed_bus_stop_waypoints_documents = self.find_detailed_bus_stop_waypoints_documents(
            object_ids=object_ids,
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names,
            line_id=line_id
        )
        for detailed_bus_stop_waypoints_document in detailed_bus_stop_waypoints_documents:
            if detailed_bus_stop_waypoints_document is not None:
                self.print_detailed_bus_stop_waypoints_document(
                    detailed_bus_stop_waypoints_document=detailed_bus_stop_waypoints_document
                )

    def print_timetable_documents(self, object_ids=None, line_ids=None, counter=None, timetables_control=True,
                                  timetable_entries_control=False, travel_requests_control=False):
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
        :param object_ids: [ObjectId]
        :param line_ids: [int]
        :param counter: int
        :param timetables_control: bool
        :param timetable_entries_control: bool
        :param travel_requests_control: bool
        :return: timetable_documents: [timetable_document]
        """
        timetable_documents = self.find_timetable_documents(
            object_ids=object_ids,
            line_ids=line_ids,
        )
        number_of_timetable_documents = len(timetable_documents)

        if counter is not None and counter < number_of_timetable_documents:
            if counter == 0:
                timetable_documents = []
            elif counter == 1:
                timetable_documents = [timetable_documents[0]]
            else:
                timetable_documents = timetable_documents[0:(counter-1)]

        print_timetables(
            timetables=timetable_documents,
            timetables_control=timetables_control,
            timetable_entries_control=timetable_entries_control,
            travel_requests_control=travel_requests_control
        )

    @staticmethod
    def print_traffic_density_document(traffic_density_document):
        """
        Print a traffic_density_document.

        traffic_density_document: {
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'traffic_density_values': [[{'edge_object_id', 'traffic_density'}]]
        }
        :param traffic_density_document
        :return: None
        """
        if traffic_density_document is not None:
            print '\nstarting_bus_stop:', traffic_density_document.get('starting_bus_stop')
            print 'ending_bus_stop:', traffic_density_document.get('ending_bus_stop')

            for traffic_density_values_of_path in traffic_density_document.get('traffic_density_values'):
                print 'traffic_density_values_of_path:', traffic_density_values_of_path

    def print_traffic_density_documents(self, bus_stops=None, bus_stop_names=None):
        """
        Print multiple traffic_density_documents.

        traffic_density_document: {
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'traffic_density_values': [[{'edge_object_id', 'traffic_density'}]]
        }
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :return: None
        """
        traffic_density_documents = self.get_traffic_density_documents(
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names
        )
        for traffic_density_document in traffic_density_documents:
            self.print_traffic_density_document(traffic_density_document=traffic_density_document)

    def update_traffic_density(self, edge_object_id, new_traffic_density_value):
        """
        Update the traffic_density value of an edge_document.

        edge_document: {
            '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
            'max_speed', 'road_type', 'way_id', 'traffic_density'
        }
        :param edge_object_id: ObjectId of edge document
        :param new_traffic_density_value: float [0, 1]
        :return: True if an edge_document was updated, otherwise False.
        """
        key = {'_id': ObjectId(edge_object_id)}
        data = {'$set': {'traffic_density': new_traffic_density_value}}
        result = self.edge_documents_collection.update_one(key, data, upsert=False)
        return result.modified_count == 1

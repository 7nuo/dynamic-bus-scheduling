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
        - BusVehicleDocuments
        - EdgeDocuments
        - NodeDocuments
        - PointDocuments
        - TimetableDocuments
        - TrafficEventDocuments
        - TravelRequestDocuments
        - WayDocuments
    """

    def __init__(self, host, port):
        self.mongo_client = MongoClient(host, port)
        self.db = self.mongo_client.dynamic_bus_scheduling
        self.address_documents_collection = self.db.AddressDocuments
        self.bus_line_documents_collection = self.db.BusLineDocuments
        self.bus_stop_documents_collection = self.db.BusStopDocuments
        self.bus_stop_waypoints_documents_collection = self.db.BusStopWaypointsDocuments
        self.bus_vehicle_documents_collection = self.db.BusVehicleDocuments
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
        self.clear_bus_vehicle_documents_collection()
        self.clear_edge_documents_collection()
        self.clear_node_documents_collection()
        self.clear_point_documents_collection()
        self.clear_timetable_documents_collection()
        self.clear_traffic_event_documents_collection()
        self.clear_travel_request_documents_collection()
        self.clear_way_documents_collection()

    def clear_address_documents_collection(self):
        """
        Delete all the documents of the AddressDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.address_documents_collection.delete_many({})
        return result.deleted_count

    def clear_bus_line_documents_collection(self):
        """
        Delete all the documents of the BusLineDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.bus_line_documents_collection.delete_many({})
        return result.deleted_count

    def clear_bus_stop_documents_collection(self):
        """
        Delete all the documents of the BusStopDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.bus_stop_documents_collection.delete_many({})
        return result.deleted_count

    def clear_bus_stop_waypoints_documents_collection(self):
        """
        Delete all the documents of the BusStopWaypointsDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.bus_stop_waypoints_documents_collection.delete_many({})
        return result.deleted_count

    def clear_bus_vehicle_documents_collection(self):
        """
        Delete all the documents of the BusVehicleDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.bus_vehicle_documents_collection.delete_many({})
        return result.deleted_count

    def clear_edge_documents_collection(self):
        """
        Delete all the documents of the EdgeDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.edge_documents_collection.delete_many({})
        return result.deleted_count

    def clear_node_documents_collection(self):
        """
        Delete all the documents of the NodeDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.node_documents_collection.delete_many({})
        return result.deleted_count

    def clear_point_documents_collection(self):
        """
        Delete all the documents of the PointDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.point_documents_collection.delete_many({})
        return result.deleted_count

    def clear_timetable_documents_collection(self):
        """
        Delete all the documents of the TimetableDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.timetable_documents_collection.delete_many({})
        return result.deleted_count

    def clear_traffic_density(self):
        """
        Set the traffic_density values of all edge_documents to 0.
        """
        key = {}
        data = {
            '$set': {
                'traffic_density': 0.0
            }
        }
        self.edge_documents_collection.update_many(key, data, upsert=False)

    def clear_traffic_event_documents_collection(self):
        """
        Delete all the documents of the TrafficEventDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.traffic_event_documents_collection.delete_many({})
        return result.deleted_count

    def clear_travel_request_documents_collection(self):
        """
        Delete all the documents of the TravelRequestDocuments collection.

        :return: The number of deleted documents.
        """
        result = self.travel_request_documents_collection.delete_many({})
        return result.deleted_count

    def clear_way_documents_collection(self):
        """
        Delete all the documents of the WayDocuments collection.

        :return The number of deleted documents.
        """
        result = self.way_documents_collection.delete_many({})
        return result.deleted_count

    def convert_bus_stop_waypoints(self, bus_stop_waypoints_document=None,
                                   detailed_bus_stop_waypoints_document=None):
        """
        Convert a bus_stop_waypoints_document to a detailed_bus_stop_waypoints document.

        :param bus_stop_waypoints_document
        :param detailed_bus_stop_waypoints_document
        :return: converted_bus_stop_waypoints: {
                     'bus_stop_waypoints_document': bus_stop_waypoints_document,
                     'detailed_bus_stop_waypoints_document': detailed_bus_stop_waypoints_document
                 }
        """
        if bus_stop_waypoints_document is not None:
            lists_of_edge_documents = []
            lists_of_edge_object_ids = bus_stop_waypoints_document.get('waypoints')

            for list_of_edge_object_ids in lists_of_edge_object_ids:
                list_of_processed_edge_object_ids = [ObjectId(i) for i in list_of_edge_object_ids]
                list_of_edge_documents = [
                    self.edge_documents_collection.find_one({'_id': i}) for i in list_of_processed_edge_object_ids
                ]
                lists_of_edge_documents.append(list_of_edge_documents)

            detailed_bus_stop_waypoints_document = bus_stop_waypoints_document
            detailed_bus_stop_waypoints_document['waypoints'] = lists_of_edge_documents

        elif detailed_bus_stop_waypoints_document is not None:
            lists_of_edge_object_ids = []
            lists_of_edge_documents = detailed_bus_stop_waypoints_document.get('waypoints')

            for list_of_edge_documents in lists_of_edge_documents:
                list_of_edge_object_ids = [edge_document.get('_id') for edge_document in list_of_edge_documents]
                lists_of_edge_object_ids.append(list_of_edge_object_ids)

            bus_stop_waypoints_document = detailed_bus_stop_waypoints_document
            bus_stop_waypoints_document['waypoints'] = lists_of_edge_object_ids

        converted_bus_stop_waypoints = {
            'bus_stop_waypoints_document': bus_stop_waypoints_document,
            'detailed_bus_stop_waypoints_document': detailed_bus_stop_waypoints_document
        }
        return converted_bus_stop_waypoints

    def delete_address_document(self, object_id=None, name=None):
        """
        Delete an address_document.

        :param object_id: ObjectId
        :param name: string
        :return: True if the address_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.address_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif name is not None:
            result = self.address_documents_collection.delete_one({
                'name': name
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_address_documents(self, object_ids=None, names=None):
        """
        Delete multiple address_documents.

        :param object_ids: [ObjectId]
        :param names: [string]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.address_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif names is not None:
            result = self.address_documents_collection.delete_many({
                'name': {'$in': names}
            })
        else:
            return 0

        return result.deleted_count

    def delete_bus_line_document(self, object_id=None, bus_line_id=None):
        """
        Delete a bus_line_document.

        :param object_id: ObjectId
        :param bus_line_id: int
        :return: True if the bus_line_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.bus_line_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif bus_line_id is not None:
            result = self.bus_line_documents_collection.delete_one({
                'bus_line_id': bus_line_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_bus_line_documents(self, object_ids=None, bus_line_ids=None):
        """
        Delete multiple bus_line_document.

        :param object_ids: [ObjectId]
        :param bus_line_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.bus_line_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif bus_line_ids is not None:
            result = self.bus_line_documents_collection.delete_many({
                'bus_line_id': {'$in': bus_line_ids}
            })
        else:
            return 0

        return result.deleted_count

    def delete_bus_stop_document(self, object_id=None, osm_id=None):
        """
        Delete a bus_stop_document.

        :param object_id: ObjectId
        :param osm_id: int
        :return: True if the bus_stop_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.bus_stop_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif osm_id is not None:
            result = self.bus_stop_documents_collection.delete_one({
                'osm_id': osm_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_bus_stop_documents(self, object_ids=None, osm_ids=None):
        """
        Delete multiple bus_stop_documents.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.bus_stop_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif osm_ids is not None:
            result = self.bus_stop_documents_collection.delete_many({
                'osm_id': {'$in': osm_ids}
            })
        else:
            return 0

        return result.deleted_count

    def delete_bus_stop_waypoints_document(self, object_id=None, starting_bus_stop=None, ending_bus_stop=None,
                                           starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Delete a bus_stop_waypoints_document.

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

        :param object_ids: [ObjectId]
        :return: The number of deleted documents.
        """
        processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
        result = self.bus_stop_waypoints_documents_collection.delete_many({
            '_id': {'$in': processed_object_ids}
        })
        return result.deleted_count

    def delete_bus_vehicle_document(self, object_id=None, bus_vehicle_id=None):
        """
        Delete a bus_vehicle_document.

        :param object_id: ObjectId
        :param bus_vehicle_id: int
        :return: True if the document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.bus_vehicle_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif bus_vehicle_id is not None:
            result = self.bus_vehicle_documents_collection.delete_one({
                'bus_vehicle_id': bus_vehicle_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_bus_vehicle_documents(self, object_ids=None, bus_vehicle_ids=None):
        """
        Delete multiple bus_vehicle_documents.

        :param object_ids: [ObjectId]
        :param bus_vehicle_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.bus_vehicle_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif bus_vehicle_ids is not None:
            result = self.bus_vehicle_documents_collection.delete_many({
                'bus_vehicle_id': {'$in': bus_vehicle_ids}
            })
        else:
            return 0

        return result.deleted_count

    def delete_edge_document(self, object_id=None, starting_node_osm_id=None, ending_node_osm_id=None):
        """
        Delete an edge_document.

        :param object_id: ObjectId
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :return: True if the document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.edge_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
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

        :param object_ids: [ObjectId]
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.edge_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif starting_node_osm_id is not None:
            result = self.edge_documents_collection.delete_many({
                'starting_node.osm_id': starting_node_osm_id
            })
        elif ending_node_osm_id is not None:
            result = self.edge_documents_collection.delete_many({
                'ending_node.osm_id': ending_node_osm_id
            })
        else:
            return 0

        return result.deleted_count

    def delete_node_document(self, object_id=None, osm_id=None):
        """
        Delete a node_document.

        :param object_id: ObjectId
        :param osm_id: int
        :return: True if node_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.node_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif osm_id is not None:
            result = self.node_documents_collection.delete_one({
                'osm_id': osm_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_node_documents(self, object_ids=None, osm_ids=None):
        """
        Delete multiple node_documents.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.node_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif osm_ids is not None:
            result = self.node_documents_collection.delete_many({
                'osm_id': {'$in': osm_ids}
            })
        else:
            return 0

        return result.deleted_count

    def delete_point_document(self, object_id=None, osm_id=None):
        """
        Delete a point_document.

        :param object_id: ObjectId
        :param osm_id: int
        :return: True if the point_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.point_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif osm_id is not None:
            result = self.point_documents_collection.delete_one({
                'osm_id': osm_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_point_documents(self, object_ids=None, osm_ids=None):
        """
        Delete multiple point_document.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.point_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif osm_ids is not None:
            result = self.point_documents_collection.delete_many({
                'osm_id': {'$in': osm_ids}
            })
        else:
            return 0

        return result.deleted_count

    def delete_timetable_document(self, object_id=None, timetable_id=None):
        """
        Delete a timetable_document.

        :param object_id: ObjectId
        :param timetable_id: int
        :return: True if the document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.timetable_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif timetable_id is not None:
            result = self.timetable_documents_collection.delete_one({
                'timetable_id': timetable_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_timetable_documents(self, object_ids=None, timetable_ids=None, bus_line_id=None):
        """
        Delete multiple timetable_documents.

        :param object_ids: [ObjectId]
        :param timetable_ids: [int]
        :param bus_line_id: int
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.timetable_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif timetable_ids is not None:
            result = self.timetable_documents_collection.delete_many({
                'timetable_id': {'$in': timetable_ids}
            })
        elif bus_line_id is not None:
            result = self.timetable_documents_collection.delete_many({
                'bus_line_id': bus_line_id
            })
        else:
            return 0

        return result.deleted_count

    def delete_traffic_event_document(self, object_id=None, event_id=None):
        """
        Delete a traffic_event_document.

        :param object_id: ObjectId
        :param event_id: string
        :return: True if the traffic_event_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.traffic_event_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif event_id is not None:
            result = self.traffic_event_documents_collection.delete_one({
                'event_id': event_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_traffic_event_documents(self, object_ids=None, event_ids=None):
        """
        Delete multiple traffic_event_documents.

        :param object_ids: [ObjectId]
        :param event_ids: [string]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.traffic_event_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif event_ids is not None:
            result = self.traffic_event_documents_collection.delete_many({
                'event_id': {'$in': event_ids}
            })
        else:
            return 0

        return result.deleted_count

    def delete_travel_request_document(self, object_id):
        """
        Delete a travel_request_document.

        :param object_id: ObjectId
        :return: True if the travel_request_document was successfully deleted, otherwise False.
        """
        result = self.travel_request_documents_collection.delete_one({
            '_id': ObjectId(object_id)
        })
        return result.deleted_count == 1

    def delete_travel_request_documents(self, object_ids=None, client_ids=None, bus_line_ids=None,
                                        min_departure_datetime=None, max_departure_datetime=None):
        """
        Delete multiple travel_request_documents.

        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param bus_line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.travel_request_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif client_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            result = self.travel_request_documents_collection.delete_many({
                'client_id': {'$in': client_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif bus_line_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            result = self.travel_request_documents_collection.delete_many({
                'bus_line_id': {'$in': bus_line_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif client_ids is not None:
            result = self.travel_request_documents_collection.delete_many({
                'client_id': {'$in': client_ids}
            })
        elif bus_line_ids is not None:
            result = self.travel_request_documents_collection.delete_many({
                'bus_line_id': {'$in': bus_line_ids}
            })
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

        :param object_id: ObjectId
        :param osm_id: int
        :return: True if the way_document was successfully deleted, otherwise False.
        """
        if object_id is not None:
            result = self.way_documents_collection.delete_one({
                '_id': ObjectId(object_id)
            })
        elif osm_id is not None:
            result = self.way_documents_collection.delete_one({
                'osm_id': osm_id
            })
        else:
            return False

        return result.deleted_count == 1

    def delete_way_documents(self, object_ids=None, osm_ids=None):
        """
        Delete multiple way_documents.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :return: The number of deleted documents.
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            result = self.way_documents_collection.delete_many({
                '_id': {'$in': processed_object_ids}
            })
        elif osm_ids is not None:
            result = self.way_documents_collection.delete_many({
                'osm_id': {'$in': osm_ids}
            })
        else:
            return 0

        return result.deleted_count

    def find_address_document(self, object_id=None, name=None, node_id=None, longitude=None, latitude=None):
        """
        Retrieve an address_document.

        :param object_id: ObjectId
        :param name: string
        :param node_id: int
        :param longitude: float
        :param latitude: float
        :return: address_document
        """
        if object_id is not None:
            address_document = self.address_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif name is not None:
            address_document = self.address_documents_collection.find_one({
                'name': name
            })
        elif node_id is not None:
            address_document = self.address_documents_collection.find_one({
                'node_id': node_id
            })
        elif longitude is not None and latitude is not None:
            address_document = self.address_documents_collection.find_one({
                'point': {
                    'longitude': longitude,
                    'latitude': latitude
                }
            })
        else:
            return None

        return address_document

    def find_address_documents(self, object_ids=None, names=None, node_ids=None, in_dictionary=False):
        """
        Retrieve multiple address_documents.

        :param object_ids: [ObjectId]
        :param names: [string]
        :param node_ids: [int]
        :param in_dictionary: bool
        :return: address_documents: [address_document] or {name -> address_document}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            address_documents_cursor = self.address_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif names is not None:
            address_documents_cursor = self.address_documents_collection.find({
                'name': {'$in': names}
            })
        elif node_ids is not None:
            address_documents_cursor = self.address_documents_collection.find({
                'node_id': {'$in': node_ids}
            })
        else:
            address_documents_cursor = self.address_documents_collection.find({})

        if in_dictionary:
            address_documents = {}

            for address_document in address_documents_cursor:
                name = address_document.get('name')
                address_documents[name] = address_document
        else:
            address_documents = list(address_documents_cursor)

        return address_documents

    def find_bus_line_document(self, object_id=None, bus_line_id=None):
        """
        Retrieve a bus_line_document.

        :param object_id: ObjectId
        :param bus_line_id: int
        :return: bus_line_document
        """
        if object_id is not None:
            bus_line_document = self.bus_line_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif bus_line_id is not None:
            bus_line_document = self.bus_line_documents_collection.find_one({
                'bus_line_id': bus_line_id
            })
        else:
            return None

        return bus_line_document

    def find_bus_line_documents(self, object_ids=None, bus_line_ids=None, in_dictionary=False):
        """
        Retrieve multiple bus_line_documents.

        :param object_ids: [ObjectId]
        :param bus_line_ids: [int]
        :param in_dictionary: bool
        :return: bus_line_documents: [bus_line_document] or {bus_line_id -> bus_line_document}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            bus_line_documents_cursor = self.bus_line_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif bus_line_ids is not None:
            bus_line_documents_cursor = self.bus_line_documents_collection.find({
                'bus_line_id': {'$in': bus_line_ids}
            })
        else:
            bus_line_documents_cursor = self.bus_line_documents_collection.find({})

        if in_dictionary:
            bus_line_documents = {}

            for bus_line_document in bus_line_documents_cursor:
                bus_line_id = bus_line_document.get('bus_line_id')
                bus_line_documents[bus_line_id] = bus_line_document
        else:
            bus_line_documents = list(bus_line_documents_cursor)

        return bus_line_documents

    def find_bus_stop_document(self, object_id=None, osm_id=None, name=None, longitude=None, latitude=None):
        """
        Retrieve a bus_stop_document.

        :param object_id: ObjectId
        :param osm_id: int
        :param name: string
        :param longitude: float
        :param latitude: float
        :return: bus_stop_document
        """
        if object_id is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif osm_id is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({
                'osm_id': osm_id
            })
        elif name is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({
                'name': name
            })
        elif longitude is not None and latitude is not None:
            bus_stop_document = self.bus_stop_documents_collection.find_one({
                'point': {
                    'longitude': longitude,
                    'latitude': latitude
                }
            })
        else:
            return None

        return bus_stop_document

    def find_bus_stop_documents(self, object_ids=None, osm_ids=None, names=None, in_dictionary=False):
        """
        Retrieve multiple bus_stop_documents.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param names: [string]
        :param in_dictionary: bool
        :return: bus_stop_documents: [bus_stop_document] or {name -> bus_stop_document}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif osm_ids is not None:
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({
                'osm_id': {'$in': osm_ids}
            })
        elif names is not None:
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({
                'name': {'$in': names}
            })
        else:
            bus_stop_documents_cursor = self.bus_stop_documents_collection.find({})

        if in_dictionary:
            bus_stop_documents = {}

            for bus_stop_document in bus_stop_documents_cursor:
                name = bus_stop_document.get('name')
                bus_stop_documents[name] = bus_stop_document
        else:
            bus_stop_documents = list(bus_stop_documents_cursor)

        return bus_stop_documents

    def find_bus_stop_waypoints_document(self, object_id=None, starting_bus_stop=None, ending_bus_stop=None,
                                         starting_bus_stop_name=None, ending_bus_stop_name=None):
        """
        Retrieve a bus_stop_waypoints_document.

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

    def find_bus_stop_waypoints_documents(self, object_ids=None, bus_stops=None, bus_stop_names=None, bus_line_id=None):
        """
        Retrieve multiple bus_stop_waypoints_documents.

        :param object_ids: [ObjectId]
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :param bus_line_id: int
        :return: bus_stop_waypoints_documents: [bus_stop_waypoints_document]
        """
        bus_stop_waypoints_documents = []

        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            bus_stop_waypoints_documents_cursor = self.bus_stop_waypoints_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
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

        elif bus_line_id is not None:
            bus_line_document = self.find_bus_line_document(bus_line_id=bus_line_id)

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
        converted_bus_stop_waypoints = self.convert_bus_stop_waypoints(
            bus_stop_waypoints_document=bus_stop_waypoints_document
        )
        detailed_bus_stop_waypoints_document = converted_bus_stop_waypoints.get(
            'detailed_bus_stop_waypoints_document'
        )
        return detailed_bus_stop_waypoints_document

    def find_detailed_bus_stop_waypoints_documents(self, object_ids=None, bus_stops=None,
                                                   bus_stop_names=None, bus_line_id=None):
        """
        Retrieve multiple detailed_bus_stop_waypoints_documents.

        :param object_ids: [ObjectId]
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :param bus_line_id: int
        :return: detailed_bus_stop_waypoints_documents: [detailed_bus_stop_waypoints_document]
        """
        detailed_bus_stop_waypoints_documents = []
        bus_stop_waypoints_documents = self.find_bus_stop_waypoints_documents(
            object_ids=object_ids,
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names,
            bus_line_id=bus_line_id
        )
        for bus_stop_waypoints_document in bus_stop_waypoints_documents:
            converted_bus_stop_waypoints = self.convert_bus_stop_waypoints(
                bus_stop_waypoints_document=bus_stop_waypoints_document
            )
            detailed_bus_stop_waypoints_document = converted_bus_stop_waypoints.get(
                'detailed_bus_stop_waypoints_document'
            )
            detailed_bus_stop_waypoints_documents.append(detailed_bus_stop_waypoints_document)

        return detailed_bus_stop_waypoints_documents

    def find_bus_vehicle_document(self, object_id=None, bus_vehicle_id=None):
        """
        Retrieve a bus_vehicle_document.

        :param object_id: ObjectId
        :param bus_vehicle_id: int
        :return: bus_vehicle_document
        """
        if object_id is not None:
            bus_vehicle_document = self.bus_vehicle_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif bus_vehicle_id is not None:
            bus_vehicle_document = self.bus_vehicle_documents_collection.find_one({
                'bus_vehicle_id': bus_vehicle_id
            })
        else:
            return None

        return bus_vehicle_document

    def find_bus_vehicle_documents(self, object_ids=None, bus_vehicle_ids=None, in_dictionary=False):
        """
        Retrieve multiple bus_vehicle_documents.

        :param object_ids: [ObjectId]
        :param bus_vehicle_ids: [int]
        :param in_dictionary: bool
        :return: bus_vehicle_documents: [bus_vehicle_document] or {bus_vehicle_id -> bus_vehicle_document}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            bus_vehicle_documents_cursor = self.bus_vehicle_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif bus_vehicle_ids is not None:
            bus_vehicle_documents_cursor = self.bus_vehicle_documents_collection.find({
                'bus_vehicle_id': {'$in': bus_vehicle_ids}
            })
        else:
            bus_vehicle_documents_cursor = self.bus_vehicle_documents_collection.find({})

        if in_dictionary:
            bus_vehicle_documents = {}

            for bus_vehicle_document in bus_vehicle_documents_cursor:
                bus_vehicle_id = bus_vehicle_document.get('bus_vehicle_id')
                bus_vehicle_documents[bus_vehicle_id] = bus_vehicle_document
        else:
            bus_vehicle_documents = list(bus_vehicle_documents_cursor)

        return bus_vehicle_documents

    def find_edge_document(self, object_id=None, starting_node_osm_id=None, ending_node_osm_id=None):
        """
        Retrieve an edge_document.

        :param object_id: ObjectId
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :return: edge_document
        """
        if object_id is not None:
            edge_document = self.edge_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif starting_node_osm_id is not None and ending_node_osm_id is not None:
            edge_document = self.edge_documents_collection.find_one({
                'starting_node.osm_id': starting_node_osm_id,
                'ending_node.oms_id': ending_node_osm_id}
            )
        else:
            return None

        return edge_document

    def find_edge_documents(self, object_ids=None, starting_node_osm_id=None,
                            ending_node_osm_id=None, in_dictionary=False):
        """
        Retrieve multiple edge_documents.

        :param object_ids: [ObjectId]
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :param in_dictionary: bool
        :return: edge_documents: [edge_document] or {starting_node_osm_id -> [edge_document]}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            edge_documents_cursor = self.edge_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif starting_node_osm_id is not None:
            edge_documents_cursor = self.edge_documents_collection.find({
                'starting_node.osm_id': starting_node_osm_id
            })
        elif ending_node_osm_id is not None:
            edge_documents_cursor = self.edge_documents_collection.find({
                'ending_node.oms_id': ending_node_osm_id
            })
        else:
            edge_documents_cursor = self.edge_documents_collection.find({})

        if in_dictionary:
            edge_documents = {}

            for edge_document in edge_documents_cursor:
                starting_node_osm_id = edge_document.get('starting_node').get('osm_id')

                if starting_node_osm_id in edge_documents:
                    edge_documents[starting_node_osm_id].append(edge_document)
                else:
                    edge_documents[starting_node_osm_id] = list(edge_document)
        else:
            edge_documents = list(edge_documents_cursor)

        return edge_documents

    def find_node_document(self, object_id=None, osm_id=None, longitude=None, latitude=None):
        """
        Retrieve a node_document.

        :param object_id: ObjectId
        :param osm_id: int
        :param longitude: float
        :param latitude: float
        :return: node_document
        """
        if object_id is not None:
            node_document = self.node_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif osm_id is not None:
            node_document = self.node_documents_collection.find_one({
                'osm_id': osm_id
            })
        elif longitude is not None and latitude is not None:
            node_document = self.node_documents_collection.find_one({
                'point': {
                    'longitude': longitude,
                    'latitude': latitude
                }
            })
        else:
            return None

        return node_document

    def find_node_documents(self, object_ids=None, osm_ids=None, in_dictionary=False):
        """
        Retrieve multiple node_documents.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param in_dictionary: bool
        :return: node_documents: [node_document] or {osm_id -> node_document}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            node_documents_cursor = self.node_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif osm_ids is not None:
            node_documents_cursor = self.node_documents_collection.find({
                'osm_id': {'$in': osm_ids}
            })
        else:
            node_documents_cursor = self.node_documents_collection.find({})

        if in_dictionary:
            node_documents = {}

            for node_document in node_documents_cursor:
                osm_id = node_document.get('osm_id')
                node_documents[osm_id] = node_document
        else:
            node_documents = list(node_documents_cursor)

        return node_documents

    def find_point_document(self, object_id=None, osm_id=None, longitude=None, latitude=None):
        """
        Retrieve a point_document.

        :param object_id: ObjectId
        :param osm_id: int
        :param longitude: float
        :param latitude: float
        :return: point_document
        """
        if object_id is not None:
            point_document = self.point_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif osm_id is not None:
            point_document = self.point_documents_collection.find_one({
                'osm_id': osm_id
            })
        elif longitude is not None and latitude is not None:
            point_document = self.point_documents_collection.find_one({
                'point': {
                    'longitude': longitude,
                    'latitude': latitude
                }
            })
        else:
            return None

        return point_document

    def find_point_documents(self, object_ids=None, osm_ids=None, in_dictionary=False):
        """
        Retrieve multiple point_documents.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param in_dictionary: bool
        :return: point_documents: [point_document] or {osm_id -> point_document}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            point_documents_cursor = self.point_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif osm_ids is not None:
            point_documents_cursor = self.point_documents_collection.find({
                'osm_id': {'$in': osm_ids}
            })
        else:
            point_documents_cursor = self.point_documents_collection.find({})

        if in_dictionary:
            point_documents = {}

            for point_document in point_documents_cursor:
                osm_id = point_document.get('osm_id')
                point_documents[osm_id] = point_document
        else:
            point_documents = list(point_documents_cursor)

        return point_documents

    def find_timetable_document(self, object_id=None, timetable_id=None):
        """
        Retrieve a timetable_document.

        :param object_id: ObjectId
        :param timetable_id: int
        :return: timetable_document
        """
        if object_id is not None:
            timetable_document = self.timetable_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif timetable_id is not None:
            timetable_document = self.timetable_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        else:
            return None

        return timetable_document

    def find_timetable_documents(self, object_ids=None, timetable_ids=None, bus_line_ids=None, in_dictionary=False):
        """
        Retrieve multiple timetable_documents.

        :param object_ids: [ObjectId]
        :param timetable_ids: [int]
        :param bus_line_ids: [int]
        :param in_dictionary: bool
        :return: timetable_documents: [timetable_document] or {timetable_id -> timetable_document}
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            timetable_documents_cursor = self.timetable_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif timetable_ids is not None:
            timetable_documents_cursor = self.timetable_documents_collection.find({
                'timetable_id': {'$in': timetable_ids}
            })
        elif bus_line_ids is not None:
            timetable_documents_cursor = self.timetable_documents_collection.find({
                'bus_line_id': {'$in': bus_line_ids}
            })
        else:
            timetable_documents_cursor = self.timetable_documents_collection.find({})

        if in_dictionary:
            timetable_documents = {}

            for timetable_document in timetable_documents_cursor:
                timetable_id = timetable_document.get('timetable_id')
                timetable_documents[timetable_id] = timetable_document
        else:
            timetable_documents = list(timetable_documents_cursor)

        return timetable_documents

    def find_traffic_event_document(self, object_id=None, event_id=None):
        """
        Retrieve a traffic_event_document.

        :param object_id: ObjectId
        :param event_id: string
        :return: traffic_event_document
        """
        if object_id is not None:
            traffic_event_document = self.traffic_event_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif event_id is not None:
            traffic_event_document = self.traffic_event_documents_collection.find_one({
                'event_id': event_id
            })
        else:
            return None

        return traffic_event_document

    def find_traffic_event_documents(self, object_ids=None, event_ids=None, in_dictionary=False):
        """
        Retrieve multiple traffic_event_documents.

        :param object_ids: [ObjectId]
        :param event_ids: [string]
        :param in_dictionary: bool
        :return: traffic_event_documents: [traffic_event_document] or {event_id -> traffic_event_document}
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

        if in_dictionary:
            traffic_event_documents = {}

            for traffic_event_document in traffic_event_documents_cursor:
                event_id = traffic_event_document.get('event_id')
                traffic_event_documents[event_id] = traffic_event_document
        else:
            traffic_event_documents = list(traffic_event_documents_cursor)

        return traffic_event_documents

    def find_travel_request_document(self, object_id):
        """
        Retrieve a travel_request_document.

        :param object_id: ObjectId
        :return: travel_request_document
        """
        travel_request_document = self.travel_request_documents_collection.find_one({'_id': ObjectId(object_id)})
        return travel_request_document

    def find_travel_request_documents(self, object_ids=None, client_ids=None, bus_line_ids=None,
                                      min_departure_datetime=None, max_departure_datetime=None, in_dictionary=False):
        """
        Retrieve multiple travel_request_documents.

        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param bus_line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :param in_dictionary: bool
        :return: travel_request_documents: [travel_request_document] or {client_id: [travel_request_document]}
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
        elif bus_line_ids is not None and min_departure_datetime is not None and max_departure_datetime is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'bus_line_id': {'$in': bus_line_ids},
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        elif client_ids is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'client_id': {'$in': client_ids}
            })
        elif bus_line_ids is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'bus_line_id': {'$in': bus_line_ids}
            })
        elif min_departure_datetime is not None and max_departure_datetime is not None:
            travel_requests_cursor = self.travel_request_documents_collection.find({
                'departure_datetime': {'$gt': min_departure_datetime},
                'departure_datetime': {'$lt': max_departure_datetime}
            })
        else:
            travel_requests_cursor = self.travel_request_documents_collection.find({})

        if in_dictionary:
            travel_requests = {}

            for travel_request in travel_requests_cursor:
                client_id = travel_request.get('client_id')

                if client_id in travel_requests:
                    travel_requests[client_id].append(travel_request)
                else:
                    travel_requests[client_id] = list(travel_request)
        else:
            travel_requests = list(travel_requests_cursor)

        return travel_requests

    def find_way_document(self, object_id=None, osm_id=None):
        """
        Retrieve a way_document.

        :param object_id: ObjectId
        :param osm_id: int
        :return: way_document
        """
        if object_id is not None:
            way_document = self.way_documents_collection.find_one({
                '_id': ObjectId(object_id)
            })
        elif osm_id is not None:
            way_document = self.way_documents_collection.find_one({
                'osm_id': osm_id
            })
        else:
            return None

        return way_document

    def find_way_documents(self, object_ids=None, osm_ids=None, in_dictionary=False):
        """
        Retrieve multiple way_documents.

        :param object_ids: [ObjectId]
        :param osm_ids: [int]
        :param in_dictionary: bool
        :return: way_documents: [way_document]
        """
        if object_ids is not None:
            processed_object_ids = [ObjectId(object_id) for object_id in object_ids]
            way_documents_cursor = self.way_documents_collection.find({
                '_id': {'$in': processed_object_ids}
            })
        elif osm_ids is not None:
            way_documents_cursor = self.way_documents_collection.find({
                'osm_id': {'$in': osm_ids}
            })
        else:
            way_documents_cursor = self.way_documents_collection.find({})

        if in_dictionary:
            way_documents = {}

            for way_document in way_documents_cursor:
                osm_id = way_document.get('osm_id')
                way_documents[osm_id] = way_document
        else:
            way_documents = list(way_documents_cursor)

        return way_documents

    # def get_bus_line_documents_cursor(self):
    #     """
    #     Retrieve a cursor of all bus_line_documents.
    #
    #     :return: bus_line_documents_cursor
    #     """
    #     bus_line_documents_cursor = self.bus_line_documents_collection.find({})
    #     return bus_line_documents_cursor
    #
    # def get_bus_lines(self):
    #     """
    #     Retrieve a dictionary containing all the bus_line_documents.
    #
    #     :return: bus_lines: {bus_line_id -> bus_line_document}
    #     """
    #     bus_lines = {}
    #     bus_line_documents_cursor = self.get_bus_line_documents_cursor()
    #
    #     for bus_line_document in bus_line_documents_cursor:
    #         bus_line_id = bus_line_document.get('bus_line_id')
    #         bus_lines[bus_line_id] = bus_line_document
    #
    #     return bus_lines
    #
    # def get_bus_line_documents_list(self):
    #     """
    #     Retrieve a list containing all the bus_line_documents.
    #
    #     :return: bus_line_documents_list: [bus_line_document]
    #     """
    #     bus_line_documents_cursor = self.get_bus_line_documents_cursor()
    #     bus_line_documents_list = list(bus_line_documents_cursor)
    #     return bus_line_documents_list

    # def get_bus_stop_documents_cursor(self):
    #     """
    #     Retrieve a cursor of all bus_stop_documents.
    #
    #     :return: bus_stop_documents_cursor
    #     """
    #     bus_stop_documents_cursor = self.bus_stop_documents_collection.find({})
    #     return bus_stop_documents_cursor
    #
    # def get_bus_stops(self):
    #     """
    #     Retrieve a dictionary containing all the bus_stop_documents.
    #
    #     :return: bus_stops: {name -> bus_stop_document}
    #     """
    #     bus_stops = {}
    #     bus_stop_documents_cursor = self.get_bus_stop_documents_cursor()
    #
    #     for bus_stop_document in bus_stop_documents_cursor:
    #         name = bus_stop_document.get('name')
    #
    #         if name not in bus_stops:
    #             bus_stops[name] = bus_stop_document
    #
    #     return bus_stops
    #
    # def get_bus_stop_documents_list(self):
    #     """
    #     Retrieve a list containing all the bus_stop_documents.
    #
    #     :return: bus_stop_documents_list: [bus_stop_document]
    #     """
    #     bus_stop_documents_cursor = self.get_bus_stop_documents_cursor()
    #     bus_stop_documents_list = list(bus_stop_documents_cursor)
    #     return bus_stop_documents_list

    # def get_edge_documents_cursor(self):
    #     """
    #     Retrieve a cursor of all the edge_documents.
    #
    #     :return: edge_documents_cursor
    #     """
    #     edge_documents_cursor = self.edge_documents_collection.find({})
    #     return edge_documents_cursor
    #
    # def get_edges_dictionary(self):
    #     """
    #     Retrieve a dictionary containing all the edge_documents.
    #
    #     :return: edges: {starting_node_osm_id -> [edge_document]}
    #     """
    #     edges = {}
    #     edge_documents_cursor = self.get_edge_documents_cursor()
    #
    #     for edge_document in edge_documents_cursor:
    #         starting_node_osm_id = edge_document.get('starting_node').get('osm_id')
    #
    #         if starting_node_osm_id in edges:
    #             edges[starting_node_osm_id].append(edge_document)
    #         else:
    #             edges[starting_node_osm_id] = [edge_document]
    #
    #     return edges
    #
    # def get_edge_documents_list(self):
    #     """
    #     Retrieve a list containing all the edge_documents.
    #
    #     :return: edge_documents_list: [edge_document]
    #     """
    #     edge_documents_cursor = self.get_edge_documents_cursor()
    #     edge_documents_list = list(edge_documents_cursor)
    #     return edge_documents_list

    def get_edge_documents_included_in_bus_line(self, bus_line=None, bus_line_id=None):
        """
        Get a list containing all the edge_documents which are contained in the waypoints of a bus_line.

        :param bus_line: bus_line_document
        :param bus_line_id: int
        :return: edge_documents: [edge_document]
        """
        edge_object_ids = self.get_edge_object_ids_included_in_bus_line(
            bus_line=bus_line,
            bus_line_id=bus_line_id
        )
        edge_documents = self.find_edge_documents(object_ids=edge_object_ids)
        return edge_documents

    def get_edge_documents_included_in_bus_stop_waypoints(self, bus_stop_waypoints):
        """
        Get a list containing all the edge_documents which are included in a bus_stop_waypoints document.

        :param bus_stop_waypoints: bus_stop_waypoints_document
        :return: edge_documents: [edge_document]
        """

        edge_object_ids = self.get_edge_object_ids_included_in_bus_stop_waypoints(
            bus_stop_waypoints=bus_stop_waypoints
        )
        edge_documents = self.find_edge_documents(object_ids=edge_object_ids)
        return edge_documents

    def get_edge_object_ids_included_in_bus_line(self, bus_line=None, bus_line_id=None):
        """
        Get a list containing the object_ids of the edge_documents,
        which are included in the waypoints of a bus_line.

        :param bus_line: bus_line_document
        :param bus_line_id: int
        :return: edge_object_ids: [edge_object_id]
        """
        edge_object_ids = []

        if bus_line is None and bus_line_id is None:
            return edge_object_ids
        elif bus_line is None:
            bus_line = self.find_bus_line_document(bus_line_id=bus_line_id)
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

        :return: ending_nodes_dictionary: {ending_node_osm_id -> [edge_document]}
        """
        ending_nodes_dictionary = {}
        edge_documents = self.find_edge_documents()

        for edge_document in edge_documents:
            ending_node_osm_id = edge_document.get('ending_node').get('osm_id')

            if ending_node_osm_id in ending_nodes_dictionary:
                ending_nodes_dictionary[ending_node_osm_id].append(edge_document)
            else:
                ending_nodes_dictionary[ending_node_osm_id] = list(edge_document)

        return ending_nodes_dictionary

    def get_maximum_or_minimum(self, collection, maximum=True):
        """
        Get maximum or minimum.

        :param collection: ('bus_line' or 'bus_vehicle' or 'timetable' or 'travel_request')
        :param maximum: bool
        :return: maximum or minimum ('bus_line_id' or 'bus_vehicle_id' or 'timetable_id' or 'client_id')
                 (0 if there is no element)
        """
        # order: (-1: Descending Order, 1: Ascending Order)
        if maximum:
            order = -1
        else:
            order = 1

        # The corresponding collection is sorted and a cursor containing the first element is retrieved.
        if collection == 'bus_line':
            comparison_entry = 'bus_line_id'
            comparison_cursor = self.bus_line_documents_collection.find({}).sort(comparison_entry, order).limit(1)

        elif collection == 'bus_vehicle':
            comparison_entry = 'bus_vehicle_id'
            comparison_cursor = self.bus_vehicle_documents_collection.find({}).sort(comparison_entry, order).limit(1)

        elif collection == 'timetable':
            comparison_entry = 'timetable_id'
            comparison_cursor = self.timetable_documents_collection.find({}).sort(comparison_entry, order).limit(1)

        elif collection == 'travel_request':
            comparison_entry = 'client_id'
            comparison_cursor = self.travel_request_documents_collection.find({}).sort(comparison_entry, order).limit(1)

        else:
            return 0

        # The first element is retrieved.
        result = [cursor_element.get(comparison_entry) for cursor_element in comparison_cursor]
        if result:
            return result[0]
        else:
            return 0

    # def get_node_documents_cursor(self):
    #     """
    #     Retrieve a cursor of all node_documents.
    #
    #     :return: node_documents_cursor
    #     """
    #     node_documents_cursor = self.node_documents_collection.find({})
    #     return node_documents_cursor
    #
    # def get_node_documents_list(self):
    #     """
    #     Retrieve a list containing all the node_documents.
    #
    #     :return: node_documents_list: [node_document]
    #     """
    #     node_documents_cursor = self.node_documents_collection.find({})
    #     node_documents_list = list(node_documents_cursor)
    #     return node_documents_list
    #
    # def get_point_documents_cursor(self):
    #     """
    #     Retrieve a cursor of all point_documents.
    #
    #     :return: point_documents_cursor
    #     """
    #     point_documents_cursor = self.point_documents_collection.find({})
    #     return point_documents_cursor
    #
    # def get_points(self):
    #     """
    #     Retrieve a dictionary containing all the point_documents.
    #
    #     :return points: {osm_id -> point_document}
    #     """
    #     points = {}
    #     point_documents_cursor = self.get_point_documents_cursor()
    #
    #     for point_document in point_documents_cursor:
    #         osm_id = point_document.get('osm_id')
    #         points[osm_id] = point_document
    #
    #     return points
    #
    # def get_point_documents_list(self):
    #     """
    #     Retrieve a list containing all the point_documents.
    #
    #     :return: point_documents_list: [point_document]
    #     """
    #     point_documents_cursor = self.point_documents_collection.find({})
    #     point_documents_list = list(point_documents_cursor)
    #     return point_documents_list

    # def get_timetable_documents_cursor(self):
    #     """
    #     Retrieve a cursor of all timetable_documents.
    #
    #     :return: timetable_documents_cursor
    #     """
    #     timetable_documents_cursor = self.timetable_documents_collection.find({})
    #     return timetable_documents_cursor
    #
    # def get_timetable_documents_list(self):
    #     """
    #     Retrieve a list containing all the timetable_documents.
    #
    #     :return: timetable_documents_list: [timetable_document]
    #     """
    #     timetable_documents_cursor = self.timetable_documents_collection.find({})
    #     timetable_documents_list = list(timetable_documents_cursor)
    #     return timetable_documents_list

    def get_traffic_density_documents(self, bus_stops=None, bus_stop_names=None):
        """
        Get multiple traffic_density_documents.

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

    # def get_travel_request_documents_cursor(self):
    #     """
    #     Retrieve a cursor of all travel_request_documents.
    #
    #     :return: travel_request_documents_cursor
    #     """
    #     travel_request_documents_cursor = self.travel_request_documents_collection.find({})
    #     return travel_request_documents_cursor
    #
    # def get_travel_request_documents_list(self):
    #     """
    #     Retrieve a list containing all the travel_request_documents.
    #
    #     :return: travel_request_documents_list: [travel_request_document]
    #     """
    #     travel_request_documents_cursor = self.get_travel_request_documents_cursor()
    #     travel_request_documents_list = list(travel_request_documents_cursor)
    #     return travel_request_documents_list

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
                'point': {
                    'longitude': point.longitude,
                    'latitude': point.latitude
                }
            }

        result = self.address_documents_collection.insert_one(address_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_address_documents(self, address_documents):
        """
        Insert multiple address_documents.

        :param address_documents: [address_document]
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if address_documents:
            result = self.address_documents_collection.insert_many(address_documents)
            new_object_ids = result.inserted_ids

        return new_object_ids

    def insert_bus_line_document(self, bus_line_document=None, bus_line_id=None, bus_stops=None):
        """
        Insert a new bus_line_document or update, if it already exists in the database.

        :param bus_line_document
        :param bus_line_id: int
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :return: new_object_id: ObjectId
        """
        if bus_line_document is None and (bus_line_id is None or bus_stops is None):
            return None

        elif bus_line_document is not None:
            object_id = bus_line_document.get('_id')

            if object_id is not None:
                key = {
                    '_id': ObjectId(object_id)
                }
                data = {
                    '$set': {
                        'bus_line_id': bus_line_document.get('bus_line_id'),
                        'bus_stops': bus_line_document.get('bus_stops')
                    }
                }
            else:
                key = {
                    'bus_line_id': bus_line_document.get('bus_line_id')
                }
                data = {
                    '$set': {
                        'bus_stops': bus_line_document.get('bus_stops')
                    }
                }
        else:
            key = {
                'bus_line_id': bus_line_id
            }
            data = {
                '$set': {
                    'bus_stops': bus_stops
                }
            }

        result = self.bus_line_documents_collection.update_one(key, data, upsert=True)
        new_object_id = result.upserted_id
        return new_object_id

    def insert_bus_line_documents(self, bus_line_documents):
        """
        Insert a list of bus_line_documents or update, if it already exists in the database.

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
                'point': {
                    'longitude': point.longitude,
                    'latitude': point.latitude
                }
            }

        result = self.bus_stop_documents_collection.insert_one(bus_stop_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_bus_stop_documents(self, bus_stop_documents):
        """
        Insert multiple bus_stop documents.

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

        :param bus_stop_waypoints_document
        :param starting_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param waypoints: [[edge_object_id]]
        :return: new_object_id: ObjectId
        """
        if bus_stop_waypoints_document is not None:
            key = {
                '_id': ObjectId(bus_stop_waypoints_document.get('_id'))
            }
            data = {
                '$set': {
                    'starting_bus_stop': bus_stop_waypoints_document.get('starting_bus_stop'),
                    'ending_bus_stop': bus_stop_waypoints_document.get('ending_bus_stop'),
                    'waypoints': bus_stop_waypoints_document.get('waypoints')
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
        if bus_vehicle_document is not None:
            key = {
                '_id': ObjectId(bus_vehicle_document.get('_id'))
            }
            data = {
                '$set': {
                    'bus_vehicle_id': bus_vehicle_document.get('bus_vehicle_id'),
                    'maximum_capacity': bus_vehicle_document.get('maximum_capacity'),
                    'routes': bus_vehicle_document.get('routes')
                }
            }
            result = self.bus_vehicle_documents_collection.update_one(key, data, upsert=True)
            new_object_id = result.upserted_id
        else:
            bus_vehicle_document = {
                'bus_vehicle_id': bus_vehicle_id,
                'maximum_capacity': maximum_capacity,
                'routes': routes
            }
            result = self.bus_vehicle_documents_collection.insert_one(bus_vehicle_document)
            new_object_id = result.inserted_id

        return new_object_id

    def insert_bus_vehicle_documents(self, bus_vehicle_documents, insert_many=False):
        """
        Insert multiple bus_vehicle_documents or update existing ones.

        :param bus_vehicle_documents:
        :param insert_many: bool
        :return: new_object_ids: [ObjectId]
        """
        new_object_ids = []

        if bus_vehicle_documents:
            if insert_many:
                result = self.bus_vehicle_documents_collection.insert_many(bus_vehicle_documents)
                new_object_ids = result.inserted_ids
            else:
                for bus_vehicle_document in bus_vehicle_documents:
                    new_object_id = self.insert_bus_vehicle_document(bus_vehicle_document=bus_vehicle_document)
                    new_object_ids.append(new_object_id)

        return new_object_ids

    def insert_edge_document(self, edge_document=None, starting_node=None, ending_node=None,
                             max_speed=None, road_type=None, way_id=None, traffic_density=None):
        """
        Insert an edge_document.

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
                'starting_node': starting_node,
                'ending_node': ending_node,
                'max_speed': max_speed,
                'road_type': road_type,
                'way_id': way_id,
                'traffic_density': traffic_density
            }

        result = self.edge_documents_collection.insert_one(edge_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_edge_documents(self, edge_documents):
        """
        Insert multiple edge_documents.

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

        :param node_document
        :param osm_id: int
        :param tags: dict
        :param point: Point
        :return: new_object_id: ObjectId
        """
        if node_document is None:
            node_document = {
                'osm_id': osm_id,
                'tags': tags,
                'point': {
                    'longitude': point.longitude,
                    'latitude': point.latitude
                }
            }

        result = self.node_documents_collection.insert_one(node_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_node_documents(self, node_documents):
        """
        Insert multiple node_documents.

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

        :param point_document
        :param osm_id: int
        :param point: Point
        :return: new_object_id: ObjectId
        """
        if point_document is None:
            point_document = {
                'osm_id': osm_id,
                'point': {
                    'longitude': point.longitude,
                    'latitude': point.latitude
                }
            }

        result = self.point_documents_collection.insert_one(point_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_point_documents(self, point_documents):
        """
        Insert multiple point_documents.

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

        :param timetable: timetable_document
        :return: new_object_id: ObjectId
        """
        key = {
            '_id': ObjectId(timetable.get('_id'))
        }
        data = {
            '$set': {
                'bus_line_id': timetable.get('bus_line_id'),
                'timetable_entries': timetable.get('timetable_entries'),
                'travel_requests': timetable.get('travel_requests')
            }
        }
        result = self.timetable_documents_collection.update_one(key, data, upsert=True)
        new_object_id = result.upserted_id
        return new_object_id

    def insert_timetable_documents(self, timetable_documents):
        """
        Insert multiple new timetable_documents or update, if they already exist in the database.

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

        :param traffic_event_document
        :return: new_object_id: ObjectId
        """
        key = {
            'event_id': traffic_event_document.get('event_id')
        }
        data = {
            '$set': {
                'event_type': traffic_event_document.get('event_type'),
                'event_level': traffic_event_document.get('event_level'),
                'point': traffic_event_document.get('point'),
                'datetime': traffic_event_document.get('datetime')
            }
        }
        result = self.traffic_event_documents_collection.update_one(key, data, upsert=True)
        new_object_id = result.upserted_id
        return new_object_id

    def insert_traffic_event_documents(self, traffic_event_documents):
        """
        Insert multiple new traffic_event_documents or update, if they already exist in the database.

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

    def insert_travel_request_document(self, travel_request_document=None, client_id=None, bus_line_id=None,
                                       starting_bus_stop=None, ending_bus_stop=None,
                                       departure_datetime=None, arrival_datetime=None,
                                       starting_timetable_entry_index=None, ending_timetable_entry_index=None):
        """
        Insert a travel_request_document.

        :param travel_request_document
        :param client_id: int
        :param bus_line_id: int
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
                'bus_line_id': bus_line_id,
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

        :param way_document
        :param osm_id: int
        :param tags: dict
        :param references: [osm_id]
        :return: new_object_id: ObjectId
        """
        if way_document is None:
            way_document = {
                'osm_id': osm_id,
                'tags': tags,
                'references': references
            }

        result = self.way_documents_collection.insert_one(way_document)
        new_object_id = result.inserted_id
        return new_object_id

    def insert_way_documents(self, way_documents):
        """
        Insert multiple way_documents.

        :param way_documents: [way_document]
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

        :param object_id: ObjectId
        :param name: string
        :param node_id: int
        :param longitude: float
        :param latitude: float
        :return: None
        """
        address_document = self.find_address_document(
            object_id=object_id,
            name=name,
            node_id=node_id,
            longitude=longitude,
            latitude=latitude
        )
        print address_document

    def print_address_documents(self, object_ids=None, names=None, node_ids=None, counter=None):
        """
        Print multiple address_documents.

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

    def print_bus_line_document(self, object_id=None, bus_line_id=None):
        """
        Print a bus_line_document.

        :param object_id: ObjectId
        :param bus_line_id: int
        :return: bus_line_document
        """
        bus_line_document = self.find_bus_line_document(
            object_id=object_id,
            bus_line_id=bus_line_id
        )
        print bus_line_document

    def print_bus_line_documents(self, object_ids=None, bus_line_ids=None, counter=None):
        """
        Print multiple bus_line_documents.

        :param object_ids: [ObjectId]
        :param bus_line_ids: [int]
        :param counter: int
        :return: None
        """
        bus_line_documents_list = self.find_bus_line_documents(
            object_ids=object_ids,
            bus_line_ids=bus_line_ids
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

        :param object_id: ObjectId
        :param osm_id: int
        :param name: string
        :param longitude: float
        :param latitude: float
        :return: None
        """
        bus_stop_document = self.find_bus_stop_document(
            object_id=object_id,
            osm_id=osm_id, name=name,
            longitude=longitude,
            latitude=latitude
        )
        print bus_stop_document

    def print_bus_stop_documents(self, object_ids=None, osm_ids=None, names=None, counter=None):
        """
        Print multiple bus_stop_documents.

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

    def print_bus_vehicle_document(self, object_id=None, bus_vehicle_id=None):
        """
        Print a bus_vehicle_document.

        :param object_id: ObjectId
        :param bus_vehicle_id: int
        :return: None
        """
        bus_vehicle_document = self.find_bus_vehicle_document(
            object_id=object_id,
            bus_vehicle_id=bus_vehicle_id
        )
        print bus_vehicle_document

    def print_bus_vehicle_documents(self, object_ids=None, bus_vehicle_ids=None, counter=None):
        """
        Print multiple bus_vehicle_documents.

        :param object_ids: [ObjectId]
        :param bus_vehicle_ids: [int]
        :param counter: int
        :return: None
        """
        bus_vehicle_documents = self.find_bus_vehicle_documents(
            object_ids=object_ids,
            bus_vehicle_ids=bus_vehicle_ids
        )
        number_of_bus_vehicle_documents = len(bus_vehicle_documents)

        if counter is None or number_of_bus_vehicle_documents <= counter:
            for bus_vehicle_document in bus_vehicle_documents:
                print bus_vehicle_document
        else:
            for i in range(0, counter):
                bus_vehicle_document = bus_vehicle_documents[i]
                print bus_vehicle_document

        print 'number_of_bus_vehicle_documents:', number_of_bus_vehicle_documents

    def print_edge_document(self, object_id=None, starting_node_osm_id=None, ending_node_osm_id=None):
        """
        Print an edge_document.

        :param object_id: ObjectId
        :param starting_node_osm_id: int
        :param ending_node_osm_id: int
        :return: None
        """
        edge_document = self.find_edge_document(
            object_id=object_id,
            starting_node_osm_id=starting_node_osm_id,
            ending_node_osm_id=ending_node_osm_id
        )
        print edge_document

    def print_edge_documents(self, object_ids=None, starting_node_osm_id=None, ending_node_osm_id=None, counter=None):
        """
        Print multiple edge_documents.

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

        :param object_id: ObjectId
        :param osm_id: int
        :param longitude: float
        :param latitude: float
        :return: None
        """
        node_document = self.find_node_document(
            object_id=object_id,
            osm_id=osm_id,
            longitude=longitude,
            latitude=latitude
        )
        print node_document

    def print_node_documents(self, object_ids=None, osm_ids=None, counter=None):
        """
        Print multiple node_documents.

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

        :param object_id: ObjectId
        :param osm_id: int
        :param longitude: float
        :param latitude: float
        :return: None
        """
        point_document = self.find_point_document(
            object_id=object_id,
            osm_id=osm_id,
            longitude=longitude,
            latitude=latitude
        )
        print point_document

    def print_point_documents(self, object_ids=None, osm_ids=None, counter=None):
        """
        Print multiple point_documents.

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

        :param object_id: ObjectId
        :return: None
        """
        travel_request_document = self.find_travel_request_document(
            object_id=object_id
        )
        print travel_request_document

    def print_travel_request_documents(self, object_ids=None, client_ids=None, bus_line_ids=None,
                                       min_departure_datetime=None, max_departure_datetime=None,
                                       counter=None):
        """
        Print multiple travel_request_documents.

        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param bus_line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime: datetime
        :param counter: int
        :return: None
        """
        travel_request_documents_list = self.find_travel_request_documents(
            object_ids=object_ids,
            client_ids=client_ids,
            bus_line_ids=bus_line_ids,
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

        :param object_id: ObjectId
        :param osm_id: int
        :return: None
        """
        way_document = self.find_way_document(
            object_id=object_id,
            osm_id=osm_id
        )
        print way_document

    def print_way_documents(self, object_ids=None, osm_ids=None, counter=None):
        """
        Print multiple way_documents.

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

    def print_bus_stop_waypoints_documents(self, object_ids=None, bus_stops=None,
                                           bus_stop_names=None, bus_line_id=None):
        """
        Print multiple bus_stop_waypoints_documents.

        :param object_ids: [ObjectId]
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :param bus_line_id: int
        :return: None
        """
        bus_stop_waypoints_documents = self.find_bus_stop_waypoints_documents(
            object_ids=object_ids,
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names,
            bus_line_id=bus_line_id
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
                                                    bus_stop_names=None, bus_line_id=None):
        """
        Print multiple detailed_bus_stop_waypoints_documents.

        :param object_ids: [ObjectId]
        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :param bus_line_id: int
        :return: None
        """
        detailed_bus_stop_waypoints_documents = self.find_detailed_bus_stop_waypoints_documents(
            object_ids=object_ids,
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names,
            bus_line_id=bus_line_id
        )
        for detailed_bus_stop_waypoints_document in detailed_bus_stop_waypoints_documents:
            if detailed_bus_stop_waypoints_document is not None:
                self.print_detailed_bus_stop_waypoints_document(
                    detailed_bus_stop_waypoints_document=detailed_bus_stop_waypoints_document
                )

    def print_timetable_documents(self, object_ids=None, timetable_ids=None, bus_line_ids=None, timetables_control=True,
                                  timetable_entries_control=False, travel_requests_control=False,
                                  counter=None):
        """
        Print multiple timetable_documents.

        :param object_ids: [ObjectId]
        :param timetable_ids: [int]
        :param bus_line_ids: [int]
        :param timetables_control: bool
        :param timetable_entries_control: bool
        :param travel_requests_control: bool
        :param counter: int
        :return: None
        """
        timetable_documents = self.find_timetable_documents(
            object_ids=object_ids,
            timetable_ids=timetable_ids,
            bus_line_ids=bus_line_ids
        )
        print_timetables(
            timetables=timetable_documents,
            timetables_control=timetables_control,
            timetable_entries_control=timetable_entries_control,
            travel_requests_control=travel_requests_control,
            counter=counter
        )

    @staticmethod
    def print_traffic_density_document(traffic_density_document):
        """
        Print a traffic_density_document.

        :param traffic_density_document
        :return: None
        """
        if traffic_density_document is not None:
            print '\nstarting_bus_stop:', traffic_density_document.get('starting_bus_stop'), \
                'ending_bus_stop:', traffic_density_document.get('ending_bus_stop')

            for traffic_density_values_of_path in traffic_density_document.get('traffic_density_values'):
                print 'traffic_density_values_of_path:', traffic_density_values_of_path

    def print_traffic_density_documents(self, bus_stops=None, bus_stop_names=None):
        """
        Print multiple traffic_density_documents.

        :param bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :param bus_stop_names: [string]
        :return: None
        """
        traffic_density_documents = self.get_traffic_density_documents(
            bus_stops=bus_stops,
            bus_stop_names=bus_stop_names
        )
        for traffic_density_document in traffic_density_documents:
            self.print_traffic_density_document(
                traffic_density_document=traffic_density_document
            )

    def print_traffic_event_document(self, traffic_event_document=None, object_id=None, event_id=None):
        """
        Print a traffic_event_document.

        :param traffic_event_document: traffic_event_document
        :param object_id: ObjectId
        :param event_id: string
        :return: traffic_event_document
        """
        if traffic_event_document is None:
            traffic_event_document = self.find_traffic_event_document(
                object_id=object_id,
                event_id=event_id
            )

        print traffic_event_document

    def print_traffic_event_documents(self, traffic_event_documents=None, object_ids=None,
                                      event_ids=None, counter=None):
        """
        Print multiple traffic_event_documents.

        :param traffic_event_documents: [traffic_event_documents]
        :param object_ids: [ObjectId]
        :param event_ids: [string]
        :param counter: int
        :return: traffic_event_documents: [traffic_event_document]
        """
        if traffic_event_documents is None:
            traffic_event_documents = self.find_traffic_event_documents(
                object_ids=object_ids,
                event_ids=event_ids
            )

        number_of_traffic_event_documents = len(traffic_event_documents)

        if counter is not None:
            if number_of_traffic_event_documents < counter:
                counter = number_of_traffic_event_documents

            for i in range(0, counter):
                traffic_event_document = traffic_event_documents[i]
                print traffic_event_document

        else:
            for traffic_event_document in traffic_event_documents:
                print traffic_event_document

        print 'number_of_traffic_event_documents:', number_of_traffic_event_documents

    def update_traffic_density(self, edge_object_id, new_traffic_density_value):
        """
        Update the traffic_density value of an edge_document.

        :param edge_object_id: ObjectId of edge document
        :param new_traffic_density_value: float [0, 1]
        :return: True if an edge_document was updated, otherwise False.
        """
        key = {
            '_id': ObjectId(edge_object_id)
        }
        data = {
            '$set': {
                'traffic_density': new_traffic_density_value
            }
        }
        result = self.edge_documents_collection.update_one(key, data, upsert=False)
        return result.modified_count == 1

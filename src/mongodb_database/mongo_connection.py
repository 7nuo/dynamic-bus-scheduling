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

    def clear_all_collections(self):
        self.clear_nodes()
        self.clear_points()
        self.clear_ways()
        self.clear_bus_stops()
        self.clear_edges()
        self.clear_address_book()
        self.clear_bus_lines()
        self.clear_bus_stop_waypoints()

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
        Clear the Nodes collection.

        :return: Number of deleted documents.
        """
        result = self.nodes_collection.delete_many({})
        return result.deleted_count

    def clear_points(self):
        """
        Clear the Points collection.

        :return: The number of deleted documents.
        """
        result = self.points_collection.delete_many({})
        return result.deleted_count

    def clear_ways(self):
        """
        Delete all the documents of the Ways collection.

        :return The number of deleted documents.
        """
        result = self.ways_collection.delete_many({})
        return result.deleted_count

    def delete_address(self, name):
        """
        Delete an address document from the AddressBook collection.

        :type name: string
        :return: True if the address exists, otherwise False
        """
        result = self.address_book_collection.delete({'name': name})
        return result.deleted_count == 1

    def delete_bus_line(self, line_id):
        """
        Delete a bus_line document based on the line_id.

        :type line_id: string
        :return: True if the bus_line exists in the database, otherwise False.
        """
        result = self.bus_lines_collection.delete_one({'line_id': line_id})
        return result.deleted_count == 1

    def delete_bus_stop(self, osm_id):
        """
        Delete a bus_stop document based on the osm_id.

        :type osm_id: integer
        :return: True if the bus_stop exists in the database, otherwise False.
        """
        result = self.bus_stops_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count == 1

    def delete_bus_stop_waypoints(self, starting_bus_stop_osm_id, ending_bus_stop_osm_id):
        """

        :type starting_bus_stop_osm_id: integer
        :type ending_bus_stop_osm_id: integer
        :return: True if the document exists, otherwise False.
        """
        result = self.bus_stop_waypoints_collection.delete_one({'starting_bus_stop.osm_id': starting_bus_stop_osm_id,
                                                                'ending_bus_stop.osm_id': ending_bus_stop_osm_id})
        return result.deleted_count == 1

    def delete_edge(self, starting_node, ending_node):
        """
        Delete an edge document based on the starting and the ending nodes.

        :param starting_node: osm_id
        :type starting_node: integer
        :param ending_node: osm_id
        :type ending_node: integer
        :return: True if the document exists, otherwise False.
        """
        result = self.edges_collection.delete_one({'starting_node': starting_node, 'ending_node': ending_node})
        return result.deleted_count

    def delete_edges(self, starting_node):
        """
        Delete the edge documents based on the starting node.
        :param starting_node: osm_id
        :type starting_node: integer
        :return: The number of deleted documents.
        """
        result = self.edges_collection.delete({'starting_node': starting_node})
        return result.deleted_count

    def delete_node(self, osm_id):
        """
        Delete a node document based on the osm_id.

        :type osm_id: integer
        :return: True if node exists in database, otherwise False.
        """
        result = self.nodes_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count == 1

    def delete_point(self, osm_id):
        """
        Delete a point documents based on the osm_id.

        :type osm_id: integer
        :return: True if the point exists in the database, otherwise False.
        """
        result = self.points_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count == 1

    def delete_way(self, osm_id):
        """
        Delete a way document based on the osm_id.

        :type osm_id: integer
        :return: True if the way exists in the database, otherwise False.
        """
        result = self.ways_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count == 1

    def find_address(self, name):
        """
        Retrieve an address document based on the name.

        :type name: string
        :return: {'name', 'node_id', 'point': {'longitude', 'latitude'}}
        """
        return self.address_book_collection.find({'name': name}, {"_id": 0})

    def find_bus_line(self, line_id):
        """
        Retrieve a bus_line based on the line_id.

        :type line_id: string
        :return: {'line_id', 'bus_stops': [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        """
        return self.bus_lines_collection.find_one({'line_id': line_id}, {"_id": 0})

    def find_bus_stop(self, osm_id):
        """
        Retrieve a bus_stop based on the osm_id.

        :type osm_id: integer
        :return: {'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        return self.bus_stops_collection.find_one({'osm_id': osm_id}, {"_id": 0})

    def find_bus_stop_from_name(self, name):
        """
        Retrieve a bus_stop based on the name.

        :type name: string
        :return: {'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        return self.bus_stops_collection.find_one({'name': name}, {"_id": 0})

    def find_multiple_bus_stops_from_names(self, names):
        """
        Retrieve a bus_stop based on the name.

        :type names: [string]
        :return: [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        """
        return self.bus_stops_collection.find({'name': {'$in': names}}, {"_id": 0})

    def find_bus_stop_from_coordinates(self, longitude, latitude):
        """
        Retrieve a bus_stop based on coordinates.

        :type longitude: float
        :type latitude: float
        :return: {'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        return self.bus_stops_collection.find_one({'point': {'longitude': longitude, 'latitude': latitude}}, {"_id": 0})

    def find_edge(self, starting_node, ending_node):
        """
        Retrieve an edge document based on the starting and the ending nodes.

        :param starting_node: osm_id
        :type starting_node: integer
        :param ending_node: osm_id
        :type ending_node: integer
        :return: {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
        """
        return self.edges_collection.find_one({'starting_node': starting_node, 'ending_node': ending_node}, {"_id": 0})

    def find_edges(self, starting_node):
        """
        Retrieve the edge documents based on the starting node.

        :param starting_node: osm_id
        :type starting_node: integer
        :return: Cursor -> {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
        """
        return self.edges_collection.find({'starting_node': starting_node}, {"_id": 0})

    def find_node(self, osm_id):
        """
        Retrieve a node document based on the osm_id.

        :type osm_id: integer
        :return: {'osm_id', 'tags', 'point': {'longitude', 'latitude'}}
        """
        return self.nodes_collection.find_one({'osm_id': osm_id}, {"_id": 0})

    def find_point(self, osm_id):
        """
        Retrieve a point document based on the osm_id.

        :type osm_id: integer
        :return: {'osm_id', 'point': {'longitude', 'latitude'}}
        """
        return self.points_collection.find_one({'osm_id': osm_id}, {"_id": 0})

    def find_way(self, osm_id):
        """
        Retrieve a way document based on the osm_id.

        :type osm_id: integer
        :return: {'osm_id', 'tags', 'references'}
        """
        return self.ways_collection.find_one({'osm_id': osm_id}, {"_id": 0})

    def get_bus_lines(self):
        """
        Retrieve all the documents of the BusLines collection.

        :return: Cursor -> {'line_id', 'bus_stops': [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        """
        return self.bus_lines_collection.find({}, {"_id": 0})

    def get_bus_lines_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the BusLines collection.

        :return: {line_id -> {'bus_stops': [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}}
        """
        bus_lines_dictionary = {}
        bus_lines_cursor = self.get_bus_lines()

        # Cursor -> {'line_id', 'bus_stops': [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        for bus_line_document in bus_lines_cursor:
            bus_lines_dictionary[bus_line_document.get('line_id')] = {'bus_stops': bus_line_document.get('bus_stops')}

        return bus_lines_dictionary

    def get_bus_stops(self):
        """
        Retrieve all the documents of the BusStops collection.

        :return: Cursor -> {'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        return self.bus_stops_collection.find({}, {"_id": 0})

    def get_bus_stops_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the BusStops collection.

        :return: {name -> {'osm_id', 'point': {'longitude', 'latitude'}}}
        """
        bus_stops_dictionary = {}
        bus_stops_cursor = self.get_bus_stops()

        # Cursor -> {'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        for bus_stop_document in bus_stops_cursor:
            name = bus_stop_document.get('name')

            if name not in bus_stops_dictionary:
                bus_stops_dictionary[name] = {'osm_id': bus_stop_document.get('osm_id'),
                                              'point': bus_stop_document.get('point')}

        return bus_stops_dictionary

    def get_bus_stop_waypoints(self, starting_bus_stop_osm_id, ending_bus_stop_osm_id):
        """
        Retrieve the waypoints between two bus_stops.

        :param starting_bus_stop_osm_id: integer
        :param ending_bus_stop_osm_id: integer
        :return: {'starting_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                  'ending_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                  'waypoints': [{'edge_id', 'starting_node': {'osm_id', 'point': {'longitude', latitude}},
                                 'ending_node': {'osm_id', 'point': {'longitude', latitude}}}]}
        """
        return self.bus_stop_waypoints_collection.find_one({'starting_bus_stop.osm_id': starting_bus_stop_osm_id,
                                                            'ending_bus_stop.osm_id': ending_bus_stop_osm_id},
                                                           {"_id": 0})

    def get_edges(self):
        """
        Retrieve all the documents of the Edges collection.

        :return: Cursor -> {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
        """
        return self.edges_collection.find({}, {"_id": 0})

    def get_edges_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Edges collection.

        :return: {starting_node -> {'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}}
        """
        edges_dictionary = {}
        edges_cursor = self.get_edges()

        # Cursor -> {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
        for edges_document in edges_cursor:
            starting_node = edges_document.get('starting_node')
            del edges_document['starting_node']

            if starting_node in edges_dictionary:
                edges_dictionary[starting_node].append(edges_document)
            else:
                edges_dictionary[starting_node] = [edges_document]

        return edges_dictionary

    def get_edges_including_ids(self):
        """
        Retrieve all the documents of the Edges collection, including their ids.

        :return: Cursor -> {'_id', 'starting_node', 'ending_node', 'max_speed',
                            'road_type', 'way_id', 'traffic_density'}
        """
        return self.edges_collection.find({})

    def get_edges_dictionary_including_ids(self):
        """
        Retrieve a dictionary containing all the documents of the Edges collection.

        :return: {starting_node -> {'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}}
        """
        edges_dictionary = {}
        edges_cursor = self.get_edges_including_ids()

        # Cursor -> {'_id', 'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
        for edges_document in edges_cursor:
            starting_node = edges_document.get('starting_node')
            del edges_document['starting_node']

            if starting_node in edges_dictionary:
                edges_dictionary[starting_node].append(edges_document)
            else:
                edges_dictionary[starting_node] = [edges_document]

        return edges_dictionary

    def get_ending_nodes_of_edges(self):
        """
        Retrieve all the ending nodes which are included in the Edges collection.

        :return: ending_nodes: set([osm_id])
        """
        ending_nodes = set()
        edges_cursor = self.get_edges()

        for edge_document in edges_cursor:
            # Cursor -> {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
            ending_nodes.add(edge_document.get('ending_node'))

        return ending_nodes

    def get_points(self):
        """
        Retrieve all the documents of the Points collection.

        :return: Cursor -> {'osm_id', 'point': {'longitude', 'latitude'}}
        """
        return self.points_collection.find({}, {"_id": 0})

    def get_starting_nodes_of_edges(self):
        """
        Retrieve all the starting nodes which are included in the Edges collection.

        :return: starting_nodes: set([osm_id])
        """
        starting_nodes = set()
        edges_cursor = self.get_edges()

        for edge_document in edges_cursor:
            # Cursor -> {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
            starting_nodes.add(edge_document.get('starting_node'))

        return starting_nodes

    def has_edges(self, node):
        """
        Check if a node exists in the Edges collection as a starting node.

        :param node: osm_id
        :type node: integer
        :return: True if exists, otherwise False
        """
        return self.edges_collection.find_one({'starting_node': node}) is not None

    def in_edges(self, node):
        """
        Check if a node exists in the Edges collection, either as a starting or an ending node.

        :param node: osm_id
        :type node: integer
        :return: True if exists, otherwise False
        """
        return self.edges_collection.find_one({"$or": [{'starting_node': node}, {'ending_node': node}]}) is not None

    def insert_address(self, name, node_id, point):
        """
        Insert an address document to the AddressBook collection.

        :type name: string
        :type node_id: integer
        :type point: Point
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
        """
        self.address_book_collection.insert_many(address_book)

    def insert_bus_line(self, line_id, bus_stops):
        """
        Insert a bus_line document to the BusLines collection.

        :type line_id: string
        :param bus_stops: [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        :return: The ObjectId of the inserted document.
        """
        document = {'line_id': line_id, 'bus_stops': bus_stops}
        result = self.bus_lines_collection.insert_one(document)
        return result.inserted_id

    def insert_bus_lines(self, bus_lines):
        """
        Insert a list of bus_line documents to the BusLines collection.

        :param bus_lines: {'line_id', 'bus_stops': [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        """
        self.bus_lines_collection.insert_many(bus_lines)

    def insert_bus_stop(self, osm_id, name, point):
        """
        Insert a bus_stop document to the BusStops collection.

        :type osm_id: integer
        :type name: string
        :type point: Point
        :return: The ObjectId of the inserted document.
        """
        document = {'osm_id': osm_id, 'name': name, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        result = self.bus_stops_collection.insert_one(document)
        return result.inserted_id

    def insert_bus_stops(self, bus_stops):
        """
        Insert a list of bus_stop documents to the BusStops collection.

        :param bus_stops: [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        """
        self.bus_stops_collection.insert_many(bus_stops)

    def insert_bus_stop_waypoints(self, starting_bus_stop, ending_bus_stop, waypoints):
        """
        Insert a new document to the BusStopWaypoints collection, or update the waypoints
        if the document already exists in the database.

        :param starting_bus_stop: {'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param ending_bus_stop: {'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        :param waypoints: [{'edge_id', 'starting_node': {'osm_id', 'point': {'longitude', latitude}},
                            'ending_node': {'osm_id', 'point': {'longitude', latitude}}}]
        :return: The ObjectId, if a new document was inserted.
        """
        # document = {'starting_bus_stop': starting_bus_stop, 'ending_bus_stop': ending_bus_stop,
        #             'waypoints': waypoints}
        # result = self.bus_stop_waypoints_collection.insert_one(document)
        # return result.inserted_id
        key = {'starting_bus_stop': starting_bus_stop, 'ending_bus_stop': ending_bus_stop}
        data = {'$set': {'waypoints': waypoints}}
        result = self.bus_stop_waypoints_collection.update_one(key, data, upsert=True)
        return result.upserted_id

    def insert_bus_stop_waypoints_documents(self, bus_stop_waypoints_documents):
        """
        Insert multiple documents to the BusStopWaypoints collection,
        or update the waypoints of the already existing ones.

        :param bus_stop_waypoints_documents:
                [{'starting_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                  'ending_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                  'waypoints': [{'edge_id', 'starting_node': {'osm_id', 'point': {'longitude', latitude}},
                                 'ending_node': {'osm_id', 'point': {'longitude', latitude}}}]}]
        """
        for document in bus_stop_waypoints_documents:
            starting_bus_stop = document.get('starting_bus_stop')
            ending_bus_stop = document.get('ending_bus_stop')
            waypoints = document.get('waypoints')
            self.insert_bus_stop_waypoints(starting_bus_stop=starting_bus_stop, ending_bus_stop=ending_bus_stop,
                                           waypoints=waypoints)

    def insert_edge(self, starting_node, ending_node, max_speed, road_type, way_id, traffic_density):
        """
        Insert an edge document to the Edges collection.

        :param starting_node: osm_id: integer
        :param ending_node: osm_id: integer
        :type max_speed: float or integer
        :type road_type: string
        :param way_id: osm_id: integer
        :param traffic_density: A value between 0 and 1 indicating the density of traffic: float
        :return: The Object Id of the inserted document.
        """
        document = {'starting_node': starting_node, 'ending_node': ending_node, 'max_speed': max_speed,
                    'road_type': road_type, 'way_id': way_id, 'traffic_density': traffic_density}
        result = self.edges_collection.insert_one(document)
        return result.inserted_id

    def insert_edges(self, edges):
        """
        Insert a list of edge documents to the Edges collection.

        :param edges: [{'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}]
        """
        self.edges_collection.insert_many(edges)

    def insert_node(self, osm_id, tags, point):
        """
        Insert a node document to the Nodes collection.

        :type osm_id: integer
        :type tags: {}
        :type point: Point
        :return: The ObjectId of the inserted document.
        """
        document = {'osm_id': osm_id, 'tags': tags, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        result = self.nodes_collection.insert_one(document)
        return result.inserted_id

    def insert_nodes(self, nodes):
        """
        Insert a list of node documents to the Nodes dictionary.

        :param nodes: [{'osm_id', 'tags', 'point': {'longitude', 'latitude'}}]
        """
        self.nodes_collection.insert_many(nodes)

    def insert_point(self, osm_id, point):
        """
        Insert a point document to the Points collection.

        :type osm_id: integer
        :type point: Point
        :return: The ObjectId of the inserted document.
        """
        document = {'osm_id': osm_id, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        result = self.points_collection.insert_one(document)
        return result.inserted_id

    def insert_points(self, points):
        """
        Insert a list of point documents to the Points collection.

        :param points: [{'osm_id', 'point': {'longitude', 'latitude'}}]
        """
        self.points_collection.insert_many(points)

    def insert_way(self, osm_id, tags, references):
        """
        Insert a way document to the Ways collection.

        :type osm_id: integer
        :type tags: {}
        :param references: [osm_id]
        :return: The ObjectId of the inserted document.
        """
        document = {'osm_id': osm_id, 'tags': tags, 'references': references}
        result = self.ways_collection.insert_one(document)
        return result.inserted_id

    def insert_ways(self, ways):
        """
        Insert a list of way documents to the Ways dictionary.

        :param ways: [{'osm_id', 'tags', 'references'}]
        """
        self.ways_collection.insert_many(ways)

    def print_bus_stops(self, counter):
        bus_stops_cursor = self.bus_stops_collection.find({}, {"_id": 0})
        i = 0

        for bus_stop in bus_stops_cursor:
            if i < counter:
                print bus_stop
                i += 1
            else:
                break

        print 'Total number of BusStops: ' + str(bus_stops_cursor.count())

    def print_edges(self, counter):
        edges_cursor = self.get_edges_including_ids()
        i = 0

        for edge in edges_cursor:
            if i < counter:
                print edge
                i += 1
            else:
                break

        print 'Total number of Edges: ' + str(edges_cursor.count())

    def print_nodes(self, counter):
        nodes_cursor = self.nodes_collection.find({}, {"_id": 0})
        i = 0

        for node in nodes_cursor:
            if i < counter:
                print node
                i += 1
            else:
                break

        print 'Total number of Nodes: ' + str(nodes_cursor.count())

    def print_waypoints_between_bus_stops(self, counter):
        documents_cursor = self.bus_stop_waypoints_collection.find({}, {'_id': 0})
        i = 0

        for document in documents_cursor:
            if i < counter:
                print document
                i += 1
            else:
                break

        print 'Total: ' + str(documents_cursor.count())

    # def test(self):
    #     self.clear_bus_stop_waypoints()
    #     print self.insert_bus_stop_waypoints(starting_bus_stop='1', ending_bus_stop='2', waypoints='0')
    #     print self.insert_bus_stop_waypoints(starting_bus_stop='2', ending_bus_stop='3', waypoints='0')
    #     print self.insert_bus_stop_waypoints(starting_bus_stop='1', ending_bus_stop='2', waypoints='00')
    #
    #     for i in self.bus_stop_waypoints_collection.find({}, {'_id': 0}):
    #         print i

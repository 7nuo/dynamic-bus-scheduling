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

    def clear_all_collections(self):
        self.clear_nodes()
        self.clear_points()
        self.clear_ways()
        self.clear_bus_stops()
        self.clear_edges()
        self.clear_address_book()

    def clear_address_book(self):
        """
        Delete all the documents of the AddressBook collection.

        :return: The number of deleted documents.
        """
        result = self.address_book_collection.delete_many({})
        return result.deleted_count

    def clear_bus_stops(self):
        """
        Delete all the documents of hte BusStops collection.

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

    def delete_bus_stop(self, osm_id):
        """
        Delete a bus_stop document based on the osm_id.

        :type osm_id: integer
        :return: True if the bus_stop exists in the database, otherwise False.
        """
        result = self.bus_stops_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count

    def delete_edge(self, starting_node, ending_node):
        """
        Delete an edge document based on the starting and the ending nodes.

        :param starting_node: osm_id
        :type starting_node: integer
        :param ending_node: osm_id
        :type ending_node: integer
        :return: True if the document exists, otherwise False
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
        # collection1.find({'albums': {'$in': [3, 7, 8]}})
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

    def get_bus_stops(self):
        """
        Retrieve all the documents of the BusStops collection.

        :return: Cursor -> {'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        return self.bus_stops_collection.find({}, {"_id": 0})

    def get_edges(self):
        """
        Retrieve all the documents of the Edges collection.

        :return: Cursor -> {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
        """
        return self.edges_collection.find({}, {"_id": 0})

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


if __name__ == '__main__':
    connection = MongoConnection(host='127.0.0.1', port=27017)
    connection.clear_all_collections()

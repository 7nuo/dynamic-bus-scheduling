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
from mongo_connection import Connection
from point import distance, Point
from path_finder import find_path
from logger import log


class MongoConnector(object):
    def __init__(self, parser, host, port):
        # log(module_name='MongoConnector', log_type='DEBUG', log_message='')
        log(module_name='MongoConnector', log_type='DEBUG', log_message='init()')

        self.list_of_points = parser.get_list_of_points()
        log(module_name='MongoConnector', log_type='DEBUG', log_message='list_of_points ok')

        self.list_of_nodes = parser.get_list_of_nodes()
        log(module_name='MongoConnector', log_type='DEBUG', log_message='list_of_nodes ok')

        self.list_of_ways = parser.get_list_of_ways()
        log(module_name='MongoConnector', log_type='DEBUG', log_message='list_of_ways ok')

        self.list_of_bus_stops = parser.get_list_of_bus_stops()
        log(module_name='MongoConnector', log_type='DEBUG', log_message='list_of_bus_stops')

        self.list_of_edges = parser.get_list_of_edges()
        log(module_name='MongoConnector', log_type='DEBUG', log_message='list_of_edges ok')

        self.list_of_addresses = parser.get_list_of_addresses()
        log(module_name='MongoConnector', log_type='DEBUG', log_message='list_of_addresses ok')

        self.connection = Connection(host=host, port=port)
        log(module_name='MongoConnector', log_type='DEBUG', log_message='connection ok')

    def populate_address_book(self):
        self.connection.insert_addresses(address_book=self.list_of_addresses)
        log(module_name='MongoConnector', log_type='DEBUG', log_message='address_book collection ok')

    def populate_edges(self):
        self.connection.insert_edges(edges=self.list_of_edges)
        log(module_name='MongoConnector', log_type='DEBUG', log_message='edges collection ok')

    def populate_nodes(self):
        self.connection.insert_nodes(nodes=self.list_of_nodes)
        log(module_name='MongoConnector', log_type='DEBUG', log_message='nodes collection ok')

    def populate_points(self):
        self.connection.insert_points(points=self.list_of_points)
        log(module_name='MongoConnector', log_type='DEBUG', log_message='points collection ok')

    def populate_bus_stops(self):
        self.connection.insert_bus_stops(bus_stops=self.list_of_bus_stops)
        log(module_name='MongoConnector', log_type='DEBUG', log_message='bus_stops collection ok')

    def populate_ways(self):
        self.connection.insert_ways(ways=self.list_of_ways)
        log(module_name='MongoConnector', log_type='DEBUG', log_message='ways collection ok')

    def populate_all_collections(self):
        self.populate_points()
        self.populate_nodes()
        self.populate_ways()
        self.populate_bus_stops()
        self.populate_edges()
        self.populate_address_book()

    def clear_all_collections(self):
        self.connection.clear_all_collections()

    def get_bus_stop_closest_to_coordinates(self, longitude, latitude):
        """
        Get the bus stop which is closest to a set of coordinates.

        :type longitude: float
        :type latitude: float
        :return bus_stop: {osm_id, name, point}
        """
        provided_point = Point(longitude=longitude, latitude=latitude)
        return self.get_bus_stop_closest_to_point(provided_point=provided_point)

    def get_bus_stop_closest_to_point(self, provided_point):
        """
        Get the bus stop which is closest to a geographic point.

        :type provided_point: Point
        :return bus_stop: {osm_id, name, point}
        """
        minimum_distance = float('Inf')
        closest_bus_stop = None

        bus_stops_cursor = self.connection.get_bus_stops()

        for bus_stop in bus_stops_cursor:
            bus_stop_point = bus_stop.get('point')
            current_distance = distance(point_one=provided_point, longitude_two=bus_stop_point.get('longitude'),
                                        latitude_two=bus_stop_point.get('latitude'))

            if current_distance == 0:
                closest_bus_stop = bus_stop
                break
            elif current_distance < minimum_distance:
                minimum_distance = current_distance
                closest_bus_stop = bus_stop
            else:
                pass

        return closest_bus_stop

    def get_bus_stop_from_coordinates(self, longitude, latitude):
        """
        Get the bus_stop which corresponds to a set of coordinates.

        :type longitude: float
        :type latitude: float
        :return bus_stop: {osm_id, name, point}
        """
        return self.connection.find_bus_stop_from_coordinates(longitude=longitude, latitude=latitude)

    def get_bus_stop_from_name(self, name):
        """
        Get the bus_stop which corresponds to a name.

        :type name: string
        :return bus_stop: {osm_id, name, point}
        """
        return self.connection.find_bus_stop_from_name(name=name)

    def get_bus_stop_from_point(self, point):
        """
        Get the bus_stop which corresponds to a name.

        :type point: Point
        :return bus_stop: {osm_id, name, point}
        """
        return self.get_bus_stop_from_coordinates(longitude=point.longitude, latitude=point.latitude)

    def get_bus_stops_within_distance_from_coordinates(self, longitude, latitude, maximum_distance):
        """
        Get the bus_stops which are within a distance from a set of coordinates.

        :type longitude: float
        :type latitude: float
        :type maximum_distance: float
        :return bus_stops: [{osm_id, name, point}]
        """
        provided_point = Point(longitude=longitude, latitude=latitude)
        bus_stops = []
        bus_stops_cursor = self.connection.get_bus_stops()

        for bus_stop in bus_stops_cursor:
            bus_stop_point = bus_stop.get('point')
            current_distance = distance(point_one=provided_point, longitude_two=bus_stop_point.get('longitude'),
                                        latitude_two=bus_stop_point.get('latitude'))

            if current_distance <= maximum_distance:
                bus_stops.append(bus_stop)

        return bus_stops

    def get_bus_stops_within_distance_from_point(self, provided_point, maximum_distance):
        """
        Get the bus_stops which are within a distance from a set of coordinates.

        :type provided_point: Point
        :type maximum_distance: float
        :return bus_stops: [{osm_id, name, point}]
        """
        bus_stops = []
        bus_stops_cursor = self.connection.get_bus_stops()

        for bus_stop in bus_stops_cursor:
            bus_stop_point = bus_stop.get('point')
            current_distance = distance(point_one=provided_point, longitude_two=bus_stop_point.get('longitude'),
                                        latitude_two=bus_stop_point.get('latitude'))

            if current_distance <= maximum_distance:
                bus_stops.append(bus_stop)

        return bus_stops

    def get_closest_ending_node_in_edges_from_coordinates(self, longitude, latitude):
        """
        Retrieve the node which is closest to a set of coordinates and is stored at
        the Edges collection as an ending node.

        :type longitude: float
        :type latitude: float
        :return closest_ending_node: osm_id
        """
        provided_point = Point(longitude=longitude, latitude=latitude)
        return self.get_closest_ending_node_in_edges_from_point(provided_point=provided_point)

    def get_closest_ending_node_in_edges_from_point(self, provided_point):
        """
        Retrieve the node which is closest to the provided point and is stored at
        the Edges collection as an ending node.

        :type provided_point: Point
        :return closest_ending_node: osm_id
        """
        closest_ending_node = None
        ending_nodes_set = self.connection.get_ending_nodes_of_edges()
        points_dictionary = self.get_points_dictionary()
        minimum_distance = float('Inf')

        for current_ending_node in ending_nodes_set:
            current_point = points_dictionary[current_ending_node]
            current_distance = distance(point_one=provided_point, point_two=current_point)

            if current_distance == 0:
                closest_ending_node = current_ending_node
                break
            elif current_distance < minimum_distance:
                minimum_distance = current_distance
                closest_ending_node = current_ending_node
            else:
                pass

        return closest_ending_node

    def get_closest_starting_node_in_edges_from_coordinates(self, longitude, latitude):
        """
        Retrieve the node which is closest to a set of coordinates and is stored at
        the Edges collection as a starting node.

        :type longitude: float
        :type latitude: float
        :return closest_starting_node: osm_id
        """
        provided_point = Point(longitude=longitude, latitude=latitude)
        return self.get_closest_starting_node_in_edges_from_point(provided_point=provided_point)

    def get_closest_starting_node_in_edges_from_point(self, provided_point):
        """
        Retrieve the node which is closest to the provided point and is stored at
        the Edges collection as a starting node.

        :type provided_point: Point
        :return closest_starting_node: osm_id
        """
        closest_starting_node = None
        starting_nodes_set = self.connection.get_starting_nodes_of_edges()
        points_dictionary = self.get_points_dictionary()
        minimum_distance = float('Inf')

        for current_starting_node in starting_nodes_set:
            current_point = points_dictionary[current_starting_node]
            current_distance = distance(point_one=provided_point, point_two=current_point)

            if current_distance == 0:
                closest_starting_node = current_starting_node
                break
            elif current_distance < minimum_distance:
                minimum_distance = current_distance
                closest_starting_node = current_starting_node
            else:
                pass

        return closest_starting_node

    def get_point_from_osm_id(self, osm_id):
        """
        Retrieve the point which correspond to a specific osm_id.

        :type osm_id: integer
        :return: Point
        """
        point = None
        # document = {'osm_id': osm_id, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        document = self.connection.find_point(osm_id=osm_id)
        point_entry = document.get('point')

        if point_entry is not None:
            point = Point(longitude=point_entry.get('longitude'), latitude=point_entry.get('latitude'))

        return point

    def get_edges_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Edges collection.

        :return: {starting_node -> {'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}}
        """
        edges_dictionary = {}
        edges_cursor = self.connection.get_edges()

        # Cursor -> {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
        for edges_document in edges_cursor:
            starting_node = edges_document.get('starting_node')

            if starting_node in edges_dictionary:
                edges_dictionary[starting_node].append({'ending_node': edges_document.get('ending_node'),
                                                        'max_speed': edges_document.get('max_speed'),
                                                        'road_type': edges_document.get('road_type'),
                                                        'way_id': edges_document.get('way_id'),
                                                        'traffic_density': edges_document.get('traffic_density')})
            else:
                edges_dictionary[starting_node] = [{'ending_node': edges_document.get('ending_node'),
                                                    'max_speed': edges_document.get('max_speed'),
                                                    'road_type': edges_document.get('road_type'),
                                                    'way_id': edges_document.get('way_id'),
                                                    'traffic_density': edges_document.get('traffic_density')}]
        return edges_dictionary

    def get_points_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Points collection.

        :return points_dictionary: {osm_id -> point}
        """
        points_dictionary = {}
        points_cursor = self.connection.get_points()

        for point_document in points_cursor:
            # {'osm_id': osm_id, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
            osm_id = point_document.get('osm_id')
            point_entry = point_document.get('point')
            points_dictionary[osm_id] = Point(longitude=point_entry.get('longitude'),
                                              latitude=point_entry.get('latitude'))

        return points_dictionary

    def get_points_of_edges(self):
        """
        Retrieve a dictionary containing the points of edges.

        :return points_of_edges: {osm_id -> point}
        """
        # edge_document = {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
        points_of_edges = {}
        edges_cursor = self.connection.get_edges()
        points_dictionary = self.get_points_dictionary()

        for edge_document in edges_cursor:
            starting_node = edge_document.get('starting_node')
            ending_node = edge_document.get('ending_node')

            if starting_node not in points_of_edges:
                points_of_edges[starting_node] = points_dictionary.get(starting_node)

            if ending_node not in points_of_edges:
                points_of_edges[ending_node] = points_dictionary.get(ending_node)

        return points_of_edges

    def get_route_from_coordinates(self, starting_longitude, starting_latitude, ending_longitude, ending_latitude):
        """
        Find a route between two pairs of coordinates, using the A* algorithm.

        :type starting_longitude: float
        :type starting_latitude: float
        :type ending_longitude: float
        :type ending_latitude: float
        :return route: [(osm_id, point, (distance_from_starting_node, time_from_starting_node))]
        """
        starting_point = Point(longitude=starting_longitude, latitude=starting_latitude)
        ending_point = Point(longitude=ending_longitude, latitude=ending_latitude)
        return self.get_route_from_points(starting_point=starting_point, ending_point=ending_point)

    def get_route_from_points(self, starting_point, ending_point):
        """
        Find a route between two points, using the A* algorithm.

        :type starting_point: Point
        :type ending_point: Point
        :return route: [(osm_id, point, (distance_from_starting_node, time_from_starting_node))]
        """
        starting_osm_id = self.get_closest_starting_node_in_edges_from_point(provided_point=starting_point)
        ending_osm_id = self.get_closest_ending_node_in_edges_from_point(provided_point=ending_point)
        edges_dictionary = self.get_edges_dictionary()
        points_dictionary = self.get_points_dictionary()
        route = find_path(starting_node=starting_osm_id, ending_node=ending_osm_id, edges=edges_dictionary,
                          points=points_dictionary)
        return route


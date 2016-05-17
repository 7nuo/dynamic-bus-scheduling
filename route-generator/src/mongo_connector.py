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
from mongo_connection import MongoConnection
from point import distance, Point
from path_finder import find_path, find_multiple_paths
from logger import log


class MongoConnector(object):
    def __init__(self, host, port):
        self.connection = MongoConnection(host=host, port=port)
        log(module_name='MongoConnector', log_type='DEBUG', log_message='connection ok')
        self.bus_stops_dictionary = {}
        self.edges_dictionary = {}
        self.points_dictionary = {}
        self.initialize_dictionaries()
        log(module_name='MongoConnector', log_type='DEBUG', log_message='initialize_dictionaries ok')

    def initialize_dictionaries(self):
        self.bus_stops_dictionary = self.get_bus_stops_dictionary()
        self.edges_dictionary = self.get_edges_dictionary()
        self.points_dictionary = self.get_points_dictionary()

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

        for bus_stop_name, bus_stop_values in self.bus_stops_dictionary:
            bus_stop_osm_id = bus_stop_values.get('osm_id')
            bus_stop_point = bus_stop_values.get('point')
            bus_stop = {'osm_id': bus_stop_osm_id, 'name': bus_stop_name, 'point': bus_stop_point}

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
        bus_stop = None

        for bus_stop_name, bus_stop_values in self.bus_stops_dictionary:
            bus_stop_osm_id = bus_stop_values.get('osm_id')
            bus_stop_point = bus_stop_values.get('point')
            current_bus_stop = {'osm_id': bus_stop_osm_id, 'name': bus_stop_name, 'point': bus_stop_point}

            if (bus_stop_point.get('longitude') == longitude) and (bus_stop_point.get('latitude') == latitude):
                bus_stop = current_bus_stop
                break

        return bus_stop

    def get_bus_stop_from_name(self, name):
        """
        Get the bus_stop which corresponds to a name.

        :type name: string
        :return bus_stop: {osm_id, name, point}
        """
        name = name.decode('utf-8')
        # return self.connection.find_bus_stop_from_name(name=name)
        bus_stop = self.bus_stops_dictionary[name]
        bus_stop['name'] = name
        return bus_stop

    def get_bus_stop_from_point(self, point):
        """
        Get the bus_stop which corresponds to a name.

        :type point: Point
        :return bus_stop: {osm_id, name, point}
        """
        return self.get_bus_stop_from_coordinates(longitude=point.longitude, latitude=point.latitude)

    def get_bus_stops_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the BusStops collection.

        :return: {name -> {'osm_id', 'point': {'longitude', 'latitude'}}}
        """
        bus_stops_dictionary = {}
        bus_stops_cursor = self.connection.get_bus_stops()

        # Cursor -> {'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        for bus_stop_document in bus_stops_cursor:
            name = bus_stop_document.get('name')

            if name not in bus_stops_dictionary:
                bus_stops_dictionary[name] = {'osm_id': bus_stop_document.get('osm_id'),
                                              'point': bus_stop_document.get('point')}

        return bus_stops_dictionary

    def get_bus_stops_dictionary_to_list(self):
        """
        Retrieve a list containing all the documents of the BusStops collection.

        :return: [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        """
        bus_stops = []

        for bus_stop_name, bus_stop_values in self.bus_stops_dictionary.iteritems():
            bus_stop_osm_id = bus_stop_values.get('osm_id')
            bus_stop_point = bus_stop_values.get('point')
            bus_stop = {'osm_id': bus_stop_osm_id, 'name': bus_stop_name, 'point': bus_stop_point}
            bus_stops.append(bus_stop)

        return bus_stops

    def get_bus_stops_within_distance_from_coordinates(self, longitude, latitude, maximum_distance):
        """
        Get the bus_stops which are within a distance from a set of coordinates.

        :type longitude: float
        :type latitude: float
        :type maximum_distance: float
        :return bus_stops: [{osm_id, name, point}]
        """
        provided_point = Point(longitude=longitude, latitude=latitude)
        return self.get_bus_stops_within_distance_from_point(provided_point=provided_point,
                                                             maximum_distance=maximum_distance)

    def get_bus_stops_within_distance_from_point(self, provided_point, maximum_distance):
        """
        Get the bus_stops which are within a distance from a set of coordinates.

        :type provided_point: Point
        :type maximum_distance: float
        :return bus_stops: [{osm_id, name, point}]
        """
        bus_stops = []

        for bus_stop_name, bus_stop_values in self.bus_stops_dictionary:
            bus_stop_point = bus_stop_values.get('point')
            current_distance = distance(point_one=provided_point, longitude_two=bus_stop_point.get('longitude'),
                                        latitude_two=bus_stop_point.get('latitude'))

            if current_distance <= maximum_distance:
                bus_stop_osm_id = bus_stop_values.get('osm_id')
                current_bus_stop = {'osm_id': bus_stop_osm_id, 'name': bus_stop_name, 'point': bus_stop_point}
                bus_stops.append(current_bus_stop)

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
        ending_nodes_set = self.get_ending_nodes_of_edges()
        minimum_distance = float('Inf')

        for current_ending_node in ending_nodes_set:
            current_point = self.points_dictionary[current_ending_node]
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
        starting_nodes_set = self.get_starting_nodes_of_edges()
        minimum_distance = float('Inf')

        for current_starting_node in starting_nodes_set:
            current_point = self.points_dictionary[current_starting_node]
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

    def get_ending_nodes_of_edges(self):
        """
        Retrieve all the ending nodes which are included in the Edges collection.

        :return: ending_nodes: set([osm_id])
        """
        ending_nodes = set()

        for starting_node, values in self.edges_dictionary.iteritems():
            ending_node = values.get('ending_node')
            ending_nodes.add(ending_node)

        return ending_nodes

    def get_point_from_osm_id(self, osm_id):
        """
        Retrieve the point which correspond to a specific osm_id.

        :type osm_id: integer
        :return: Point
        """
        point = None
        # document = {'osm_id': osm_id, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        # document = self.connection.find_point(osm_id=osm_id)
        # point_entry = document.get('point')

        point_entry = self.points_dictionary.get(osm_id, None)

        if point_entry is not None:
            point = Point(longitude=point_entry.get('longitude'), latitude=point_entry.get('latitude'))

        return point

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

        for starting_node, values in self.edges_dictionary.iteritems():
            ending_node = values.get('ending_node')

            if starting_node not in points_of_edges:
                points_of_edges[starting_node] = self.points_dictionary.get(starting_node)

            if ending_node not in points_of_edges:
                points_of_edges[ending_node] = self.points_dictionary.get(ending_node)

        return points_of_edges

    def get_starting_nodes_of_edges(self):
        """
        Retrieve all the starting nodes which are included in the Edges collection.

        :return: starting_nodes: set([osm_id])
        """
        starting_nodes = set()

        for starting_node in self.edges_dictionary:
            starting_nodes.add(starting_node)

        return starting_nodes

    def get_route_from_coordinates(self, starting_longitude, starting_latitude, ending_longitude, ending_latitude):
        """
        Find a route between two pairs of coordinates.

        :type starting_longitude: float
        :type starting_latitude: float
        :type ending_longitude: float
        :type ending_latitude: float
        :return route: {'total_distance', 'total_time', 'nodes', 'points', 'total_distances',
                        'total_times', 'partial_distances', 'partial_times'}
        """
        starting_point = Point(longitude=starting_longitude, latitude=starting_latitude)
        ending_point = Point(longitude=ending_longitude, latitude=ending_latitude)
        return self.get_route_from_points(starting_point=starting_point, ending_point=ending_point)

    def get_route_from_points(self, starting_point, ending_point):
        """
        Find a route between two points.

        :type starting_point: Point
        :type ending_point: Point
        :return route: {'total_distance', 'total_time', 'nodes', 'points', 'total_distances',
                        'total_times', 'partial_distances', 'partial_times'}
        """
        starting_osm_id = self.get_closest_starting_node_in_edges_from_point(provided_point=starting_point)
        ending_osm_id = self.get_closest_ending_node_in_edges_from_point(provided_point=ending_point)
        route = find_path(starting_node_osm_id=starting_osm_id,
                          ending_node_osm_id=ending_osm_id,
                          edges=self.edges_dictionary,
                          points=self.points_dictionary)
        return route

    def get_route_between_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        """
        Find a route between two bus_stops, based on their names.

        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return: {'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
                  'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}
        """
        starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
        ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

        route = find_path(starting_node_osm_id=starting_bus_stop.get('osm_id'),
                          ending_node_osm_id=ending_bus_stop.get('osm_id'),
                          edges=self.edges_dictionary,
                          points=self.points_dictionary)
        return route

    def get_multiple_routes_between_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        """
        Find multiple routes between two bus_stops, based on their names.

        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return: [{'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
                   'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}]
        """
        starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
        ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

        routes = find_multiple_paths(starting_node_osm_id=starting_bus_stop.get('osm_id'),
                                     ending_node_osm_id=ending_bus_stop.get('osm_id'),
                                     edges=self.edges_dictionary,
                                     points=self.points_dictionary)
        return routes

    def get_route_between_multiple_bus_stops(self, bus_stop_names):
        """
        Find a route between multiple bus_stops, based on their names.

        :param bus_stop_names: [string]
        :return: [{'starting_bus_stop_name', 'ending_bus_stop_name', 'total_distance', 'total_time', 'node_osm_ids',
                   'points', 'distances_from_starting_node', 'times_from_starting_node',
                   'distances_from_previous_node', 'times_from_previous_node'}]
        """
        intermediate_routes = []

        for i in range(0, len(bus_stop_names) - 1):
            starting_bus_stop_name = bus_stop_names[i]
            starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
            ending_bus_stop_name = bus_stop_names[i + 1]
            ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

            route = find_path(starting_node_osm_id=starting_bus_stop.get('osm_id'),
                              ending_node_osm_id=ending_bus_stop.get('osm_id'),
                              edges=self.edges_dictionary,
                              points=self.points_dictionary)

            if route is not None:
                route['starting_bus_stop_name'] = starting_bus_stop_name
                route['ending_bus_stop_name'] = ending_bus_stop_name

            intermediate_routes.append(route)

        return intermediate_routes


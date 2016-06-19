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
from path_finder import find_path
from multiple_paths_finder import find_waypoints_between_two_nodes
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port
from src.geospatial_data.point import distance, Point
from src.mongodb_database.mongo_connection import MongoConnection


class Router(object):
    def __init__(self):
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='Router', log_type='DEBUG', log_message='connection ok')
        self.bus_stops_dictionary = {}
        self.edges_dictionary = {}
        self.points_dictionary = {}
        self.initialize_dictionaries()
        log(module_name='Router', log_type='DEBUG', log_message='initialize_dictionaries ok')

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
        :return bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        provided_point = Point(longitude=longitude, latitude=latitude)
        bus_stop = self.get_bus_stop_closest_to_point(provided_point=provided_point)
        return bus_stop

    def get_bus_stop_closest_to_point(self, provided_point):
        """
        Get the bus stop which is closest to a geographic point.

        :type provided_point: Point
        :return bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        minimum_distance = float('Inf')
        closest_bus_stop = None

        # bus_stops_dictionary: {name -> {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}}
        for bus_stop in self.bus_stops_dictionary.values():
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
        :return bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        bus_stop = None

        # bus_stops_dictionary: {name -> {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}}
        for current_bus_stop in self.bus_stops_dictionary.values():
            current_bus_stop_point = current_bus_stop.get('point')

            if (current_bus_stop_point.get('longitude') == longitude) and \
                    (current_bus_stop_point.get('latitude') == latitude):
                bus_stop = current_bus_stop
                break

        return bus_stop

    def get_bus_stop_from_name(self, name):
        """
        Get the bus_stop which corresponds to a name.

        :type name: string
        :return bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        name = name.decode('utf-8')
        bus_stop = self.bus_stops_dictionary.get(name)
        return bus_stop

    def get_bus_stop_from_point(self, point):
        """
        Get the bus_stop which corresponds to a name.

        :type point: Point
        :return bus_stop: {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}
        """
        bus_stop = self.get_bus_stop_from_coordinates(longitude=point.longitude, latitude=point.latitude)
        return bus_stop

    def get_bus_stops_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the BusStops collection.

        :return: bus_stops_dictionary: {name -> {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}}
        """
        bus_stops_dictionary = self.connection.get_bus_stops_dictionary()
        return bus_stops_dictionary

    def get_bus_stops_list(self):
        """
        Retrieve a list containing all the documents of the BusStops collection.

        :return: bus_stops_list: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        """
        bus_stops_list = self.connection.get_bus_stops_list()
        return bus_stops_list

    # def get_bus_stops_within_distance_from_coordinates(self, longitude, latitude, maximum_distance):
    #     """
    #     Get the bus_stop_names which are within a distance from a set of coordinates.
    #
    #     :type longitude: float
    #     :type latitude: float
    #     :type maximum_distance: float
    #     :return bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
    #     """
    #     provided_point = Point(longitude=longitude, latitude=latitude)
    #     bus_stops = self.get_bus_stops_within_distance_from_point(provided_point=provided_point,
    #                                                               maximum_distance=maximum_distance)
    #     return bus_stops

    # def get_bus_stops_within_distance_from_point(self, provided_point, maximum_distance):
    #     """
    #     Get the bus_stop_names which are within a distance from a set of coordinates.
    #
    #     :type provided_point: Point
    #     :type maximum_distance: float
    #     :return bus_stops: [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
    #     """
    #     bus_stops = []
    #
    #     # bus_stops_dictionary: {name -> {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}}
    #     for bus_stop in self.bus_stops_dictionary.values():
    #         bus_stop_point = bus_stop.get('point')
    #         current_distance = distance(point_one=provided_point, longitude_two=bus_stop_point.get('longitude'),
    #                                     latitude_two=bus_stop_point.get('latitude'))
    #
    #         if current_distance <= maximum_distance:
    #             bus_stops.append(bus_stop)
    #
    #     return bus_stops

    # def get_closest_ending_node_in_edges_from_coordinates(self, longitude, latitude):
    #     """
    #     Retrieve the node which is closest to a set of coordinates and is stored at
    #     the Edges collection as an ending node.
    #
    #     :type longitude: float
    #     :type latitude: float
    #     :return closest_ending_node: osm_id
    #     """
    #     provided_point = Point(longitude=longitude, latitude=latitude)
    #     return self.get_closest_ending_node_in_edges_from_point(provided_point=provided_point)

    # def get_closest_ending_node_in_edges_from_point(self, provided_point):
    #     """
    #     Retrieve the node which is closest to the provided point and is stored at
    #     the Edges collection as an ending node.
    #
    #     :type provided_point: Point
    #     :return closest_ending_node: osm_id
    #     """
    #     closest_ending_node = None
    #     ending_nodes = self.get_ending_nodes_of_edges_dictionary().keys()
    #     # {ending_node_osm_id -> {'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    #     #                         'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    #     #                         'max_speed', 'road_type', 'way_id', 'traffic_density'}
    #     ending_nodes_set = self.get_ending_nodes_of_edges_dictionary()
    #     minimum_distance = float('Inf')
    #
    #     for current_ending_node in ending_nodes_set:
    #         current_point = self.points_dictionary[current_ending_node]
    #         current_distance = distance(point_one=provided_point, point_two=current_point)
    #
    #         if current_distance == 0:
    #             closest_ending_node = current_ending_node
    #             break
    #         elif current_distance < minimum_distance:
    #             minimum_distance = current_distance
    #             closest_ending_node = current_ending_node
    #         else:
    #             pass
    #
    #     return closest_ending_node

    # def get_closest_starting_node_in_edges_from_coordinates(self, longitude, latitude):
    #     """
    #     Retrieve the node which is closest to a set of coordinates and is stored at
    #     the Edges collection as a starting node.
    #
    #     :type longitude: float
    #     :type latitude: float
    #     :return closest_starting_node: osm_id
    #     """
    #     provided_point = Point(longitude=longitude, latitude=latitude)
    #     return self.get_closest_starting_node_in_edges_from_point(provided_point=provided_point)

    # def get_closest_starting_node_in_edges_from_point(self, provided_point):
    #     """
    #     Retrieve the node which is closest to the provided point and is stored at
    #     the Edges collection as a starting node.
    #
    #     :type provided_point: Point
    #     :return closest_starting_node: osm_id
    #     """
    #     closest_starting_node = None
    #     starting_nodes_set = self.get_starting_nodes_of_edges()
    #     minimum_distance = float('Inf')
    #
    #     for current_starting_node in starting_nodes_set:
    #         current_point = self.points_dictionary[current_starting_node]
    #         current_distance = distance(point_one=provided_point, point_two=current_point)
    #
    #         if current_distance == 0:
    #             closest_starting_node = current_starting_node
    #             break
    #         elif current_distance < minimum_distance:
    #             minimum_distance = current_distance
    #             closest_starting_node = current_starting_node
    #         else:
    #             pass
    #
    #     return closest_starting_node

    def get_edges_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Edges collection.

        :return: {starting_node_osm_id -> [{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                            'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                                            'max_speed', 'road_type', 'way_id', 'traffic_density'}]}
        """
        edges_dictionary = self.connection.get_edges_dictionary()
        return edges_dictionary

    def get_edges_list(self):
        """
        Retrieve a list containing all the documents of the Edges collection.

        :return: edges_list: [{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                               'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                               'max_speed', 'road_type', 'way_id', 'traffic_density'}]
        """
        edges_list = self.connection.get_edges_list()
        return edges_list

    # def get_ending_nodes_of_edges_dictionary(self):
    #     """
    #     Retrieve a dictionary containing all the ending_nodes which are included in the Edges collection.
    #
    #     :return: {ending_node_osm_id -> [{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    #                                       'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    #                                       'max_speed', 'road_type', 'way_id', 'traffic_density'}]}
    #     """
    #     ending_nodes_dictionary = {}
    #     edges_list = self.get_edges_list()
    #
    #     # edges_list: [{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    #     #               'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    #     #               'max_speed', 'road_type', 'way_id', 'traffic_density'}]
    #     for edges_document in edges_list:
    #         ending_node_osm_id = edges_document.get('ending_node').get('osm_id')
    #
    #         if ending_node_osm_id in ending_nodes_dictionary:
    #             ending_nodes_dictionary[ending_node_osm_id].append(edges_document)
    #         else:
    #             ending_nodes_dictionary[ending_node_osm_id] = [edges_document]
    #
    #     return ending_nodes_dictionary

    # def get_point_from_osm_id(self, osm_id):
    #     """
    #     Retrieve the point which correspond to a specific osm_id.
    #
    #     :type osm_id: integer
    #     :return: Point
    #     """
    #     point = None
    #     # document = {'osm_id': osm_id, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
    #     # document = self.connection.find_point(osm_id=osm_id)
    #     # point_entry = document.get('point')
    #
    #     point_entry = self.points_dictionary.get(osm_id, None)
    #
    #     if point_entry is not None:
    #         point = Point(longitude=point_entry.get('longitude'), latitude=point_entry.get('latitude'))
    #
    #     return point

    def get_points_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the Points collection.

        :return points_dictionary: {osm_id -> {'_id', 'osm_id', 'point': {'longitude', 'latitude'}}}
        """
        points_dictionary = self.connection.get_points_dictionary()
        return points_dictionary

    # def get_points_of_edges(self):
    #     """
    #     Retrieve a dictionary containing the points of edges.
    #
    #     :return points_of_edges: {osm_id -> point}
    #     """
    #     # edge_document = {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
    #     points_of_edges = {}
    #
    #     for starting_node, values in self.edges_dictionary.iteritems():
    #         ending_node = values.get('ending_node')
    #
    #         if starting_node not in points_of_edges:
    #             points_of_edges[starting_node] = self.points_dictionary.get(starting_node)
    #
    #         if ending_node not in points_of_edges:
    #             points_of_edges[ending_node] = self.points_dictionary.get(ending_node)
    #
    #     return points_of_edges

    # def get_starting_nodes_of_edges(self):
    #     """
    #     Retrieve all the starting nodes which are included in the Edges collection.
    #
    #     :return: starting_nodes: set([osm_id])
    #     """
    #     starting_nodes = set()
    #
    #     for starting_node in self.edges_dictionary:
    #         starting_nodes.add(starting_node)
    #
    #     return starting_nodes

    # def get_route_from_coordinates(self, starting_longitude, starting_latitude, ending_longitude, ending_latitude):
    #     """
    #     Find a route between two pairs of coordinates.
    #
    #     :type starting_longitude: float
    #     :type starting_latitude: float
    #     :type ending_longitude: float
    #     :type ending_latitude: float
    #     :return route: {'total_distance', 'total_time', 'nodes', 'points', 'total_distances',
    #                     'total_times', 'partial_distances', 'partial_times'}
    #     """
    #     starting_point = Point(longitude=starting_longitude, latitude=starting_latitude)
    #     ending_point = Point(longitude=ending_longitude, latitude=ending_latitude)
    #     return self.get_route_from_points(starting_point=starting_point, ending_point=ending_point)

    # def get_route_from_points(self, starting_point, ending_point):
    #     """
    #     Find a route between two points.
    #
    #     :type starting_point: Point
    #     :type ending_point: Point
    #     :return {'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
    #              'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}}
    #     """
    #     starting_osm_id = self.get_closest_starting_node_in_edges_from_point(provided_point=starting_point)
    #     ending_osm_id = self.get_closest_ending_node_in_edges_from_point(provided_point=ending_point)
    #     route = find_path(starting_node_osm_id=starting_osm_id,
    #                       ending_node_osm_id=ending_osm_id,
    #                       edges=self.edges_dictionary,
    #                       points=self.points_dictionary)
    #     return route

    def get_route_between_two_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        """
        Find a route between two bus_stops, based on their names.

        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return {'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                 'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                 'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
                           'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}}
        """
        starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
        ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

        route = find_path(starting_node_osm_id=starting_bus_stop.get('osm_id'),
                          ending_node_osm_id=ending_bus_stop.get('osm_id'),
                          edges=self.edges_dictionary,
                          points=self.points_dictionary)

        response = {'starting_bus_stop': starting_bus_stop, 'ending_bus_stop': ending_bus_stop, 'route': route}
        return response

    def get_route_between_multiple_bus_stops(self, bus_stop_names):
        """
        Find a route between multiple bus_stop, based on their names.

        :param bus_stop_names: [string]
        :return [{'starting_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                  'ending_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                  'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
                            'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}}]
        """
        response = []

        for i in range(0, len(bus_stop_names) - 1):
            starting_bus_stop_name = bus_stop_names[i]
            starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
            ending_bus_stop_name = bus_stop_names[i + 1]
            ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

            route = find_path(starting_node_osm_id=starting_bus_stop.get('osm_id'),
                              ending_node_osm_id=ending_bus_stop.get('osm_id'),
                              edges=self.edges_dictionary,
                              points=self.points_dictionary)

            intermediate_route = {'starting_bus_stop': starting_bus_stop,
                                  'ending_bus_stop': ending_bus_stop,
                                  'route': route}

            response.append(intermediate_route)

        return response

    def get_waypoints_between_two_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name):
        """
        Find the waypoints of all possible routes between two bus_stops, based on their names.

        :param starting_bus_stop_name: string
        :param ending_bus_stop_name: string
        :return {'starting_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                 'ending_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                 'waypoints': [[{'osm_id', 'point': {'longitude', 'latitude'}}]]}
        """
        starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
        ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

        waypoints = find_waypoints_between_two_nodes(starting_node_osm_id=starting_bus_stop.get('osm_id'),
                                                     ending_node_osm_id=ending_bus_stop.get('osm_id'),
                                                     edges=self.edges_dictionary,
                                                     points=self.points_dictionary)

        response = {'starting_bus_stop': starting_bus_stop, 'ending_bus_stop': ending_bus_stop, 'waypoints': waypoints}
        return response

    def get_waypoints_between_multiple_bus_stops(self, bus_stop_names):
        """
        Find the waypoints of all possible routes between multiple bus_stops, based on their names.

        :param bus_stop_names: [string]
        :return [{'starting_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                  'ending_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                  'waypoints': [[{'osm_id', 'point': {'longitude', 'latitude'}}]]}]
        """
        response = []

        for i in range(0, len(bus_stop_names) - 1):
            starting_bus_stop_name = bus_stop_names[i]
            starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
            ending_bus_stop_name = bus_stop_names[i + 1]
            ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)

            waypoints = find_waypoints_between_two_nodes(starting_node_osm_id=starting_bus_stop.get('osm_id'),
                                                         ending_node_osm_id=ending_bus_stop.get('osm_id'),
                                                         edges=self.edges_dictionary,
                                                         points=self.points_dictionary)

            intermediate_response = {'starting_bus_stop': starting_bus_stop,
                                     'ending_bus_stop': ending_bus_stop,
                                     'waypoints': waypoints}

            response.append(intermediate_response)

        return response

    # def get_multiple_routes_between_bus_stops(self, starting_bus_stop_name, ending_bus_stop_name, number_of_routes):
    #     """
    #     Find multiple routes between two bus_stop_names, based on their names.
    #
    #     :param starting_bus_stop_name: string
    #     :param ending_bus_stop_name: string
    #     :param number_of_routes: integer
    #     :return {'starting_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #              'ending_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #              'routes': [{'total_distance', 'total_time', 'node_osm_ids', 'points',
    #                          'distances_from_starting_node', 'times_from_starting_node',
    #                          'distances_from_previous_node', 'times_from_previous_node'}]}
    #     """
    #     starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
    #     ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)
    #
    #     routes = find_multiple_paths(starting_node_osm_id=starting_bus_stop.get('osm_id'),
    #                                  ending_node_osm_id=ending_bus_stop.get('osm_id'),
    #                                  edges=self.edges_dictionary,
    #                                  points=self.points_dictionary,
    #                                  number_of_paths=number_of_routes)
    #
    #     result = {'starting_bus_stop': starting_bus_stop, 'ending_bus_stop': ending_bus_stop, 'routes': routes}
    #     return result

    # def get_multiple_routes_between_multiple_bus_stops(self, bus_stop_names, number_of_routes):
    #     """
    #     Find a multiple routes between multiple bus_stop_names, based on their names.
    #
    #     :param bus_stop_names: [string]
    #     :param number_of_routes: integer
    #     :return [{'starting_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #               'ending_bus_stop': {'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    #               'routes': [{'total_distance', 'total_time', 'node_osm_ids', 'points',
    #                           'distances_from_starting_node', 'times_from_starting_node',
    #                           'distances_from_previous_node', 'times_from_previous_node'}]}]
    #     """
    #     final_route = []
    #
    #     for i in range(0, len(bus_stop_names) - 1):
    #         starting_bus_stop_name = bus_stop_names[i]
    #         starting_bus_stop = self.get_bus_stop_from_name(name=starting_bus_stop_name)
    #         ending_bus_stop_name = bus_stop_names[i + 1]
    #         ending_bus_stop = self.get_bus_stop_from_name(name=ending_bus_stop_name)
    #
    #         routes = find_multiple_paths(starting_node_osm_id=starting_bus_stop.get('osm_id'),
    #                                      ending_node_osm_id=ending_bus_stop.get('osm_id'),
    #                                      edges=self.edges_dictionary,
    #                                      points=self.points_dictionary,
    #                                      number_of_paths=number_of_routes)
    #
    #         intermediate_route = {'starting_bus_stop': starting_bus_stop,
    #                               'ending_bus_stop': ending_bus_stop,
    #                               'routes': routes}
    #
    #         final_route.append(intermediate_route)
    #
    #     return final_route


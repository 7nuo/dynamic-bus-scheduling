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
from src.common.variables import bus_road_types, standard_speed
from src.geospatial_data.point import distance, Point

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class Node(object):
    def __init__(self, osm_id, point_document):
        self.osm_id = osm_id
        self.point_document = point_document
        self.f_score_distance = float('inf')
        self.f_score_time_on_road = float('inf')
        self.g_score_distance = float('inf')
        self.g_score_time_on_road = float('inf')
        self.heuristic_estimated_distance = float('inf')
        self.heuristic_estimated_time_on_road = float('inf')
        self.previous_nodes = []

    def set_f_score(self, f_score_distance, f_score_time_on_road):
        self.f_score_distance = f_score_distance
        self.f_score_time_on_road = f_score_time_on_road

    def get_f_score(self):
        return self.f_score_distance, self.f_score_time_on_road

    def set_g_score(self, g_score_distance, g_score_time_on_road):
        self.g_score_distance = g_score_distance
        self.g_score_time_on_road = g_score_time_on_road

    def get_g_score(self):
        return self.g_score_distance, self.g_score_time_on_road

    def set_previous_nodes(self, previous_nodes):
        self.previous_nodes = previous_nodes

    def get_previous_nodes(self):
        return self.previous_nodes

    def add_previous_node(self, node):
        self.previous_nodes.append(node)

    def clear_previous_nodes(self):
        self.previous_nodes = []


class OrderedSet(object):
    def __init__(self):
        self.nodes = []

    def __len__(self):
        return len(self.nodes)

    def exists(self, node_osm_id):
        """
        Check if a node exists in the nodes list.

        :type node_osm_id: int
        :return: boolean
        """
        returned_value = False

        for node in self.nodes:
            if node.osm_id == node_osm_id:
                returned_value = True
                break

        return returned_value

    def index_of_insertion(self, new_node):
        """
        Retrieve the index in which a new node should be inserted, according to the corresponding f_score value.

        :param new_node: Node
        :return index: int
        """
        index = 0

        for node in self.nodes:
            if new_node.f_score_time_on_road < node.f_score_time_on_road:
                break
            index += 1

        return index

    def insert(self, new_node):
        """
        Insert a new node.

        :param new_node: Node
        """
        new_index = self.index_of_insertion(new_node=new_node)
        self.nodes.insert(new_index, new_node)

    def pop(self):
        """
        Remove - retrieve the node with the lowest f_score values.

        :return: (f_score_distance, f_score_time_on_road), node
        """
        node = self.nodes.pop(0)
        return node

    def remove(self, index):
        """
        Remove node at index.

        :type index: int
        """
        self.nodes.pop(index)


def find_path_between_two_nodes(start, end, edges_dictionary):
    """
    Implement the A* search algorithm in order to find the less time-consuming path
    between the starting and the ending node.

    :param start: {'osm_id', 'point': {'longitude', 'latitude'}}
    :param end: {'osm_id', 'point': {'longitude', 'latitude'}}

    edge_document: {
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'}

    :param edges_dictionary: {starting_node_osm_id -> [edge_document]}

    :return: path_between_two_nodes: {
                 'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges', 'distances_from_starting_node',
                 'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}

            (None if there is no path between the provided nodes)
    """
    # A dictionary with the nodes that have already been evaluated: {node_osm_id -> node}
    closed_set = {}

    # The set of currently discovered nodes still to be evaluated. Initially, only the starting node is known.
    open_set = OrderedSet()

    starting_node_osm_id = start.get('osm_id')
    starting_node_point_document = start.get('point')
    ending_node_osm_id = end.get('osm_id')
    ending_node_point_document = end.get('point')

    # Initialize starting_node and ending_node.
    starting_node = Node(osm_id=starting_node_osm_id, point_document=starting_node_point_document)
    ending_node = Node(osm_id=ending_node_osm_id, point_document=ending_node_point_document)

    # Distance and time from starting_node equal to zero.
    starting_node.set_g_score(g_score_distance=0.0, g_score_time_on_road=0.0)

    # Distance and time to ending node is estimated heuristically.
    starting_node_f_score_distance, starting_node_f_score_time_on_road = heuristic_cost_estimate(
        starting_point_document=starting_node.point_document,
        ending_point_document=ending_node.point_document
    )
    starting_node.set_f_score(
        f_score_distance=starting_node_f_score_distance,
        f_score_time_on_road=starting_node_f_score_time_on_road
    )

    # Add the starting_node to the list of previous nodes.
    starting_node.add_previous_node(node=starting_node)

    # Add the starting_node to the closed_set, since it has already been evaluated.
    closed_set[starting_node_osm_id] = starting_node

    # Add the starting_node to the open_set, since its edges_dictionary should be evaluated.
    open_set.insert(new_node=starting_node)

    # While there are more nodes, whose edges_dictionary have not been evaluated.
    while len(open_set) > 0:

        # During the first iteration of this loop, current_node will be equal to starting_node.
        current_node = open_set.pop()

        # ending_node has been discovered: path should be reconstructed.
        if current_node.osm_id == ending_node_osm_id:
            return reconstruct_path(
                list_of_nodes=current_node.get_previous_nodes(),
                edges_dictionary=edges_dictionary
            )

        # current_node does not have any edges_dictionary.
        if current_node.osm_id not in edges_dictionary:
            continue

        for edge in edges_dictionary.get(current_node.osm_id):
            next_node_osm_id = edge.get('ending_node').get('osm_id')
            next_node_point_document = edge.get('ending_node').get('point')

            # Check whether the next_node has already been evaluated.
            if next_node_osm_id in closed_set:
                next_node = closed_set.get(next_node_osm_id)
                # continue
            else:
                next_node = Node(osm_id=next_node_osm_id, point_document=next_node_point_document)
                next_node.heuristic_estimated_distance, next_node.heuristic_estimated_time_on_road = \
                    heuristic_cost_estimate(
                        starting_point_document=next_node.point_document,
                        ending_point_document=ending_node.point_document
                    )

            max_speed = edge.get('max_speed')
            road_type = edge.get('road_type')
            traffic_density = edge.get('traffic_density')

            # Calculate the difference in values between current_node and next_node.
            additional_g_score_distance, additional_g_score_time_on_road = g_score_estimate(
                starting_point_document=current_node.point_document,
                ending_point_document=next_node.point_document,
                max_speed=max_speed,
                road_type=road_type,
                traffic_density=traffic_density
            )

            # Calculate new g_score values
            new_g_score_distance = current_node.g_score_distance + additional_g_score_distance
            new_g_score_time_on_road = current_node.g_score_time_on_road + additional_g_score_time_on_road

            if next_node.g_score_time_on_road < new_g_score_time_on_road:
                continue

            next_node.g_score_distance = new_g_score_distance
            next_node.g_score_time_on_road = new_g_score_time_on_road

            # Calculate new f_score values
            next_node.f_score_distance = new_g_score_distance + next_node.heuristic_estimated_distance
            next_node.f_score_time_on_road = new_g_score_time_on_road + next_node.heuristic_estimated_time_on_road

            # Add next_node to the list of previous nodes.
            next_node.set_previous_nodes(previous_nodes=current_node.get_previous_nodes() + [next_node])

            # next_node has been evaluated.
            closed_set[next_node_osm_id] = next_node

            # Add next_node to the open_set, so as to allow its edges_dictionary to be evaluated.
            if not open_set.exists(next_node_osm_id):
                open_set.insert(new_node=next_node)

    return None


def reconstruct_path(list_of_nodes, edges_dictionary):
    """
    Get a dictionary containing the parameters of the path.

    :param list_of_nodes: The list of nodes which consist the optimal path.
    
    edge_document: {
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'}

    :param edges_dictionary: {starting_node_osm_id -> [edge_document]}
    
    :return: path: {
                 'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges', 'distances_from_starting_node',
                 'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}
    """
    node_osm_ids = []
    points = []
    distances_from_starting_node = []
    times_from_starting_node = []
    distances_from_previous_node = []
    times_from_previous_node = []

    partial_distance = 0
    partial_time = 0
    previous_distance = None
    previous_time = None

    for node in list_of_nodes:
        node_osm_ids.append(node.osm_id)
        points.append(node.point_document)
        distances_from_starting_node.append(node.g_score_distance)
        times_from_starting_node.append(node.g_score_time_on_road)

        if previous_distance is not None:
            partial_distance = node.g_score_distance - previous_distance

        distances_from_previous_node.append(partial_distance)
        previous_distance = node.g_score_distance

        if previous_time is not None:
            partial_time = node.g_score_time_on_road - previous_time

        times_from_previous_node.append(partial_time)
        previous_time = node.g_score_time_on_road

    total_distance = previous_distance
    total_time = previous_time

    followed_edges = []

    for i in range(0, len(node_osm_ids) - 1):
        starting_node_osm_id = node_osm_ids[i]
        ending_node_osm_id = node_osm_ids[i + 1]
        list_of_starting_node_edges = edges_dictionary.get(starting_node_osm_id)
        edge = None

        for starting_node_edge in list_of_starting_node_edges:
            if starting_node_edge.get('ending_node').get('osm_id') == ending_node_osm_id:
                edge = starting_node_edge
                break

        followed_edges.append(edge)

    path = {
        'total_distance': total_distance,
        'total_time': total_time,
        'node_osm_ids': node_osm_ids,
        'points': points,
        'edges': followed_edges,
        'distances_from_starting_node': distances_from_starting_node,
        'times_from_starting_node': times_from_starting_node,
        'distances_from_previous_node': distances_from_previous_node,
        'times_from_previous_node': times_from_previous_node
    }

    return path


def estimate_road_type_speed_decrease_factor(road_type):
    """
    Estimate a speed decrease factor, based on the type of the road.

    :param road_type: One of the bus_road_types.
    :return: 0 <= road_type_speed_decrease_factor <= 1
    """
    road_type_index = bus_road_types.index(road_type)
    road_type_speed_decrease_factor = 1 - (float(road_type_index) / 50)
    return road_type_speed_decrease_factor


def estimate_traffic_speed_decrease_factor(traffic_density):
    """
    Estimate a speed decrease factor, based on the density of traffic.

    :param traffic_density: float value between 0 and 1.
    :return: 0 <= traffic_speed_decrease_factor <= 1
    """
    traffic_speed_decrease_factor = 1 - float(traffic_density)
    return traffic_speed_decrease_factor


def g_score_estimate(starting_point_document, ending_point_document, max_speed, road_type, traffic_density):
    """
    Estimate the cost of getting from the starting point to the ending point.

    :param starting_point_document: {'longitude', 'latitude'}}
    :param ending_point_document: {'longitude', 'latitude'}}
    :param max_speed: float
    :param road_type: One of the road types that can be accessed by a bus (string).
    :param traffic_density: float value between 0 and 1.
    :return: (f_score_distance in meters, f_score_time_on_road in seconds)
    """
    starting_point = Point(
        longitude=starting_point_document.get('longitude'),
        latitude=starting_point_document.get('latitude')
    )
    ending_point = Point(
        longitude=ending_point_document.get('longitude'),
        latitude=ending_point_document.get('latitude')
    )
    estimated_distance = distance(point_one=starting_point, point_two=ending_point)
    road_type_speed_decrease_factor = estimate_road_type_speed_decrease_factor(road_type=road_type)
    traffic_speed_decrease_factor = estimate_traffic_speed_decrease_factor(traffic_density=traffic_density)
    estimated_time_on_road = estimated_distance / (road_type_speed_decrease_factor * traffic_speed_decrease_factor *
                                                   (float(max_speed) * 1000 / 3600))
    return estimated_distance, estimated_time_on_road


def heuristic_cost_estimate(starting_point_document, ending_point_document):
    """
    Make a rough estimation regarding the cost of getting from the starting point to the ending point.

    :param starting_point_document: {'longitude', 'latitude'}
    :param ending_point_document:  {'longitude', 'latitude'}
    :return: (f_score_distance in meters, f_score_time_on_road in seconds)
    """
    starting_point = Point(
        longitude=starting_point_document.get('longitude'),
        latitude=starting_point_document.get('latitude')
    )
    ending_point = Point(
        longitude=ending_point_document.get('longitude'),
        latitude=ending_point_document.get('latitude')
    )
    estimated_distance = distance(point_one=starting_point, point_two=ending_point)
    estimated_time_on_road = estimated_distance / (float(standard_speed) * 1000 / 3600)
    return estimated_distance, estimated_time_on_road

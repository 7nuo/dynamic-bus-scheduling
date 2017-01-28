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
        self.real_distance_cost = float('inf')
        self.real_travelling_time_cost = float('inf')
        self.heuristic_distance_cost = float('inf')
        self.heuristic_travelling_time_cost = float('inf')
        self.total_distance_score = float('inf')
        self.total_travelling_time_score = float('inf')
        self.followed_path = []

    def get_real_cost(self):
        return self.real_distance_cost, self.real_travelling_time_cost

    def set_real_cost(self, real_distance_cost, real_travelling_time_cost):
        self.real_distance_cost = real_distance_cost
        self.real_travelling_time_cost = real_travelling_time_cost

    def get_heuristic_cost(self):
        return self.heuristic_distance_cost, self.heuristic_travelling_time_cost

    def set_heuristic_cost(self, heuristic_distance_cost, heuristic_travelling_time_cost):
        self.heuristic_distance_cost = heuristic_distance_cost
        self.heuristic_travelling_time_cost = heuristic_travelling_time_cost

    def estimate_total_score(self):
        self.total_distance_score = self.real_distance_cost + self.heuristic_distance_cost

    def get_total_score(self):
        return self.total_distance_score, self.total_travelling_time_score

    def set_total_score(self, total_distance_score, total_travelling_time_score):
        self.total_distance_score = total_distance_score
        self.total_travelling_time_score = total_travelling_time_score

    def add_node_to_followed_path(self, node):
        self.followed_path.append(node)

    def clear_followed_path(self):
        self.followed_path = []

    def get_followed_path(self):
        return self.followed_path

    def set_followed_path(self, followed_path):
        self.followed_path = followed_path


class OrderedSet(object):
    """
    Node storing structure capable of keeping priority among nodes according to their
    total_travelling_time_score values. Nodes with lower total_travelling_time_score are
    retrieved first. This rule could be changed by modifying the index_of_insertion
    function, which estimates the index of insertion for each new node.
    """
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
        Retrieve the index in which a new node should be inserted, comparing the corresponding
        total_travelling_time_score values. The lower the total_travelling_time_score value,
        the lower the index of insertion.

        :param new_node: Node
        :return index: int
        """
        index = 0

        for node in self.nodes:
            if new_node.total_travelling_time_score < node.total_travelling_time_score:
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
        Remove - retrieve the node with the lowest total_travelling_time_score value.

        :return: node: Node
        """
        node = self.nodes.pop(0)
        return node


def estimate_heuristic_cost(starting_point_document, ending_point_document):
    """
    Make a heuristic estimation regarding the cost of travelling from starting_point to ending_point.

    :param starting_point_document: {'longitude', 'latitude'}
    :param ending_point_document:  {'longitude', 'latitude'}
    :return: (heuristic_distance_cost, heuristic_travelling_time_cost): (float, float) in (meters, seconds)
    """
    starting_point = Point(
        longitude=starting_point_document.get('longitude'),
        latitude=starting_point_document.get('latitude')
    )
    ending_point = Point(
        longitude=ending_point_document.get('longitude'),
        latitude=ending_point_document.get('latitude')
    )
    heuristic_distance_cost = distance(
        point_one=starting_point,
        point_two=ending_point
    )
    heuristic_travelling_time_cost = estimate_travelling_time(
        distance_to_be_covered=heuristic_distance_cost,
        max_speed=standard_speed
    )
    return heuristic_distance_cost, heuristic_travelling_time_cost


def estimate_real_cost(starting_point_document, ending_point_document, max_speed, road_type, traffic_density):
    """
    Estimate the real cost of travelling from starting_point to ending_point.

    :param starting_point_document: {'longitude', 'latitude'}
    :param ending_point_document: {'longitude', 'latitude'}
    :param max_speed: float
    :param road_type: One of the road types that can be accessed by a bus (string).
    :param traffic_density: float value between 0 and 1.
    :return: (real_distance_cost, real_travelling_time_cost): (float, float) in (meters, seconds)
    """
    starting_point = Point(
        longitude=starting_point_document.get('longitude'),
        latitude=starting_point_document.get('latitude')
    )
    ending_point = Point(
        longitude=ending_point_document.get('longitude'),
        latitude=ending_point_document.get('latitude')
    )
    real_distance_cost = distance(
        point_one=starting_point,
        point_two=ending_point
    )
    real_travelling_time_cost = estimate_travelling_time(
        distance_to_be_covered=real_distance_cost,
        max_speed=max_speed,
        road_type=road_type,
        traffic_density=traffic_density
    )
    return real_distance_cost, real_travelling_time_cost


def estimate_road_type_speed_decrease_factor(road_type):
    """
    Estimate a speed decrease factor, based on road_type.

    :param road_type: One of the bus_road_types.
    :return: 0 <= road_type_speed_decrease_factor <= 1
    """
    road_type_index = bus_road_types.index(road_type)
    road_type_speed_decrease_factor = 1 - (float(road_type_index) / 50)
    return road_type_speed_decrease_factor


def estimate_traffic_speed_decrease_factor(traffic_density):
    """
    Estimate a speed decrease factor, based on the current levels of traffic_density.

    :param traffic_density: float value between 0 and 1.
    :return: 0 <= traffic_speed_decrease_factor <= 1
    """
    traffic_speed_decrease_factor = 1 - float(traffic_density)
    return traffic_speed_decrease_factor


def estimate_travelling_time(distance_to_be_covered, max_speed, road_type=None, traffic_density=None):
    """
    Estimate travelling_time.

    :param distance_to_be_covered: float (in meters)
    :param max_speed: float
    :param road_type: One of the road types that can be accessed by a bus (string).
    :param traffic_density: float value between 0 and 1.
    :return: travelling_time: float (in seconds)
    """
    road_type_speed_decrease_factor = 1.0
    traffic_speed_decrease_factor = 1.0

    if road_type is not None:
        road_type_speed_decrease_factor = estimate_road_type_speed_decrease_factor(road_type=road_type)

    if traffic_density is not None:
        traffic_speed_decrease_factor = estimate_traffic_speed_decrease_factor(traffic_density=traffic_density)

    speed = road_type_speed_decrease_factor * traffic_speed_decrease_factor * (float(max_speed) * 1000 / 3600)
    travelling_time = distance_to_be_covered / speed
    return travelling_time


def identify_path_with_lowest_cost(start, end, edges_dictionary):
    """
    This function is capable of identifying the path with the lowest cost value
    (less time-consuming in this case), connecting the starting with the ending
    node, implementing a variation of the A* search algorithm.

    :param start: {'osm_id', 'point': {'longitude', 'latitude'}}
    :param end: {'osm_id', 'point': {'longitude', 'latitude'}}

    edge_document: {
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'}

    :param edges_dictionary: {starting_node_osm_id -> [edge_document]}

    :return: path_between_two_nodes: {
                 'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                 'distances_from_starting_node', 'times_from_starting_node',
                 'distances_from_previous_node', 'times_from_previous_node'
             }

            (None if there is no path between the provided nodes)
    """
    # A dictionary ({node_osm_id -> node}) containing nodes that have
    # already been evaluated (cost values have been estimated).
    closed_set = {}

    # A node storing structure containing nodes whose neighbors
    # should be evaluated (cost values should be estimated).
    open_set = OrderedSet()

    # Initialize starting_node.
    starting_node_osm_id = start.get('osm_id')
    starting_node_point_document = start.get('point')
    starting_node = Node(
        osm_id=starting_node_osm_id,
        point_document=starting_node_point_document
    )

    # Initialize ending_node.
    ending_node_osm_id = end.get('osm_id')
    ending_node_point_document = end.get('point')
    ending_node = Node(
        osm_id=ending_node_osm_id,
        point_document=ending_node_point_document
    )

    # Real cost values of starting_node are equal to zero.
    starting_node.set_real_cost(
        real_distance_cost=0.0,
        real_travelling_time_cost=0.0
    )

    # Estimate heuristic cost values of starting_node.
    heuristic_distance_cost, heuristic_travelling_time_cost = estimate_heuristic_cost(
        starting_point_document=starting_node.point_document,
        ending_point_document=ending_node.point_document
    )
    starting_node.set_heuristic_cost(
        heuristic_distance_cost=heuristic_distance_cost,
        heuristic_travelling_time_cost=heuristic_travelling_time_cost
    )

    # Estimate total score values of starting_node.
    starting_node.estimate_total_score()

    # Set the followed_path of starting_node.
    starting_node.add_node_to_followed_path(node=starting_node)

    # Add the starting_node to the closed_set, since it has already been evaluated.
    closed_set[starting_node_osm_id] = starting_node

    # Add the starting_node to the open_set, since its neighbors should be evaluated.
    open_set.insert(new_node=starting_node)

    # The node with the lowest total_score value is retrieved from the open_set,
    # as long as the number of stored nodes is greater than zero.
    while len(open_set) > 0:

        # During the first iteration of this loop, current_node will be equal to starting_node.
        current_node = open_set.pop()

        # Ending condition: ending_node has been discovered => followed path should be processed in order to
        # retrieve its parameters (covered distance, travelling time, intermediate nodes, points, and edges).
        if current_node.osm_id == ending_node_osm_id:
            return process_followed_path(
                list_of_nodes=current_node.get_followed_path(),
                edges_dictionary=edges_dictionary
            )

        # Continuation condition: current_node has no neighbors.
        if current_node.osm_id not in edges_dictionary:
            continue

        # Case that current_node has neighbors. Each neighbor should be evaluated,
        # taking into consideration the parameters of corresponding edges.
        for edge in edges_dictionary.get(current_node.osm_id):
            next_node_osm_id = edge.get('ending_node').get('osm_id')
            next_node_point_document = edge.get('ending_node').get('point')
            max_speed = edge.get('max_speed')
            road_type = edge.get('road_type')
            traffic_density = edge.get('traffic_density')

            # Check whether next_node has already been evaluated.
            if next_node_osm_id in closed_set:
                next_node = closed_set.get(next_node_osm_id)
            else:
                # Case that next_node has not been evaluated
                next_node = Node(
                    osm_id=next_node_osm_id,
                    point_document=next_node_point_document
                )
                # Heuristic cost should be estimated.
                heuristic_distance_cost, heuristic_travelling_time_cost = estimate_heuristic_cost(
                    starting_point_document=next_node.point_document,
                    ending_point_document=ending_node.point_document
                )
                next_node.set_heuristic_cost(
                    heuristic_distance_cost=heuristic_distance_cost,
                    heuristic_travelling_time_cost=heuristic_travelling_time_cost
                )

            # Estimate the real cost values for travelling from current_node to next_node.
            additional_real_distance_cost, additional_real_travelling_time_cost = estimate_real_cost(
                starting_point_document=current_node.point_document,
                ending_point_document=next_node.point_document,
                max_speed=max_speed,
                road_type=road_type,
                traffic_density=traffic_density
            )

            # Estimate the real cost values for travelling from starting_node to next_node.
            new_real_distance_cost = current_node.real_distance_cost + additional_real_distance_cost
            new_real_travelling_time_cost = current_node.real_travelling_time_cost + \
                                            additional_real_travelling_time_cost

            # Compare newly estimated real cost values with previous ones (in case next_node
            # was evaluated again). If the previously followed_path has lower cost value,
            # then the loop continues evaluating the next neighbor. (Non-evaluated nodes
            # are initialized with real cost values equal to infinity).
            if next_node.real_travelling_time_cost < new_real_travelling_time_cost:
                continue

            # Real cost values of next_node should be replaced.
            next_node.set_real_cost(
                real_distance_cost=new_real_distance_cost,
                real_travelling_time_cost=new_real_travelling_time_cost
            )

            # Total cost values of next_nodes are estimated.
            next_node.estimate_total_score()

            # Followed path of next_node is updated.
            next_node.set_followed_path(
                followed_path=current_node.get_followed_path() + [next_node]
            )

            # Since it has been evaluated, next_node is pushed into the closed_set.
            closed_set[next_node_osm_id] = next_node

            # Add next_node to the open_set, so as to allow its neighbors to be evaluated.
            if not open_set.exists(next_node_osm_id):
                open_set.insert(new_node=next_node)

    return None


def process_followed_path(list_of_nodes, edges_dictionary):
    """
    Process the nodes of followed path and retrieve a dictionary containing parameters such as
    covered distance, travelling time, intermediate nodes, geographical points, and edges.

    :param list_of_nodes: The list of nodes which consist the optimal path.

    edge_document: {
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'}

    :param edges_dictionary: {starting_node_osm_id -> [edge_document]}

    :return: path: {
                 'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
                 'distances_from_starting_node', 'times_from_starting_node',
                 'distances_from_previous_node', 'times_from_previous_node'
             }
    """
    node_osm_ids = []
    points = []
    distances_from_starting_node = []
    times_from_starting_node = []
    distances_from_previous_node = []
    times_from_previous_node = []
    total_distance = 0.0
    total_time = 0.0

    # Process nodes of followed path.
    for node in list_of_nodes:
        # Add osm_id and point_document of current node.
        node_osm_ids.append(node.osm_id)
        points.append(node.point_document)

        # Add distance and travelling_time from starting to current node.
        distances_from_starting_node.append(node.real_distance_cost)
        times_from_starting_node.append(node.real_travelling_time_cost)

        # Estimate distance from previous to current node, and update total_distance.
        distance_from_previous_node = node.real_distance_cost - total_distance
        distances_from_previous_node.append(distance_from_previous_node)
        total_distance = node.real_distance_cost

        # Estimate travelling_time from previous to current node, and update total_time.
        time_from_previous_node = node.real_travelling_time_cost - total_time
        times_from_previous_node.append(time_from_previous_node)
        total_time = node.real_travelling_time_cost

    # Identify followed edge_documents.
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

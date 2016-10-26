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

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class MultiplePathsNode(object):
    def __init__(self, osm_id):
        self.osm_id = osm_id
        self.followed_paths = []

    def __str__(self):
        return str(self.osm_id)

    def add_followed_path(self, followed_path):
        if followed_path not in self.followed_paths:
            self.followed_paths.append(followed_path)

    def set_followed_paths(self, followed_paths_of_previous_node):
        if len(followed_paths_of_previous_node) > 0:
            for followed_path_of_previous_node in followed_paths_of_previous_node:
                followed_path = followed_path_of_previous_node + [self.osm_id]
                self.add_followed_path(followed_path=followed_path)
        else:
            followed_path = [self.osm_id]
            self.followed_paths.append(followed_path)

    def get_followed_paths(self):
        return self.followed_paths


class MultiplePathsSet(object):
    def __init__(self):
        self.node_osm_ids = []
        self.nodes = []

    def __len__(self):
        return len(self.node_osm_ids)

    def __contains__(self, node_osm_id):
        """
        Check if a node exists in the nodes list.

        :type node_osm_id: integer
        :return: boolean
        """
        return node_osm_id in self.node_osm_ids

    def __str__(self):
        return str(self.node_osm_ids)

    def push(self, new_node):
        """
        Insert a new node.

        :param new_node: Node
        """
        new_node_osm_id = new_node.osm_id
        self.node_osm_ids.append(new_node_osm_id)
        self.nodes.append(new_node)

    def pop(self):
        """

        :return:
        """
        node = self.nodes.pop(0)
        self.node_osm_ids.remove(node.osm_id)
        return node


def find_waypoints_between_two_nodes(starting_node_osm_id, ending_node_osm_id, edges_dictionary):
    """
    Find all the possible lists of edges which connect two nodes.

    :param starting_node_osm_id: integer
    :param ending_node_osm_id: integer

    edge_document: {
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'}

    :param edges_dictionary: {starting_node_osm_id -> [edge_document]}
    :return: waypoints: [[edge_document]]
    """
    waypoints = []
    closed_set = {}
    open_set = MultiplePathsSet()

    starting_node = MultiplePathsNode(osm_id=starting_node_osm_id)
    starting_node.followed_paths = [[starting_node.osm_id]]
    open_set.push(new_node=starting_node)

    while len(open_set) > 0:
        current_node = open_set.pop()

        if current_node.osm_id == ending_node_osm_id:

            for followed_path in current_node.get_followed_paths():
                waypoints.append(process_followed_path(followed_path=followed_path, edges_dictionary=edges_dictionary))

            current_node.followed_paths = []
            continue

        if current_node.osm_id not in edges_dictionary or current_node.osm_id in closed_set:
            continue

        for edge in edges_dictionary.get(current_node.osm_id):
            next_node_osm_id = edge.get('ending_node').get('osm_id')

            if next_node_osm_id in closed_set:
                continue
            else:
                next_node = MultiplePathsNode(osm_id=next_node_osm_id)
                next_node.set_followed_paths(followed_paths_of_previous_node=current_node.get_followed_paths())
                open_set.push(new_node=next_node)

        closed_set[current_node.osm_id] = current_node

    return waypoints


def process_followed_path(followed_path, edges_dictionary):
    """
    Get the edges which are included in the followed_path.

    :param followed_path: [osm_id]

    edge_document: {
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'}

    :param edges_dictionary: {starting_node_osm_id -> [edge_document]}
    :return: detailed_followed_path: [edge_document]
    """
    detailed_followed_path = []

    for i in range(0, len(followed_path) - 1):
        starting_node = followed_path[i]
        ending_node = followed_path[i + 1]
        edge = get_edge(starting_node=starting_node, ending_node=ending_node, edges_dictionary=edges_dictionary)
        # path_entry = {'edge_id': edge.get('_id'), 'starting_node': starting_node, 'ending_node': ending_node}
        detailed_followed_path.append(edge)

    return detailed_followed_path


def get_edge(starting_node, ending_node, edges_dictionary):
    """
    Get the edge which connects the selected nodes.

    :param starting_node: osm_id
    :param ending_node: osm_id

    edge_document: {
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'}

    :param edges_dictionary: {starting_node_osm_id -> [edge_document]}
    :return: edge
    """
    edge = None
    starting_node_edges = edges_dictionary[starting_node]

    for starting_node_edge in starting_node_edges:
        if starting_node_edge.get('ending_node').get('osm_id') == ending_node:
            edge = starting_node_edge
            break

    return edge

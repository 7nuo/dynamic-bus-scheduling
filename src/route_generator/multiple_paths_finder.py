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
    '_id', 'timetable_id', 'line_id', 'bus_vehicle_id',
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
        '_id', 'client_id', 'line_id',
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
    '_id', 'client_id', 'line_id',
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

    def get_followed_paths(self):
        return self.followed_paths

    def update_followed_paths(self, followed_paths_of_previous_node):
        if len(followed_paths_of_previous_node) > 0:
            for followed_path_of_previous_node in followed_paths_of_previous_node:
                followed_path = followed_path_of_previous_node + [self.osm_id]
                self.add_followed_path(followed_path=followed_path)
        else:
            followed_path = [self.osm_id]
            self.followed_paths.append(followed_path)


class MultiplePathsSet(object):
    """
    Following the principles of breadth-first search, the neighbors of each node are explored first,
    before moving to the next level neighbors. For this reason, a data storing structure is implemented
    in order to store the nodes whose neighbors have not yet been explored.
    """
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

        :param new_node: MultiplePathsNode
        """
        new_node_osm_id = new_node.osm_id
        self.node_osm_ids.append(new_node_osm_id)
        self.nodes.append(new_node)

    def pop(self):
        """
        Remove - retrieve the first node of followed path.

        :return: node: MultiplePathsNode
        """
        node = self.nodes.pop(0)
        self.node_osm_ids.remove(node.osm_id)
        return node


def get_edge(starting_node, ending_node, edges_dictionary):
    """
    Get the edge_document which connects starting_node with ending_node.

    :param starting_node: osm_id
    :param ending_node: osm_id

    :param edges_dictionary: {starting_node_osm_id -> [edge_document]}
    :return: edge: edge_document
    """
    edge = None
    starting_node_edges = edges_dictionary[starting_node]

    for starting_node_edge in starting_node_edges:
        if starting_node_edge.get('ending_node').get('osm_id') == ending_node:
            edge = starting_node_edge
            break

    return edge


def identify_all_paths(starting_node_osm_id, ending_node_osm_id, edges_dictionary):
    """
    This function is capable of identifying all the possible paths connecting the
    starting with the ending node, implementing a variation of the Breadth-first
    search algorithm. Each path is represented by a list of edge_documents (waypoints),
    including details about intermediate nodes, maximum allowed speed, road type, and
    current levels of traffic density. The returned value of the function is a
    double list of edge_documents.

    :param starting_node_osm_id: integer
    :param ending_node_osm_id: integer
    :param edges_dictionary: {starting_node_osm_id -> [edge_document]}
    :return: waypoints: [[edge_document]]
    """
    # Returned value
    waypoints = []

    #  A data storing structure used in order to keep the nodes
    # whose neighbors should be considered.
    open_set = MultiplePathsSet()

    # A dictionary ({node_osm_id -> node}) containing nodes
    # whose neighbors have already been considered.
    closed_set = {}

    # starting_node is initialized and pushed into the open_set.
    starting_node = MultiplePathsNode(osm_id=starting_node_osm_id)
    starting_node.followed_paths = [[starting_node.osm_id]]
    open_set.push(new_node=starting_node)

    # The node in the first position of the open_set is retrieved,
    # as long as the number of stored nodes is above zero.
    while len(open_set) > 0:
        current_node = open_set.pop()

        # Continuation condition: ending_node has been discovered.
        if current_node.osm_id == ending_node_osm_id:

            # Each one of the followed paths is processed, in order to retrieve the
            # corresponding edge_documents, and added to the returned double list.
            for followed_path in current_node.get_followed_paths():
                waypoints.append(process_followed_path(
                    followed_path=followed_path,
                    edges_dictionary=edges_dictionary)
                )

            current_node.followed_paths = []
            continue

        # Continuation condition: current_node is ignored in case it has no neighbors,
        # or its neighbors have already been considered.
        if current_node.osm_id not in edges_dictionary or current_node.osm_id in closed_set:
            continue

        # Following the edges of current_node, each one of its neighbors is considered.
        for edge in edges_dictionary.get(current_node.osm_id):
            next_node_osm_id = edge.get('ending_node').get('osm_id')

            # Continuation condition: next_node has already been considered.
            if next_node_osm_id in closed_set:
                continue
            else:
                # Followed paths of next_node are updated and the node is pushed into the open_set,
                # so as to allow its neighbors to be considered.
                next_node = MultiplePathsNode(osm_id=next_node_osm_id)
                next_node.update_followed_paths(followed_paths_of_previous_node=current_node.get_followed_paths())
                open_set.push(new_node=next_node)

        # Since all its neighbors have been considered, current_node is added to the closed_set.
        closed_set[current_node.osm_id] = current_node

    return waypoints


def process_followed_path(followed_path, edges_dictionary):
    """
    This function is able to process the nodes of followed_path and
    identify the edge_documents which connect them.

    :param followed_path: [osm_id]
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

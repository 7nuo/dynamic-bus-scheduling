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
from src.common.variables import bus_road_types, standard_speed
from src.geospatial_data.point import distance


class MultiplePathsNode(object):
    def __init__(self, osm_id, point):
        self.osm_id = osm_id
        self.point = point
        self.followed_paths = []

    def __str__(self):
        return str(self.osm_id)

    def add_followed_path(self, followed_path):
        if followed_path not in self.followed_paths:
            self.followed_paths.append(followed_path)

    def set_followed_paths(self, followed_paths_of_previous_node):
        # print followed_paths_of_previous_node

        if len(followed_paths_of_previous_node) > 0:
            for followed_path_of_previous_node in followed_paths_of_previous_node:
                # followed_path = followed_path_of_previous_node
                # followed_path.append(self.osm_id)
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

    # def __repr__(self):
    #     return str(self.node_osm_ids)

    def push(self, new_node):
        """
        Insert a new node.

        :param new_node: Node
        """
        new_node_osm_id = new_node.osm_id
        self.node_osm_ids.append(new_node_osm_id)
        self.nodes.append(new_node)

        # if new_node_osm_id not in self.node_osm_ids:
        #     self.node_osm_ids.add(new_node_osm_id)
        #     self.nodes.append(new_node)

    def pop(self):
        """

        :return:
        """
        node = self.nodes.pop(0)
        self.node_osm_ids.remove(node.osm_id)
        return node


def _find_multiple_paths(starting_node_osm_id, ending_node_osm_id, edges, points, number_of_paths):
    paths = []
    closed_set = {}
    open_set = MultiplePathsSet()

    starting_node = MultiplePathsNode(osm_id=starting_node_osm_id, point=points.get(starting_node_osm_id))
    # starting_node.add_followed_path([starting_node.osm_id])
    starting_node.followed_paths = [[starting_node.osm_id]]
    open_set.push(new_node=starting_node)

    while len(open_set) > 0:
        current_node = open_set.pop()
        # print 'current_node:', current_node.osm_id, 'open_set:', str(open_set)

        if current_node.osm_id == ending_node_osm_id:
            print 'ok'
            for followed_path in current_node.get_followed_paths():
                paths.append(followed_path)
            current_node.followed_paths = []
            continue

        if current_node.osm_id not in edges or current_node.osm_id in closed_set:
            continue

        for edge in edges.get(current_node.osm_id):
            next_node_osm_id = edge.get('ending_node')
            # print edge

            if next_node_osm_id in closed_set:
                continue
            else:
                next_node = MultiplePathsNode(osm_id=next_node_osm_id, point=points.get(next_node_osm_id))
                next_node.set_followed_paths(followed_paths_of_previous_node=current_node.get_followed_paths())
                # print 'followed_paths_of_current_node:', current_node.get_followed_paths(), \
                #       'followed_paths_of_next_node:', next_node.get_followed_paths()
                open_set.push(new_node=next_node)

        closed_set[current_node.osm_id] = current_node

    return paths


# def _find_multiple_paths(starting_node_osm_id, ending_node_osm_id, edges, points, number_of_paths):
#     """
#
#     :param starting_node_osm_id: osm_id: integer
#     :param ending_node_osm_id: osm_id: integer
#     :param edges: {starting_node_osm_id -> [{ending_node_osm_id, max_speed, road_type, way_id, traffic_density}]
#     :param points: {osm_id -> point}
#     :param number_of_paths: integer
#     :return: [{'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
#                'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}]
#     """
#     paths = []
#
#     # A dictionary with the nodes that have already been evaluated: {node_osm_id -> node}
#     closed_set = {}
#
#     open_set = MultipleSet()
#
#     starting_node = MultipleNode(osm_id=starting_node_osm_id, point=points.get(starting_node_osm_id))
#
#     open_set.add_node(starting_node)
#
#     # While there are more nodes, whose edges have not been evaluated.
#     while len(open_set) > 0:
#
#         # During the first iteration of this loop, current_node will be equal to starting_node.
#         current_node = open_set.pop()
#
#     #     # ending_node has been discovered.
#         if current_node.osm_id == ending_node_osm_id:
#             paths.append(current_node)
#             continue
#             # return paths
#     #         paths.append(reconstruct_path(list_of_nodes=current_node.get_previous_nodes()))
#     #
#             # if len(paths) > number_of_paths - 1:
#             #     return paths
#             # else:
#             #     continue
#     #
#         # current_node does not have any edges.
#         if current_node.osm_id not in edges:
#             continue
#
#         for edge in edges.get(current_node.osm_id):
#             next_node_osm_id = edge.get('ending_node')
#
#             if next_node_osm_id in closed_set:
#                 next_node = closed_set.get(next_node_osm_id)
#                 next_node.add_parent(parent=current_node)
#                 continue
#             else:
#                 next_node = MultipleNode(next_node_osm_id, point=points.get(next_node_osm_id))
#                 next_node.add_parent(parent=current_node)
#                 closed_set[next_node_osm_id] = next_node
#                 open_set.add_node(new_node=next_node)
#
#     #         # Check whether the next_node has already been evaluated.
#     #         if next_node_osm_id in closed_set:
#     #             next_node = closed_set.get(next_node_osm_id)
#     #             # continue
#     #         else:
#     #             next_node = Node(osm_id=next_node_osm_id, point=points.get(next_node_osm_id))
#     #             next_node.heuristic_estimated_distance, next_node.heuristic_estimated_time_on_road = \
#     #                 heuristic_cost_estimate(starting_point=next_node.point,
#     #                                         ending_point=points.get(ending_node_osm_id))
#     #
#     #         # next_node = Node(osm_id=next_node_osm_id, point=points.get(next_node_osm_id))
#     #         # next_node.heuristic_estimated_distance, next_node.heuristic_estimated_time_on_road = \
#     #         #     heuristic_cost_estimate(starting_point=next_node.point,
#     #         #                             ending_point=points.get(ending_node_osm_id))
#     #
#     #         max_speed = edge.get('max_speed')
#     #         road_type = edge.get('road_type')
#     #         traffic_density = edge.get('traffic_density')
#     #
#     #         # Calculate the difference in values between current_node and next_node.
#     #         additional_g_score_distance, additional_g_score_time_on_road = g_score_estimate(
#     #             starting_point=current_node.point,
#     #             ending_point=next_node.point,
#     #             max_speed=max_speed,
#     #             road_type=road_type,
#     #             traffic_density=traffic_density
#     #         )
#     #
#     #         # Calculate new g_score values
#     #         new_g_score_distance = current_node.g_score_distance + additional_g_score_distance
#     #         new_g_score_time_on_road = current_node.g_score_time_on_road + additional_g_score_time_on_road
#     #
#     #         if next_node.g_score_time_on_road < new_g_score_time_on_road:
#     #             continue
#     #
#     #         next_node.g_score_distance = new_g_score_distance
#     #         next_node.g_score_time_on_road = new_g_score_time_on_road
#     #
#     #         # Calculate new f_score values
#     #         next_node.f_score_distance = new_g_score_distance + next_node.heuristic_estimated_distance
#     #         next_node.f_score_time_on_road = new_g_score_time_on_road + next_node.heuristic_estimated_time_on_road
#     #
#     #         # Add next_node to the list of previous nodes.
#     #         next_node.set_previous_nodes(previous_nodes=current_node.get_previous_nodes() + [next_node])
#     #
#     #         # next_node has been evaluated.
#     #         closed_set[next_node_osm_id] = next_node
#     #
#     #         # Add next_node to the open_set, so as to allow its edges to be evaluated.
#     #         if not open_set.exists(next_node_osm_id):
#     #             open_set.insert(new_node=next_node)
#     #
#     #         # open_set.insert(new_node=next_node)
#
#
#     # # The set of currently discovered nodes still to be evaluated. Initially, only the starting node is known.
#     # open_set = OrderedSet()
#     #
#     # # Initialize starting_node.
#     # starting_node = Node(osm_id=starting_node_osm_id, point=points.get(starting_node_osm_id))
#     #
#     # # Distance and time from starting_node equal to zero.
#     # starting_node.set_g_score(g_score_distance=0.0, g_score_time_on_road=0.0)
#     #
#     # # Distance and time to ending node is estimated heuristically.
#     # starting_node_f_score_distance, starting_node_f_score_time_on_road = heuristic_cost_estimate(
#     #     starting_point=starting_node.point, ending_point=points.get(ending_node_osm_id))
#     #
#     # starting_node.set_f_score(f_score_distance=starting_node_f_score_distance,
#     #                           f_score_time_on_road=starting_node_f_score_time_on_road)
#     #
#     # # Add the starting_node to the list of previous nodes.
#     # starting_node.add_previous_node(node=starting_node)
#     #
#     # # Add the starting_node to the closed_set, since it has already been evaluated.
#     # closed_set[starting_node_osm_id] = starting_node
#     #
#     # # Add the starting_node to the open_set, since its edges should be evaluated.
#     # open_set.insert(new_node=starting_node)
#     #
#     # # While there are more nodes, whose edges have not been evaluated.
#     # while len(open_set) > 0:
#     #
#     #     # During the first iteration of this loop, current_node will be equal to starting_node.
#     #     current_node = open_set.pop()
#     #
#     #     # ending_node has been discovered.
#     #     if current_node.osm_id == ending_node_osm_id:
#     #         paths.append(reconstruct_path(list_of_nodes=current_node.get_previous_nodes()))
#     #
#     #         if len(paths) > number_of_paths - 1:
#     #             return paths
#     #         else:
#     #             continue
#     #
#     #     # current_node does not have any edges.
#     #     if current_node.osm_id not in edges:
#     #         continue
#     #
#     #     for edge in edges.get(current_node.osm_id):
#     #         next_node_osm_id = edge.get('ending_node')
#     #
#     #         # Check whether the next_node has already been evaluated.
#     #         if next_node_osm_id in closed_set:
#     #             next_node = closed_set.get(next_node_osm_id)
#     #             # continue
#     #         else:
#     #             next_node = Node(osm_id=next_node_osm_id, point=points.get(next_node_osm_id))
#     #             next_node.heuristic_estimated_distance, next_node.heuristic_estimated_time_on_road = \
#     #                 heuristic_cost_estimate(starting_point=next_node.point,
#     #                                         ending_point=points.get(ending_node_osm_id))
#     #
#     #         # next_node = Node(osm_id=next_node_osm_id, point=points.get(next_node_osm_id))
#     #         # next_node.heuristic_estimated_distance, next_node.heuristic_estimated_time_on_road = \
#     #         #     heuristic_cost_estimate(starting_point=next_node.point,
#     #         #                             ending_point=points.get(ending_node_osm_id))
#     #
#     #         max_speed = edge.get('max_speed')
#     #         road_type = edge.get('road_type')
#     #         traffic_density = edge.get('traffic_density')
#     #
#     #         # Calculate the difference in values between current_node and next_node.
#     #         additional_g_score_distance, additional_g_score_time_on_road = g_score_estimate(
#     #             starting_point=current_node.point,
#     #             ending_point=next_node.point,
#     #             max_speed=max_speed,
#     #             road_type=road_type,
#     #             traffic_density=traffic_density
#     #         )
#     #
#     #         # Calculate new g_score values
#     #         new_g_score_distance = current_node.g_score_distance + additional_g_score_distance
#     #         new_g_score_time_on_road = current_node.g_score_time_on_road + additional_g_score_time_on_road
#     #
#     #         if next_node.g_score_time_on_road < new_g_score_time_on_road:
#     #             continue
#     #
#     #         next_node.g_score_distance = new_g_score_distance
#     #         next_node.g_score_time_on_road = new_g_score_time_on_road
#     #
#     #         # Calculate new f_score values
#     #         next_node.f_score_distance = new_g_score_distance + next_node.heuristic_estimated_distance
#     #         next_node.f_score_time_on_road = new_g_score_time_on_road + next_node.heuristic_estimated_time_on_road
#     #
#     #         # Add next_node to the list of previous nodes.
#     #         next_node.set_previous_nodes(previous_nodes=current_node.get_previous_nodes() + [next_node])
#     #
#     #         # next_node has been evaluated.
#     #         closed_set[next_node_osm_id] = next_node
#     #
#     #         # Add next_node to the open_set, so as to allow its edges to be evaluated.
#     #         if not open_set.exists(next_node_osm_id):
#     #             open_set.insert(new_node=next_node)
#     #
#     #         # open_set.insert(new_node=next_node)
#     #
#     return paths

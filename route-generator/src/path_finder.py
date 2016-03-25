"""
Copyright 2016 Ericsson

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from heapq import heappush, heappop
import point

# Maximum amount of speed for roads without a predefined value
standard_speed = 50
# Road types that can be accessed by a bus
bus_road_types = ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary',
                  'secondary_link', 'tertiary', 'tertiary_link', 'unclassified', 'residential', 'bus_road')


class AStar:
    def __init__(self):
        pass

    def find_path(self, starting_node, ending_node, edges, points):
        # The set of nodes already evaluated.
        closed_set = set()
        # The set of currently discovered nodes still to be evaluated. Initially, only the starting node is known.
        open_set = []
        heappush(open_set, starting_node)
        # For each node, came_from keeps the node which can most efficiently be reached from.
        came_from = {}
        # g_score contains the [estimated_time_on_road, estimated_distance] cost of getting from the starting_node
        # to the current_node.
        g_score = {starting_node: [0, 0]}
        # f_score contains the total cost, for each node, of getting from the starting_node to the ending_node by
        # passing by that node. That value is partly known, partly heuristic.
        f_score = {starting_node: heuristic_cost_estimate(starting_point=points.get(starting_node),
                                                          ending_point=points.get(ending_node))}

        while not (len(open_set) == 0):
            current_node = heappop(open_set)

            if current_node == ending_node:
                break

            closed_set.add(current_node)
            for edge in edges.get(current_node):
                next_node = edge.get('to_node')

                # Ignore the node which has already been evaluated.
                if next_node in closed_set:
                    continue

                max_speed = edge.get('max_speed')
                road_type = edge.get('road_type')
                traffic_rate = edge.get('traffic_rate')

                [estimated_distance, estimated_time_on_road] = g_score_estimate(
                    starting_point=points.get(current_node), ending_point=points.get(next_node), max_speed=max_speed,
                    road_type=road_type, traffic_rate=traffic_rate)

                tentative_g_score = [g_score.get(current_node)[0] + estimated_distance,
                                     g_score.get(current_node)[1] + estimated_time_on_road]

                if next_node not in open_set:
                    heappush(open_set, next_node)
                elif tentative_g_score >= g_score.get(next_node):
                    continue

                came_from[next_node] = current_node
                g_score[next_node] = tentative_g_score
                [heuristic_estimate_distance, heuristic_estimated_time_on_road] = heuristic_cost_estimate(
                    starting_point=points.get(next_node), ending_point=points.get(ending_node))
                f_score[next_node] = [g_score.get(next_node)[0] + heuristic_estimate_distance,
                                      g_score.get(next_node)[1] + heuristic_estimated_time_on_road]

        return None


def estimate_road_type_speed_decrease_factor(road_type):
    road_type_index = bus_road_types.index(road_type)
    road_type_speed_decrease_factor = 1 - (float(road_type_index) / 50)
    return road_type_speed_decrease_factor


def estimate_traffic_speed_decrease_factor(traffic_rate):
    traffic_speed_decrease_factor = 1 - float(traffic_rate)
    return traffic_speed_decrease_factor


def g_score_estimate(starting_point, ending_point, max_speed, road_type, traffic_rate):
    estimated_distance = point.distance(point_one=starting_point, point_two=ending_point)
    road_type_speed_decrease_factor = estimate_road_type_speed_decrease_factor(road_type=road_type)
    traffic_speed_decrease_factor = estimate_traffic_speed_decrease_factor(traffic_rate=traffic_rate)
    estimated_time_on_road = estimated_distance / (road_type_speed_decrease_factor * traffic_speed_decrease_factor *
                                                   (float(max_speed) * 1000 / 3600))
    return [estimated_distance, estimated_time_on_road]


def heuristic_cost_estimate(starting_point, ending_point):
    estimated_distance = point.distance(point_one=starting_point, point_two=ending_point)
    estimated_time_on_road = estimated_distance / (float(standard_speed) * 1000 / 3600)
    return [estimated_distance, estimated_time_on_road]


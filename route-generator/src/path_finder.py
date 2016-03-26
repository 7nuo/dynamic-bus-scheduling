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
import point

# Maximum amount of speed for roads without a predefined value
standard_speed = 50
# Road types that can be accessed by a bus
bus_road_types = ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary',
                  'secondary_link', 'tertiary', 'tertiary_link', 'unclassified', 'residential', 'bus_road')


class OrderedSet(object):

    def __init__(self):
        self.f_scores = []
        self.nodes = []

    def __len__(self):
        return len(self.nodes)

    def exists(self, node):
        """
        Check if a node exists in the nodes list.

        :param node:
        :return: boolean
        """
        return node in self.nodes

    def index_of_insertion(self, _estimated_time_on_road):
        """
        Retrieve the index in which a new node should be inserted, according to the corresponding f_score value.

        :param _estimated_time_on_road: f_score comparator value
        :return index: integer
        """
        index = 0

        for (_, estimated_time_on_road) in self.f_scores:
            if _estimated_time_on_road < estimated_time_on_road:
                break
            index += 1

        return index

    def insert(self, (new_estimated_distance, new_estimated_time_on_road), new_node):
        """
        Insert a new node and its corresponding f_score values.

        :param (new_estimated_distance, new_estimated_time_on_road)
        :param new_node
        """
        new_index = self.index_of_insertion(new_estimated_time_on_road)
        self.f_scores.insert(new_index, (new_estimated_distance, new_estimated_time_on_road))
        self.nodes.insert(new_index, new_node)

    def pop(self):
        """
        Remove - retrieve the node with the lowest f_score values.

        :return: (estimated_distance, estimated_time_on_road), node
        """
        f_score = self.f_scores.pop(0)
        node = self.nodes.pop(0)
        return f_score, node

    def remove(self, index):
        """
        Remove node at index, and its corresponding f_score values.

        :type index: integer
        """
        self.f_scores.pop(index)
        self.nodes.pop(index)

    # def index_of_node(self, node):
    #     index = 0
    #
    #     for _node in self.nodes:
    #         if _node == node:
    #             return index
    #         index += 1
    #
    #     return -1
    #
    #
    # def lower_f_score(self, index, new_estimated_time_on_road):
    #     returned_value = False
    #     estimated_time_on_road = self.f_scores[index][1]
    #
    #     if new_estimated_time_on_road < estimated_time_on_road:
    #         returned_value = True
    #
    #     return returned_value


def find_path(starting_node, ending_node, edges, points):
        # The set of nodes already evaluated.
        closed_set = set()
        # The set of currently discovered nodes still to be evaluated. Initially, only the starting node is known.
        # open_set = []
        open_set = OrderedSet()
        # For each node, came_from keeps the node which can most efficiently be reached from.
        came_from = {}
        # g_score contains the [estimated_time_on_road, estimated_distance] cost of getting from the starting_node
        # to the current_node.
        g_score = {starting_node: [0, 0]}
        # f_score contains the total cost, for each node, of getting from the starting_node to the ending_node by
        # passing by that node. That value is partially known, partially heuristic.
        f_score = {starting_node: heuristic_cost_estimate(starting_point=points.get(starting_node).get('point'),
                                                          ending_point=points.get(ending_node).get('point'))}
        # heappush(open_set, (f_score, starting_node))
        open_set.insert(f_score.get(starting_node), starting_node)

        while len(open_set) > 0:
            # current_node = heappop(open_set)[1]
            current_node = open_set.pop()[1]
            print current_node

            if current_node == ending_node:
                return reconstruct_path(came_from=came_from, current_node=ending_node)

            closed_set.add(current_node)

            if current_node not in edges:
                continue

            for edge in edges.get(current_node):
                next_node = edge.get('to_node')

                # Ignore the node which has already been evaluated.
                if next_node in closed_set:
                    continue

                max_speed = edge.get('max_speed')
                road_type = edge.get('road_type')
                traffic_rate = edge.get('traffic_rate')

                estimated_distance, estimated_time_on_road = g_score_estimate(
                    starting_point=points.get(current_node).get('point'), ending_point=points.get(next_node).get('point'), max_speed=max_speed,
                    road_type=road_type, traffic_rate=traffic_rate)

                tentative_g_score = (g_score.get(current_node)[0] + estimated_distance,
                                     g_score.get(current_node)[1] + estimated_time_on_road)

                # if next_node not in open_set:
                #     heappush(open_set, next_node)
                # elif tentative_g_score >= g_score.get(next_node):
                #     continue

                if next_node in g_score and tentative_g_score[1] >= g_score.get(next_node)[1]:
                    continue

                came_from[next_node] = current_node
                g_score[next_node] = tentative_g_score
                heuristic_estimate_distance, heuristic_estimated_time_on_road = heuristic_cost_estimate(
                    starting_point=points.get(next_node).get('point'), ending_point=points.get(ending_node).get('point'))
                f_score[next_node] = (g_score.get(next_node)[0] + heuristic_estimate_distance,
                                      g_score.get(next_node)[1] + heuristic_estimated_time_on_road)

                if not open_set.exists(next_node):
                    open_set.insert(f_score.get(next_node), next_node)

        return None


def reconstruct_path(came_from, current_node):
    total_path = [current_node]

    while current_node in came_from:
        current_node = came_from.get(current_node)
        total_path = [current_node] + total_path

    return total_path


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
    return estimated_distance, estimated_time_on_road


def heuristic_cost_estimate(starting_point, ending_point):
    estimated_distance = point.distance(point_one=starting_point, point_two=ending_point)
    estimated_time_on_road = estimated_distance / (float(standard_speed) * 1000 / 3600)
    return estimated_distance, estimated_time_on_road


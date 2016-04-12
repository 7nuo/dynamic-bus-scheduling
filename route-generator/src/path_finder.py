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
from point import distance

# Maximum amount of speed for roads without a predefined value
standard_speed = 50
# Road types that can be accessed by a bus
bus_road_types = ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary',
                  'secondary_link', 'tertiary', 'tertiary_link', 'unclassified', 'residential', 'bus_road')


class Node(object):
    def __init__(self, osm_id):
        self.osm_id = osm_id
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

        :type node_osm_id: integer
        :return: boolean
        """
        returned_value = False

        for node in self.nodes:
            if node.osm_id == node_osm_id:
                returned_value = True
                break

        returned_value

    def index_of_insertion(self, new_node):
        """
        Retrieve the index in which a new node should be inserted, according to the corresponding f_score value.

        :param new_node: Node
        :return index: integer
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

        :type index: integer
        """
        self.nodes.pop(index)


def find_path(starting_node_osm_id, ending_node_osm_id, edges, points):
    """
    Implement the A* search algorithm in order to find the less time-consuming path
    between the starting and the ending node.

    :param starting_node_osm_id: osm_id: integer
    :param ending_node_osm_id: osm_id: integer
    :param edges: {starting_node_osm_id -> [{ending_node_osm_id, max_speed, road_type, way_id, traffic_density}]
    :param points: {osm_id -> point}
    :return: {'total_distance', 'total_time', 'nodes', 'points', 'total_distances',
              'total_times', 'partial_distances', 'partial_times'}
    """
    # A dictionary with the nodes that have already been evaluated: {node_osm_id -> node}
    closed_set = {}

    # The set of currently discovered nodes still to be evaluated. Initially, only the starting node is known.
    open_set = OrderedSet()

    # Initialize starting_node.
    starting_node = Node(osm_id=starting_node_osm_id)

    # Distance and time from starting_node equal to zero.
    starting_node.set_g_score(g_score_distance=0.0, g_score_time_on_road=0.0)

    # Distance and time to ending node is estimated heuristically.
    starting_node_f_score_distance, starting_node_f_score_time_on_road = heuristic_cost_estimate(
        starting_point=points.get(starting_node_osm_id), ending_point=points.get(ending_node_osm_id))

    starting_node.set_f_score(f_score_distance=starting_node_f_score_distance,
                              f_score_time_on_road=starting_node_f_score_time_on_road)

    # Add the starting_node to the list of previous nodes.
    starting_node.add_previous_node(node=starting_node)

    # Add the starting_node to the closed_set, since it has already been evaluated.
    closed_set[starting_node_osm_id] = starting_node

    # Add the starting_node to the open_set, since its edges should be evaluated.
    open_set.insert(new_node=starting_node)

    # While there are more nodes, whose edges have not been evaluated.
    while len(open_set) > 0:

        # During the first iteration of this loop, current_node will be equal to starting_node.
        current_node = open_set.pop()

        # ending_node has been discovered.
        if current_node.osm_id == ending_node_osm_id:
            return current_node.get_previous_nodes()

        # current_node does not have any edges.
        if current_node.osm_id not in edges:
            continue

        for edge in edges.get(current_node.osm_id):
            next_node_osm_id = edge.get('ending_node')

            # Check whether the next_node has already been evaluated.
            if next_node_osm_id in closed_set:
                next_node = closed_set.get(next_node_osm_id)
                # continue
            else:
                next_node = Node(osm_id=next_node_osm_id)
                next_node.heuristic_estimated_distance, next_node.heuristic_estimated_time_on_road = \
                    heuristic_cost_estimate(starting_point=points.get(next_node_osm_id),
                                            ending_point=points.get(ending_node_osm_id))

            max_speed = edge.get('max_speed')
            road_type = edge.get('road_type')
            traffic_density = edge.get('traffic_density')

            # Calculate the difference in values between current_node and next_node.
            additional_g_score_distance, additional_g_score_time_on_road = g_score_estimate(
                starting_point=points.get(current_node.osm_id),
                ending_point=points.get(next_node_osm_id),
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
            next_node.set_previous_nodes(previous_nodes=current_node.get_previous_nodes() + [next_node_osm_id])

            # next_node has been evaluated.
            closed_set[next_node_osm_id] = next_node

            # Add next_node to the open_set, so as to allow its edges to be evaluated.
            if not open_set.exists(next_node_osm_id):
                open_set.insert(new_node=next_node)

    return None


def find_multiple_paths(starting_node, ending_node, edges, points):
    """
    Implement the A* search algorithm in order to find the less time-consuming path
    between the starting and the ending node.

    :param starting_node: osm_id: integer
    :param ending_node: osm_id: integer
    :param edges: {starting_node -> [{ending_node, max_speed, road_type, way_id, traffic_density}]
    :param points: {osm_id -> point}
    :return: {'total_distance', 'total_time', 'nodes', 'points', 'total_distances',
              'total_times', 'partial_distances', 'partial_times'}
    """
    # The set of nodes already evaluated.
    # closed_set = set()
    # The set of currently discovered nodes still to be evaluated. Initially, only the starting node is known.
    # open_set = []
    open_set = OrderedSet()
    # For each node, came_from keeps the node which can most efficiently be reached from.
    came_from = {}
    # g_score contains the [f_score_time_on_road, f_score_distance] cost of getting from the starting_node
    # to the current_node.
    g_score = {starting_node: (0, 0)}
    # f_score contains the total cost, for each node, of getting from the starting_node to the ending_node by
    # passing by that node. That value is partially known, partially heuristic.
    f_score = {starting_node: heuristic_cost_estimate(starting_point=points.get(starting_node),
                                                      ending_point=points.get(ending_node))}
    open_set.insert(f_score.get(starting_node), starting_node)

    final_paths = []

    # While there are more nodes to be investigated.
    while len(open_set) > 0:
        current_node = open_set.pop()[1]

        print current_node

        if current_node == ending_node:
            final_paths.append(reconstruct_path(ending_node=ending_node, came_from=came_from,
                                                g_score=g_score, points=points))
            # came_from = {}
        else:
            # closed_set.add(current_node)

            if current_node not in edges:
                continue

            for edge in edges.get(current_node):
                next_node = edge.get('ending_node')

                # Ignore nodes which have already been evaluated.
                # if next_node in closed_set:
                #     continue

                max_speed = edge.get('max_speed')
                road_type = edge.get('road_type')
                traffic_density = edge.get('traffic_density')

                estimated_distance, estimated_time_on_road = g_score_estimate(
                    starting_point=points.get(current_node),
                    ending_point=points.get(next_node),
                    max_speed=max_speed,
                    road_type=road_type,
                    traffic_density=traffic_density
                )

                tentative_g_score = (g_score.get(current_node)[0] + estimated_distance,
                                     g_score.get(current_node)[1] + estimated_time_on_road)

                # if next_node in g_score and tentative_g_score[1] >= g_score.get(next_node)[1]:
                #     continue

                came_from[next_node] = current_node
                g_score[next_node] = tentative_g_score
                heuristic_estimated_distance, heuristic_estimated_time_on_road = heuristic_cost_estimate(
                    starting_point=points.get(next_node),
                    ending_point=points.get(ending_node)
                )
                f_score[next_node] = (g_score.get(next_node)[0] + heuristic_estimated_distance,
                                      g_score.get(next_node)[1] + heuristic_estimated_time_on_road)

                # if not open_set.exists(next_node):
                open_set.insert(f_score.get(next_node), next_node)

                print open_set.nodes

    return final_paths


def reconstruct_path(ending_node, came_from, g_score, points):
    """
    Connect the nodes of the optimal path.

    :param ending_node: osm_id
    :param came_from: Dictionary containing references to previous nodes: {osm_id -> osm_id}
    :param g_score: {osm_id -> (f_score_distance, f_score_time_on_road)}
    :param points: {osm_id -> point}
    :return: {'total_distance', 'total_time', 'nodes', 'points', 'total_distances',
              'total_times', 'partial_distances', 'partial_times'}
    """
    total_path = [(ending_node, points.get(ending_node), g_score.get(ending_node))]
    current_node = ending_node

    while current_node in came_from:
        current_node = came_from.get(current_node)
        total_path = [(current_node, points.get(current_node), g_score.get(current_node))] + total_path

    # total_path: [(node, point, (f_score_distance, f_score_time_on_road))]

    nodes = []
    points = []
    total_distances = []
    total_times = []
    partial_distances = []
    partial_times = []
    partial_distance = 0
    partial_time = 0
    previous_distance = None
    previous_time = None

    for node, point, (estimated_distance, estimated_time_on_road) in total_path:
        nodes.append(node)
        points.append(point)
        total_distances.append(estimated_distance)
        total_times.append(estimated_time_on_road)

        if previous_distance is not None:
            partial_distance = estimated_distance - previous_distance

        partial_distances.append(partial_distance)

        if previous_time is not None:
            partial_time = estimated_time_on_road - previous_time

        partial_times.append(partial_time)

        previous_distance = estimated_distance
        previous_time = estimated_time_on_road

    total_distance = previous_distance
    total_time = previous_time

    final_path = {'total_distance': total_distance, 'total_time': total_time, 'nodes': nodes, 'points': points,
                  'total_distances': total_distances, 'total_times': total_times,
                  'partial_distances': partial_distances, 'partial_times': partial_times}

    return final_path


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


def g_score_estimate(starting_point, ending_point, max_speed, road_type, traffic_density):
    """
    Estimate the cost of getting from the starting point to the ending point.

    :param starting_point: Point
    :param ending_point: Point
    :param max_speed: float
    :param road_type: One of the road types that can be accessed by a bus (string).
    :param traffic_density: float value between 0 and 1.
    :return: (f_score_distance in meters, f_score_time_on_road in seconds)
    """
    estimated_distance = distance(point_one=starting_point, point_two=ending_point)
    road_type_speed_decrease_factor = estimate_road_type_speed_decrease_factor(road_type=road_type)
    traffic_speed_decrease_factor = estimate_traffic_speed_decrease_factor(traffic_density=traffic_density)
    estimated_time_on_road = estimated_distance / (road_type_speed_decrease_factor * traffic_speed_decrease_factor *
                                                   (float(max_speed) * 1000 / 3600))
    return estimated_distance, estimated_time_on_road


def heuristic_cost_estimate(starting_point, ending_point):
    """
    Make a rough estimation regarding the cost of getting from the starting point to the ending point.

    :param starting_point: Point
    :param ending_point:  Point
    :return: (f_score_distance in meters, f_score_time_on_road in seconds)
    """
    estimated_distance = distance(point_one=starting_point, point_two=ending_point)
    estimated_time_on_road = estimated_distance / (float(standard_speed) * 1000 / 3600)
    return estimated_distance, estimated_time_on_road

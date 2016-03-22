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
import numpy as np
import point

# Maximum amount of speed for roads without a predefined value
standard_speed = 50
# Road types that can be accessed by a bus
bus_road_types = ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary',
                  'secondary_link', 'tertiary', 'tertiary_link', 'unclassified', 'residential', 'bus_road')


class AStar:
    def __init__(self):
        pass

    # def find_path(self, edges, start, goal):
    #     """
    #     Finds a path between start and goal using A*. The search is done in the
    #     graph self.edges.
    #     """
    #     open_set = []
    #     heappush(open_set, (0, start))
    #     path = {}
    #     cost = {}
    #     path[start] = 0
    #     cost[start] = np.asarray([0, 0])
    #
    #     # A value that a real path should not have.
    #     cost[goal] = np.asarray([float('Inf'), float('Inf')])
    #
    #     if start == goal:
    #         cost[goal] = np.asarray([0, 0])
    #         open_set = []
    #
    #     # As long as there are paths to be explored
    #     while not (len(open_set) == 0):
    #         current = heappop(open_set)[1]
    #
    #         # We found the goal, stop searching, we are done.
    #         if current == goal:
    #             break
    #
    #         # For all nodes connected to the one we are looking at for the
    #         # moment.
    #         for nextNode, speed, roadInt, _ in edges[current]:
    #             # How fast you can go on a road matters on the type of the road
    #             # It can be seen as a penalty for "smaller" roads.
    #             speedDecrease = (1 - (float(roadInt) / 50))
    #             #fromCoordinate = nodes[current]
    #             #toCoordinate = nodes[nextNode]
    #
    #             roadLength = coordinate.measure(current, nextNode)
    #
    #             timeOnRoad = (roadLength /
    #                           (speedDecrease * (float(speed) * 1000 / 3600)))
    #
    #             newCost = cost[current] + [timeOnRoad, roadLength]
    #
    #             if nextNode not in cost or (newCost[0] < cost[nextNode][0]):
    #                 cost[nextNode] = newCost
    #
    #                 weight = (newCost[0] + (roadInt ** 1) +
    #                           (heuristic(nextNode, goal) /
    #                            (float(self.standardSpeed) * 1000 / 3600)))
    #
    #                 heappush(open_set, (weight, nextNode))
    #                 path[nextNode] = current
    #
    #     # Is there a shortest path
    #     if cost[goal][0] is float('Inf'):
    #         shortestpath = []
    #     else:
    #         shortestpath = reconstruct_path(path, start, goal)
    #
    #     return shortestpath, cost
    #

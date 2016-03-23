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
from point import center


class Address(object):
    """
    An address object is used to store street address. A address has a street
    name, points of street, and possibly numbers (usually marking a
    house or entrance).

    A building can be associated to several numbers, e.g 10A, 10B, and 10C. If
    the exact location of the entrance is unknown, all numbers can have a
    coordinate of the building.
    """

    def __init__(self, name, node_id, point):
        """
        :param name: The name of the address
        :type name: string
        :type node_id: integer
        :type point: Point
        """
        self.name = name
        self.nodes = [(node_id, point)]

    def add_node(self, node_id, point):
        """
        Add a node to the nodes list.

        :type node_id: integer
        :type point: Point
        """
        if (node_id, point) not in self.nodes:
            self.nodes.append((node_id, point))

    def nodes_to_string(self):
        result = '['
        for node_id, point in self.nodes:
            result += '(node_id:' + str(node_id) + ', point: ' + point.coordinates_to_string() + ')'

        result += ']'
        return result

    def get_center(self):
        return center([point for _, point in self.nodes])

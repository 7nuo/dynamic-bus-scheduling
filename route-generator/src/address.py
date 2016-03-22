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
    name, coordinates of street, and possibly numbers (usually marking a
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

        # numbers = []
        #
        # if number is not None:
        #     for num in address_range(number):
        #         numbers.append(num)
        #
        # self.nodes[node_id] = {'type': node_type, 'point': point, 'street': street, 'numbers': numbers}

        # def add_point(self, point):
        #     """
        #     Add a point to the list of coordinates which are related to this address.
        #
        #     :type point: Point
        #     """
        #     self.coordinates.append(point)
        #
        # def add_number(self, number, point):
        #     """
        #     Add a number and its corresponding coordinates to the numbers dictionary.
        #
        #     :type number: string
        #     :type point: Point
        #     """
        #     for num in address_range(number):
        #         self.numbers[num] = point
        #
        # def __str__(self):
        #     return "%s : %s" % (self.numbers, self.coordinates)
        #
        # def __repr__(self):
        #     return "%s : %s" % (self.numbers, self.coordinates)

# def make_address(name):
#     address = Address(name)
#     return address
#
#
# def address_range(number):
#     """
#     Turn address number format into a range. E.g. '1A-1C' to '1A','1B','1C'.
#
#     :param number: string
#     :return: generator
#     """
#     regular_expression = re.compile(
#         '''
#         ((?P<starting_address_number>(\d+))
#         (?P<starting_address_letter> ([a-zA-Z]*))
#         \s*-\s*
#         (?P<ending_address_number>(\d+))
#         (?P<ending_address_letter>([a-zA-Z]*)))
#         ''',
#         re.VERBOSE
#     )
#     match = regular_expression.search(number)
#
#     if match:
#         starting_number = match.groupdict()['starting_address_number']
#         starting_letter = match.groupdict()['starting_address_letter']
#         ending_number = match.groupdict()['ending_address_number']
#         ending_letter = match.groupdict()['ending_address_letter']
#
#         if starting_letter and ending_letter:
#             for c in xrange(ord(starting_letter), ord(ending_letter) + 1):
#                 yield '' + starting_number + chr(c)
#         elif starting_number and ending_number:
#             for c in xrange(int(starting_number), int(ending_number) + 1):
#                 yield c
#         else:
#             yield '' + starting_number + starting_letter
#     else:
#         numbers = number.split(',')
#
#         if len(numbers) > 1:
#             for num in numbers:
#                 yield num.strip()
#         else:
#             yield number

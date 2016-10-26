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
from src.geospatial_data.point import center

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


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

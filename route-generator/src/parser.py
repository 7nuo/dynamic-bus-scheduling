"""
Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from imposm.parser import OSMParser
# from bus_stop import BusStop
from point import Point
from address import Address
# from multiprocessing import Process
import os
import re

# import time
# import signal

# Maximum amount of speed for roads without a predefined value
standard_speed = 50
# Road types that can be accessed by a bus
bus_road_types = ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary',
                  'secondary_link', 'tertiary', 'tertiary_link', 'unclassified', 'residential', 'bus_road')


class Parser(object):
    ways_filter = None
    nodes_filter = None
    relations_filter = None

    def __init__(self, osm_filename):
        """
        :param osm_filename: Directory of the input OSM file
        :type osm_filename: string
        """
        self.osm_filename = osm_filename
        self.nodes = {}
        self.coordinates = {}
        self.ways = {}
        self.relations = []
        self.bus_stops = {}
        self.edges = {}
        self.address_book = {}

    def get_point(self, osm_id):
        """
        Retrieve the pair of coordinates which correspond to a specific osm_id.
        The osm_id could represent a node, a bus stop, or a pair of coordinates.

        :type osm_id: integer
        :return: Point
        """
        point = None

        if osm_id in self.nodes:
            point = self.nodes.get(osm_id)['point']
        elif osm_id in self.bus_stops:
            point = self.bus_stops.get(osm_id)['point']
        elif osm_id in self.coordinates:
            point = self.coordinates.get(osm_id)['point']
        else:
            pass

        return point

    def parse_nodes(self, nodes):
        """
        Parse the list of nodes and populate the corresponding dictionary.
        Parse the list of bus stops, which are included in the nodes.
        Parse the list of addresses, where the nodes correspond to.

        :type nodes: [()]
        """
        for node in nodes:
            osm_id, tags, (longitude, latitude) = node
            point = Point(longitude=longitude, latitude=latitude)
            self.add_node(osm_id=osm_id, tags=tags, point=point)

            if all(term in tags for term in ['bus', 'name']):
                self.add_bus_stop(osm_id=osm_id, name=tags.get('name'), point=point)

            self.parse_address(osm_id=osm_id, tags=tags, point=point)

    def add_node(self, osm_id, tags, point):
        """
        Add node to the nodes dictionary and node name to the address_book dictionary.

        :type osm_id: integer
        :type tags: {}
        :type point: Point
        """
        self.nodes[osm_id] = {'tags': tags, 'point': point}

    def add_bus_stop(self, osm_id, name, point):
        """
        Add bus_stop to the bus_stops dictionary.

        :type osm_id: integer
        :type name: string
        :type point: Point
        """
        self.bus_stops[osm_id] = {'name': name, 'point': point}

    def parse_address(self, osm_id, tags, point):
        """
        Parse the name, the street, and the house numbers of an address, and add them to the address_book dictionary
        along with their corresponding osm_id and coordinates.

        :type osm_id: integer
        :param tags: {}
        :param point: Point
        """
        name = tags.get('name', '')
        street = tags.get('addr:street', '')
        house_number = tags.get('addr:housenumber', '')

        if name != '':
            self.add_address(name=name, node_id=osm_id, point=point)

        if street != '' and house_number != '':
            for num in address_range(house_number):
                address = street + ' ' + str(num)
                self.add_address(name=address, node_id=osm_id, point=point)

    def add_address(self, name, node_id, point):
        """
        Add an address to the address_book dictionary.

        :type name: string
        :type node_id: integer
        :type point: Point
        """
        # name = name.lower()

        if name not in self.address_book:
            self.address_book[name] = Address(name, node_id, point)
        else:
            self.address_book[name].add_node(node_id=node_id, point=point)

    def parse_coordinates(self, coordinates):
        """
        Parse the list of coordinates and populate the corresponding dictionary.

        :type coordinates: [()]
        """
        for osm_id, longitude, latitude in coordinates:
            point = Point(longitude=longitude, latitude=latitude)
            self.add_coordinates(osm_id=osm_id, point=point)

    def add_coordinates(self, osm_id, point):
        """
        Add geographical point to the coordinates dictionary.

        :type osm_id: integer
        :type point: Point
        """
        self.coordinates[osm_id] = {'point': point}

    def parse_ways(self, ways):
        """
        Parse the list of ways and populate the corresponding dictionary
        with the ones that can be accessed by bus vehicles.

        :type ways: [()]
        """
        for way in ways:
            osm_id, tags, references = way

            if tags.get('motorcar') != 'no' and tags.get('highway') in bus_road_types:
                self.add_way(osm_id=osm_id, tags=tags, references=references)
                self.parse_edges(osm_id=osm_id, tags=tags, references=references)

            name = tags.get('name', '')
            if name != '':
                for reference in references:
                    self.add_address(name=name, node_id=reference, point=self.get_point(osm_id=reference))

    def add_way(self, osm_id, tags, references):
        """
        Add way to the ways dictionary.

        :type osm_id: integer
        :type tags: {}
        :type references: [integer]
        """
        self.ways[osm_id] = {'tags': tags, 'references': references}

    def parse_edges(self, osm_id, tags, references):
        oneway = tags.get('oneway', '') in ('yes', 'true', '1')
        max_speed = tags.get('maxspeed', standard_speed)

        for reference_index in range(len(references) - 1):
            self.add_edge(from_node=references[reference_index], to_node=references[reference_index + 1],
                          max_speed=max_speed, way_id=osm_id)

            if not oneway:
                self.add_edge(from_node=references[reference_index + 1], to_node=references[reference_index],
                              max_speed=max_speed, way_id=osm_id)

    def add_edge(self, from_node, to_node, max_speed, way_id):
        """
        Add edge to the edges dictionary.

        :type from_node: integer
        :type to_node: integer
        :type max_speed: integer
        :type way_id: integer
        """
        if from_node in self.edges:
            self.edges[from_node].append({'to_node': to_node, 'max_speed': max_speed, 'way_id': way_id})
        else:
            self.edges[from_node] = [{'to_node': to_node, 'max_speed': max_speed, 'way_id': way_id}]

    def parse_relations(self, relations):
        self.relations.extend(relations)

    def validate_references(self):
        nodes = 0
        bus_stops = 0
        coordinates = 0
        none = 0
        for osm_id, values in self.ways.iteritems():
            references = values.get('references')
            for reference in references:
                if str(reference) in self.nodes:
                    nodes += 1
                    if str(reference) in self.bus_stops:
                        bus_stops += 1
                elif str(reference) in self.coordinates:
                    coordinates += 1
                else:
                    none += 1

        print 'Nodes:', nodes
        print 'Bus_Stops:', bus_stops
        print 'Coordinates:', coordinates
        print 'None:', none

    def validate_coordinates(self):
        nodes = 0
        none = 0
        for osm_id in self.coordinates:
            if str(osm_id) in self.nodes:
                nodes += 1
            else:
                none += 1

        print 'Nodes:', nodes
        print 'None:', none

    def print_nodes(self):
        for osm_id, values in self.nodes.iteritems():
            print 'Node: ' + str(osm_id) + ', Tags: ' + str(values.get('tags')) + \
                  ', Point: ' + values.get('point').coordinates_to_string()

    def print_bus_stops(self):
        for osm_id, values in self.bus_stops.iteritems():
            print 'Bus_Stop:', osm_id + ', Name:', values.get('name') + \
                                                   ', Point:', values.get('point').coordinates_to_string()

    def print_coordinates(self):
        for osm_id, values in self.coordinates.iteritems():
            print 'Coordinates:', osm_id + ', Point:', values.get('point').coordinates_to_string()

    def print_ways(self):
        for osm_id, values in self.ways.iteritems():
            print 'Way:', osm_id + ', Tags:', str(values.get('tags')) + ', References:', values.get('references')

    def print_totals(self):
        print '-- Printing Totals --'
        print 'Number of Nodes: ', len(self.nodes)
        print 'Number of Coordinates: ', len(self.coordinates)
        print 'Number of Ways: ', len(self.ways)
        print 'Number of Relations: ', len(self.relations)

    def parse(self):
        parser = OSMParser(
            concurrency=2,
            nodes_callback=self.parse_nodes,
            coords_callback=self.parse_coordinates,
            ways_callback=self.parse_ways,
            # relations_ callback=self.parse_relations,
            # nodes_tag_filter=self.nodes_filter,
            # ways_tag_filter=self.ways_filter,
            # relations_tag_filter=self.relations_filter
        )
        parser.parse(self.osm_filename)

        # self.print_nodes()
        # self.print_bus_stops()
        # self.print_coordinates()
        # self.print_ways()

        # self.print_totals()

        # self.validate_references()
        # self.validate_coordinates()

        # self.parse_edges()
        # for key, value in self.edges.iteritems():
        #     print key, value

        # for relation in self.relations:
        #     print 'Relation: ', relation


def address_range(number):
    """
    Turn address number format into a range. E.g. '1A-1C' to '1A','1B','1C'.

    :param number: string
    :return: generator
    """
    regular_expression = re.compile(
        '''
        ((?P<starting_address_number>(\d+))
        (?P<starting_address_letter> ([a-zA-Z]*))
        \s*-\s*
        (?P<ending_address_number>(\d+))
        (?P<ending_address_letter>([a-zA-Z]*)))
        ''',
        re.VERBOSE
    )
    match = regular_expression.search(number)

    if match:
        starting_number = match.groupdict()['starting_address_number']
        starting_letter = match.groupdict()['starting_address_letter']
        ending_number = match.groupdict()['ending_address_number']
        ending_letter = match.groupdict()['ending_address_letter']

        if starting_letter and ending_letter:
            for c in xrange(ord(starting_letter), ord(ending_letter) + 1):
                yield '' + starting_number + chr(c)
        elif starting_number and ending_number:
            for c in xrange(int(starting_number), int(ending_number) + 1):
                yield c
        else:
            yield '' + starting_number + starting_letter
    else:
        numbers = number.split(',')

        if len(numbers) > 1:
            for num in numbers:
                yield num.strip()
        else:
            yield number


class Router(object):

    def __init__(self, osm_filename):
        self.parser = Parser(osm_filename=osm_filename)
        self.parser.parse()
        self.parser.print_nodes()


# def printer():
#     # start_time = time.time()
#     pattern = ''
#
#     while (True):
#         # elapsed_time = time.time() - start_time
#         pattern += '='
#         print pattern,
#         time.sleep(1)


if __name__ == '__main__':
    osm_filename = os.path.join(os.path.dirname(__file__), '../resources/map.osm')
    Router(osm_filename=osm_filename)

    # p = Process(target=printer, args=())
    # p.start()
    # time.sleep(10)
    # p.terminate()
    # p.join()

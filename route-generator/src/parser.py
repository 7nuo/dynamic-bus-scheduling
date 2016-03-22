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
from imposm.parser import OSMParser

from path_finder import standard_speed, bus_road_types

# from bus_stop import BusStop
from point import *

# import point
from address import Address
# from multiprocessing import Process
import os
import re

# import time
# import signal


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

    def add_address(self, name, node_id, point):
        """
        Add an address to the address_book dictionary.

        :type name: string
        :type node_id: integer
        :type point: Point
        """
        if name is None or name == '' or node_id is None or point is None:
            return

        if name not in self.address_book:
            self.address_book[name] = Address(name, node_id, point)
        else:
            self.address_book[name].add_node(node_id=node_id, point=point)

    def add_bus_stop(self, osm_id, name, point):
        """
        Add bus_stop to the bus_stops dictionary.

        :type osm_id: integer
        :type name: string
        :type point: Point
        """
        self.bus_stops[osm_id] = {'name': name, 'point': point}

    def add_coordinates(self, osm_id, point):
        """
        Add geographical point to the coordinates dictionary.

        :type osm_id: integer
        :type point: Point
        """
        self.coordinates[osm_id] = {'point': point}

    def add_edge(self, from_node, to_node, max_speed, way_id):
        """
        Add edge to the edges dictionary.

        :param from_node: osm_id
        :type from_node: integer
        :param to_node: osm_id
        :type to_node: integer
        :type max_speed: integer
        :type way_id: integer
        """
        if from_node in self.edges:
            self.edges[from_node].append({'to_node': to_node, 'max_speed': max_speed, 'way_id': way_id})
        else:
            self.edges[from_node] = [{'to_node': to_node, 'max_speed': max_speed, 'way_id': way_id}]

    def add_node(self, osm_id, tags, point):
        """
        Add node to the nodes dictionary, and node name to the address_book dictionary.

        :type osm_id: integer
        :type tags: {}
        :type point: Point
        """
        self.nodes[osm_id] = {'tags': tags, 'point': point}

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

    def check_coordinates_list(self, coordinates_list):
        """

        :param coordinates_list: [(longitude, latitude)]
        :return:
        """
        for index, coordinates in enumerate(coordinates_list):

            if not self.parser.coordinates_in_edges(longitude=coordinates[0], latitude=coordinates[1]):
                coordinates_list[index] = self.closest_coordinates_in_edges(coordinates)

        return coordinates_list

    def closest_coordinates_in_edges(self, coordinates):
        """

        :param coordinates: (longitude, latitude)
        :type coordinates: (float, float)
        :return:
        """
        closest_coordinates = closest_point_in_list(Point(longitude=coordinates[0], latitude=coordinates[1]),
                                                    self.parser.get_points_of_edges())

        return closest_coordinates

    def coordinates_in_edges(self, longitude, latitude):
        """
        Check if a pair of coordinates exist in the edges dictionary.

        :type longitude: float
        :type latitude: float
        :return: boolean
        """
        return_value = False

        for osm_id in self.edges:
            point = self.get_point(osm_id=osm_id)

            if (point is not None) and (point.equal_to_coordinates(longitude=longitude, latitude=latitude)):
                return_value = True
                break

        return return_value

    def get_bus_stop_closest_to_coordinates(self, longitude, latitude):
        """
        Finds the closest bus stop to the position of (lon, lat).

        :param lon: longitude
        :param lat: latitude
        :return: BusStop object
        """
        provided_point = Point(longitude=longitude, latitude=latitude)
        minimum_distance = pow(10, 12)
        bus_stop = None

        for osm_id, values in self.bus_stops.iteritems():
            current_distance = distance(provided_point, values.get('point'))

            if current_distance == 0:
                values['osm_id'] = osm_id
                bus_stop = values
                break
            elif current_distance < minimum_distance:
                minimum_distance = current_distance
                values['osm_id'] = osm_id
                bus_stop = values
            else:
                pass

        return bus_stop

    def get_bus_stop_from_coordinates(self, longitude, latitude):
        """

        :type longitude: float
        :type latitude: float
        :return: string
        """
        bus_stop = None

        for osm_id, values in self.bus_stops.iteritems():
            if values.get('point').equal_to_coordinates(longitude=longitude, latitude=latitude):
                values['osm_id'] = osm_id
                bus_stop = values
                break

        return bus_stop

    def get_bus_stop_from_name(self, name):
        name = name.lower()
        bus_stop = None

        for osm_id, values in self.bus_stops.iteritems():
            if values.get('name').lower() == name:
                values['osm_id'] = osm_id
                bus_stop = values
                break

        return bus_stop

    def get_bus_stops_within_distance(self, longitude, latitude, maximum_distance):
        provided_point = Point(longitude=longitude, latitude=latitude)
        bus_stops = []

        for osm_id, values in self.bus_stops.iteritems():
            current_distance = distance(provided_point, values.get('point'))

            if current_distance <= maximum_distance:
                values['osm_id'] = osm_id
                bus_stops.append(values)

        return bus_stops

    def get_center_point_from_address_name(self, address_name):
        retrieved_center = None

        if address_name in self.address_book:
            retrieved_center = self.address_book[address_name].get_center()

        return retrieved_center

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

    def get_points_of_edges(self):
        [self.get_point(osm_id=osm_id) for osm_id in self.edges]

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

    def parse_coordinates(self, coordinates):
        """
        Parse the list of coordinates and populate the corresponding dictionary.

        :type coordinates: [()]
        """
        for osm_id, longitude, latitude in coordinates:
            point = Point(longitude=longitude, latitude=latitude)
            self.add_coordinates(osm_id=osm_id, point=point)

    def parse_nodes(self, nodes):
        """
        Parse the list of nodes and populate the corresponding dictionary.
        Parse the list of bus stops, which are included in the nodes, and populate the corresponding dictionary.
        Parse the list of addresses, where the nodes correspond to, and populate the corresponding dictionary.

        :type nodes: [()]
        """
        for node in nodes:
            osm_id, tags, (longitude, latitude) = node
            point = Point(longitude=longitude, latitude=latitude)
            self.add_node(osm_id=osm_id, tags=tags, point=point)

            if all(term in tags for term in ['bus', 'name']):
                self.add_bus_stop(osm_id=osm_id, name=tags.get('name'), point=point)

            self.parse_address(osm_id=osm_id, tags=tags, point=point)

    def parse_relations(self, relations):
        self.relations.extend(relations)

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

    def print_address_book(self):
        print '-- Printing Address Book --'
        for name, values in self.address_book.iteritems():
            print 'Address: ' + name + ', Nodes:' + values.nodes_to_string()
            # print 'Address: ' + name + ', Center:' + values.get_center().coordinates_to_string()

    def print_bus_stops(self):
        print '-- Printing Bus Stops --'
        for osm_id, values in self.bus_stops.iteritems():
            print 'Bus_Stop: ' + str(osm_id) + ', Name: ' + str(values.get('name').encode('utf-8')) + \
                  ', Point: ' + values.get('point').coordinates_to_string()

    def print_coordinates(self):
        print '-- Printing Coordinates --'
        for osm_id, values in self.coordinates.iteritems():
            print 'Coordinates: ' + str(osm_id) + ', Point: ' + values.get('point').coordinates_to_string()

    def print_edges(self):
        print '-- Printing Edges --'
        for osm_id, list_of_values in self.edges.iteritems():
            for values in list_of_values:
                print 'From_Node: ' + str(osm_id) + ', To_Node: ' + str(values.get('to_node')) + \
                      ', Max_Speed: ' + str(values.get('max_speed')) + ', Way: ' + str(values.get('way_id'))

    def print_nodes(self):
        print '-- Printing Nodes --'
        for osm_id, values in self.nodes.iteritems():
            print 'Node: ' + str(osm_id) + ', Tags: ' + str(values.get('tags')) + \
                  ', Point: ' + values.get('point').coordinates_to_string()

    def print_totals(self):
        print '-- Printing Totals --'
        print 'Number of Nodes: ', len(self.nodes)
        print 'Number of Coordinates: ', len(self.coordinates)
        print 'Number of Ways: ', len(self.ways)
        print 'Number of Relations: ', len(self.relations)

    def print_ways(self):
        print '-- Printing Ways --'
        for osm_id, values in self.ways.iteritems():
            print 'Way: ' + str(osm_id) + ', Tags: ' + str(values.get('tags')) + \
                  ', References: ' + str(values.get('references'))


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
        # self.parser.print_nodes()
        # self.parser.print_edges()
        # self.parser.print_bus_stops()
        # self.parser.print_address_book()
        # print self.get_bus_stop_closest_to_coordinates(17.5945912, 59.8462059)
        # print self.get_bus_stops_within_distance(17.5945912, 59.8462059, 100)
        # print self.get_center_point_from_address_name('Forno Romano').coordinates_to_string()
        # Center:(17.6433065, 59.8579188)

        # points = []
        #
        # point = Point(longitude=1.0, latitude=1.0)
        # points.append(point)
        # point = Point(longitude=2.0, latitude=2.0)
        # points.append(point)
        # point = Point(longitude=3.0, latitude=3.0)
        # points.append(point)
        # point = Point(longitude=0.5, latitude=0.5)
        # points.append(point)
        #
        # point = Point(longitude=0.0, latitude=0.0)
        #
        # print closest_to(point, points)

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

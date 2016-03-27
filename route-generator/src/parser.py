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

from path_finder import standard_speed, bus_road_types, find_path

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
    relations = None
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
        self.points = {}
        self.ways = {}
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
        Add a bus_stop to the bus_stops dictionary.

        :type osm_id: integer
        :type name: string
        :type point: Point
        """
        self.bus_stops[osm_id] = {'name': name, 'point': point}

    def add_edge(self, from_node, to_node, max_speed, road_type, way_id):
        """
        Add an edge to the edges dictionary.

        :param from_node: osm_id
        :type from_node: integer
        :param to_node: osm_id
        :type to_node: integer
        :type max_speed: integer
        :type road_type: string
        :type way_id: integer
        """
        if from_node in self.edges:
            self.edges[from_node].append({'to_node': to_node, 'max_speed': max_speed, 'road_type': road_type,
                                          'way_id': way_id})
        else:
            self.edges[from_node] = [{'to_node': to_node, 'max_speed': max_speed, 'road_type': road_type,
                                      'way_id': way_id}]

        if to_node not in self.edges:
            self.edges[to_node] = []

    def add_node(self, osm_id, tags, point):
        """
        Add a node to the nodes dictionary.

        :type osm_id: integer
        :type tags: {}
        :type point: Point
        """
        self.nodes[osm_id] = {'tags': tags, 'point': point}

    def add_point(self, osm_id, point):
        """
        Add a point to the points dictionary.

        :type osm_id: integer
        :type point: Point
        """
        self.points[osm_id] = point

    def add_way(self, osm_id, tags, references):
        """
        Add a way to the ways dictionary.

        :type osm_id: integer
        :type tags: {}
        :type references: [integer]
        """
        self.ways[osm_id] = {'tags': tags, 'references': references}

    def address_range(self, number):
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


# def check_coordinates_list(self, coordinates_list):
#     """
#
#     :param coordinates_list: [(longitude, latitude)]
#     :return:
#     """
#     for index, coordinates in enumerate(coordinates_list):
#
#         if not self.coordinates_in_edges(longitude=coordinates[0], latitude=coordinates[1]):
#             coordinates_list[index] = self.closest_coordinates_in_edges(coordinates)
#
#     return coordinates_list
#
# def coordinates_in_edges(self, longitude, latitude):
#     """
#     Check if a pair of points exist in the edges dictionary.
#
#     :type longitude: float
#     :type latitude: float
#     :return: boolean
#     """
#     return_value = False
#
#     for osm_id in self.edges:
#         point = self.get_point_from_osm_id(osm_id=osm_id)
#
#         if (point is not None) and (point.equal_to_coordinates(longitude=longitude, latitude=latitude)):
#             return_value = True
#             break
#
#     return return_value

def get_bus_stop_closest_to_coordinates(self, longitude, latitude):
    """
    Get the bus stop which is closest to a set of coordinates.

    :type longitude: float
    :type latitude: float
    :return bus_stop: {osm_id, name, point}
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
    Get the bus_stop which corresponds to a set of coordinates.

    :type longitude: float
    :type latitude: float
    :return bus_stop: {osm_id, name, point}
    """
    bus_stop = None

    for osm_id, values in self.bus_stops.iteritems():
        if values.get('point').equal_to_coordinates(longitude=longitude, latitude=latitude):
            values['osm_id'] = osm_id
            bus_stop = values
            break

    return bus_stop


def get_bus_stop_from_name(self, name):
    """
    Get the bus_stop which corresponds to a name.

    :type name: string
    :return bus_stop: {osm_id, name, point}
    """
    name = name.lower()
    bus_stop = None

    for osm_id, values in self.bus_stops.iteritems():
        if values.get('name').lower() == name:
            values['osm_id'] = osm_id
            bus_stop = values
            break

    return bus_stop


def get_bus_stops_within_distance(self, longitude, latitude, maximum_distance):
    """
    Get the bus_stops which are within a distance from a set of coordinates.

    :type longitude:
    :type latitude:
    :type maximum_distance:
    :return bus_stops: [{osm_id, name, point}]
    """
    provided_point = Point(longitude=longitude, latitude=latitude)
    bus_stops = []

    for osm_id, values in self.bus_stops.iteritems():
        current_distance = distance(provided_point, values.get('point'))

        if current_distance <= maximum_distance:
            values['osm_id'] = osm_id
            bus_stops.append(values)

    return bus_stops


def get_center_point_from_address_name(self, address_name):
    """
    Retrieve the point which corresponds to the center of a registered address.

    :type address_name: string
    :return: Point
    """
    retrieved_center = None

    if address_name in self.address_book:
        retrieved_center = self.address_book[address_name].get_center()

    return retrieved_center


def get_closest_point_in_edges(self, point):
    """
    Retrieve the point which is closely to an input point and is contained at the edges.

    :type point: Point
    :return closest_point: (osm_id, point)
    """
    minimum_distance = float('Inf')
    closest_point = None

    for osm_id, point_in_edge in self.get_points_of_edges().iteritems():
        distance_of_points = distance(point, point_in_edge)

        if distance_of_points < minimum_distance:
            minimum_distance = distance_of_points
            closest_point = (osm_id, point_in_edge)

    return closest_point


def get_point_from_osm_id(self, osm_id):
    """
    Retrieve the point which correspond to a specific osm_id.

    :type osm_id: integer
    :return: Point
    """
    return self.points.get(osm_id)


def get_points_of_edges(self):
    """
    Retrieve a dictionary containing the points of edges.

    :return points_of_edges: {osm_id, point}
    """
    points_of_edges = {}

    for osm_id in self.edges:
        points_of_edges[osm_id] = self.get_point_from_osm_id(osm_id=osm_id)

    return points_of_edges


def get_route_from_coordinates(self, starting_longitude, starting_latitude, ending_longitude, ending_latitude):
    """
    Find a route between two set of coordinates, using the A* algorithm.

    :type starting_longitude: float
    :type starting_latitude: float
    :type ending_longitude: float
    :type ending_latitude: float
    :return route: [(osm_id, point, (distance_from_starting_node, time_from_starting_node))]
    """
    starting_point = Point(longitude=starting_longitude, latitude=starting_latitude)
    ending_point = Point(longitude=ending_longitude, latitude=ending_latitude)
    starting_osm_id, starting_point_in_edges = self.get_closest_point_in_edges(point=starting_point)
    ending_osm_id, ending_point_in_edges = self.get_closest_point_in_edges(point=ending_point)

    route = find_path(starting_node=starting_osm_id, ending_node=ending_osm_id,
                      edges=self.edges, points=self.points)
    return route


def parse(self):
    parser = OSMParser(
        concurrency=2,
        coords_callback=self.parse_points,
        nodes_callback=self.parse_nodes,
        ways_callback=self.parse_ways,
        # relations_ callback=self.relations,
        # nodes_tag_filter=self.nodes_filter,
        # ways_tag_filter=self.ways_filter,
        # relations_tag_filter=self.relations_filter
    )
    parser.parse(self.osm_filename)


def parse_address(self, osm_id, tags, point):
    """
    Parse the name, the street, and the house numbers which are related to an address, and add them to the
    address_book dictionary along with their corresponding osm_id val and points.

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


def parse_edges(self, osm_id, tags, references):
    """
    Parse the edges which connect the nodes, bus_stops, and points of the map.

    :param osm_id: Corresponds to the osm_id of the way.
    :type osm_id: integer
    :type tags: {}
    :param references: [osm_id] The list of osm_id objects which are connected to each other.
    :type references: [integer]
    """
    oneway = tags.get('oneway', '') in ('yes', 'true', '1')
    max_speed = tags.get('maxspeed', standard_speed)
    road_type = tags.get('highway')

    for reference_index in range(len(references) - 1):
        self.add_edge(from_node=references[reference_index], to_node=references[reference_index + 1],
                      max_speed=max_speed, road_type=road_type, way_id=osm_id)

        if not oneway:
            self.add_edge(from_node=references[reference_index + 1], to_node=references[reference_index],
                          max_speed=max_speed, road_type=road_type, way_id=osm_id)


def parse_nodes(self, nodes):
    """
    Parse the list of nodes and populate the corresponding dictionary.
    Parse the list of bus stops, which are included in the nodes, and populate the corresponding dictionary.
    Parse the list of addresses, where the nodes correspond to, and populate the corresponding dictionary.

    :type nodes: [(osm_id, tags, (longitude, latitude))]
    """
    for node in nodes:
        osm_id, tags, (longitude, latitude) = node
        point = Point(longitude=longitude, latitude=latitude)
        self.add_node(osm_id=osm_id, tags=tags, point=point)

        if all(term in tags for term in ['bus', 'name']):
            self.add_bus_stop(osm_id=osm_id, name=tags.get('name'), point=point)

        self.parse_address(osm_id=osm_id, tags=tags, point=point)


def parse_points(self, coordinates):
    """
    Parse the list of points and populate the corresponding dictionary.

    :param coordinates: [(osm_id, longitude, latitude)]
    :type coordinates: [(integer, float, float)]
    """
    for osm_id, longitude, latitude in coordinates:
        point = Point(longitude=longitude, latitude=latitude)
        self.add_point(osm_id=osm_id, point=point)


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
                self.add_address(name=name, node_id=reference, point=self.get_point_from_osm_id(osm_id=reference))


def validate_coordinates(self):
    nodes = 0
    none = 0
    for osm_id in self.points:
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
            elif str(reference) in self.points:
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
    for osm_id, point in self.points.iteritems():
        print 'Coordinates: ' + str(osm_id) + ', Point: ' + point.coordinates_to_string()


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
    print 'Number of Coordinates: ', len(self.points)
    print 'Number of Ways: ', len(self.ways)
    print 'Number of Relations: ', len(self.relations)


def print_ways(self):
    print '-- Printing Ways --'
    for osm_id, values in self.ways.iteritems():
        print 'Way: ' + str(osm_id) + ', Tags: ' + str(values.get('tags')) + \
              ', References: ' + str(values.get('references'))


def test_edges(self):
    counter = 0
    for osm_id, list_of_values in self.edges.iteritems():
        for values in list_of_values:
            if values.get('to_node') not in self.points:
                counter += 1
                # print 'From_Node: ' + str(osm_id) + ', To_Node: ' + str(values.get('to_node'))

    print counter


class Router(object):
    def __init__(self, osm_filename):
        self.parser = Parser(osm_filename=osm_filename)
        self.parser.parse()
        self.parser.test_edges()
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


def addy_edge(edges, from_node, to_node, max_speed, road_type):
    """
    Add an edge to the edges dictionary.

    :param from_node: osm_id
    :type from_node: integer
    :param to_node: osm_id
    :type to_node: integer
    :type max_speed: integer
    :type road_type: string
    :type way_id: integer
    """
    if from_node in edges:
        edges[from_node].append({'to_node': to_node, 'max_speed': max_speed, 'road_type': road_type, 'traffic_rate': 0})
    else:
        edges[from_node] = [{'to_node': to_node, 'max_speed': max_speed, 'road_type': road_type, 'traffic_rate': 0}]


def test():
    points = {}
    point = Point(longitude=1.0, latitude=1.0)
    points[1] = point
    point = Point(longitude=2.0, latitude=2.0)
    points[2] = point
    point = Point(longitude=3.0, latitude=3.0)
    points[3] = point
    point = Point(longitude=4.0, latitude=4.0)
    points[4] = point
    point = Point(longitude=5.0, latitude=5.0)
    points[5] = point

    edges = {}
    addy_edge(edges=edges, from_node=1, to_node=2, max_speed=50, road_type='motorway')
    addy_edge(edges=edges, from_node=2, to_node=3, max_speed=50, road_type='motorway')
    addy_edge(edges=edges, from_node=3, to_node=4, max_speed=50, road_type='motorway')
    addy_edge(edges=edges, from_node=4, to_node=5, max_speed=50, road_type='motorway')
    # addy_edge(edges=edges, from_node=, to_node=, max_speed=50, road_type='motorway')
    # addy_edge(edges=edges, from_node=, to_node=, max_speed=50, road_type='motorway')
    # addy_edge(edges=edges, from_node=, to_node=, max_speed=50, road_type='motorway')
    # addy_edge(edges=edges, from_node=, to_node=, max_speed=50, road_type='motorway')
    # addy_edge(edges=edges, from_node=, to_node=, max_speed=50, road_type='motorway')
    # addy_edge(edges=edges, from_node=, to_node=, max_speed=50, road_type='motorway')

    print find_path(starting_node=1, ending_node=5, edges=edges, points=points)
    print find_path(starting_node=2, ending_node=3, edges=edges, points=points)


if __name__ == '__main__':
    # osm_filename = os.path.join(os.path.dirname(__file__), '../resources/map.osm')
    # Router(osm_filename=osm_filename)
    test()

    # p = Process(target=printer, args=())
    # p.start()
    # time.sleep(10)
    # p.terminate()
    # p.join()

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
from imposm.parser import OSMParser
from path_finder import bus_road_types, find_path, standard_speed
from point import distance, Point
from address import Address
import re


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
        self.points = {}
        self.nodes = {}
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

    def add_edge(self, starting_node, ending_node, max_speed, road_type, way_id, traffic_density=None):
        """
        Add an edge to the edges dictionary.

        :param starting_node: osm_id: integer
        :param ending_node: osm_id: integer
        :type max_speed: float or integer
        :type road_type: string
        :param way_id: osm_id: integer
        :param traffic_density: A value between 0 and 1 indicating the density of traffic: float
        """
        if traffic_density is None:
            traffic_density = 0

        if starting_node in self.edges:
            self.edges[starting_node].append({'ending_node': ending_node, 'max_speed': max_speed,
                                              'road_type': road_type, 'way_id': way_id,
                                              'traffic_density': traffic_density})
        else:
            self.edges[starting_node] = [{'ending_node': ending_node, 'max_speed': max_speed, 'road_type': road_type,
                                          'way_id': way_id, 'traffic_density': traffic_density}]

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
        :param references: [osm_id]
        """
        # document = {'osm_id': osm_id, 'tags': tags, 'references': references}
        self.ways[osm_id] = {'tags': tags, 'references': references}

    @staticmethod
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

    def get_list_of_addresses(self):
        list_of_addresses = []

        for name, address in self.address_book.iteritems():
            for node_id, point in address.nodes:
                document = {'name': name, 'node_id': node_id,
                            'point': {'longitude': point.longitude, 'latitude': point.latitude}}
                list_of_addresses.append(document)

        return list_of_addresses

    def get_list_of_bus_stops(self):
        list_of_bus_stops = []

        for osm_id, values in self.bus_stops.iteritems():
            name = values.get('name')
            point = values.get('point')
            document = {'osm_id': osm_id, 'name': name,
                        'point': {'longitude': point.longitude, 'latitude': point.latitude}}
            list_of_bus_stops.append(document)

        return list_of_bus_stops

    def get_list_of_edges(self):
        list_of_edges = []

        for osm_id, list_of_values in self.edges.iteritems():
            for values in list_of_values:
                ending_node = values.get('ending_node')
                max_speed = values.get('max_speed')
                road_type = values.get('road_type')
                way_id = values.get('way_id')
                traffic_density = values.get('traffic_density')
                document = {'starting_node': osm_id, 'ending_node': ending_node, 'max_speed': max_speed,
                            'road_type': road_type, 'way_id': way_id, 'traffic_density': traffic_density}
                list_of_edges.append(document)

        return list_of_edges

    def get_list_of_nodes(self):
        list_of_nodes = []

        for osm_id, values in self.nodes.iteritems():
            tags = values.get('tags')
            point = values.get('point')
            document = {'osm_id': osm_id, 'tags': tags,
                        'point': {'longitude': point.longitude, 'latitude': point.latitude}}
            list_of_nodes.append(document)

        return list_of_nodes

    def get_list_of_points(self):
        list_of_points = []

        for osm_id, point in self.points.iteritems():
            document = {'osm_id': osm_id, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
            list_of_points.append(document)

        return list_of_points

    def get_list_of_ways(self):
        list_of_ways = []

        for osm_id, values in self.ways.iteritems():
            tags = values.get('tags')
            references = values.get('references')
            document = {'osm_id': osm_id, 'tags': tags, 'references': references}
            list_of_ways.append(document)

        return list_of_ways

    def get_point_from_osm_id(self, osm_id):
        """
        Retrieve the point which correspond to a specific osm_id.

        :type osm_id: integer
        :return: Point
        """
        self.points.get(osm_id)

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
            for num in self.address_range(house_number):
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
            self.add_edge(starting_node=references[reference_index], ending_node=references[reference_index + 1],
                          max_speed=max_speed, road_type=road_type, way_id=osm_id)

            if not oneway:
                self.add_edge(starting_node=references[reference_index + 1], ending_node=references[reference_index],
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
                    self.add_address(name=name, node_id=reference,
                                     point=self.get_point_from_osm_id(osm_id=reference))

    # def print_address_book(self):
    #     print '-- Printing Address Book --'
    #     for name, values in self.address_book.iteritems():
    #         print 'Address: ' + name + ', Nodes:' + values.nodes_to_string()
    #         # print 'Address: ' + name + ', Center:' + values.get_center().coordinates_to_string()
    #
    # def print_bus_stops(self):
    #     print '-- Printing Bus Stops --'
    #     for osm_id, values in self.bus_stops.iteritems():
    #         print 'Bus_Stop: ' + str(osm_id) + ', Name: ' + str(values.get('name').encode('utf-8')) + \
    #               ', Point: ' + values.get('point').coordinates_to_string()
    #
    # def print_coordinates(self):
    #     print '-- Printing Coordinates --'
    #     for osm_id, point in self.points.iteritems():
    #         print 'Coordinates: ' + str(osm_id) + ', Point: ' + point.coordinates_to_string()
    #
    # def print_edges(self):
    #     print '-- Printing Edges --'
    #     for osm_id, list_of_values in self.edges.iteritems():
    #         for values in list_of_values:
    #             print 'starting_node: ' + str(osm_id) + ', ending_node: ' + str(values.get('ending_node')) + \
    #                   ', Max_Speed: ' + str(values.get('max_speed')) + ', Way: ' + str(values.get('way_id'))
    #
    # def print_nodes(self):
    #     print '-- Printing Nodes --'
    #     for osm_id, values in self.nodes.iteritems():
    #         print 'Node: ' + str(osm_id) + ', Tags: ' + str(values.get('tags')) + \
    #               ', Point: ' + values.get('point').coordinates_to_string()
    #
    # def print_totals(self):
    #     print '-- Printing Totals --'
    #     print 'Number of Nodes: ', len(self.nodes)
    #     print 'Number of Coordinates: ', len(self.points)
    #     print 'Number of Ways: ', len(self.ways)
    #     print 'Number of Relations: ', len(self.relations)
    #
    # def print_ways(self):
    #     print '-- Printing Ways --'
    #     for osm_id, values in self.ways.iteritems():
    #         print 'Way: ' + str(osm_id) + ', Tags: ' + str(values.get('tags')) + \
    #               ', References: ' + str(values.get('references'))
    #
        # self.parser.test_edges()
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

    # def check_coordinates_in_edges(self, longitude, latitude):
    #     """
    #     Check if a pair of coordinates exists in the edges dictionary.
    #
    #     :type longitude: float
    #     :type latitude: float
    #     :return: boolean
    #     """
    #     return self.check_point_in_edges(point=Point(longitude=longitude, latitude=latitude))
    #
    # def check_point_in_edges(self, point):
    #     """
    #     Check if a point exists in the edges dictionary.
    #
    #     :type point: Point
    #     :return: boolean
    #     """
    #     for osm_id in self.edges:
    #         point_in_edge = self.edges.get(osm_id)
    #
    #         if point.equal_to_coordinates(longitude=point_in_edge.longitude, latitude=point_in_edge.latitude):
    #             return True
    #
    #     return False

    # def get_center_point_from_address_name(self, address_name):
    #     """
    #     Retrieve the point which corresponds to the center of a registered address.
    #
    #     :type address_name: string
    #     :return: Point
    #     """
    #     retrieved_center = None
    #
    #     if address_name in self.address_book:
    #         retrieved_center = self.address_book[address_name].get_center()
    #
    #     return retrieved_center

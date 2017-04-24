#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
- LICENCE

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


- DESCRIPTION OF DOCUMENTS

-- MongoDB Database Documents:

address_document: {
    '_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}
}
bus_line_document: {
    '_id', 'bus_line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
}
bus_stop_document: {
    '_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}
}
bus_stop_waypoints_document: {
    '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[edge_object_id]]
}
bus_vehicle_document: {
    '_id', 'bus_vehicle_id', 'maximum_capacity',
    'routes': [{'starting_datetime', 'ending_datetime', 'timetable_id'}]
}
detailed_bus_stop_waypoints_document: {
    '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[edge_document]]
}
edge_document: {
    '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    'max_speed', 'road_type', 'way_id', 'traffic_density'
}
node_document: {
    '_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}
}
point_document: {
    '_id', 'osm_id', 'point': {'longitude', 'latitude'}
}
timetable_document: {
    '_id', 'timetable_id', 'bus_line_id', 'bus_vehicle_id',
    'timetable_entries': [{
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime', 'number_of_onboarding_passengers',
        'number_of_deboarding_passengers', 'number_of_current_passengers',
        'route': {
            'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
            'distances_from_starting_node', 'times_from_starting_node',
            'distances_from_previous_node', 'times_from_previous_node'
        }
    }],
    'travel_requests': [{
        '_id', 'client_id', 'bus_line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }]
}
traffic_event_document: {
    '_id', 'event_id', 'event_type', 'event_level', 'point': {'longitude', 'latitude'}, 'datetime'
}
travel_request_document: {
    '_id', 'client_id', 'bus_line_id',
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'departure_datetime', 'arrival_datetime',
    'starting_timetable_entry_index', 'ending_timetable_entry_index'
}
way_document: {
    '_id', 'osm_id', 'tags', 'references'
}

-- Route Generator Responses:

get_route_between_two_bus_stops: {
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'route': {
        'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        'distances_from_starting_node', 'times_from_starting_node',
        'distances_from_previous_node', 'times_from_previous_node'
    }
}
get_route_between_multiple_bus_stops: [{
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'route': {
        'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        'distances_from_starting_node', 'times_from_starting_node',
        'distances_from_previous_node', 'times_from_previous_node'
    }
}]
get_waypoints_between_two_bus_stops: {
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[{
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'
    }]]
}
get_waypoints_between_multiple_bus_stops: [{
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[{
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'
    }]]
}]
"""
import re
from imposm.parser import OSMParser
from src.common.parameters import bus_road_types, standard_speed, mongodb_host, mongodb_port
from src.geospatial_data.point import Point
from src.geospatial_data.address import Address
from src.mongodb_database.mongodb_database_connection import MongodbDatabaseConnection
from src.common.logger import log

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class OsmParser(object):
    relations = None
    ways_filter = None
    nodes_filter = None
    relations_filter = None

    def __init__(self, osm_filename):
        """
        :param osm_filename: Directory of the input OSM file.
        :type osm_filename: string
        """
        self.osm_filename = osm_filename
        self.address_documents_dictionary = {}
        self.bus_stop_documents_dictionary = {}
        self.edge_documents_dictionary = {}
        self.node_documents_dictionary = {}
        self.point_documents_dictionary = {}
        self.way_documents_dictionary = {}
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='osm_parser', log_type='DEBUG',
            log_message='mongodb_database_connection: established')

    def add_address(self, name, node_id, point):
        """
        Add an address to the address_documents_dictionary.

        :type name: string
        :type node_id: int
        :type point: Point
        """
        if name is None or name == '' or node_id is None or point is None:
            return

        if name not in self.address_documents_dictionary:
            self.address_documents_dictionary[name] = Address(name, node_id, point)
        else:
            self.address_documents_dictionary[name].add_node(node_id=node_id, point=point)

    def add_bus_stop(self, osm_id, name, point):
        """
        Add a bus_stop to the bus_stop_names dictionary.

        :type osm_id: int
        :type name: string
        :type point: {'longitude', 'latitude'}
        """
        bus_stop_document = {'osm_id': osm_id, 'name': name, 'point': point}
        self.bus_stop_documents_dictionary[osm_id] = bus_stop_document

    def add_edge(self, starting_node, ending_node, max_speed, road_type, way_id, traffic_density=None):
        """
        Add an edge to the edge_documents_dictionary.

        :param starting_node: {'osm_id', 'point': {'longitude', 'latitude'}}
        :param ending_node: {'osm_id', 'point': {'longitude', 'latitude'}}
        :type max_speed: float or int
        :type road_type: string
        :param way_id: osm_id: int
        :param traffic_density: A value between 0 and 1 indicating the density of traffic: float
        """
        if traffic_density is None:
            traffic_density = 0

        starting_node_osm_id = starting_node.get('osm_id')
        edge_document = {'starting_node': starting_node, 'ending_node': ending_node, 'max_speed': max_speed,
                         'road_type': road_type, 'way_id': way_id, 'traffic_density': traffic_density}

        if starting_node_osm_id in self.edge_documents_dictionary:
            self.edge_documents_dictionary[starting_node_osm_id].append(edge_document)
        else:
            self.edge_documents_dictionary[starting_node_osm_id] = [edge_document]

    def add_node(self, osm_id, tags, point):
        """
        Add a node to the node_documents_dictionary.

        :type osm_id: int
        :type tags: {}
        :type point: {'longitude', 'latitude'}
        """
        node_document = {'osm_id': osm_id, 'tags': tags, 'point': point}
        self.node_documents_dictionary[osm_id] = node_document

    def add_point(self, osm_id, point):
        """
        Add a point to the point_documents_dictionary.

        :type osm_id: int
        :type point: {'longitude': longitude, 'latitude': latitude}
        """
        point_document = {'osm_id': osm_id, 'point': point}
        self.point_documents_dictionary[osm_id] = point_document

    def add_way(self, osm_id, tags, references):
        """
        Add a way to the way_documents_dictionary.

        :type osm_id: int
        :type tags: {}
        :param references: [osm_id]
        """
        way_document = {'osm_id': osm_id, 'tags': tags, 'references': references}
        self.way_documents_dictionary[osm_id] = way_document

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

        for name, address in self.address_documents_dictionary.iteritems():
            for node_id, point in address.nodes:
                document = {'name': name, 'node_id': node_id,
                            'point': {'longitude': point.longitude, 'latitude': point.latitude}}
                list_of_addresses.append(document)

        return list_of_addresses

    def get_list_of_bus_stops(self):
        """
        Retrieve a list containing all the bus_stop documents.

        :return: [{'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        """
        list_of_bus_stops = self.bus_stop_documents_dictionary.values()
        return list_of_bus_stops

    def get_list_of_edges(self):
        """
        Retrieve a list containing all the edge_documents_dictionary documents.

        :return: [{'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                   'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
                   'max_speed', 'road_type', 'way_id', 'traffic_density'}]
        """
        list_of_edges = []

        for starting_node_edges in self.edge_documents_dictionary.values():
            for edge in starting_node_edges:
                list_of_edges.append(edge)

        return list_of_edges

    def get_list_of_nodes(self):
        """
        Retrieve a list containing all the node documents.

        :return: [{'osm_id', 'tags', 'point': {'longitude', 'latitude'}}]
        """
        list_of_nodes = self.node_documents_dictionary.values()
        return list_of_nodes

    def get_list_of_points(self):
        """
        Retrieve a list containing all the point documents.

        :return: [{'osm_id', 'point': {'longitude', 'latitude'}}]
        """
        list_of_points = self.point_documents_dictionary.values()
        return list_of_points

    def get_list_of_ways(self):
        """
        Retrieve a list containing all the way documents.

        :return: [{'osm_id', 'tags', 'references'}]
        """
        list_of_ways = self.way_documents_dictionary.values()
        return list_of_ways

    def get_point_from_osm_id(self, osm_id):
        """
        Retrieve the point which corresponds to a specific osm_id.

        :type osm_id: int
        :return: Point
        """
        point = None
        # {'osm_id', 'point': {'longitude', 'latitude'}}
        point_document = self.point_documents_dictionary.get(osm_id)

        if point_document is not None:
            point_entry = point_document.get('point')
            point = Point(longitude=point_entry.get('longitude'), latitude=point_entry.get('latitude'))

        return point

    def get_point_coordinates_from_osm_id(self, osm_id):
        """
        Retrieve the {'longitude', 'latitude'} values which correspond to a specific osm_id.

        :type osm_id: int
        :return: {'longitude', 'latitude'}
        """
        point_coordinates = None
        # {'osm_id', 'point': {'longitude', 'latitude'}}
        point_document = self.point_documents_dictionary.get(osm_id)

        if point_document is not None:
            point_coordinates = point_document.get('point')

        return point_coordinates

    def parse_osm_file(self):
        osm_parser = OSMParser(
            concurrency=2,
            coords_callback=self.parse_points,
            nodes_callback=self.parse_nodes,
            ways_callback=self.parse_ways,
            # relations_ callback=self.relations,
            # nodes_tag_filter=self.nodes_filter,
            # ways_tag_filter=self.ways_filter,
            # relations_tag_filter=self.relations_filter
        )
        osm_parser.parse(self.osm_filename)

    def parse_address(self, osm_id, tags, point):
        """
        Parse the name, the street, and the house numbers which are related to an address, and add them to the
        address_documents_dictionary along with their corresponding osm_id and point.

        :type osm_id: int
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
                # num = str(num)
                try:
                    num = str(num)
                except UnicodeEncodeError:
                    num = ''
                address = street + ' ' + num
                self.add_address(name=address, node_id=osm_id, point=point)

    def parse_edges(self, osm_id, tags, references):
        """
        Parse the edges which connect the nodes, bus_stops, and points of the map.

        :param osm_id: Corresponds to the osm_id of the way.
        :type osm_id: int
        :type tags: {}
        :param references: [osm_id] The list of osm_id objects which are connected to each other.
        :type references: [int]
        """
        oneway = tags.get('oneway', '') in ('yes', 'true', '1')
        max_speed = tags.get('maxspeed', standard_speed)
        road_type = tags.get('highway')

        for reference_index in range(len(references) - 1):
            starting_node_osm_id = references[reference_index]
            starting_node_point = self.get_point_coordinates_from_osm_id(osm_id=starting_node_osm_id)

            ending_node_osm_id = references[reference_index + 1]
            ending_node_point = self.get_point_coordinates_from_osm_id(osm_id=ending_node_osm_id)

            if (starting_node_point is None) or (ending_node_point is None):
                continue

            starting_node = {'osm_id': starting_node_osm_id, 'point': starting_node_point}
            ending_node = {'osm_id': ending_node_osm_id, 'point': ending_node_point}

            self.add_edge(starting_node=starting_node, ending_node=ending_node,
                          max_speed=max_speed, road_type=road_type, way_id=osm_id)

            if not oneway:
                self.add_edge(starting_node=ending_node, ending_node=starting_node,
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

            point = {'longitude': longitude, 'latitude': latitude}
            self.add_node(osm_id=osm_id, tags=tags, point=point)

            bus = tags.get('bus')
            highway = tags.get('highway')
            name = tags.get('name')
            public_transport = tags.get('public_transport')

            if (bus == 'yes' or highway == 'bus_stop' or public_transport == 'platform' or
                        public_transport == 'stop_area') and name:
                self.add_bus_stop(osm_id=osm_id, name=tags.get('name'), point=point)

            point = Point(longitude=longitude, latitude=latitude)
            self.parse_address(osm_id=osm_id, tags=tags, point=point)

    def parse_points(self, coordinates):
        """
        Parse the list of point_documents_dictionary and populate the corresponding dictionary.

        :param coordinates: [(osm_id, longitude, latitude)]
        :type coordinates: [(int, float, float)]
        """
        for osm_id, longitude, latitude in coordinates:
            point = {'longitude': longitude, 'latitude': latitude}
            self.add_point(osm_id=osm_id, point=point)

    def parse_ways(self, ways):
        """
        Parse the list of way_documents_dictionary and populate the corresponding dictionary
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
                    point = self.get_point_from_osm_id(osm_id=reference)
                    self.add_address(name=name, node_id=reference, point=point)

    def populate_address_documents_collection(self):
        address_documents = self.get_list_of_addresses()
        number_of_address_documents = len(address_documents)
        self.mongodb_database_connection.insert_address_documents(address_documents=address_documents)
        self.address_documents_dictionary = {}
        log(module_name='osm_parser_tester', log_type='DEBUG',
            log_message='populate_address_documents_collection (mongodb_database) ok - '
                        'Number of new address_documents: ' + str(number_of_address_documents))

    def populate_bus_stop_documents_collection(self):
        bus_stop_documents = self.get_list_of_bus_stops()
        number_of_bus_stop_documents = len(bus_stop_documents)
        self.mongodb_database_connection.insert_bus_stop_documents(bus_stop_documents=bus_stop_documents)
        self.bus_stop_documents_dictionary = {}
        log(module_name='osm_parser_tester', log_type='DEBUG',
            log_message='populate_bus_stop_documents_collection (mongodb_database) ok - '
                        'Number of new bus_stop_documents: ' + str(number_of_bus_stop_documents))

    def populate_edge_documents_collection(self):
        edge_documents = self.get_list_of_edges()
        number_of_edge_documents = len(edge_documents)
        self.mongodb_database_connection.insert_edge_documents(edge_documents=edge_documents)
        self.edge_documents_dictionary = {}
        log(module_name='osm_parser_tester', log_type='DEBUG',
            log_message='populate_edge_documents_collection (mongodb_database) ok - '
                        'Number of new edge_documents: ' + str(number_of_edge_documents))

    def populate_node_documents_collection(self):
        node_documents = self.get_list_of_nodes()
        number_of_node_documents = len(node_documents)
        self.mongodb_database_connection.insert_node_documents(node_documents=node_documents)
        self.node_documents_dictionary = {}
        log(module_name='osm_parser_tester', log_type='DEBUG',
            log_message='populate_node_documents_collection (mongodb_database) ok - '
                        'Number of new node_documents: ' + str(number_of_node_documents))

    def populate_point_documents_collection(self):
        point_documents = self.get_list_of_points()
        number_of_point_documents = len(point_documents)
        self.mongodb_database_connection.insert_point_documents(point_documents=point_documents)
        self.point_documents_dictionary = {}
        log(module_name='osm_parser_tester', log_type='DEBUG',
            log_message='populate_point_documents_collection (mongodb_database) ok - '
                        'Number of new point_documents: ' + str(number_of_point_documents))

    def populate_way_documents_collection(self):
        way_documents = self.get_list_of_ways()
        number_of_way_documents = len(way_documents)
        self.mongodb_database_connection.insert_way_documents(way_documents=way_documents)
        self.way_documents_dictionary = {}
        log(module_name='osm_parser_tester', log_type='DEBUG',
            log_message='populate_way_documents_collection (mongodb_database) ok - '
                        'Number of new way_documents: ' + str(number_of_way_documents))

    def populate_all_collections(self):
        self.populate_address_documents_collection()
        self.populate_bus_stop_documents_collection()
        self.populate_edge_documents_collection()
        self.populate_node_documents_collection()
        self.populate_point_documents_collection()
        self.populate_way_documents_collection()

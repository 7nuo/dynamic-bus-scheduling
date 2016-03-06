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
# from multiprocessing import Process
import os

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
        :param osm_filename: Directory of input osm file
        :type osm_filename: str
        """
        self.osm_filename = osm_filename
        self.nodes = {}
        self.coordinates = {}
        self.ways = {}
        self.relations = []
        self.bus_stops = {}
        self.edges = {}

    def add_node(self, osm_id, tags, point):
        self.nodes[str(osm_id)] = {'tags': tags, 'point': point}

    def add_bus_stop(self, osm_id, name, point):
        self.bus_stops[str(osm_id)] = {'name': name, 'point': point}

    def add_coordinates(self, osm_id, point):
        self.coordinates[str(osm_id)] = {'point': point}

    def add_way(self, osm_id, tags, references):
        self.ways[str(osm_id)] = {'tags': tags, 'references': references}

    def add_edge(self, from_node, to_node, max_speed, way_id):
        if from_node in self.edges:
            self.edges[from_node].append({'to_node': to_node, 'max_speed': max_speed, 'way_id': way_id})
        else:
            self.edges[from_node] = [{'to_node': to_node, 'max_speed': max_speed, 'way_id': way_id}]

    def print_nodes(self):
        for osm_id, values in self.nodes.iteritems():
            print 'Node:', osm_id + ', Tags:', str(values.get('tags')) + \
                                               ', Point:', values.get('point').coordinates_to_string()

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

    def parse_nodes(self, nodes):
        for node in nodes:
            osm_id, tags, (longitude, latitude) = node
            point = Point(longitude=longitude, latitude=latitude)
            self.add_node(osm_id=osm_id, tags=tags, point=point)

            if all(term in tags for term in ['bus', 'name']):
                self.add_bus_stop(osm_id=osm_id, name=tags.get('name'), point=point)

    def parse_coordinates(self, coordinates):
        for osm_id, longitude, latitude in coordinates:
            point = Point(longitude=longitude, latitude=latitude)
            self.add_coordinates(osm_id=osm_id, point=point)

    def parse_ways(self, ways):
        for way in ways:
            osm_id, tags, references = way
            motorcar = tags.get('motorcar')
            highway = tags.get('highway')

            if motorcar != 'no' and highway in bus_road_types:
                self.add_way(osm_id=osm_id, tags=tags, references=references)

    def parse_edges(self):
        for osm_id, values in self.ways.iteritems():
            tags = values.get('tags')
            references = values.get('references')

            # print references

            highway = tags.get('highway', '')
            oneway = tags.get('oneway', '') in ('yes', 'true', '1')
            max_speed = tags.get('maxspeed', standard_speed)

            for reference_index in range(len(references) - 1):
                self.add_edge(from_node=references[reference_index], to_node=references[reference_index + 1],
                              max_speed=max_speed, way_id=osm_id)

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
            relations_callback=self.parse_relations,
            nodes_tag_filter=self.nodes_filter,
            ways_tag_filter=self.ways_filter,
            relations_tag_filter=self.relations_filter
        )
        parser.parse(self.osm_filename)

        # self.print_nodes()
        # self.print_bus_stops()
        # self.print_coordinates()
        # self.print_ways()

        # self.print_totals()

        # self.validate_references()
        # self.validate_coordinates()

        self.parse_edges()
        print self.edges

        # for relation in self.relations:
        #     print 'Relation: ', relation

    def test(self):
        self.parse()


class Tester(object):
    osm_filename = os.path.join(os.path.dirname(__file__), '../resources/map.osm')
    parser = Parser(osm_filename)
    parser.parse()


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
    Tester()

    # p = Process(target=printer, args=())
    # p.start()
    # time.sleep(10)
    # p.terminate()
    # p.join()

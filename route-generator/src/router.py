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
from parser import Parser
from connection_handler import MongoConnector
from path_finder import find_path
from point import Point
from logger import log
import os
import time
# import signal
# from multiprocessing import Process

# def printer():
#     # start_time = time.time()
#     pattern = ''
#
#     while (True):
#         # elapsed_time = time.time() - start_time
#         pattern += '='
#         print pattern,
#         time.sleep(1)


class Tester(object):
    """

    """
    def __init__(self):
        self.edges = {}
        self.points = {}
        self.populate_points()
        self.populate_edges()

    def add_edge(self, starting_node, ending_node, max_speed, road_type=None, way_id=None, traffic_density=None):
        """
        Add an edge to the edges dictionary.

        :param starting_node: osm_id: integer
        :param ending_node: osm_id: integer
        :type max_speed: float or integer
        :type road_type: string
        :param way_id: osm_id: integer
        :param traffic_density: A value between 0 and 1 indicating the density of traffic: float
        """
        if road_type is None:
            road_type = 'motorway'

        if traffic_density is None:
            traffic_density = 0

        if starting_node in self.edges:
            self.edges[starting_node].append({'ending_node': ending_node, 'max_speed': max_speed,
                                              'road_type': road_type, 'way_id': way_id,
                                              'traffic_density': traffic_density})
        else:
            self.edges[starting_node] = [{'ending_node': ending_node, 'max_speed': max_speed, 'road_type': road_type,
                                      'way_id': way_id, 'traffic_density': traffic_density}]

        if ending_node not in self.edges:
            self.edges[ending_node] = []

    def add_point(self, osm_id, longitude, latitude):
        """
        Add a point to the points dictionary.

        :type osm_id: integer
        :type longitude: float
        :type latitude: float
        """
        point = Point(longitude=longitude, latitude=latitude)
        self.points[osm_id] = point

    def populate_edges(self):
        self.add_edge(starting_node=1, ending_node=2, max_speed=50)
        self.add_edge(starting_node=2, ending_node=3, max_speed=50)
        self.add_edge(starting_node=3, ending_node=4, max_speed=50)
        self.add_edge(starting_node=4, ending_node=5, max_speed=50)

    def populate_points(self):
        self.add_point(osm_id=1, longitude=1.0, latitude=1.0)
        self.add_point(osm_id=2, longitude=2.0, latitude=2.0)
        self.add_point(osm_id=3, longitude=3.0, latitude=3.0)
        self.add_point(osm_id=4, longitude=4.0, latitude=4.0)
        self.add_point(osm_id=5, longitude=5.0, latitude=5.0)

    def test(self):
        print find_path(starting_node=1, ending_node=5, edges=self.edges, points=self.points)
        # print find_path(starting_node=2, ending_node=3, edges=self.edges, points=self.points)


if __name__ == '__main__':
    osm_filename = os.path.join(os.path.dirname(__file__), '../resources/map.osm')
    parser = Parser(osm_filename=osm_filename)

    log(module_name='Parser', log_type='INFO', log_message='parse(): starting')
    start_time = time.time()
    parser.parse()
    elapsed_time = time.time() - start_time
    log(module_name='Parser', log_type='INFO',
        log_message='parse(): finished - elapsed time = ' + str(elapsed_time) + ' sec')

    mongo = MongoConnector(parser=parser, host='127.0.0.1', port=27017)

    log(module_name='MongoConnector', log_type='INFO', log_message='clear_all_collections(): starting')
    start_time = time.time()
    mongo.clear_all_collections()
    elapsed_time = time.time() - start_time
    log(module_name='MongoConnector', log_type='INFO',
        log_message='clear_all_collections(): finished - elapsed time = ' + str(elapsed_time) + ' sec')

    log(module_name='MongoConnector', log_type='INFO', log_message='populate_all_collections(): starting')
    start_time = time.time()
    mongo.populate_all_collections()
    elapsed_time = time.time() - start_time
    log(module_name='MongoConnector', log_type='INFO',
        log_message='populate_all_collections(): finished - elapsed time = ' + str(elapsed_time) + ' sec')

    Tester().test()

    # log(module_name='', log_type='', log_message='')

    # Router(osm_filename=osm_filename)
    # Tester().test()

    # p = Process(target=printer, args=())
    # p.start()
    # time.sleep(10)
    # p.terminate()
    # p.join()

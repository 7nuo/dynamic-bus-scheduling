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
from mongo_connection import Connection
from point import distance, Point


class MongoConnector(object):
    def __init__(self, parser, host, port):
        print 'Initializing MongoConnector'
        self.list_of_points = parser.get_list_of_points()
        print 'Points ok'
        self.list_of_nodes = parser.get_list_of_nodes()
        print 'Nodes ok'
        self.list_of_ways = parser.get_list_of_ways()
        print 'Ways ok'
        self.list_of_bus_stops = parser.get_list_of_bus_stops()
        print 'BusStops ok'
        self.list_of_edges = parser.get_list_of_edges()
        print 'Edges ok'
        self.list_of_addresses = parser.get_list_of_addresses()
        print 'Addresses ok'
        self.connection = Connection(host=host, port=port)
        print 'Connection ok'

    def populate_address_book(self):
        self.connection.insert_addresses(address_book=self.list_of_addresses)
        print 'MongoConnector: populate_address_book: ok'

    def populate_edges(self):
        self.connection.insert_edges(edges=self.list_of_edges)
        print 'MongoConnector: populate_edges: ok'

    def populate_nodes(self):
        self.connection.insert_nodes(nodes=self.list_of_nodes)
        print 'MongoConnector: populate_nodes: ok'

    def populate_points(self):
        self.connection.insert_points(points=self.list_of_points)
        print 'MongoConnector: populate_points: ok'

    def populate_bus_stops(self):
        self.connection.insert_bus_stops(bus_stops=self.list_of_bus_stops)
        print 'MongoConnector: populate_bus_stops: ok'

    def populate_ways(self):
        self.connection.insert_ways(ways=self.list_of_ways)
        print 'MongoConnector: populate_ways: ok'

    def populate_all_collections(self):
        print 'MongoConnector: populate_all_collections'
        self.populate_points()
        self.populate_nodes()
        self.populate_ways()
        self.populate_bus_stops()
        self.populate_edges()
        self.populate_address_book()

    def get_bus_stop_closest_to_coordinates(self, longitude, latitude):
        """
        Get the bus stop which is closest to a set of coordinates.

        :type longitude: float
        :type latitude: float
        :return bus_stop: {osm_id, name, point}
        """
        provided_point = Point(longitude=longitude, latitude=latitude)
        return self.get_bus_stop_closest_to_point(provided_point=provided_point)

    def get_bus_stop_closest_to_point(self, provided_point):
        """
        Get the bus stop which is closest to a geographic point.

        :type provided_point: Point
        :return bus_stop: {osm_id, name, point}
        """
        minimum_distance = float('Inf')
        closest_bus_stop = None

        bus_stops_cursor = self.connection.get_bus_stops()

        for bus_stop in bus_stops_cursor:
            bus_stop_point = bus_stop.get('point')
            current_distance = distance(point_one=provided_point, longitude_two=bus_stop_point.get('longitude'),
                                        latitude_two=bus_stop_point.get('latitude'))

            if current_distance == 0:
                closest_bus_stop = bus_stop
                break
            elif current_distance < minimum_distance:
                minimum_distance = current_distance
                closest_bus_stop = bus_stop
            else:
                pass

        return closest_bus_stop

    def get_bus_stop_from_coordinates(self, longitude, latitude):
        """
        Get the bus_stop which corresponds to a set of coordinates.

        :type longitude: float
        :type latitude: float
        :return bus_stop: {osm_id, name, point}
        """
        return self.connection.find_bus_stop_from_coordinates(longitude=longitude, latitude=latitude)

    def get_bus_stop_from_name(self, name):
        """
        Get the bus_stop which corresponds to a name.

        :type name: string
        :return bus_stop: {osm_id, name, point}
        """
        return self.connection.find_bus_stop_from_name(name=name)

    def get_bus_stop_from_point(self, point):
        """
        Get the bus_stop which corresponds to a name.

        :type point: Point
        :return bus_stop: {osm_id, name, point}
        """
        return self.get_bus_stop_from_coordinates(longitude=point.longitude, latitude=point.latitude)

    def get_bus_stops_within_distance_from_coordinates(self, longitude, latitude, maximum_distance):
        """
        Get the bus_stops which are within a distance from a set of coordinates.

        :type longitude: float
        :type latitude: float
        :type maximum_distance: float
        :return bus_stops: [{osm_id, name, point}]
        """
        provided_point = Point(longitude=longitude, latitude=latitude)
        bus_stops = []
        bus_stops_cursor = self.connection.get_bus_stops()

        for bus_stop in bus_stops_cursor:
            bus_stop_point = bus_stop.get('point')
            current_distance = distance(point_one=provided_point, longitude_two=bus_stop_point.get('longitude'),
                                        latitude_two=bus_stop_point.get('latitude'))

            if current_distance <= maximum_distance:
                bus_stops.append(bus_stop)

        return bus_stops

    def get_bus_stops_within_distance_from_point(self, provided_point, maximum_distance):
        """
        Get the bus_stops which are within a distance from a set of coordinates.

        :type provided_point: Point
        :type maximum_distance: float
        :return bus_stops: [{osm_id, name, point}]
        """
        bus_stops = []
        bus_stops_cursor = self.connection.get_bus_stops()

        for bus_stop in bus_stops_cursor:
            bus_stop_point = bus_stop.get('point')
            current_distance = distance(point_one=provided_point, longitude_two=bus_stop_point.get('longitude'),
                                        latitude_two=bus_stop_point.get('latitude'))

            if current_distance <= maximum_distance:
                bus_stops.append(bus_stop)

        return bus_stops

    # def get_closest_point_in_edges(self, point):
    #     """
    #     Retrieve the point which is closely to an input point and is contained at the edges.
    #
    #     :type point: Point
    #     :return closest_point: (osm_id, point)
    #     """
    #     minimum_distance = float('Inf')
    #     closest_point = None
    #
    #     points_of_edges = self.get_points_of_edges()
    #
    #     for osm_id, point_in_edge in points_of_edges.iteritems():
    #         distance_of_points = distance(point_one=point, point_two=point_in_edge)
    #
    #         if distance_of_points < minimum_distance:
    #             minimum_distance = distance_of_points
    #             closest_point = (osm_id, point_in_edge)
    #
    #     return closest_point

    # def get_point_from_osm_id(self, osm_id):
    #     """
    #     Retrieve the point which correspond to a specific osm_id.
    #
    #     :type osm_id: integer
    #     :return: Point
    #     """
    #     point = None
    #     # document = {'osm_id': osm_id, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
    #     document = self.connection.find_point(osm_id=osm_id)
    #     point_entry = document.get('point')
    #
    #     if point_entry is not None:
    #         point = Point(longitude=point_entry.get('longitude'), latitude=point_entry.get('latitude'))
    #
    #     return point

    # def get_points_dictionary(self):
    #     points_dictionary = {}
    #     points_cursor = self.connection.get_points()
    #
    #     for point_document in points_cursor:
    #         # {'osm_id': osm_id, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
    #         points_dictionary[point_document.get('osm_id')] = \
    #             Point(longitude=point_document.get('point').get('longitude'),
    #                   latitude=point_document.get('point').get('latitude'))
    #
    #     return points_dictionary

    def get_points_of_edges(self):
        """
        Retrieve a dictionary containing the points of edges.

        :return points_of_edges: {osm_id, point}
        """
        # edge_document = {'starting_node', 'ending_node', 'max_speed', 'road_type', 'way_id', 'traffic_density'}
        points_of_edges = {}
        edges_cursor = self.connection.get_edges()
        points_dictionary = self.get_points_dictionary()

        for edge_document in edges_cursor:
            starting_node = edge_document.get('starting_node')
            ending_node = edge_document.get('ending_node')

            if starting_node not in points_of_edges:
                points_of_edges[starting_node] = points_dictionary.get(starting_node)

            if ending_node not in points_of_edges:
                points_of_edges[ending_node] = points_dictionary.get(ending_node)

        return points_of_edges

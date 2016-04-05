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

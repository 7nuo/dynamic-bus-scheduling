from src.geospatial_data.point import Point
from src.route_generator.multiple_paths_finder import _find_multiple_paths

class Tester(object):
    def __init__(self):
        self.edges = {}
        self.points = {}

    def add_edge(self, starting_node, ending_node):
        if starting_node in self.edges:
            self.edges[starting_node].append({'ending_node': ending_node})
        else:
            self.edges[starting_node] = [{'ending_node': ending_node}]

    def add_point(self, osm_id, longitude, latitude):
        point = Point(longitude=longitude, latitude=latitude)
        self.points[osm_id] = point

    def populate_edges(self):
        self.add_edge(starting_node=0, ending_node=1)
        self.add_edge(starting_node=0, ending_node=2)
        self.add_edge(starting_node=1, ending_node=11)
        self.add_edge(starting_node=11, ending_node=12)
        self.add_edge(starting_node=12, ending_node=13)
        self.add_edge(starting_node=13, ending_node=14)
        self.add_edge(starting_node=14, ending_node=15)
        self.add_edge(starting_node=15, ending_node=3)
        self.add_edge(starting_node=2, ending_node=21)
        self.add_edge(starting_node=21, ending_node=22)
        self.add_edge(starting_node=22, ending_node=23)
        self.add_edge(starting_node=23, ending_node=24)
        self.add_edge(starting_node=24, ending_node=25)
        self.add_edge(starting_node=25, ending_node=3)

    def populate_points(self):
        self.add_point(osm_id=0, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=1, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=11, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=12, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=13, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=14, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=15, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=2, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=21, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=22, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=23, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=24, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=25, longitude=0.0, latitude=0.0)
        self.add_point(osm_id=00, longitude=0.0, latitude=0.0)


if __name__ == '__main__':
    tester = Tester()
    tester.populate_points()
    tester.populate_edges()
    paths = _find_multiple_paths(starting_node_osm_id=0, ending_node_osm_id=3, edges=tester.edges,
                                 points=tester.points, number_of_paths=0)
    print paths

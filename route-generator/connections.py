from pymongo import MongoClient


class Connection(object):
    def __init__(self, host, port):
        self.mongo_client = MongoClient(host, port)
        self.db = self.mongo_client.monad
        self.nodes_collection = self.db.Nodes
        self.points_collection = self.db.Points
        self.ways_collection = self.db.Ways
        self.bus_stops_collection = self.db.BusStops
        self.edges_collection = self.db.Edges
        self.address_book_collection = self.db.AddressBook

    # Functions of nodes
    def insert_node(self, osm_id, tags, point):
        document = {'osm_id': osm_id, 'tags': tags, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        result = self.nodes_collection.insert_one(document)
        return result.inserted_id

    def find_node(self, osm_id):
        return self.nodes_collection.find_one({'osm_id': osm_id})

    def delete_node(self, osm_id):
        result = self.nodes_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count

    # Functions of points
    def insert_point(self, osm_id, point):
        document = {'osm_id': osm_id, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        result = self.points_collection.insert_one(document)
        return result.inserted_id

    def find_point(self, osm_id):
        return self.points_collection.find_one({'osm_id': osm_id})

    def delete_point(self, osm_id):
        result = self.points_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count

    # Functions of ways
    def insert_way(self, osm_id, tags, references):
        document = {'osm_id': osm_id, 'tags': tags, 'references': references}
        result = self.ways_collection.insert_one(document)
        return result.inserted_id

    def find_way(self, osm_id):
        return self.ways_collection.find_one({'osm_id': osm_id})

    def delete_way(self, osm_id):
        result = self.ways_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count

    # Functions of bus_stops
    def insert_bus_stop(self, osm_id, name, point):
        document = {'osm_id': osm_id, 'name': name, 'point': {'longitude': point.longitude, 'latitude': point.latitude}}
        result = self.bus_stops_collection.insert_one(document)
        return result.inserted_id

    def find_bus_stop(self, osm_id):
        return self.bus_stops_collection.find_one({'osm_id': osm_id})

    def delete_bus_stop(self, osm_id):
        result = self.bus_stops_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count

    # Functions of edges
    def insert_edge(self, from_node, to_node, max_speed, road_type, way_id, traffic_density=None):
        if traffic_density is None:
            traffic_density = 0

        document = {'from_node': from_node, 'to_node': to_node, 'max_speed': max_speed, 'road_type': road_type,
                    'way_id': way_id, 'traffic_density': traffic_density}
        result = self.edges_collection.insert_one(document)
        return result.inserted_id

    def find_edge(self, from_node, to_node):
        return self.edges_collection.find_one({'from_node': from_node, 'to_node': to_node})

    def find_edges(self, from_node):
        return self.edges_collection.find({'from_node': from_node})

    def delete_edge(self, from_node, to_node):
        result = self.edges_collection.delete_one({'from_node': from_node, 'to_node': to_node})
        return result.deleted_count

    def delete_edges(self, from_node):
        result = self.edges_collection.delete({'from_node': from_node})
        return result.deleted_count

    # Functions of address_book
    def insert_address(self, name, node_id, point):
        if name is None or name == '' or node_id is None or point is None:
            return

        document = {'name': name, 'node_id': node_id,
                    'point': {'longitude': point.longitude, 'latitude': point.latitude}}

        result = self.address_book_collection.insert_one(document)
        return result.inserted_id

    def find_address(self, name):
        return self.address_book_collection.find({'name': name})

    def delete_address(self, name):
        result = self.address_book_collection.delete({'name': name})
        return result.deleted_count


if __name__ == '__main__':
    connection = Connection(host='127.0.0.1', port=27017)
    # connection.insert_node(osm_id=1, tags='hi', point={'longitude': 1.0, 'latitude': 2.0})
    # print connection.delete_node(osm_id=1)

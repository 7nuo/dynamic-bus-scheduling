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

    # Functions of Nodes
    def insert_node(self, osm_id, tags, point):
        self.nodes_collection.insert_one({'osm_id': osm_id, 'tags': tags,
                                          'point': {'longitude': point.longitude, 'latitude': point.latitude}})

    def find_node(self, osm_id):
        return self.nodes_collection.find_one({'osm_id': osm_id})

    def delete_node(self, osm_id):
        result = self.nodes_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count

    # Functions of Points
    def insert_point(self, osm_id, point):
        self.points_collection.insert_one({'osm_id': osm_id,
                                           'point': {'longitude': point.longitude, 'latitude': point.latitude}})

    def find_point(self, osm_id):
        return self.points_collection.find_one({'osm_id': osm_id})

    def delete_point(self, osm_id):
        result = self.points_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count

    # Functions of Ways
    def insert_way(self, osm_id, tags, references):
        self.ways_collection.insert_one({'osm_id': osm_id, 'tags': tags, 'references': references})

    def find_way(self, osm_id):
        return self.ways_collection.find_one({'osm_id': osm_id})

    def delete_way(self, osm_id):
        result = self.ways_collection.delete_one({'osm_id': osm_id})
        return result.deleted_count


if __name__ == '__main__':
    connection = Connection(host='127.0.0.1', port=27017)
    # connection.insert_node(osm_id=1, tags='hi', point={'longitude': 1.0, 'latitude': 2.0})
    # print connection.delete_node(osm_id=1)

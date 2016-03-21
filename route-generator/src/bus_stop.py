from point import Point


class BusStop(Point):
    __slots__ = ['osm_id', 'name', 'longitude', 'latitude']

    def __init__(self, osm_id, name, longitude, latitude):
        self.osm_id = osm_id
        self.name = name
        Point.__init__(self, longitude, latitude)

    def print_values(self):
        print 'OSM_ID:', self.osm_id, '| Name:', self.name, '| Longitude:', self.longitude, \
            '| Latitude:', self.latitude

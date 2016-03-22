"""
Copyright 2016 Ericsson

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
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

#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import json

import time
# from multiprocessing import Process, Pool

host = 'http://127.0.0.1'
port = '2000'


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def get_bus_stops():
    url = host + ':' + port + '/get_bus_stops_dictionary_to_list'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {}
    request = requests.post(url, data=data, headers=headers)
    bus_stops = json.loads(request.text)

    for bus_stop in bus_stops:
        print bus_stop


def get_route_between_bus_stops(starting_bus_stop_name, ending_bus_stop_name):
    url = host + ':' + port + '/get_route_between_bus_stops'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {'starting_bus_stop_name': starting_bus_stop_name,
            'ending_bus_stop_name': ending_bus_stop_name}
    request = requests.post(url, data=data, headers=headers)
    route = json.loads(request.text)

    # print route

    # route: {'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
    #         'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}

    total_distance = route.get('total_distance')
    total_time = route.get('total_time')
    node_osm_ids = route.get('node_osm_ids')
    points = route.get('points')
    distances_from_starting_node = route.get('distances_from_starting_node')
    times_from_starting_node = route.get('times_from_starting_node')
    distances_from_previous_node = route.get('distances_from_previous_node')
    times_from_previous_node = route.get('times_from_previous_node')

    output = '\nRequest: get_route_between_bus_stops' + \
             '\nstarting_bus_stop: ' + starting_bus_stop_name + \
             '\nending_bus_stop: ' + ending_bus_stop_name + \
             '\ntotal_distance: ' + str(total_distance) +\
             '\ntotal_time: ' + str(total_time) +\
             '\nnode_osm_ids: ' + str(node_osm_ids) +\
             '\npoints: ' + str(points) +\
             '\ndistances_from_starting_node: ' + str(distances_from_starting_node) +\
             '\ntimes_from_starting_node: ' + str(times_from_starting_node) +\
             '\ndistances_from_previous_node: ' + str(distances_from_previous_node) +\
             '\ntimes_from_previous_node: ' + str(times_from_previous_node)

    print output


def get_multiple_routes_between_bus_stops(starting_bus_stop_name, ending_bus_stop_name):
    url = host + ':' + port + '/get_multiple_routes_between_bus_stops'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {'starting_bus_stop_name': starting_bus_stop_name,
            'ending_bus_stop_name': ending_bus_stop_name}

    # sess = requests.Session()
    # adapter = requests.adapters.HTTPAdapter(max_retries=10)
    # sess.mount('http://', adapter)
    # request = sess.post(url, data=data, headers=headers, timeout=60)

    request = requests.post(url, data=data, headers=headers, timeout=60)
    routes = json.loads(request.text)

    # print routes

    # routes: [{'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
    #           'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}]

    for route in routes:
        total_distance = route.get('total_distance')
        total_time = route.get('total_time')
        node_osm_ids = route.get('node_osm_ids')
        points = route.get('points')
        distances_from_starting_node = route.get('distances_from_starting_node')
        times_from_starting_node = route.get('times_from_starting_node')
        distances_from_previous_node = route.get('distances_from_previous_node')
        times_from_previous_node = route.get('times_from_previous_node')

        output = '\nRequest: get_multiple_routes_between_bus_stops' + \
                 '\nstarting_bus_stop: ' + starting_bus_stop_name + \
                 '\nending_bus_stop: ' + ending_bus_stop_name + \
                 '\ntotal_distance: ' + str(total_distance) +\
                 '\ntotal_time: ' + str(total_time) +\
                 '\nnode_osm_ids: ' + str(node_osm_ids) +\
                 '\npoints: ' + str(points) +\
                 '\ndistances_from_starting_node: ' + str(distances_from_starting_node) +\
                 '\ntimes_from_starting_node: ' + str(times_from_starting_node) +\
                 '\ndistances_from_previous_node: ' + str(distances_from_previous_node) +\
                 '\ntimes_from_previous_node: ' + str(times_from_previous_node)

        print output


def get_route_between_multiple_bus_stops(bus_stop_names):
    url = host + ':' + port + '/get_route_between_multiple_bus_stops'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {'bus_stop_names': bus_stop_names}
    request = requests.post(url, data=data, headers=headers)
    intermediate_routes = json.loads(request.text)

    # intermediate_routes: [{'starting_bus_stop_name', 'ending_bus_stop_name', 'total_distance', 'total_time',
    #                        'node_osm_ids', 'points', 'distances_from_starting_node', 'times_from_starting_node',
    #                        'distances_from_previous_node', 'times_from_previous_node'}]

    print '\nRequest: get_route_between_multiple_bus_stops'

    for route in intermediate_routes:
        starting_bus_stop_name = route.get('starting_bus_stop_name')
        ending_bus_stop_name = route.get('ending_bus_stop_name')
        total_distance = route.get('total_distance')
        total_time = route.get('total_time')
        node_osm_ids = route.get('node_osm_ids')
        points = route.get('points')
        distances_from_starting_node = route.get('distances_from_starting_node')
        times_from_starting_node = route.get('times_from_starting_node')
        distances_from_previous_node = route.get('distances_from_previous_node')
        times_from_previous_node = route.get('times_from_previous_node')

        output = '\nstarting_bus_stop: ' + starting_bus_stop_name + \
                 '\nending_bus_stop: ' + ending_bus_stop_name + \
                 '\ntotal_distance: ' + str(total_distance) +\
                 '\ntotal_time: ' + str(total_time) +\
                 '\nnode_osm_ids: ' + str(node_osm_ids) +\
                 '\npoints: ' + str(points) +\
                 '\ndistances_from_starting_node: ' + str(distances_from_starting_node) +\
                 '\ntimes_from_starting_node: ' + str(times_from_starting_node) +\
                 '\ndistances_from_previous_node: ' + str(distances_from_previous_node) +\
                 '\ntimes_from_previous_node: ' + str(times_from_previous_node)

        print output


if __name__ == '__main__':
    bus_stop_names = ['Centralstationen', 'Stadshuset', 'Skolgatan', 'Ekonomikum', 'Studentstaden', 'Rickomberga',
                      'Oslogatan', 'Reykjaviksgatan', 'Ekebyhus', 'Sernanders väg', 'Flogsta centrum']

    start = time.time()
    get_route_between_multiple_bus_stops(bus_stop_names=bus_stop_names)
    print 'Time: ' + str(time.time() - start)



    # get_route_between_bus_stops(starting_bus_stop_name='Flogsta centrum', ending_bus_stop_name='Säves väg')
    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='Centralstationen', ending_bus_stop_name='Stadshuset')

    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='Stenhagenskolan', ending_bus_stop_name='Stenhagens Centrum')
    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='', ending_bus_stop_name='')
    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='', ending_bus_stop_name='')
    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='', ending_bus_stop_name='')
    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='', ending_bus_stop_name='')
    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='', ending_bus_stop_name='')
    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='', ending_bus_stop_name='')
    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='', ending_bus_stop_name='')
    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='', ending_bus_stop_name='')
    # get_multiple_routes_between_bus_stops(starting_bus_stop_name='', ending_bus_stop_name='')






    # get_bus_stops_dictionary_to_list()

    # p = Pool(5)
    # p.map(get_bus_stops_dictionary_to_list(), [1, 2, 3, 4, 5])
    # for i in range(0, 1):
    #     p = Process(target=get_bus_stops_dictionary_to_list, args=())
    #     p.start()
    #     p.join()
    # p1 = Process(target=get_bus_stops_dictionary_to_list, args=())
    # p2 = Process(target=get_bus_stops_dictionary_to_list, args=('two', 2))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()

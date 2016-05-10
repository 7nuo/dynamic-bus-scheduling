import requests
import json

# import time
# from multiprocessing import Process, Pool

host = 'http://127.0.0.1'
port = '2000'


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def post_request():
    url = host + ':' + port + '/get_bus_stops'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {}
    request = requests.post(url, data=data, headers=headers)

    # request = requests.post(url=url, headers=headers)
    print request.text


def get_route_between_bus_stops(starting_bus_stop_name, ending_bus_stop_name):
    url = host + ':' + port + '/get_route_between_bus_stops'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {'starting_bus_stop_name': starting_bus_stop_name,
            'ending_bus_stop_name': ending_bus_stop_name}
    request = requests.post(url, data=data, headers=headers)
    json_response = json.loads(request.text)

    # print json_response

    # json_response: {'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
    #                 'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}

    total_distance = json_response.get('total_distance')
    total_time = json_response.get('total_time')
    node_osm_ids = json_response.get('node_osm_ids')
    points = json_response.get('points')
    distances_from_starting_node = json_response.get('distances_from_starting_node')
    times_from_starting_node = json_response.get('times_from_starting_node')
    distances_from_previous_node = json_response.get('distances_from_previous_node')
    times_from_previous_node = json_response.get('times_from_previous_node')

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
    json_response = json.loads(request.text)

    print json_response

    # json_response: {'total_distance', 'total_time', 'node_osm_ids', 'points', 'distances_from_starting_node',
    #                 'times_from_starting_node', 'distances_from_previous_node', 'times_from_previous_node'}

    # total_distance = json_response.get('total_distance')
    # total_time = json_response.get('total_time')
    # node_osm_ids = json_response.get('node_osm_ids')
    # points = json_response.get('points')
    # distances_from_starting_node = json_response.get('distances_from_starting_node')
    # times_from_starting_node = json_response.get('times_from_starting_node')
    # distances_from_previous_node = json_response.get('distances_from_previous_node')
    # times_from_previous_node = json_response.get('times_from_previous_node')
    #
    # output = '\nRequest: get_route_between_bus_stops' + \
    #          '\nstarting_bus_stop: ' + starting_bus_stop_name + \
    #          '\nending_bus_stop: ' + ending_bus_stop_name + \
    #          '\ntotal_distance: ' + str(total_distance) +\
    #          '\ntotal_time: ' + str(total_time) +\
    #          '\nnode_osm_ids: ' + str(node_osm_ids) +\
    #          '\npoints: ' + str(points) +\
    #          '\ndistances_from_starting_node: ' + str(distances_from_starting_node) +\
    #          '\ntimes_from_starting_node: ' + str(times_from_starting_node) +\
    #          '\ndistances_from_previous_node: ' + str(distances_from_previous_node) +\
    #          '\ntimes_from_previous_node: ' + str(times_from_previous_node)
    #
    # print output

if __name__ == '__main__':
    # get_route_between_bus_stops(starting_bus_stop_name='Centralstationen', ending_bus_stop_name='Stadshuset')
    get_multiple_routes_between_bus_stops(starting_bus_stop_name='Centralstationen', ending_bus_stop_name='Stadshuset')
    # post_request()

    # p = Pool(5)
    # p.map(post_request(), [1, 2, 3, 4, 5])
    # for i in range(0, 1):
    #     p = Process(target=post_request, args=())
    #     p.start()
    #     p.join()
    # p1 = Process(target=post_request, args=())
    # p2 = Process(target=post_request, args=('two', 2))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()

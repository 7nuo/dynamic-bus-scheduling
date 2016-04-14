import requests
import json
# import time
# from multiprocessing import Process, Pool

host = 'http://127.0.0.1'
port = '2000'


def post_request():
    url = host + ':' + port + '/get_route'
    data = {'starting_point': (1.0, 1.0), 'ending_point': (2.0, 2.0)}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # headers = {'content-type': 'application/json'}
    request = requests.post(url, data=data, headers=headers)

    # request = requests.get(url=url, headers=headers)
    print request.text


if __name__ == '__main__':
    post_request()
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
    # post_request('one')
    # post_request('two')

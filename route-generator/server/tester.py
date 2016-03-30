# 127.0.0.1:2000

import requests
# import json
import time
from multiprocessing import Process, Pool


def post_request():
    url = "http://127.0.0.1:2000"
    # data = {'data': user}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # request = requests.post(url, data=json.dumps(data), headers=headers)

    time.sleep(2)
    request = requests.get(url=url, headers=headers)
    # print request.text


if __name__ == "__main__":
    # p = Pool(5)
    # p.map(post_request(), [1, 2, 3, 4, 5])
    for i in range(0, 4):
        p = Process(target=post_request, args=())
        p.start()
        p.join()
    # p1 = Process(target=post_request, args=())
    # p2 = Process(target=post_request, args=('two', 2))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    # post_request('one')
    # post_request('two')

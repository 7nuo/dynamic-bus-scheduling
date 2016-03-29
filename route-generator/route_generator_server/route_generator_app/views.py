# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import time


@csrf_exempt
def testy(request):
    if request.method == 'GET':
        return HttpResponse("Welcome to the Route Generator!!")
    elif request.method == 'POST':
        print 'Method:', request.method
        print 'POST:', request.POST.get('data')

        if request.POST.get('data') == 'one':
            time.sleep(5)

    # if request.method == 'POST':
    #         received_json_data = json.loads(request.POST['data'])
    #
    # print str(received_json_data)
    return HttpResponse('OK' + request.POST.get('data'))

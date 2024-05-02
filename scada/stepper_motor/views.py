import datetime
import os
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.conf import settings
from stepper_motor import utils, models


def control_mode(request):

    return render(
                    request,
                    "stepper_motor/control_mode.html",
                    {
                    }
    )


def data_table(request):
    return render(
                    request,
                    "stepper_motor/data_table.html",
                    {
                        'data': models.NodeDataPoint.objects.values,
                    }
    )

def show_node(request):
    print(request)
    return render(  request,
                    "stepper_motor/show_node.html",
                    {
                    })

@csrf_exempt
def receive_data(request):
    if request.method=='POST':
        # Take our received JSON data and load that into python dictionary
        data_dict =json.loads(request.body)
        # If our data is not empty
        if data_dict:
            utils.save_data(data_dict)
            # Return success response code
            return HttpResponse(status=200)
        # if empty return no data response code
        else:
            # Return no content response code
            return HttpResponse(status=204)

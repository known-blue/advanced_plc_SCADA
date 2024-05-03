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

def show_node(request, number):
    #print(number)
    return render(  request,
                    "stepper_motor/show_node.html",
                    {
                        'data':models.NodeDataPoint.objects.values,
                        'count':number,
                    })


def graph(request):
    # Predefine our lists for graphing
    value_list = []
    timestamp_list = []
    tag_name = None

    # Query the step motor DP table for distinct (unique) values in the tag_name field
    tag_names = models.StepperMotorDataPoint.objects.values_list('tag_name').distinct()

    # Cast our queryset to a list of tuples as its easier to deal with
    tag_names = list(tag_names)
    # Covert out queryset list of tuples to a single list of the tag names
    tag_names = list(sum(tag_names, ()))


    if request.method=="POST":
        tag_name = request.POST['tag_name']
        data = models.StepperMotorDataPoint.objects.filter(tag_name=tag_name).order_by('timestamp')
    
        for data_point in data:
            value_list.append(data_point.tag_value)
            timestamp_list.append(data_point.timestamp.strftime("%m/%d/%Y, %H:%M:%S"))


    return render(
                    request,
                    "stepper_motor/graph.html",
                    {
                        'chosen_tag': tag_name,
                        'tag_options': tag_names,
                        'values': value_list,
                        'timestamps': timestamp_list,
                    }
    )


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

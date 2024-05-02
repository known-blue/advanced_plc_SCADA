import json
from stepper_motor import models
from datetime import datetime

def save_data(node_dict):
	# Delete any nodes that aren't in the list anymore
	models.NodeDataPoint.objects.exclude(name__in=node_dict.keys()).delete()
	# Add in any new nodes
	# WIP: Check the dict before sending it to webserver to see if there's any new info to add or remove
	# This would limit the number of messages coming to the server and would simplify this sides code.
	for key, value in node_dict.items():
		existing_data = models.NodeDataPoint.objects.filter(
															name = key,
															type = value[0],
															interface_name = value[1],
															interface = value[2],
															info = value[3],
														)
		if existing_data.exists():
			pass
			#print("Data point already exists in DB")
		else:
			TempDataPoint = models.NodeDataPoint(
												name = key,
												type = value[0],
												interface_name = value[1],
												interface = value[2],
												info = value[3],
											)
			TempDataPoint.save()
	print("Table update done...")

def read_json_file(filename):
	with open(filename) as f:
		data = json.load(f)
	return data
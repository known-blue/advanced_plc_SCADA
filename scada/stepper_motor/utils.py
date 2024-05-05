import json
from stepper_motor import models
from datetime import datetime

def save_data(node_dict):
	# Delete any nodes that aren't in the list anymore
	models.NodeDataPoint.objects.exclude(name__in=node_dict.keys()).delete()
	# Add in any new nodes
	for key, value in node_dict.items():
		existing_data = models.NodeDataPoint.objects.filter(name = key)
		if not existing_data.exists():
			TempDataPoint = models.NodeDataPoint(
												name = key,
												type = value[0],
												interface_name = value[1],
												interface = value[2],
												info = value[3],
												data = value[4]
											)
			TempDataPoint.save()
	print("Table update done...")

def read_json_file(filename):
	with open(filename) as f:
		data = json.load(f)
	return data
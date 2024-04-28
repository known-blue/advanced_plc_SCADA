import json
from stepper_motor import models
from datetime import datetime

def save_data(node_dict):
	for key, value in node_dict.items():
		existing_data = models.NodeDataPoint.objects.filter(
															name = key,
															type = value[0],
															interface_name = value[1],
															interface = value[2],
															info = value[3],
														)
		if existing_data.exists():
			print("Data point already exists in DB")
		else:
			TempDataPoint = models.NodeDataPoint(
												name = key,
												type = value[0],
												interface_name = value[1],
												interface = value[2],
												info = value[3],
											)
			TempDataPoint.save()


def read_json_file(filename):
	with open(filename) as f:
		data = json.load(f)
	return data
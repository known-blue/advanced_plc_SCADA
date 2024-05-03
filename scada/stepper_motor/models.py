from django.db import models

class NodeDataPoint(models.Model):
	name = models.CharField(max_length=256)
	type = models.CharField(max_length=256)
	interface_name = models.CharField(max_length=256)
	# No max length because these can be on the longer side
	interface = models.CharField(max_length=2560)
	info = models.CharField(max_length=2560)
	data = models.CharField(max_length=2560)

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('stepper-motor-control-mode/', views.control_mode, name="stepper-motor-control-mode"),
    path('stepper-motor-data-table/', views.data_table, name="stepper-motor-data-table"),
    path('receive-data/', views.receive_data, name="receive-data"),
    path('stepper-motor-graph/', views.graph, name="stepper-motor-graph"),
    path('node-details/<int:number>/', views.show_node, name="node-details"),
]
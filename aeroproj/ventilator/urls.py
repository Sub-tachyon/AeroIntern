from django.urls import path
from . import views

urlpatterns = [
    #path("device_reg", views.device_reg, name="device_reg"),
    path("device_reg2", views.device_reg2, name="device_reg2"),
    path("patient", views.patient_data, name="patient"),
    path("patient_list", views.patient_list, name="patient_list"),
    path("device_list", views.device_list, name="device_list"),
]

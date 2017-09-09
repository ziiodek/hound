from django.conf.urls import url
from .views.vehicle_view import VehicleView

urlpatterns = [
    url( r'^vehicles/(?P<lenguage>[0-1])/(?P<status>[0])/', VehicleView.get_all_vehicles, name='vehicles'),
    url(r'^archiver_vehicles/(?P<lenguage>[0-1])/(?P<status>[1])/', VehicleView.get_all_vehicles, name='vehicles'),
    url(r'^add_vehicle/(?P<lenguage>[0-1])/',VehicleView.add_vehicle,name='add_vehicle'),
    url(r'^profile_vehicle/(?P<lenguage>[0-1])/(?P<economic_no>[0-9]+)/(?P<state>[0-1])/', VehicleView.upload_vehicle_profile, name='profile_vehicle'),
    url(r'^view_vehicle/(?P<lenguage>[0-1])/(?P<economic_no>[0-9]+)/',VehicleView.view_vehicle,name='view_vehicle'),
    url(r'^edit_vehicle/(?P<lenguage>[0-1])/(?P<economic_no>[0-9]+)/',VehicleView.edit_vehicle,name='edit_vehicle'),
    url(r'^manager_vehicles/(?P<lenguage>[0-1])/',VehicleView.manager_vehicles,name='manager_vehicles'),
    url(r'^restore_vehicle/(?P<lenguage>[0-1])/(?P<economic_no>[0-9]+)/', VehicleView.restore_vehicle, name='restore_vehicle'),
    url( r'^delete_vehicle/(?P<lenguage>[0-1])/(?P<economic_no>[0-9]+)/', VehicleView.delete_vehicle, name='delete_vehicle'),
    url(r'^search_vehicle/(?P<lenguage>[0-1])/(?P<status>[0-1])/', VehicleView.search_vehicle, name='search_vehicle'),
]

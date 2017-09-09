from django.conf.urls import url
from .views.trip_view import TripView

urlpatterns = [
    url(r'^trip_status/(?P<lenguage>[0-1])/(?P<trip_id>[0-9]+)/', TripView.get_trip, name='trip_status'),
    url( r'^trip_status/(?P<lenguage>[0-1])/', TripView.get_today_trips, name='trip_status'),
    url( r'^bitacora/(?P<lenguage>[0-1])/', TripView.get_all_trips, name='bitacora'),
    url(r'^assign_trip/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/(?P<economic_no>[0-9]+)/',TripView.assign_trip,name='assign_trip'),
    url(r'^edit_trip/(?P<lenguage>[0-1])/(?P<trip_id>[0-9]+)/(?P<assigned_id>[0-9]+)/(?P<economic_no>[0-9]+)/',TripView.edit_trip,name='edit_trip'),
    url(r'^manager_trip_status/(?P<lenguage>[0-1])/',TripView.manager_trip_status,name='manager_trip_status'),
    url(r'^manager_bitacora/(?P<lenguage>[0-1])/',TripView.manager_bitacora,name='manager_bitacora'),
    url( r'^delete_bitacora/(?P<lenguage>[0-1])/',TripView.delete_bitacora, name='delete_bitacora'),
    url(r'^cancel_trip/(?P<lenguage>[0-1])/(?P<trip_id>[0-9]+)/', TripView.cancel_trip,name='cancel_trip'),
    url(r'^search_today_trip/(?P<lenguage>[0-1])/', TripView.search_today_trip, name='search_today_trip'),
    url(r'^search_bitacora_trip/(?P<lenguage>[0-1])/', TripView.search_bitacora_trip, name='search_bitacora_trip'),
]

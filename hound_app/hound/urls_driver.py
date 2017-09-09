from django.conf.urls import url
from .views.driver_view import DriverView

urlpatterns = [
    url( r'^drivers/(?P<lenguage>[0-1])/(?P<status>[0])/', DriverView.get_all_drivers, name='drivers'),
    url(r'^archiver_drivers/(?P<lenguage>[0-1])/(?P<status>[1])/', DriverView.get_all_drivers, name='drivers'),
    url(r'^add_driver/(?P<lenguage>[0-1])/',DriverView.add_driver,name='add_driver'),
    url(r'^print_driver/(?P<assigned_id>[0-9]+)/', DriverView.generate_case_file, name='print_driver'),
    url(r'^print_driver_esp/(?P<assigned_id>[0-9]+)/', DriverView.generate_case_file_esp, name='print_driver_esp'),
    url(r'^profile_driver/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/(?P<state>[0-1])/', DriverView.upload_driver_profile,name='profile_driver'),
    url(r'^prints_driver/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/(?P<state>[0-1])/', DriverView.upload_driver_prints,name='prints_driver'),
    url(r'^view_driver/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/',DriverView.view_driver,name='view_driver'),
    url(r'^edit_driver/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/',DriverView.edit_driver,name='edit_driver'),
    url(r'^restore_driver/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/', DriverView.restore_driver, name='restore_driver'),
    url(r'^manager_drivers/(?P<lenguage>[0-1])/',DriverView.manager_drivers,name='manager_drivers'),
    url( r'^delete_driver/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/', DriverView.delete_driver, name='delete_driver'),
    url(r'^search_driver/(?P<lenguage>[0-1])/(?P<status>[0-1])/', DriverView.search_driver, name='search_driver'),
    url( r'^print/(?P<lenguage>[0-1])/', DriverView.export_drivers, name='print'),
]

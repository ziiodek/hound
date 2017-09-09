from django.conf.urls import url
from .views.directory_view import DirectoryView

urlpatterns = [
    url( r'^add_directory/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/', DirectoryView.add_directory, name='directory' ),
    url(r'^edit_directory/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/(?P<phone_id>[0-9]+)/', DirectoryView.edit_directory, name='directory'),
    url(r'^empty_directory/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/',DirectoryView.empty_directory, name='empty_directory'),
    url(r'^delete_number/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/', DirectoryView.delete_number,name='delete_number'),
    url(r'^export_directory/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/', DirectoryView.export_directory,name='export_directory'),

]

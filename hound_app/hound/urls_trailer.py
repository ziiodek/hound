from django.conf.urls import url
from .views.trailer_view import TrailerView

urlpatterns = [
    url( r'^trailers/(?P<lenguage>[0-1])/(?P<status>[0])/', TrailerView.get_all_trailers, name='trailers'),
    url(r'^archiver_trailers/(?P<lenguage>[0-1])/(?P<status>[1])/', TrailerView.get_all_trailers, name='trailers'),
    url(r'^add_trailer/(?P<lenguage>[0-1])/',TrailerView.add_trailer,name='add_trailer'),
    url(r'^profile_trailer/(?P<lenguage>[0-1])/(?P<economic_no>[0-9]+)/(?P<state>[0-1])/', TrailerView.upload_trailer_profile, name='profile_trailer'),
    url(r'^view_trailer/(?P<lenguage>[0-1])/(?P<economic_no>[0-9]+)/',TrailerView.view_trailer,name='view_trailer'),
    url(r'^edit_trailer/(?P<lenguage>[0-1])/(?P<economic_no>[0-9]+)/',TrailerView.edit_trailer,name='edit_trailer'),
    url(r'^manager_trailers/(?P<lenguage>[0-1])/',TrailerView.manager_trailers,name='manager_trailers'),
    url(r'^restore_trailer/(?P<lenguage>[0-1])/(?P<economic_no>[0-9]+)/', TrailerView.restore_trailer,name='restore_trailer'),
    url( r'^delete_trailer/(?P<lenguage>[0-1])/(?P<economic_no>[0-9]+)/', TrailerView.delete_trailer, name='delete_trailer'),
    url(r'^search_trailer/(?P<lenguage>[0-1])/(?P<status>[0-1])/', TrailerView.search_trailer, name='search_trailer'),
]

from django.conf.urls import url
from .views.settings_view import SettingsView

urlpatterns = [
    url( r'^settings/(?P<lenguage>[0-1])/', SettingsView.settings, name='settings'),
    url( r'^change_password/(?P<lenguage>[0-1])/', SettingsView.change, name='change_password'),
    url(r'^url_settings/(?P<lenguage>[0-1])/(?P<hash>\w+)/', SettingsView.change_view, name='url_settings'),
    url(r'^profile/(?P<lenguage>[0-1])/', SettingsView.upload_profile,name='profile'),
]

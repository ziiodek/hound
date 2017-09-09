from django.conf.urls import url
from .views.activate_view import ActivateView

urlpatterns = [
    url( r'^reactivate_account/(?P<lenguage>[0-1])/', ActivateView.activate, name='Activate Account'),
    url(r'^url_activate/(?P<lenguage>[0-1])/(?P<hash>\w+)/', ActivateView.activate_view, name='url_activate'),
]

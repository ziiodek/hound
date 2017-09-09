"""hound_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
    url(r'^',include('hound.urls_driver')),
    url(r'^', include('hound.urls_trailer')),
    url(r'^', include('hound.urls_vehicle')),
    url( r'^', include( 'hound.urls_vacations')),
    url( r'^', include( 'hound.urls_directory')),
    url( r'^', include( 'hound.urls_trip')),
    url( r'^', include( 'hound.urls_settings')),
    url( r'^', include( 'hound.urls_activate')),
    url( r'^', include( 'hound.urls_authentication')),
    url(r'^admin/', admin.site.urls),
]

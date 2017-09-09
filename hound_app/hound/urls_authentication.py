from django.conf.urls import url
from .views.authentication_view import AuthenticationView
from .views.generic_view import GenericView

urlpatterns = [
    url(r'^esp/', AuthenticationView.home_page_esp, name='home'),
    url( r'^email/(?P<lenguage>[0-1])/', AuthenticationView.email_auth, name='email' ),
    url( r'^password/(?P<lenguage>[0-1])/', AuthenticationView.password_auth, name='password' ),
    url( r'^registration/(?P<lenguage>[0-1])/', AuthenticationView.registration, name='registration' ),
    url( r'^version/', AuthenticationView.version, name='version' ),
    url( r'^url/(?P<lenguage>[0-1])/(?P<hash>\w+)/', AuthenticationView.reset_view, name='url' ),
    url(r'^confirm/(?P<lenguage>[0-1])/(?P<hash>\w+)/', AuthenticationView.confirm_view, name='confirm'),
    url( r'^recover_password/(?P<lenguage>[0-1])/', AuthenticationView.reset, name='recover_password'),
    url(r'^confirm_email/(?P<lenguage>[0-1])/', AuthenticationView.confirm, name='confirm_email'),
    url(r'^logout/(?P<lenguage>[0-1])/', AuthenticationView.log_out, name='logout'),
    url(r'^activate/(?P<lenguage>[0-1])/', AuthenticationView.activate, name='logout'),
    url(r'^', AuthenticationView.home_page_eng, name='home')

]

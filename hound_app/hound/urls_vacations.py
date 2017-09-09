from django.conf.urls import url
from .views.vacation_view import VacationView

urlpatterns = [
    url( r'^vacations/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/', VacationView.get_vacations, name='vacations' ),
    url(r'^search_vacation/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/', VacationView.search_vacation, name='search_vacation'),
    url( r'^vacations_dates/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/(?P<vacation_id>[0-9]+)/', VacationView.get_vacations_dates, name='vacations' ),
    url( r'^add_vacations/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/', VacationView.add_vacations, name='add_vacations' ),
    url( r'^add_date/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/(?P<vacation_id>[0-9]+)/', VacationView.add_date, name='add_date' ),
    url( r'^delete_dates/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/(?P<vacation_id>[0-9]+)/', VacationView.delete_dates, name='delete_dates' ),
    url( r'^delete_vacations/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/(?P<vacation_id>[0-9]+)/', VacationView.delete_vacations, name='delete_vacations' ),
    url( r'^delete_all/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/', VacationView.delete_all, name='delete_all' ),
    url( r'^edit_vacations/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/(?P<vacation_id>[0-9]+)/', VacationView.edit_vacations,name='edit_vacations' ),
    url(r'^export_vacations/(?P<lenguage>[0-1])/(?P<assigned_id>[0-9]+)/', VacationView.export_vacations,name='export_vacations')
]

from django.urls import path, include
from .views import (
    RetrieveUpdateAircraftView,
    ListCreateAircraftView,
    RetrieveUpdateDeleteFlightView,
    ListCreateFlightView,
    ReportsList,
    CreateFlightView,
    ListAirportsView
)


app_name = "aviation"

urlpatterns = [
    path('airports/', ListAirportsView.as_view(), name='list_airports'),
    path('aircraft/<str:serial_number>', RetrieveUpdateAircraftView.as_view(), name='get_update_aicraft'),
    path('aircraft/', ListCreateAircraftView.as_view(), name='list_create_aircraft'),
    path("flights/<int:id>", RetrieveUpdateDeleteFlightView.as_view(), name='get_update_delete_flights'),
    path("flights/create/", CreateFlightView.as_view(), name='create_flights'),
    path("flights/", ListCreateFlightView.as_view(), name='list_flights'),
    path("report/", ReportsList.as_view(), name='report'),
]

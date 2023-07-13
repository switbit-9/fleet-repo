import django_filters
from .models import Flights

class FlightsFilter(django_filters.rest_framework.FilterSet):
    date_from = django_filters.rest_framework.DateTimeFilter(field_name='departure_date', lookup_expr='gte')
    date_to = django_filters.rest_framework.DateTimeFilter(field_name='departure_date', lookup_expr='lte')
    departure_airport =  django_filters.rest_framework.CharFilter(field_name='departure_airport', lookup_expr='exact')
    arrival_airport =  django_filters.rest_framework.CharFilter(field_name='arrival_airport', lookup_expr='exact')

    class Meta:
        model = Flights
        fields = {
            "departure_airport" : ['exact']
        }


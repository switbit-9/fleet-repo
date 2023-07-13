from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from .models import (
    Aircraft,
    Flights
)
from .serializers import (
    RetrieveAircraftSerializer,
    UpdateAircraftSerializer,
    CreateFlightsSerializer,
    RetrieveFlightsSerializer,
    ReportSerializer

)
from .filters import FlightsFilter

@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Only manufacturer field can be updated",
    request_body=UpdateAircraftSerializer
))
class RetrieveUpdateAircraftView(RetrieveUpdateAPIView):
    queryset = Aircraft.activeobjects.all()
    serializer_class = RetrieveAircraftSerializer
    lookup_field = 'serial_number'

    def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = RetrieveAircraftSerializer(instance)
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateAircraftSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)


class ListCreateAircraftView(ListCreateAPIView):
    queryset =  Aircraft.activeobjects.all()
    serializer_class = RetrieveAircraftSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = RetrieveAircraftSerializer(qs, many=True)
        return Response(serializer.data)


class RetrieveUpdateDeleteFlightView(RetrieveUpdateDestroyAPIView):
    queryset = Flights.objects.all()
    serializer_class = RetrieveFlightsSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CreateFlightsSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RetrieveFlightsSerializer(instance)
        return Response(serializer.data)


class ListCreateFlightView(ListCreateAPIView):
    serializer_class = RetrieveFlightsSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightsFilter

    def get_queryset(self, *args, **kwargs):
        queryset = Flights.objects.order_by('departure_date')
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = CreateFlightsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

manual_params= [
    openapi.Parameter('date_from', openapi.IN_QUERY, description="From Date format :  2023-08-22T16:00:00", type=openapi.TYPE_STRING),
    openapi.Parameter('date_to', openapi.IN_QUERY, description="To Date format :  2023-08-22T16:00:00",  type=openapi.TYPE_STRING)
]
@method_decorator(name='list', decorator=swagger_auto_schema(
    manual_parameters=manual_params,
    responses=ReportSerializer
))
class ReportsList(ListAPIView):
    serializer_class = ReportSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        date_from = self.request.GET.get('date_from', False)
        date_to = self.request.GET.get('date_to', False)
        date_from_formated, date_to_formated = self.handle_datetime(date_from, date_to)

        queryset = Flights.objects.raw(
            """
                SELECT
                id,
              f.departure_airport_id,
              a.serial_number AS in_flight_aircraft,
              ROUND(EXTRACT(EPOCH FROM (
                CASE
                  WHEN f.arrival_date < '%(date_to)s' THEN f.arrival_date
                  ELSE '%(date_to)s'
                END
                -
                CASE
                  WHEN f.departure_date > '%(date_form)s' THEN f.departure_date
                  ELSE '%(date_form)s'
                END
              )) / 60) AS in_flight_minutes
            FROM
              flights AS f
            INNER JOIN
              aircraft AS a ON a.serial_number = f.aircraft_id
            WHERE
              (
                f.departure_date >= '%(date_form)s' AND
                f.departure_date <= '%(date_to)s'
              )
              OR
              (
                f.arrival_date >= '%(date_form)s' AND
                f.arrival_date <= '%(date_to)s'
              );
            """ % {'date_to': date_to_formated, 'date_form': date_from_formated}
        )
        return queryset

    def handle_datetime(self, date_from, date_to):
        if not date_from or not date_to:
            return Response({"msg": "Need to select date_from and date_to"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            date_from_formated = str(datetime.fromisoformat(date_from).strftime('%Y-%m-%d %H:%M:%S%z')) + "+02"
            date_to_formated = str(datetime.fromisoformat(date_to).strftime('%Y-%m-%d %H:%M:%S%z'))+ "+02"
            return date_from_formated, date_to_formated
        except Exception as e:
            return Response({"msg": "Format not correct. DateTime : YYYY-MM-DDTHH:MM:SS "}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone
from drf_yasg.utils import swagger_serializer_method
from .models import (
    Aircraft,
    Flights,
    Airports
)

class RetrieveAircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['serial_number', 'manufacturer']


class UpdateAircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['manufacturer']


class RetrieveAirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airports
        fields = "__all__"

class CreateFlightsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flights
        fields = ['departure_airport', 'arrival_airport', 'departure_date', 'arrival_date', 'aircraft']
        extra_kwargs = {
            "departure_date": {
                "required": False
            },
            "arrival_date": {
                "required": False
            },
            "aircraft": {
                "required": False
            },
        }

    def validate_departure_date(self, value):
        if value is not None:
            try:
                if value < (datetime.now() + timedelta(days=1)).replace(tzinfo=timezone.utc):
                    raise serializers.ValidationError({"departure_date": "Departure date must be set at 1 day from current datetime"})
                return value
            except Exception as e:
                raise serializers.ValidationError(
                    {"departure_date": "Error format. DateTime : 23-08-22T20:00:00"})
        return None

    def validate(self, data):
            departure_date = data.get('departure_date', False)
            arrival_date = data.get('arrival_date', False)
            if departure_date and arrival_date:
                try:
                    if departure_date > arrival_date:
                        raise serializers.ValidationError({"arrival_date": "arrival_date must occur after departure_date"})
                    if departure_date and not arrival_date or not departure_date and arrival_date:
                        missing_value = departure_date if not departure_date else arrival_date
                        raise serializers.ValidationError({f"{missing_value}": f"{missing_value} is missing"})
                    return data
                except Exception as e:
                    raise serializers.ValidationError(
                        {"arrival_date": "Error format. DateTime : 23-08-22T20:00:00"})
            if 'departure_airport' and 'arrival_airport' not in data.keys():
                raise serializers.ValidationError({"departure_airport": "Required Field", "arrival_airport": "Required Field"})

            return data


class RetrieveFlightsSerializer(serializers.ModelSerializer):
    aircraft = RetrieveAircraftSerializer(read_only=True)
    departure_airport = RetrieveAirportSerializer(read_only=True)
    arrival_airport = RetrieveAirportSerializer(read_only=True)

    class Meta:
        model = Flights
        fields = '__all__'



class ReportSerializer(serializers.ModelSerializer):
    departure_airport = serializers.SerializerMethodField('get_departure_airport')
    in_flight_aircraft = serializers.SerializerMethodField('get_in_flight_aircraft')
    in_flight_minutes = serializers.SerializerMethodField('get_in_flight_minutes')

    class Meta:
        model = Flights
        fields = ['departure_airport', 'in_flight_aircraft', 'in_flight_minutes']

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_in_flight_minutes(self, object):
        return object.in_flight_minutes

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_in_flight_aircraft(self, object):
        return object.in_flight_aircraft

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_departure_airport(self, object):
        return object.departure_airport_id





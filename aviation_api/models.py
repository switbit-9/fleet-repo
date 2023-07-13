
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class Aircraft(models.Model):

    class Meta:
        db_table = 'aircraft'

    class ActiveAircraftObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(deleted_at__isnull=True)

    serial_number = models.CharField(primary_key=True)
    manufacturer = models.CharField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)
    activeobjects = ActiveAircraftObjects()
    objects = models.Manager()

    def __str__(self):
        return f"{self.manufacturer} : {self.serial_number}"



class Airports(models.Model):

    class Meta:
        db_table = 'airports'

    code = models.CharField(max_length=4, primary_key=True, validators=[
        RegexValidator(
            regex=r'^[A-Za-z0-9]{4}$',
            message="Field should be a 4 uppercase and number characters"
        )
    ])
    name = models.CharField(null=True, blank=True)
    city = models.CharField(null=True, blank=True)
    country = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.code}"



class Flights(models.Model):

    class Meta:
        db_table = 'flights'

    id = models.AutoField(primary_key=True)
    departure_airport = models.ForeignKey(
        "Airports",
        on_delete=models.PROTECT,
        related_name="departure_flights"
    )
    arrival_airport = models.ForeignKey(
        "Airports",
        on_delete=models.PROTECT,
        related_name="arrival_flights"
    )
    departure_date = models.DateTimeField(null=True, blank=True)
    arrival_date = models.DateTimeField(null=True, blank=True)
    aircraft = models.ForeignKey('Aircraft', on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id}"








from django.db import models


class Airplane(models.Model):
    airplane_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'airplane'


class BoardingPass(models.Model):
    boarding_pass_id = models.IntegerField(primary_key=True)
    purchase = models.ForeignKey('Purchase', models.DO_NOTHING, blank=True, null=True)
    passenger = models.ForeignKey('Passenger', models.DO_NOTHING, blank=True, null=True)
    seat_type = models.ForeignKey('SeatType', models.DO_NOTHING, blank=True, null=True)
    seat = models.ForeignKey('Seat', models.DO_NOTHING, blank=True, null=True)
    flight = models.ForeignKey('Flight', models.DO_NOTHING, blank=True, null=True, related_name='flight')

    class Meta:
        managed = False
        db_table = 'boarding_pass'


class Flight(models.Model):
    flight_id = models.IntegerField(primary_key=True)
    takeoff_date_time = models.IntegerField(blank=True, null=True)
    takeoff_airport = models.CharField(max_length=255, blank=True, null=True)
    landing_date_time = models.IntegerField(blank=True, null=True)
    landing_airport = models.CharField(max_length=255, blank=True, null=True)
    airplane = models.ForeignKey('Airplane', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flight'


class Passenger(models.Model):
    passenger_id = models.IntegerField(primary_key=True)
    dni = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger'


class Purchase(models.Model):
    purchase_id = models.IntegerField(primary_key=True)
    purchase_date = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase'


class Seat(models.Model):
    seat_id = models.IntegerField(primary_key=True)
    seat_column = models.CharField(max_length=2, blank=True, null=True)
    seat_row = models.IntegerField(blank=True, null=True)
    seat_type = models.ForeignKey('SeatType', models.DO_NOTHING, blank=True, null=True)
    airplane = models.ForeignKey('Airplane', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat'


class SeatType(models.Model):
    seat_type_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat_type'

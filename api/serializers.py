from rest_framework import serializers
from .models import (
        Airplane,
        BoardingPass,
        Flight,
        Passenger,
        Purchase,
        Seat,
        SeatType
    )


class PassengerSerializer(serializers.ModelSerializer):
    passengerId = serializers.IntegerField(read_only=True, source="passenger_id")
    dni = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.IntegerField()
    country = serializers.CharField()

    class Meta:
        model = Passenger
        fields = [
            'passengerId',
            'dni',
            'name',
            'age',
            'country',
        ]


class PurchaseSerializer(serializers.ModelSerializer):
    purchaseId = serializers.CharField(read_only=True, source='purchase_id')
    purchaseDate = serializers.IntegerField(source='purchase_date')

    class Meta:
        model = Purchase
        fields = [
            'purchaseId',
            'purchaseDate'
        ]


class AirplaneSerializer(serializers.ModelSerializer):
    airplaneId = serializers.IntegerField(read_only=True, source='airplane_id')
    name = serializers.CharField()

    class Meta:
        model = Airplane
        fields = [
            'airplaneId',
            'name'
        ]


class SeatTypeSerializer(serializers.ModelSerializer):
    seatTypeId = serializers.IntegerField(read_only=True, source='seat_type_id')
    name = serializers.CharField()

    class Meta:
        model = SeatType
        fields = [
            'seatTypeId',
            'name'
        ]


class SeatSerializer(serializers.ModelSerializer):
    seatId = serializers.IntegerField(read_only=True, source='seat_id')
    seatColumn = serializers.CharField(source='seat_column')
    seatRow = serializers.IntegerField(source='seat_row')
    seatType = SeatTypeSerializer(source='seat_type')
    airplane = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Seat
        fields = [
            'seatId',
            'seatColumn',
            'seatRow',
            'seatType',
            'airplane',
        ]
        depth = 1


class FlightSerializer(serializers.ModelSerializer):
    flightId = serializers.IntegerField(read_only=True, source='flight_id')
    takeoffDateTime = serializers.IntegerField(source='takeoff_date_time')
    takeoffAirport = serializers.CharField(source='takeoff_airport')
    landingDateTime = serializers.IntegerField(source='landing_date_time')
    landingAirport = serializers.CharField(source='landing_airport')
    airplane = AirplaneSerializer()

    class Meta:
        model = Flight
        fields = [
            'flightId',
            'takeoffDateTime',
            'takeoffAirport',
            'landingDateTime',
            'landingAirport',
            'airplane'
        ]
        depth = 3


class BoardingPassSerializer(serializers.ModelSerializer):
    boardingPassId = serializers.IntegerField(source='boarding_pass_id')
    purchaseId = serializers.PrimaryKeyRelatedField(read_only=True, source='purchase_id')
    passengerId = serializers.PrimaryKeyRelatedField(read_only=True, source='passenger_id')
    seatTypeId = serializers.PrimaryKeyRelatedField(read_only=True, source='seat_type')
    seatId = serializers.PrimaryKeyRelatedField(read_only=True, source='seat_id')
    flightId = serializers.PrimaryKeyRelatedField(read_only=True, source='flight_id')

    class Meta:
        model = BoardingPass
        fields = [
            'flightId',
            'passengerId',
            'boardingPassId',
            'purchaseId',
            'seatTypeId',
            'seatId'
        ]
        depth = 1

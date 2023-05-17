from django.contrib import admin
from .models import (
        Airplane,
        BoardingPass,
        Flight,
        Passenger,
        Purchase,
        Seat,
        SeatType
    )

# Register your models here.

admin.site.register(Airplane)
admin.site.register(BoardingPass)
admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Purchase)
admin.site.register(Seat)
admin.site.register(SeatType)

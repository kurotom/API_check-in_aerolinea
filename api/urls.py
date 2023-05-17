from django.urls import path
from .views import VuelosAPI

urlpatterns = [
        path(
            'flights/<int:vueloID>/passengers',
            VuelosAPI.as_view(),
            name='apiFlights'
        )
]

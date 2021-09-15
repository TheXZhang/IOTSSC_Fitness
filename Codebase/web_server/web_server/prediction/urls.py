from django.urls import path

from .views import *

show_realtime = PredictionViewSet.as_view({"get": "real_time"})

show_historical = PredictionViewSet.as_view({"get": "historical"})

urlpatterns = [
    # ex: /api/mobile/booking/cancel/booking_id/
    path("realtime/", show_realtime, name="realtime_pred"),
    # ex: /api/mobile/booking/limits/
    path("historical/", show_historical, name="historical_pred"),
]
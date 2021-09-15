from rest_framework import serializers
from .models import *


class PredictionSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=None)
    timestamp = serializers.CharField(default=None)
    classification = serializers.CharField(default=None)

    class Meta:
        model = Classification
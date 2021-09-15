from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Classification
from .serializers import PredictionSerializer
from rest_framework.permissions import IsAuthenticated


class PredictionViewSet(viewsets.ViewSet):

    def real_time(self, request: Request):

        result = Classification.objects.all()
        result = result.last()
        if result.exists():
            response = dict(status=True,
                            message=PredictionSerializer(instance=result).data)
        else:
            response = dict(status=False,
                            message=None)

        return Response(response)

    def historical(self, request: Request):
        result = Classification.objects.all()

        if result.exists():
            response = dict(status=True,
                            message=PredictionSerializer(instance=result, many=True).data)
        else:
            response = dict(status=False,
                            message=None)

        return Response(response)

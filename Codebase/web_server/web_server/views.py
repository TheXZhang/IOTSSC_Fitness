from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class IndexViewSet(viewsets.ViewSet):

    def index(self, request: Request):

        output = dict(status=True)

        return Response(output)

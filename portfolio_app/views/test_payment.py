from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TestWorkshopOrderView(APIView):
    def post(self, request):
        return Response({"message": "Test workshop order view working", "data": request.data}, status=status.HTTP_200_OK)

class TestServiceOrderView(APIView):
    def post(self, request):
        return Response({"message": "Test service order view working", "data": request.data}, status=status.HTTP_200_OK)
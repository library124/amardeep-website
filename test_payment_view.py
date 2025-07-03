from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TestPaymentView(APIView):
    def post(self, request):
        return Response({"message": "Test payment view working"}, status=status.HTTP_200_OK)
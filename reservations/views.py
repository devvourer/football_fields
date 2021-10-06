from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from.serializers import ReservationSerializer
from .models import Reservation


class ReservationView(APIView):
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        serializer = ReservationSerializer(data=request.data, context={'user': request.user.id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




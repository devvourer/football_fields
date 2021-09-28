from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet

from .serializers import FieldSerializer


class FieldView(mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = FieldSerializer



class GameView():
    pass
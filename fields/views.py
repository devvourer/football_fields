from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from .serializers import FieldSerializer, GameSerializer, JoinToGameSerializer
from .models import Field, Game
from .permissions import IsOwner
from .fields_services import send_request_to_game

from users.models import User


class FieldViewSet(ViewSet):
    serializer_class = FieldSerializer
    queryset = Field.objects.all()


    def get_permissions(self):
        """ Доступ для изменения и создания имеют только админ и владелец """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser, IsOwner]

        return [permission() for permission in permission_classes]

    def list(self, request):
        serializer = FieldSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        field = get_object_or_404(self.queryset, pk=pk)
        serializer = FieldSerializer(field)
        return Response(serializer.data)

    def create(self, request):
        serializer = FieldSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        field = serializer.save()
        return self.retrieve(request, pk=field.pk)

    def partial_update(self, request, pk=None):
        field = get_object_or_404(self.queryset, pk=pk)
        serializer = FieldSerializer(field, partial=True)
        return Response(serializer.data)


class GameViewSet(ViewSet):
    queryset = Game.objects.filter(is_active=True)
    serializer_class = GameSerializer

    def get_permissions(self):
        if self.action == 'partial_update':
            permission_classes = [IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        serializer = GameSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        serializer = GameSerializer(game)
        # if game.owner == request.user:
        #     serializer = GameSerializer(game, context={'owner': True})
        # else:
        #     serializer = GameSerializer(game, context={'owner': False})
        return Response(serializer.data)

    def create(self, request):
        serializer = GameSerializer(data=request.data, context={'user': request.user.id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        game = serializer.save()
        return self.retrieve(request, pk=game.pk)

    def partial_update(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        serializer = GameSerializer(game, partial=True)
        return Response(serializer.data)


class JoinToGameView(APIView):

    def get(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            sender = request.user.phone
            send_request_to_game(sender, game.owner.phone, pk)
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({'error': 'Не удалось отправить запрос на присоединение к игре'},
                            status=status.HTTP_400_BAD_REQUEST)


class AcceptUserView(APIView):

    def get(self, request, game_id, sender_id):
        try:
            game = Game.objects.get(id=game_id)
            sender = User.objects.get(id=sender_id)
            if request.user == game.owner:
                game.played_users.add(sender)
                print(game.played_users.count())
                print(game.need_players)
                if game.played_users.count() == game.need_players:
                    game.is_active = False
                    game.save(update_fields=['is_active'])

                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)



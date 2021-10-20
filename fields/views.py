from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from .serializers import FieldSerializer, GameSerializer, FavouriteFieldSerializer, ReservationSerializer
from .models import Field, Game, FavouriteField
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
        queryset = Field.objects.all()
        serializer = FieldSerializer(queryset, many=True)
        test.delay('hehllo')
        if request.GET.get('price_ot'):
            price_ot = request.GET.get('price_ot')
            price_do = request.GET.get('price_do')
            queryset = Field.objects.filter(price__gte=price_ot, price__lte=price_do)
            serializer = FieldSerializer(queryset, many=True)
        if request.GET.get('service'):
            service = request.GET.get('service').split(',')
            queryset = queryset.filter(services__name__in=service)
            serializer = FieldSerializer(queryset, many=True)
        if request.GET.get('location'):
            location = request.GET.get('location').split(',')
            queryset = queryset.filter(location__in=location)
            serializer = FieldSerializer(queryset, many=True)
        if request.GET.get('type'):
            field_type = request.GET.get('type').split(',')
            queryset = queryset.filter(type__in=field_type)
            serializer = FieldSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        field = get_object_or_404(self.queryset, pk=pk)
        serializer = FieldSerializer(field)
        return Response(serializer.data)

    def create(self, request):
        serializer = FieldSerializer(data=request.data, context={'request': request})
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
        queryset = Game.objects.all()
        serializer = GameSerializer(queryset, many=True)

        if request.GET.get('price_ot'):
            price_ot = request.GET.get('price_ot')
            price_do = request.GET.get('price_do')
            queryset = queryset.filter(price__gte=price_ot, price__lte=price_do)
            serializer = GameSerializer(queryset, many=True)
        if request.GET.get('age_ot'):
            age_ot = request.GET.get('age_ot')
            age_do = request.GET.get('age_do')
            queryset = queryset.filter(age__gte=age_ot, age__do=age_do)
            serializer = GameSerializer(queryset, many=True)
        if request.GET.get('match_type'):
            match_type = request.GET.get('match_type').split(',')
            queryset = queryset.filter(match_type__in=match_type)
            serializer = GameSerializer(queryset, many=True)
        if request.GET.get('location'):
            location = request.GET.get('location').split(',')
            queryset = queryset.filter(location__in=location)
            serializer = GameSerializer(queryset, many=True)

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
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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


class UserGameView(APIView):
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Game.objects.filter(owner=request.user)
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)


class FavouriteFieldView(APIView):
    serializer_class = FavouriteFieldSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = FavouriteField.objects.filter(user=request.user)
        serializer = FavouriteFieldSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        try:
            field = Field.objects.get(pk=request.data['field'])
            check = FavouriteField.objects.get(user=request.user, field=field) or None
            if check:   # если поле уже в избранном не создавать новую запись в бд
                serializer = FavouriteFieldSerializer(check)
                return Response(serializer.data, status=status.HTTP_200_OK)

            favourite = FavouriteField.objects.create(user=request.user, field=field)
            serializer = FavouriteFieldSerializer(favourite)
        except Exception as e:
            print(e)
            return Response({'ошибка': 'неудалось добавить в избранное'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReservationView(APIView):
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data, context={'user': request.user.id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print(serializer.validated_data)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


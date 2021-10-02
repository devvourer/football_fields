from django.shortcuts import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login, logout

from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    UserCreateSerializer, UserActivateSerializer,
    LoginSerializer, ResetPhoneSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer
)
from .models import User
from .user_services import send_code, send_code_to_reset_pwd
from .backends import authenticate


class Register(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        user.is_active = False
        user.save()

        request.session['phone'] = user.phone

        # send activation code to user phone number
        send_code(user.phone)
        return HttpResponseRedirect(reverse('activate'))


class Activate(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserActivateSerializer

    def get(self, request):
        print(request.session['phone'])
        serializer = UserActivateSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = UserActivateSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(phone=request.session['phone'])
            code = serializer.validated_data['code']
            if user.code == code:
                user.is_active = True
                user.save(update_fields=['is_active'])
                user_auth = authenticate(request)
                print(user_auth)
                if user is not None:
                    login(request, user_auth)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                return Response(status=status.HTTP_201_CREATED)
            else:
                serializer = UserActivateSerializer()
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def get(self, request):
        serializer = LoginSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                user = User.objects.get(phone=data['phone'], password=data['password'])
            except User.DoesNotExist:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(APIView):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class ResetPhoneView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResetPhoneSerializer

    def get(self, request):
        serializer = ResetPhoneSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = ResetPhoneSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            request.user.phone = serializer.validated_data['new_phone']
            request.user.save(update_fields=['phone'])
            return Response({'reset_phone': 'номер успешно изменен'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def get(self, request):
        serializer = ForgotPasswordSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(phone=serializer.validated_data['phone'])
                user.code = user.generate_code()
                user.save(update_fields=['code'])

                send_code_to_reset_pwd(user.phone, user.code)
                return Response({'send_url': 'сообщение для сброса пароля отправленно'},
                                status=status.HTTP_202_ACCEPTED)

            except User.DoesNotExist:
                return Response({'user': 'Пользователь с таким номером не найден'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def get(self, request, phone, code):
        serializer = ResetPasswordSerializer()
        return Response(serializer.data)

    def post(self, request, phone, code):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(phone=phone)
                user.password = serializer.validated_data['password']
                user.save(update_fields=['password'])
                login(request, user)
                return Response({'user': 'Пароль успешно сброшен'}, status=status.HTTP_202_ACCEPTED)

            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)






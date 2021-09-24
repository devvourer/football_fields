from django.urls import path

from . import views


urlpatterns = [
    path('', views.FieldView),
    path('game/', views.GameView),
]
from django.urls import path

from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('fields', views.FieldViewSet, basename='field')
router.register('game', views.GameViewSet, basename='game')

urlpatterns = [
    # path('fields/', views.FieldViewSet.as_view({'get': 'list'}), name='field')
    path('game/<int:pk>/join/', views.JoinToGameView.as_view(), name='join'),
    path('game/<int:game_id>/<int:sender_id>', views.AcceptUserView.as_view(), name='accept'),
]

urlpatterns += router.urls

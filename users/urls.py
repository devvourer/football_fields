from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('register/activate/', views.Activate.as_view(), name='activate'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('profile/', views.ProfileView),
]

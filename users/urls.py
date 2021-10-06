from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('register/activate/', views.Activate.as_view(), name='activate'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('reset_phone/', views.ResetPhoneView.as_view(), name='reset_phone'),
    path('forgot_password/', views.ForgotPasswordView.as_view(), name='forgot_pwd'),
    path('<int:phone>/<int:code>/reset/', views.ResetPasswordView.as_view(), name='reset_pwd'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]

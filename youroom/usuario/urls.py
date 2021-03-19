from django.urls import path
from .views import LoginView, HomeView
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('logout/', logout_then_login, name='logout')
]
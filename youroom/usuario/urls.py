from django.urls import path
from .views import LoginView
from django.contrib.auth.views import logout_then_login
from timeline import urls as timeline_urls
from django.urls import include, path

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('', include(timeline_urls), name='home'),
    path('logout/', logout_then_login, name='logout')
]

from django.urls import path
from .views import LoginView, RegistroView
from django.contrib.auth.views import logout_then_login
from timeline import urls as timeline_urls
from django.urls import include

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('', include(timeline_urls)),
    path('logout/', logout_then_login, name='logout'),
    path('registro/', RegistroView.as_view(), name='registro')
]

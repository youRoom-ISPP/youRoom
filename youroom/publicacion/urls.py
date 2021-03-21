from django.urls import path
from .views import FormPubView

urlpatterns = [
    path('new/', FormPubView.as_view())
]
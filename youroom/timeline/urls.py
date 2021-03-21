from django.urls import path
from .views import TimelineView

urlpatterns = [
    path('', TimelineView.as_view())
]
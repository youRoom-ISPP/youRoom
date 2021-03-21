from django.urls import path
from .views import TimelineView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('timeline/', login_required(TimelineView.as_view()), name='timeline')
]

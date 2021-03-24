from django.urls import path
from .views import TimelineView
from django.contrib.auth.decorators import login_required
from ranking.views import ValorarPublicacionView

urlpatterns = [
    path('', login_required(TimelineView.as_view()), name='timeline'),
    path('valorar/', ValorarPublicacionView.as_view(), name='publicacion_valorar'),
]

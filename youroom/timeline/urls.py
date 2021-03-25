from django.urls import path
from .views import TimelineView, TimelineViewCategorias
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(TimelineView.as_view()), name='timeline'),
    path('<categoria>', login_required(TimelineViewCategorias.as_view()), name='timeline_categoria')
]

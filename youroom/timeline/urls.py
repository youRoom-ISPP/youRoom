from django.urls import path
from .views import TimelineView, TimelineViewCategorias, TimelineViewValoraciones
from django.contrib.auth.decorators import login_required
from ranking import urls as ranking_urls
from django.urls import include

urlpatterns = [
    path('', login_required(TimelineView.as_view()), name='timeline'),
    path('valoraciones/', login_required(TimelineViewValoraciones.as_view()), name='timeline_valoraciones'),
    path('', include(ranking_urls)),
    path('<categoria>', login_required(TimelineViewCategorias.as_view()), name='timeline_categoria')
]

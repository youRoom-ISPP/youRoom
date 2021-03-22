from django.shortcuts import render
from django.views.generic import TemplateView
from publicacion.models import Publicacion


class TimelineView(TemplateView):
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publicaciones'] = Publicacion.objects.all()
        return context

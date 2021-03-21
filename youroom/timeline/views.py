from django.shortcuts import render
from django.views.generic import TemplateView

class TimelineView(TemplateView):
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['n'] = range(10)
        return context

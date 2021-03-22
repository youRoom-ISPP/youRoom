from django.shortcuts import render
from django.views.generic import TemplateView

class TimelineView(TemplateView):
    template_name = 'timeline/timeline.html'

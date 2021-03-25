from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView

class RankingView(TemplateView):
    template_name = 'ranking/ranking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = User.objects.all()
        return context

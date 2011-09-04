from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from cablegate.cable.models import *


class CableView(DetailView):
    template_name = 'cable/cable_detail.html'
    model = Cable
    def get_context_data(self, **kwargs):
        context = super(CableView, self).get_context_data(**kwargs)
        return context


class CableListView(DetailView):
    template_name = 'cable/cable_list.html'
    paginate_by = 8
    def get_context_data(self, **kwargs):
        context = super(CableListView, self).get_context_data(**kwargs)
        return context


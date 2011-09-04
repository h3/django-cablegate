from django.conf.urls.defaults import *
from django.conf import settings
from cablegate.cable.views import *

urlpatterns=patterns('',
    url(r'^cables/$',                   CableListView.as_view(),    name='cable-list'),
    url(r'^cables/(?P<pk>[\-\d]+)/$',   CableView.as_view(),        name='cable-view'),
)


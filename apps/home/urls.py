# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('landing', views.landing),
    path('range', views.range),
    path('final', views.final,),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    #path('', views.pie_chart, name='pie-chart'),
]

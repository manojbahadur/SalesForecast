# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # The home page
    #path('', views.index, name='home'),
    path('', views.index, name='home'),
    path('landing', views.landing),

    # Matches any html file
    path(r'^.*\.*', views.pages, name='pages'),
    #path('', views.pie_chart, name='pie-chart'),
    re_path(r'^.*\.*', views.population_chart, name='population_chart')
]

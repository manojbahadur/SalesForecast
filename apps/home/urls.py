# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page

    #path('', views.index, name='home'),
    path('', views.index, name='home'),
    path('landing', views.landing),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),

]

# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from json import dumps


@login_required(login_url="/login/")
def index(request):
    store = pd.read_csv("C:/Users/manoj/OneDrive/Documents/GitHub/hope/apps/templates/csv/stores.csv")
    gk = store.groupby('Type').mean()

    mylabels = ["A", "B", "C"]
    context = {
        'segment': 'index',
        'labels': mylabels,
        'data': [177247.727273,101190.705882,40541.666667]
        }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    labels = ["a", "b", "c", "d", "e", "f", "g", "h"]
    data = [100, 200, 120, 230, 123, 100, 123, 235]
    context = {}
    val = {"labels": labels,
           "data": data}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def landing(self):
    html_template = loader.get_template('home/landing.html')
    return HttpResponse(html_template.render())

def population_chart():
    labels = ["a", "b", "c", "d", "e", "f", "g", "h"]
    data = [100, 200, 120, 230, 123, 100, 123, 235]
    context = {
        "labels": labels,
        "data": data,
    }

    return render(context, 'home/index.html')

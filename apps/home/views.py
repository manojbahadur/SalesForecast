# -*- encoding: utf-8 -*-
import os
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import pandas as pd
import numpy as np
import range

@login_required(login_url="/login/")
def index(request):

    path=os.getcwd()
    
    train_data = pd.read_csv(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/csv/train.csv"),delimiter=',')
    #train_data = pd.read_csv('train.csv')
    total_sales_for_each_store = train_data.groupby('Store')['Weekly_Sales'].sum()
    total_sales_for_each_store_array = np.array(total_sales_for_each_store)
    print(total_sales_for_each_store_array)
    mylabels = list(range(1,46))
    context = {
        'segment': 'index',
        'labels': mylabels,
        'data': total_sales_for_each_store_array
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


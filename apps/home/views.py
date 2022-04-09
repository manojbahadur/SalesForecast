# -*- encoding: utf-8 -*-
import os
from datetime import datetime
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from datetime import datetime
import pandas as pd
import numpy as np


@login_required(login_url="/login/")
def index(request):
    context = dataVisualization()
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
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

# Index Page Data Visualization
def dataVisualization():

    # Load the data
    path=os.getcwd()
    #train_df = pd.read_csv(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/csv/train.csv"),delimiter=',')
    features_df = pd.read_csv(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/csv/features.csv"),delimiter=',')
    stores_df = pd.read_csv(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/csv/stores.csv"),delimiter=',')
    #test_df = pd.read_csv(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/csv/test.csv"),delimiter=',')
    features_df['Date'] =  pd.to_datetime(features_df['Date'])
    features_df["Day"]= pd.DatetimeIndex(features_df['Date']).day
    features_df['Month'] = pd.DatetimeIndex(features_df['Date']).month
    features_df['Year'] = pd.DatetimeIndex(features_df['Date']).year


    # 1st Chart for yearly sales
    yearly_sales_2010 = features_df[(features_df['Date'] > '2010-01-01') & (features_df['Date'] < '2010-12-31')].groupby(['Year','Month'])['Weekly_Sales'].sum()
    yearly_sales_2011 = features_df[(features_df['Date'] > '2011-01-01') & (features_df['Date'] < '2011-12-31')].groupby(['Year','Month'])['Weekly_Sales'].sum()
    yearly_sales_2012 = features_df[(features_df['Date'] > '2012-01-01') & (features_df['Date'] < '2012-12-31')].groupby(['Year','Month'])['Weekly_Sales'].sum()
    mylabels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
    

    # Pie chart for store type
    store_type_data = stores_df.groupby('Type').sum()


    # Pie chart for total sales
    yearly_sales_pie_chart = features_df.groupby("Year")[["Weekly_Sales"]].sum()
        
        
    # Bar chart for weekly sales   
    #data = pd.read_csv('features.csv') 
    dataset = features_df.merge(stores_df, how='inner', on='Store')
    dataset['Week'] = dataset.Date.dt.week # for the week data
    dataset['Year'] = dataset.Date.dt.year # for the year data
    train_merge = pd.read_csv(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/csv/features.csv"),delimiter=',')
    train_merge['Date'] =  pd.to_datetime(train_merge['Date'])
    train_merge["Day"]= pd.DatetimeIndex(train_merge['Date']).day
    train_merge['Month'] = pd.DatetimeIndex(train_merge['Date']).month
    train_merge['Year'] = pd.DatetimeIndex(train_merge['Date']).year
    train_merge['Week'] = train_merge.Date.dt.week # for the week data
    train_merge['Year'] = train_merge.Date.dt.year # for the year data

    weekly_sales_2010 = train_merge[train_merge['Year']==2010]['Weekly_Sales'].groupby(train_merge['Week']).mean()
    weekly_sales_2012 = train_merge[train_merge['Year']==2012]['Weekly_Sales'].groupby(train_merge['Week']).mean()
    weekly_sales_2011 = train_merge[train_merge['Year']==2011]['Weekly_Sales'].groupby(train_merge['Week']).mean()



    #Sales for holiday bar chart
    Super_Bowl =['12-2-2010', '11-2-2011', '10-2-2012']
    Labour_Day =  ['10-9-2010', '9-9-2011', '7-9-2012']
    Thanksgiving =  ['26-11-2010', '25-11-2011', '23-11-2012']
    Christmas = ['31-12-2010', '30-12-2011', '28-12-2012']

    Super_Bowl_df = pd.DataFrame(features_df.loc[features_df.Date.isin(Super_Bowl)].groupby('Year')['Weekly_Sales'].sum())
    Thanksgiving_df = pd.DataFrame(features_df.loc[features_df.Date.isin(Thanksgiving)].groupby('Year')['Weekly_Sales'].sum())
    Labour_Day_df = pd.DataFrame(features_df.loc[features_df.Date.isin(Labour_Day)].groupby('Year')['Weekly_Sales'].sum())
    Christmas_df = pd.DataFrame(features_df.loc[features_df.Date.isin(Christmas)].groupby('Year')['Weekly_Sales'].sum())

    a = [Super_Bowl_df.values[0][0],Super_Bowl_df.values[1][0],Super_Bowl_df.values[2][0]]
    b = [Thanksgiving_df.values[0][0],Thanksgiving_df.values[1][0],68042461.04]
    c = [Labour_Day_df.values[0][0],Labour_Day_df.values[1][0],50042461.04]
    d = [Christmas_df.values[0][0],Christmas_df.values[1][0],56042461.0423]


    context = {
        'segment': 'index',
        'total_sales_labels': mylabels,
        'total_sales_data_2010': list(yearly_sales_2010),
        'total_sales_data_2011': list(yearly_sales_2011),
        'total_sales_data_2012': list(yearly_sales_2012),
        'store_type_data': list(store_type_data['Size']),
        "yearly_sales_pie_chart": list(yearly_sales_pie_chart['Weekly_Sales']),
        "weekly_sales_2010":list(weekly_sales_2010),
        "weekly_sales_2011": list(weekly_sales_2011),
        "weekly_sales_2012": list(weekly_sales_2012),
        "weekly_sales_labels_2010": list(weekly_sales_2010.index),
        "weekly_sales_labels_2011": list(weekly_sales_2011.index),
        "weekly_sales_labels_2012": list(weekly_sales_2012.index),
        "super_bowl": a,
        "thanks_giving": b,
        "labour_day": c,
        "christmas_day": d
        }
    
    return context
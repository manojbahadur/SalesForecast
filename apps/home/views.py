import os
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from datetime import datetime
import pandas as pd
import pickle
import datetime
from datetime import timedelta
import xgboost
from sklearn import preprocessing
from numpy import int64
from numpy import int8
import json

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
    train_df = pd.read_csv(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/csv/train.csv"),delimiter=',')
    features_df = pd.read_csv(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/csv/train.csv"),delimiter=',')
    stores_df = pd.read_csv(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/csv/stores.csv"),delimiter=',')

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
    train_merge = pd.read_csv(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/csv/train.csv"),delimiter=',')
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

    train_df["Day"]= pd.DatetimeIndex(train_df['Date']).day
    train_df['Month'] = pd.DatetimeIndex(train_df['Date']).month
    train_df['Year'] = pd.DatetimeIndex(train_df['Date']).year

    Super_Bowl =['2010-02-12', '2011-02-11', '2012-02-10']
    Labour_Day =  ['2010-09-10', '2011-09-09', '2012-09-07']
    Thanksgiving =  ['2010-11-26', '2011-11-25']
    Christmas = ['2010-12-31', '2011-12-30']

    Super_Bowl_df = pd.DataFrame(train_df.loc[train_df.Date.isin(Super_Bowl)].groupby('Year')['Weekly_Sales'].sum())
    Thanksgiving_df = pd.DataFrame(train_df.loc[train_df.Date.isin(Thanksgiving)].groupby('Year')['Weekly_Sales'].sum())
    Labour_Day_df = pd.DataFrame(train_df.loc[train_df.Date.isin(Labour_Day)].groupby('Year')['Weekly_Sales'].sum())
    Christmas_df = pd.DataFrame(train_df.loc[train_df.Date.isin(Christmas)].groupby('Year')['Weekly_Sales'].sum())

    a = Super_Bowl_df['Weekly_Sales'].tolist()
    b = Thanksgiving_df['Weekly_Sales'].tolist()
    c = Labour_Day_df['Weekly_Sales'].tolist()
    d = Christmas_df['Weekly_Sales'].tolist()

    context = {
        'segment': 'index',
        'total_sales_labels': mylabels,
        'total_sales_labels_2010': mylabels[1::],
        'total_sales_labels_2012': mylabels[0:-2],
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

def range(request):
    context = {}
    html_template = loader.get_template('home/range.html')
    return HttpResponse(html_template.render(context,request))

def final(request):

    path = os.getcwd()

    with open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/wmae_list.pkl"),'rb') as f:
        # load using pickle de-serializer
        wmae_list = pickle.load(f)

    with open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/mean_vals.pkl"),'rb') as g:
        # load using pickle de-serializer
        mean_vals = pickle.load(g)

    with open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/XGBRegressor.pkl"),'rb') as h:
        # load using pickle de-serializer
        XGB = pickle.load(h)

    with open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/LinearRegression.pkl"),'rb') as i:
        # load using pickle de-serializer
        LR = pickle.load(i)

    with open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/KNeighborsRegressor.pkl"),'rb') as j:
        # load using pickle de-serializer
        KNN = pickle.load(j)

    #wmae_list = pickle.load(open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/wmae_list.pkl")),'rb')
    #mean_vals = pickle.load(open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/mean_vals.pkl")),'rb')
    #XGB = pickle.load(open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/XGBRegressor.pkl")),'rb')
    #LR = pickle.load(open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/pickles/LinearRegression.pkl")), 'rb')
    #KNN = pickle.load(open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/pickles/KNeighborsRegressor.pkl")), 'rb')

    df_1 = pd.DataFrame(mean_vals).transpose()
   
    #print("final..........",request.POST)
    date = request.POST.get('date_range')
    store = request.POST.get('store')
    dept = request.POST.get('department')
    store_type = request.POST.get('type')
    str(date)
    #print("date.........",date)
    #date = datetime.datetime.strptime(str(date), '%d/%m/%y')
    user = {'Store': store,
            'Dept': dept,
            'Type': store_type,
            'Date': date }
    df = pd.DataFrame(user,index=[0])
    df['Date'] = pd.to_datetime(df.Date, format='%d/%m/%y')

    '''print(date)
    print(store)
    print(dept)
    print(store_type)'''

    def nearest_fri(df, date_column):
        month_delta = 4
        dayofweek = df[date_column].dt.dayofweek
        if (int(dayofweek != month_delta)):
            x = month_delta - dayofweek
            # print("HI THIS IS X VAL",x[0])
            y = x[0]
            y = int(y)
            y = abs(y)
            # print(y)
            if (int(dayofweek > month_delta)):
                dayofweek - y
                df["Date"] = df["Date"] - timedelta(days=y)
            elif (int(dayofweek < month_delta)):
                dayofweek + y
                df["Date"] = df["Date"] + timedelta(days=y)

        return df

    df_test = nearest_fri(df, "Date")
    df = df_test

    def split_dates(df, date_column):
        date_df = pd.DataFrame({"year": df[date_column].dt.year,
                                "month": df[date_column].dt.month,
                                "day": df[date_column].dt.day,
                                "dayofyear": df[date_column].dt.dayofyear,
                                "week": df[date_column].dt.week,
                                "weekofyear": df[date_column].dt.weekofyear,
                                "dayofweek": df[date_column].dt.dayofweek,
                                "weekday": df[date_column].dt.weekday,
                                "quarter": df[date_column].dt.quarter,
                                })
        df = df.drop(date_column, axis=1)
        df = pd.concat([df, date_df], axis=1)
        return df

    df_2 = split_dates(df, "Date")
    final_df = pd.concat([df_2, df_1], axis=1)

    '''print("------------------")
    print(final_df.dtypes)'''

    lbl = preprocessing.LabelEncoder()
    final_df['Store'] = lbl.fit_transform(final_df['Store'].astype(int64))
    final_df['Dept'] = lbl.fit_transform(final_df['Dept'].astype(int64))
    final_df['Type'] = lbl.fit_transform(final_df['Type'].astype(int8))

    m1 = LR.predict(final_df)
    m2 = KNN.predict(final_df)
    m3 = XGB.predict(final_df)

    data=[int(m1),int(m2),int(m3)]
    #print("table data.....",data)
    
    context = {
        "wmae_xgb": "{:.2f}".format(wmae_list.iloc[0][1]),
        "wmae_knn": "{:.2f}".format(wmae_list.iloc[2][1]),
        "wmae_lr": "{:.2f}".format(wmae_list.iloc[3][1]),
        "lr": int(m1),
        "knn": int(m2),
        "xgb": int(m3),
        "bar_data": data
        }
    html_template = loader.get_template('home/final.html')
    return HttpResponse(html_template.render(context,request))


'''def process():
    path=os.getcwd()
    wmae_list = pickle.load(open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/pickles/wmae_list.pkl")),'rb')
    mean_vals = pickle.load(open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)),"hope/apps/templates/pickles/mean_vals.pkl")),'rb')
    XGB = pickle.load(open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/XGBRegressor.pkl")),'rb')
    LR = pickle.load(open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/LinearRegression.pkl")),'rb')
    KNN = pickle.load(open(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "hope/apps/templates/pickles/KNeighborsRegressor.pkl")),'rb')

    df_1 = pd.DataFrame(mean_vals).transpose()

    #TAKE USER INPUT HERE
    user = {'Store': [1],
            'Dept': [1],
            'Type': [1],
            'Date': ['2010-05-12'], }
    df = pd.DataFrame(user)
    df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')

    def nearest_fri(df, date_column):
        month_delta = 4
        dayofweek = df[date_column].dt.dayofweek
        if (int(dayofweek != month_delta)):
            x = month_delta - dayofweek
            # print("HI THIS IS X VAL",x[0])
            y = x[0]
            y = int(y)
            y = abs(y)
            # print(y)
            if (int(dayofweek > month_delta)):
                dayofweek - y
                df["Date"] = df["Date"] - timedelta(days=y)
            elif (int(dayofweek < month_delta)):
                dayofweek + y
                df["Date"] = df["Date"] + timedelta(days=y)

        return df

    df_test = nearest_fri(df, "Date")
    df = df_test

    def split_dates(df, date_column):
        date_df = pd.DataFrame({"year": df[date_column].dt.year,
                                "month": df[date_column].dt.month,
                                "day": df[date_column].dt.day,
                                "dayofyear": df[date_column].dt.dayofyear,
                                "week": df[date_column].dt.week,
                                "weekofyear": df[date_column].dt.weekofyear,
                                "dayofweek": df[date_column].dt.dayofweek,
                                "weekday": df[date_column].dt.weekday,
                                "quarter": df[date_column].dt.quarter,
                                })
        df = df.drop(date_column, axis=1)
        df = pd.concat([df, date_df], axis=1)
        return df

    df_2 = split_dates(df, "Date")
    final_df = pd.concat([df_2, df_1], axis=1)

    m1 = LR.predict(final_df)
    m2 = KNN.predict(final_df)
    m3 = XGB.predict(final_df)'''
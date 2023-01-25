from datetime import datetime as dt

from dash.dependencies import Input
from dash.dependencies import Output
import boto3
import time, os
import botocore
import pandas as pd
from dash.dependencies import State
from flask_login import current_user
import pandas_datareader as pdr
import plotly.express as px
import numpy as np

all_options = {
    'Purchase_Intent_N12Mnths': ['Purchase_Intent_N12Mnths_Used Car','Purchase_Intent_N12Mnths_New Car', 'Purchase_Intent_N12Mnths_Domestic Holiday', 'Purchase_Intent_N12Mnths_International Holiday', 'Purchase_Intent_N12Mnths_Regional Australia Holiday', 'Purchase_Intent_N12Mnths_Caravan', 'Purchase_Intent_N12Mnths_Boat', 'Purchase_Intent_N12Mnths_General furniture',
    'Purchase_Intent_N12Mnths_White goods', 'Purchase_Intent_N12Mnths_Small electrical goods', 'Purchase_Intent_N12Mnths_Computer / Tablet / iPad', 'Purchase_Intent_N12Mnths_Mobile / Smartphone', 'Purchase_Intent_N12Mnths_Renovation materials'],

    'Purchase_Intent_N6Mnths': [u'Purchase_Intent_N6Mnths_Garden / Nursery Products', 'Purchase_Intent_N6Mnths_Apparel / Shoes / Accessories', 'Purchase_Intent_N6Mnths_Sport / Fitness Products', 'Purchase_Intent_N6Mnths_Health / Beauty Products', 'Purchase_Intent_N6Mnths_Homewares', 'Purchase_Intent_N6Mnths_Outdoor Clothing / Equipment', 'Purchase_Intent_N6Mnths_Car Parts & Accessories'],
     
    'CarPurchase' : [u'CarPurchase_SmallCarSUV', 'CarPurchase_LargeCarSUV', 'CarPurchase_UteVan'],

    'Property_Intentions' : [u'Property_Intentions_Buy home to live in', 'Property_Intentions_Buy an investment property', 'Property_Intentions_Sell a property', 'Property_Intentions_Rent a new property to live in', 'Property_Intentions_Move house', 'Property_Intentions_Build / rebuild a home',
    'Property_Intentions_Renovations' 'First_Home_Buyer'],

    'Activities_N6Mnths' : [u'Activities_N6Mnths_Purchase or reassess life insurance', 'Activities_N6Mnths_Purchase or reassess health insurance', 'Activities_N6Mnths_Purchase or reassess motor vehicle insurance', 'Activities_N6Mnths_Purchase or reassess home/contents insurance',  'Activities_N6Mnths_Reassess who I bank with',
    'Activities_N6Mnths_Obtain or reassess a mortgage', 'Activities_N6Mnths_Sign up or reassess a mobile phone plan', 'Activities_N6Mnths_Sign up or reassess an internet plan', "Activities_N6Mnths_Sign up to a new streaming service I've not used previously (e.g. Netflix)", 'Activities_N6Mnths_Re-subscribe to a streaming service I had previously cancelled',
    'Activities_N6Mnths_Change or reassess superannuation funds', 'Activities_N6Mnths_Change electricity/gas supplier', 'Activities_N6Mnths_Obtain or reassess a car loan', 'Activities_N6Mnths_Obtain or reassess a personal loan', 'Activities_N6Mnths_Start or reassess a gym/fitness centre membership',  'Activities_N6Mnths_Look for or start a new career / role'],

    'Activities_N1Mnths' : [u'Activities_N1Month_Purchase fast food',  'Activities_N1Month_Purchase home delivery of food (e.g. Uber Eats)', 'Activities_N1Month_Purchase takeaway from a restaurant', 'Activities_N1Month_Dine in at a restaurant / caf�', 'Activities_N1Month_Visit a pub / bar', 'Activities_N1Month_Purchase home delivered meal kit / ready-made meal service', 'Activities_N1Month_Visit a gym / fitness centre',
    'Activities_N1Month_Visit a shopping centre',  'Activities_N1Month_Visit a cinema','Activities_N1Month_Visit an art gallery / museum',  'Activities_N1Month_Gamble on sport  racing or lotteries', 'Activities_N1Month_Purchase alcohol from a bottle shop / alcohol retailer'],

    'Alcohol_Types' : [u'Alcohol_Types_Beer', 'Alcohol_Types_Scotch / Whisky', 'Alcohol_Types_Dark Rum', 'Alcohol_Types_Bourbon', 'Alcohol_Types_White Rum','Alcohol_Types_Vodka', 'Alcohol_Types_Gin', 
    'Alcohol_Types_Liqueur','Alcohol_Types_Pre-Mix', 'Alcohol_Types_White Wine','Alcohol_Types_Red Wine', 'Alcohol_Types_Sparkling Wine'],

    'Finance' : [u'Finance_WellOff','Finance_Comfortable', 'Finance_GettingBy','Finance_Struggle']

}

def transform_data(df):

    listLS = df['lslocal'].unique()
    allDemos = df['demo'].unique()

    df=df[df['demo'].isin(allDemos)]
    df=df[df['lslocal'].isin(listLS)]
    df=df[df['stationtype']!='DAB+']

    df['ue'] = df['ue'].astype(float)
    df_1 = df.pivot_table(['totpeople', 'ue'], index=['week','txmarket', 'stnbrand', 'stationtype','ssdemo', 'lslocal', 'demo', 'daypart'], columns='ssvalue',margins=True)
    df_3 = df.pivot_table(['totpeople'], index=['week','txmarket', 'stnbrand', 'stationtype','ssdemo', 'lslocal', 'demo', 'daypart'], columns='ssvalue',margins=True)
    df_4 = df.pivot_table(['totmins'], index=['week','txmarket', 'stnbrand', 'stationtype','ssdemo', 'lslocal', 'demo', 'daypart'], columns='ssvalue',margins=True)

    df_1=df_1.reset_index()
    df_3=df_3.reset_index()
    df_4=df_4.reset_index()

    df_1 = df_1.fillna(0)
    df_3 = df_3.fillna(0)
    df_4 = df_4.fillna(0)

    df_1['peopleshare']= (df_1['totpeople'][1]/df_1['totpeople']['All'] * 100)
    df_1['ueshare']=(df_1['ue'][1]/df_1['ue']['All'] * 100)

    df_1.sort_index(axis=1).drop(['totpeople','ue'],axis=1)

    df_2 = df_1

    df_1 = df_1.groupby(['week', 'txmarket', 'stnbrand',  'stationtype', 'ssdemo', 'lslocal', 'demo', 'daypart'])['ueshare'].mean()
    df_2 = df_2.groupby(['week', 'txmarket', 'stnbrand', 'stationtype', 'ssdemo', 'lslocal', 'demo', 'daypart'])['peopleshare'].mean()

    df_3['PeopleCount']=df_3['totpeople'][1]
    df_4['MinutesCount'] = df_4['totmins'][1]

    df_3.sort_index(axis=1).drop(['totpeople'],axis=1)
    df_4.sort_index(axis=1).drop(['totmins'],axis=1)

    df_5 = df_4

    df_3 = df_3.groupby(['week', 'txmarket', 'stnbrand', 'stationtype', 'ssdemo', 'lslocal', 'demo','daypart'])['PeopleCount'].sum()
    df_4 = df_4.groupby(['week', 'txmarket', 'stnbrand', 'stationtype', 'ssdemo', 'lslocal', 'demo','daypart'])['MinutesCount'].sum()
    df_5 = df_5.groupby(['daypart', 'txmarket', 'stnbrand', 'ssdemo', 'demo'])['MinutesCount'].sum()

    return df_1.reset_index(), df_2.reset_index(), df_3.reset_index(), df_4.reset_index(), df_5.reset_index()

def get_from_athena(query):
    client = boto3.client('athena', region_name='ap-southeast-2')
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': 'sca-dash'
        },
        ResultConfiguration={
            'OutputLocation': 's3://sca-dash-data/'
        }
    )
    execution_id = response["QueryExecutionId"]
    filename = execution_id + ".csv"
    s3 = boto3.resource('s3')

    time.sleep(0.5)
    bucket = s3.Bucket('sca-dash-data')
    objs = []
    count = 0
    while (len(objs) == 0) and (count < 100):
        objs = list(bucket.objects.filter(Prefix=filename, MaxKeys=1))
        time.sleep(0.1)
        count += 1

    print(count)
    try:
        s3.Object('sca-dash-data', filename).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("File not found")
            
            if e.response['Error']['Code'] == "404":
                print("File not found")
        
    else:
        print("File found")
        local_filename: str = "sca_dash/data/" + execution_id + ".csv"
        s3.Bucket("sca-dash-data").download_file(execution_id + ".csv", local_filename)
        df = pd.read_csv(local_filename)
        os.remove(local_filename)
        s3.Object("sca-dash-data", filename).delete()

    return df

def register_callbacks(dashapp):
    # @dashapp.callback(
    #     Output('my-graph', 'figure'),
    #     Input('my-dropdown', 'value'),
    #     State('user-store', 'data'))
    # def update_graph(selected_dropdown_value, data):
    #     df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
    #     return {
    #         'data': [{
    #             'x': df.index,
    #             'y': df.Close
    #         }],
    #         'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    #     }

    # @dashapp.callback(
    #     Output('user-store', 'data'),
    #     Input('my-dropdown', 'value'),
    #     State('user-store', 'data'))
    # def cur_user(args, data):
    #     if current_user.is_authenticated:
    #         return current_user.username

    # @dashapp.callback(Output('username', 'children'), Input('user-store', 'data'))
    # def username(data):
    #     if data is None:
    #         return ''
    #     else:
    #         return f'Hello {data}'

    @dashapp.callback(
        Output('SSDemo-filter', 'options'),
        Input('Category-SSDemo-filter', 'value'))
    def set_SSDemo_options(selected_Category):
        return [{'label': i, 'value': i} for i in all_options[selected_Category]]

    @dashapp.callback(
        Output('SSDemo-filter', 'value'),
        Input('SSDemo-filter', 'options'))
    def set_SSDemo_value(available_options):
        return available_options[0]['value']

    @dashapp.callback(
    [Output("bar_chart",   "figure"),
        Output("bar_chart_2", "figure"),
        Output("bar_chart_3", "figure"),
        Output("bar_chart_4", "figure"),
        Output("bar_chart_5", "figure")],
        [
            Input("TXMarket-filter", "value"),
            Input("SSDemo-filter", "value"), 
            Input("StnBrand-filter", "value"), 
            Input("Demo-filter", "value"), 
            Input("Daypart-filter", "value"),
            Input("people_mins_radio","value"),     
        ],
    )

    def update_charts(TXMarket, SSDemo, StnBrand, Demo, Daypart, Radio):

        TXMarket_region = TXMarket.split("-")[0]
        StationType = TXMarket.split("-")[1]

        df = get_from_athena(f"SELECT * FROM scass_allrpt WHERE txmarket = '{TXMarket_region}' AND stationtype = '{StationType}' AND SSDemo = '{SSDemo}' AND StnBrand = '{StnBrand}'")

        filtered_data, filtered_data_2, filtered_data_3, filtered_data_4, filtered_data_5 = transform_data(df)
        
        Daypart = [Daypart] if type(Daypart) == str else Daypart
        Demo = [Demo] if type(Demo) == str else Demo

        filtered_data = filtered_data[filtered_data['daypart'].isin(Daypart) ]
        filtered_data = filtered_data[filtered_data['demo'].isin(Demo) ]
        filtered_data= filtered_data.groupby(['week','stnbrand'], as_index=False)['ueshare'].mean()

        filtered_data_2 = filtered_data_2[filtered_data_2['daypart'].isin(Daypart) ]
        filtered_data_2 = filtered_data_2[filtered_data_2['demo'].isin(Demo) ]
        filtered_data_2 = filtered_data_2.groupby(['week','stnbrand'], as_index=False)['peopleshare'].mean()

        count = filtered_data.shape[0] 

        count_2 = filtered_data_2.shape[0] 

        UEShare_Average = (filtered_data['ueshare'].sum())/(count)

        PeopleShare_Average = (filtered_data_2['peopleshare'].sum())/(count_2)
        
        data = [['UE%',UEShare_Average], ['Listeners%', PeopleShare_Average]]

        average = pd.DataFrame(data, columns=['Type', 'Average%'])

        Index_value = (PeopleShare_Average/UEShare_Average) * 100
        Index_value = Index_value.astype(int)

        ULS_fig = px.bar(average,x=average.Type, y=average['Average%'], title = f"{StnBrand} SS Index for : {SSDemo} ({TXMarket}) Index = {Index_value.astype(str)} %", text=average['Average%'].astype(int))
        ULS_fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)

        SSDemo_df = filtered_data_3[filtered_data_3['demo'].isin(Demo) ]
        SSDemo_df= SSDemo_df.groupby(['week'], as_index=False)['PeopleCount'].sum()
                
        SSDemo_df['PeopleCount'] = SSDemo_df['PeopleCount'].astype(int)
        
        SSDemo_fig = px.bar(SSDemo_df,x=SSDemo_df['week'], y=SSDemo_df.PeopleCount,  title=f"SSDemo Trend for {TXMarket}", labels=dict(x="Week", y="Listeners"), text=SSDemo_df['PeopleCount'])

        if Radio == 'Total People':
            DemoP_df = filtered_data_3
            DemoP_df = DemoP_df[DemoP_df['daypart'].isin(Daypart) ]
            DemoP_df= DemoP_df.groupby(['week', 'demo'], as_index=False)['PeopleCount'].sum()
            DemoP_fig = px.bar(DemoP_df,x=DemoP_df['week'], y=DemoP_df.PeopleCount, color=DemoP_df.demo, title="SSDemo Trend", labels=dict(x="Week", y="Listeners"), text=DemoP_df['PeopleCount'].astype(int))

        else:
            DemoP_df = filtered_data_4
            DemoP_df = DemoP_df[DemoP_df['daypart'].isin(Daypart) ]
            DemoP_df= DemoP_df.groupby(['week', 'demo'], as_index=False)['MinutesCount'].sum()
                
            DemoP_fig = px.bar(DemoP_df,x=DemoP_df['week'], y=DemoP_df.MinutesCount, color=DemoP_df.demo, title="SSDemo Trend", labels=dict(x="Week", y="Minutes"), text=DemoP_df['MinutesCount'].astype(int))

        DemoP_fig.update_layout(legend_title="Demo")

        DemoP_fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)

        DPMins_df = filtered_data_5[filtered_data_5['demo'].isin(Demo) ]
        DPMins_df = DPMins_df.groupby(['daypart'], as_index=False)['MinutesCount'].sum()
        DPMins_fig = px.bar(DPMins_df,x=DPMins_df['daypart'], y=DPMins_df.MinutesCount, title="Total Mins (000) by Daypart: " + TXMarket + " " + StnBrand, labels=dict(x="Daypart", y="Total Minutes Listened"), text=DPMins_df['MinutesCount'].astype(int))
        DPMins_fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)

        s = (filtered_data_5['MinutesCount'].where(filtered_data_5.demo.isin(['F18-24', 'F25-39', 'F40-54', 'F55+', 'M18-24', 'M25-39', 'M40-54', 'M55+']))
                        .groupby(filtered_data_5['daypart'])
                        .transform('sum'))

        filtered_data_5['Demo%'] = filtered_data_5['MinutesCount'].div(s).mul(100)
        filtered_data_5 = filtered_data_5.replace([np.inf, -np.inf], np.nan).dropna(axis=0)

        DPProf_fig = px.bar(filtered_data_5,x=filtered_data_5['daypart'], y=filtered_data_5['Demo%'], color=filtered_data_5['demo'],  title="Total Mins (000) by Daypart: " + TXMarket + " " + StnBrand, labels=dict(x="Daypart", y="Total Minutes Listened"), text=filtered_data_5['Demo%'].astype(int))
        DPProf_fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)
        DPProf_fig.update_layout(legend_title="Demo")

        return [ULS_fig, SSDemo_fig, DemoP_fig, DPMins_fig, DPProf_fig]


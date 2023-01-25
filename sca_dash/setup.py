import pandas as pd
import os


class sca_dash:

    def __init__(self):

        self.app_title = "Fred"

        self.df_SSDemo = pd.read_csv(os.path.join('sca_dash','data','SSDemo.csv'))
        self.df_Demo = pd.read_csv(os.path.join('sca_dash','data','Demo.csv'))
        self.df_TXMarket = pd.read_csv(os.path.join('sca_dash','data','TXMarket.csv'))
        self.df_StnBrand = pd.read_csv(os.path.join('sca_dash','data','StnBrand.csv'))
        self.df_Daypart = pd.read_csv(os.path.join('sca_dash','data','Daypart.csv'))

        self.all_options = {
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

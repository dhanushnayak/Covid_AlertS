import pandas as pd
import random
import pymongo
import urllib
from math import cos, asin, sqrt
from geopy.geocoders import Nominatim
import datetime
class MongoData():
    def __init__(self):
        self.connect =pymongo.MongoClient("mongodb+srv://dhanush:"+urllib.parse.quote_plus('Dhanushp@1')+"@sih.koyg5.gcp.mongodb.net/Sih?retryWrites=true&w=majority")
        self.db = self.connect.SIH
        
        
    def Density(self):
        fd = self.db['Density']
        l=[]
        for i in fd.find():
            l.append(i)
        df=pd.DataFrame(l).drop('_id',axis=1)
        del l,i,fd
        return df
    def Polygon(self):
        fd = self.db['Polygon']
        l=[]
        for i in fd.find():
                l.append(i)
        df=pd.DataFrame(l).drop("_id",axis=1)
        del l,i,fd
        return df
    def station(self):
        fd = self.db['Station']
        l=[]
        for i in fd.find():
            l.append(i)
        
        df1 = pd.DataFrame(l).drop("_id",axis=1)
        del l,i,fd
        l1=[]
        df1['icon']="police"
        for x in range(len(df1)):
            x1 =  "<strong>"+df1['name'][x]+"</strong><p>"+df1['address'][x]+"</p><p>"+"<strong>"+df1['phoneno'][x]+"</strong></p>."
            l1.append(x1)
        df1['description'] = l1
        del l1
        return df1
    def closestpolice(self,df1,df2):
       
        return min(df1, key=lambda p: distance(df2[0].df2[1],p['longitude'],p['latitude']))
    
        
    
    def feedback(self,Name,crime,location):
        fd = self.db['feedback']
        d={}
        d['Name']=Name
        d['crime']=crime
        geolocator = Nominatim(user_agent='myapplication')
        location = geolocator.geocode("{}, Bangalore".format(location))
        d['latitude']=location.latitude
        d['longitude']=location.longitude
        d['Date']=datetime.datetime.now().strftime("%x")
        fd.insert_one(d)
        del fd,d,location,geolocator
        return True
    def Imagesupload(self,data,images):
        fd = self.db['Imagereported']
        d={}
        d['Date']=datetime.datetime.now().strftime("%x")
        d['Name'] = data['Name']
        d["Email"]=data['email']
        d['Phone'] = data['phone']
        d['Images']= [i for i in images]
        fd.insert_one(d)
        del fd,d
        return True
        
    def getfeedback(self):
        fd = self.db['feedback']
        l=[]
        for i in fd.find():
            l.append(i)
        df = pd.DataFrame(l)
        df=df[df['Date']==datetime.datetime.now().strftime("%x")].drop(["_id","Date"],axis=1)
        
        return list(df.T.to_dict().values())
   
class Df_to_geojson:
    def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
        geojson = {"type":"FeatureCollection", "features":[]}
        for _, row in df.iterrows():
            feature = {"type":"Feature",
                       "properties":{},
                       "geometry":{"type":"Point",
                                   "coordinates":[]}}
            if properties[1]=="population_density":
                feature["geometry"]["coordinates"] = [row[lon],row[lat],random.randrange(0,150)]
            else:
                feature["geometry"]["coordinates"] = [row[lon],row[lat]]
            if properties[0]=="description":
                feature["properties"]['description']=row[properties][0]
            else:
                feature["properties"]["id"] = row[properties][0]
            if properties[1]=="icon":
                feature['properties']['icon']=row[properties][1]
            else:
                feature['properties']['mag']=row[properties][1]
            geojson["features"].append(feature)
        return geojson
    
class Closestpolice:
    def closestpolice(df1,df2):
            def distance(lat1, lon1, lat2, lon2):
                p = 0.017453292519943295
                a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
                return 12742 * asin(sqrt(a))

            return list(min(df1, key=lambda p: distance(df2[1],df2[0],p['latitude'],p['longitude'])).values())[::-1]
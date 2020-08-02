import pandas as pd
import pymongo
import urllib
class GraphDetails:
    def __init__(self,place):
        self.connect =client = pymongo.MongoClient("mongodb://dhanush:"+urllib.parse.quote_plus('Dhanushp@1')+"@sih-shard-00-00.koyg5.gcp.mongodb.net:27017,sih-shard-00-01.koyg5.gcp.mongodb.net:27017,sih-shard-00-02.koyg5.gcp.mongodb.net:27017/Sih?ssl=true&replicaSet=atlas-uqs6ic-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.db = self.connect.SIH
        self.place = place
    def placerating_linegraph(self):
        try:
            fd = self.db['places_rating_last10covid']
            l=[]
            for i in fd.find():
                l.append(i)
            df = pd.DataFrame(l)
            df['places']=df['places'].str.lower()
            df=df[df['places'].str.contains(self.place.lower())]
            cases  = [int(i/10) for i in list(df.iloc[:,3:].values[0])][:9]
            l=['2020-08-01','2020-07-31','2020-07-30','2020-07-29','2020-07-28','2020-07-27','2020-07-26','2020-07-25','2020-07-24','2020-07-23']
            return (df['rating'].values[0],dict(zip(l,cases)))
        except:
            return 0
    def places_piechart(self):
        try:
            fd = self.db['places_corona_report']
            l=[]
            for i in fd.find():
                l.append(i)
            df = pd.DataFrame(l)
            f = df[df['places'].str.contains(self.place.lower())]

            return dict(zip(list(f.drop(['_id','places'],axis=1).columns),list(f.drop(['_id','places'],axis=1).values[0])))
        except:
            return 0
    def place_crimepie(self):
        try:
            fd = self.db['places_crime']
            l=[]
            for i in fd.find():
                l.append(i)
            df = pd.DataFrame(l)
            f = df[df['places'].str.contains(self.place.lower())]
            return dict(zip(list(f.drop(['_id','places'],axis=1).columns),list(f.drop(['_id','places'],axis=1).values[0])))
        except:
            return 0
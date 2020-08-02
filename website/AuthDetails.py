import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np
import datetime
class AuthDetails():
    def __init__(self,Email):
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate(r'C://Users/NayakD/Desktop/cir/my-firebase-app-ad067-firebase-adminsdk-1lclz-d3de05a319.json')
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        docs = self.db.collection(u'users').stream()
        self.email = Email 
    
    def authDetails(self):
        try:
            docs = self.db.collection(u'users').stream()
            for i in docs:
                if i.id == self.email:
                    break
            return i.to_dict()
        except:
            return False
       
class groupdetails():
    def __init__(self,Groupid):
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate(r'C://Users/NayakD/Desktop/cir/my-firebase-app-ad067-firebase-adminsdk-1lclz-d3de05a319.json')
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.docs = self.db.collection(u'users').stream()
        self.group = Groupid
        
    def Groupmember(self):
        l=[]
        for i in self.docs:
            if i.to_dict()['GroupId']==self.group:
                l.append(i.to_dict())
        return l
    
    
class Location():
    def __init__(self,groupid,email):
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate(r'my-firebase-app-ad067-firebase-adminsdk-1lclz-d3de05a319.json')
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        
        self.gid = groupid
        self.email = email 
        self.date = datetime.datetime.now()
    def getlocation(self):
       
            docs = self.db.collection(u'Location').document(self.gid).collection('users').stream()
            for i in docs:
                if i.id == self.email:
                    return list(map(float,i.to_dict().values()))
    def ImagesfromPhone(self):
        docs = self.db.collection(u'police').document(self.gid).collection(self.email).stream()

        for doc in docs:
          #if(doc.id ==(self.date.strftime("%d")+'-'+self.date.strftime("%m")+"-"+self.date.strftime("%Y")) ):
          if(doc.id =="31-07-2020" ):
            return list(doc.to_dict().values())

        
    
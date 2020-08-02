import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from skimage import io
import face_recognition
import cv2 
import os
class Firebase():
    def __init__(self,groupid,Email,password):
        path=os.path.dirname(os.path.realpath(__file__))
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate(str(path)+"\my-firebase-app-ad067-firebase-adminsdk-1lclz-d3de05a319.json")
            
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.gid = groupid
        self.email = Email 
        self.password = password
        self.valid1=False
        self.valid2=False
    
    def authDetails(self):
        try:
            docs = self.db.collection(u'users').stream()
            for i in docs:
                if i.id == self.email:
                    break
            return i.to_dict()
        except:
            return False
            
    def Location(self,usermail):
        try:
            if self.valid1 and self.valid2:
                    docs = self.db.collection(u'Location').document(self.gid).collection('users').stream()
                    for i in docs:
                        if i.id == usermail:
                            return i.to_dict()
            else:
                return False
        except:
            return False
        
        
    def auth(self):
        try:
            if self.authDetails()!=False:
                if self.gid == self.authDetails()['GroupId'] and self.authDetails()['password'] == str(self.password):
                    self.valid1=True
                    if self.facedect(self.authDetails()['image_url']):
                        self.valid2=True
                        return True
                    
            else:
                return False
        except:
            return False
    
    def facedect(self,url):
        try:
            cam = cv2.VideoCapture(0)   
            s, img = cam.read()
            if s:    
                    face_1_image = io.imread(url)
                    print(face_1_image.shape)
                    face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

                 

                    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

                    rgb_small_frame = small_frame[:, :, ::-1]

                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)

                    print(check)
                    if check[0]:
                            cam.release()
                            cv2.destroyAllWindows()
                            self.valid2= True
                            return True

                    else :
                            cam.release()
                            cv2.destroyAllWindows()
                            return False    
        except:
            cam.release()
            cv2.destroyAllWindows()
            return False

        
            
        
        

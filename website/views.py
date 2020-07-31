from django.template import RequestContext
from .forms import LoginForm
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404, get_list_or_404,reverse,render_to_response
from django.db.models import signals
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseServerError
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from .FirebaseAuthSIH import Firebase
from .AuthDetails import AuthDetails,groupdetails,Location
from .LocationDetails import Df_to_geojson,MongoData,Closestpolice

def Login(request): 
    
    if request.method =="POST":
                    form =LoginForm(request.POST)
                    if form.is_valid():
                            Email=request.POST['Email']
                            password=request.POST['Password']
                            Groupid = request.POST['GroupId']
                            auth = Firebase(Groupid,Email,password)
                            if auth.auth():
                                            print("True")
                                            messages.warning(request, 'Face Recon Successful !!!!') 
                                            
                                            
                                            return redirect(f"names/{Email}")

                            else:
                                    messages.warning(request, f'account done not exit plz sign in') 
                                    return HttpResponse("Auth Failed")        
    else:
                    form = LoginForm()
    
    form = LoginForm()
    messages.warning(request, 'Allow Webcam for Verfication')
    return render(request, 'user/login.html', {'form':form, 'title':'log in'}) 

def names(request,Email):
        mongo = MongoData() 
        a = AuthDetails(Email)
        group = groupdetails(a.authDetails()['GroupId'])
        member = group.Groupmember()
        density = Df_to_geojson.df_to_geojson(df=mongo.Density(),properties=['place',"population_density"])
        sdf = mongo.station()
        station = Df_to_geojson.df_to_geojson(df=sdf,properties=["description","icon"])
        sdf = sdf[['latitude','longitude']].T.to_dict().values()
        feedback = mongo.getfeedback()
        currentlocation=[77.6070,13.1155]
        if request.GET.get("name",''):
                name = request.GET.get('name', '')
                place = request.GET.get("place",'')
                crime = request.GET.getlist('checks[]')[0]
                        
                print(type(name),place,type(crime))
                mongo.feedback(Name=name,crime=crime,location=place)
                print("done")
                messages.success(request, '✔️ Report Submitted')
        return render(request,'index.html',{"pro":a.authDetails(),"group":member,"currentlocation":currentlocation,"density":density,"station":station,"feedback":feedback})

def location(request,Email,groupid,submail):
        a = AuthDetails(Email)
        group = groupdetails(a.authDetails()['GroupId'])
        member = group.Groupmember()
        b = Location(groupid,submail)
        mongo = MongoData()
        density = Df_to_geojson.df_to_geojson(df=mongo.Density(),properties=['place',"population_density"])
        sdf = mongo.station()
        station = Df_to_geojson.df_to_geojson(df=sdf,properties=["description","icon"])
        sdf = sdf[['latitude','longitude']].T.to_dict().values()
        curr=b.getlocation()
        closestation=Closestpolice.closestpolice(df1=sdf,df2=curr)
        feedback = mongo.getfeedback()
        if not feedback:
                feedback = None
        policealert = mongo.GetPoliceAlert()
        if not policealert:
                policealert = None
        try:
                name = request.GET.get('name', '')
                place = request.GET.get("place",'')
                crime = request.GET.getlist('checks[]')[0]
                try:
                        print(name,place,crime)
                        print(mongo.feedback(Name=name,crime=crime,location=place))
                        messages.success(request, '✔️ Report Submitted')
                except:
                        messages.success(request," Please provide valid location")
                
        except:
                pass
        if b.ImagesfromPhone():
                image = b.ImagesfromPhone()
        else:
                image = None
                
        if image != None and (request.GET.get('sendimage')):
                try:
                        mongo.Imagesupload(data=a.authDetails(),location=b.getlocation(),images=image)
                        print("Done")
                        messages.success(request,"Uploaded/Submited")
                except:
                        messages.warning(request, "NO Images TO submit")
                
                
        return render(request,'index.html',{"pro":a.authDetails(),"group":member,"currentlocation":curr,"density":density,"station":station,"closestation":closestation,"feedback":feedback,"images":image,"policealert":policealert})
        #return HttpResponse("{}{}{}{}".format(a.authDetails(),member,b.getlocation(),density))
def register(request):
        return HttpResponse("Use Mobile App to Register")
        
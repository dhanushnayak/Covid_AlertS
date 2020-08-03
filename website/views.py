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
from .fusioncharts import FusionCharts
from .Graphdetail import GraphDetails
def Login(request): 
    
    if request.method =="POST":
                    
                            Email=request.POST.get('email')
                            password=request.POST.get('pass')
                            Groupid = request.POST.get('groupid')
                            print(Groupid)
                            auth = Firebase(Groupid,Email,password)
                            if not auth.auth():
                                            print("True")
                                            messages.success(request, 'Face Recon Successful !!!!') 
                                            
                                            
                                            return redirect(f"user/{Email}/{Groupid}")

                            else:
                                    messages.success(request, f'account done not exit plz sign in') 
                                    return HttpResponse("Auth Failed")        
   
                   
    
    
        
    return render(request, 'admin/login.html') 



def location(request,Email,groupid,submail):
        try:
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
                try:
                        closestation=Closestpolice.closestpolice(df1=sdf,df2=curr)
                except:
                        closestation=0
                feedback = mongo.getfeedback()
                if not feedback:
                        feedback = None
                covidpublic=mongo.getcovidpubilc()
                if not covidpublic:
                        covidpublic = None
                try:
                        closecovid=Closestpolice.closestpolice(df1=covidpublic[['latitude','longitude']].T.to_dict().values(),df2=curr)
                except:
                        closecovid=0
                
                policealert = mongo.GetPoliceAlert()
                if not policealert:
                        policealert = None
                try:
                        query = request.GET.get('place', '')
                        if query:
                                try:
                                        return redirect(chart,Email=Email,location=query)
                                except:
                                        return("/error/{Email}")
                except:
                        return("/error/{Email}")
        except:
                return("/error/{Email}")        
        return render(request,'admin/map.html',{"auth":a.authDetails(),"group":member,"currentlocation":curr,"density":density,"station":station,"closestation":closestation,"feedback":feedback,"policealert":policealert,"places":mongo.places(),"covidpublic":covidpublic,"closecovid":closecovid,"submail":submail})
        #return HttpResponse("{}{}{}{}".format(a.authDetails(),member,b.getlocation(),density))
def register(request):
        return HttpResponse("Use Mobile App to Register")
       
def temp(request,Email,GroupId):
        try:
                mongo = MongoData()
                a = AuthDetails(Email)
                group = groupdetails(a.authDetails()['GroupId'])
                member = group.Groupmember()
                df2={}
                df2['chart']={
                        "caption": "Corona Cased Reported In  Bangalore",
                        "subcaption":"Last 10 Days",
                        "showValues": "1",
                        "showpercentvalues": "0",
                "defaultcenterlabel": "Reported",
                "yaxisname": "Cases",
                "xaxisname":"Dates",
                "anchorradius": "5",
                "aligncaptionwithcanvas": "0",
                "captionpadding": "0",
                "decimals": "1",
                "theme" : "fusion",
                        }
                df2['data']=[]
                datedf = mongo.getcovidcases()
                for key,value in datedf.items():
                        d22={}
                        d22['label']=key
                        d22['value']=str(value)
                        d22['color']="#FF5A87"
                        df2['data'].append(d22)
                dTotal = FusionCharts("spline", "ex2" , "800", "390", "chart-2", "json",df2) 
                chartObj = FusionCharts( 'doughnut2d', 'ex1', '500', '390', 'chart-1', 'json', """{
                        "chart": {
                        "caption": "Corona Blast in Bangalore",
                        "subcaption": "Overall Count",
                        "showvalues": "1",
                        "showpercentintooltip": "0",
                        "numberprefix": "",
                        "enablemultislicing": "1",
                        "theme": "fusion"
                        },
                        "data": [
                        {
                        "label": "Active Cases",
                        "value": "53324"
                        },
                        {
                        "label": "Recoverd",
                        "value": "32045"
                        },
                        {
                        "label": "Deaths",
                        "value": "1103"
                        },
                        
                        ]
                        }""")
        
                query = request.GET.get('place', '')
                try:
                        if query:
                                try:
                                        return redirect(chart,Email=Email,location=query)
                                except:
                                        return("/error/{Email}")
                except:
                        return("/error/{Email}")
        
        except:
                return("/error/{Email}")
        
        return render(request,"admin/home.html",{'output2':dTotal.render(),'output': chartObj.render(),"group":member,"auth":a.authDetails(),"places":mongo.places()})


def chart(request,Email,location):
        try:
                if location!= None:
                        graph = GraphDetails(location)
                        mongo = MongoData()
                        a = AuthDetails(Email)
                        group = groupdetails(a.authDetails()['GroupId'])
                        member = group.Groupmember()
                        rating=round(graph.placerating_linegraph()[0],1)
                        rate = rating*10
                        line = graph.placerating_linegraph()[1]
                        df2={}
                        df2['chart']={
                                "caption": "Corona Cased Reported ",
                                "subcaption":"Last 10 Days",
                                "showValues": "1",
                                "showpercentvalues": "0",
                        "defaultcenterlabel": "Reported",
                        "yaxisname": "Cases",
                        "xaxisname":"Dates",
                        "anchorradius": "5",
                        "aligncaptionwithcanvas": "0",
                        "captionpadding": "0",
                        "decimals": "1",
                        "theme" : "fusion",
                                }
                        df2['data']=[]
                        datedf = line
                        for key,value in datedf.items():
                                d22={}
                                d22['label']=key
                                d22['value']=str(value)
                                d22['color']="#FF5A87"
                                df2['data'].append(d22)
                        dTotal = FusionCharts("spline", "ex2" , "800", "390", "chart-2", "json",df2)
                        dataSource = {}
                        dataSource['chart'] = {
                                "caption": "Covid-19 of Zone ",
                                "subcaption":"Overview",
                                "showValues": "1",
                                "theme": "fusion"
                                }
                        dataSource['data'] = []
                        for i,j in graph.places_piechart().items():
                                data={}
                                data['label']=str(i)
                                data['value']=str(j)
                                dataSource['data'].append(data)

                        covidpie = FusionCharts("pie2d","ex1","500","390","chart-1","json",dataSource)
                        ds={}
                        ds['chart']={
                        "caption": "Crime Analysis ",
                                "subcaption":"Overview",
                                "showValues": "1",
                                "theme": "fusion"  
                        }
                        ds['data']=[]
                        for i,j in graph.place_crimepie().items():
                                data={}
                                data['label']=str(i)
                                data['value']=str(j)
                                ds['data'].append(data)
                        crimepie = FusionCharts("pie3d","ex3","800","390","chart-3","json",ds)
                        query = request.GET.get('place', '')
                        try:
                                if query:
                                        try:
                                                return redirect(chart,Email=Email,location=query)
                                        except:
                                                return("/error/{Email}")
                        except:
                                return("/error/{Email}")
        except:
                return("/error/{Email}")
        return render(request,"admin/chart.html",{"places":mongo.places(),"rate":rate,'output2':dTotal.render(),"auth":a.authDetails(),"location":location,"group":member,"rating":rating,"output1":covidpie.render(),"crime":crimepie.render()})
        
        
        
def Coronaform(request,Email):
        a= AuthDetails(Email)
        mongo = MongoData()
        if request.method == 'POST':
                address = request.POST.get("Address")
                location = request.POST.get("place")
                try:
                        mongo.coronareport(data=a.authDetails(), address=address, location=location)
                
                        messages.success(request, 'Covid Case Reported Successfully!')
                except:
                        messages.success(request, 'Place is not valid give valid zonal area')
                        pass
        return render(request,'admin/form.html',{"auth":a.authDetails()})
        
def reportcase(request,Email):
        a = AuthDetails(Email)
        mongo = MongoData()
        if request.method == "POST":
                address = request.POST.get("Address")
                crime = request.POST.get("crime")
                location = request.POST.get("place")
                try:
                        mongo.feedback(data=a.authDetails(), crime=crime, address=address, location=location)
                        messages.success(request, 'Case Reported Successfully!')
                except:
                        messages.success(request,"Please provide valid Information and valid Zonal area!")
                        pass
        return render(request,"admin/caseform.html",{"auth":a.authDetails()})

def table(request,Email):
        try:
                a = AuthDetails(Email)
                mongo=MongoData()
                a = AuthDetails(Email)
                group = groupdetails(a.authDetails()['GroupId'])
                member = group.Groupmember()
                table1=mongo.Table()
        except:
                return("/error/{Email}")
        return render(request,"admin/table.html",{"auth":a.authDetails(),"group":member,"table":table1})

def wanted(request,Email):
        a = AuthDetails(Email)
        mongo1=MongoData()
        group = groupdetails(a.authDetails()['GroupId'])
        member = group.Groupmember()
        
        return render(request,"admin/wanted.html",{"auth":a.authDetails(),"group":member})
        
def mobileimages(request,Email,groupid,submail):
        try:
                a = AuthDetails(Email)
                mongo = MongoData()
                group = groupdetails(a.authDetails()['GroupId'])
                member = group.Groupmember()
                b = Location(groupid,submail)
                if b.ImagesfromPhone() == None:
                        messages.success(request,"No Images from Device")
                if request.method == "POST":
                        location = request.POST.get("place")
                        if location.lower() == "forward":
                                mongo.Imagesupload(data=a.authDetails(), location=b.getlocation(), images=b.ImagesfromPhone())
                                messages.success(request,"Images Forward To Osint") 
                try:
                        query = request.GET.get('place', '')
                        if query:
                                try:
                                        return redirect(chart,Email=Email,location=query)
                                except:
                                        return("/error/{Email}")
                except:
                        return("/error/{Email}")
        except:
                return("/error/{Email")
        return render(request,"admin/mobile.html",{"auth":a.authDetails(),"group":member,"images":b.ImagesfromPhone(),"user":submail})

def notfound(request,Email):
        a = AuthDetails(Email)
        group = groupdetails(a.authDetails()['GroupId'])
        member = group.Groupmember()
        return render(request, "admin/404.html",{"auth":a.authDetails(),"group":member})
"""funds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
   path("", views.Login, name ='login'), 
  
   path("register",views.register,name='register'),
   url(r'location/(?P<Email>[a-zA-Z0-9@.$]+)/(?P<groupid>[a-zA-Z0-9@.$]+)/(?P<submail>[a-zA-Z0-9@.$]+)$',views.location),
   url(r'user/(?P<Email>[a-zA-Z0-9@.$]+)/(?P<GroupId>[a-zA-Z0-9@.$]+)$',views.temp),
   url(r'place/(?P<Email>[a-zA-Z0-9@.$]+)/(?P<location>[a-zA-Z]+)$',views.chart),
   url(r'corona/(?P<Email>[a-zA-Z0-9@.$]+)/',views.Coronaform),
   url(r'crimecase/(?P<Email>[a-zA-Z0-9@.$]+)/',views.reportcase),
   url(r'report/(?P<Email>[a-zA-Z0-9@.$]+)/',views.table),
   url(r'mobile/(?P<Email>[a-zA-Z0-9@.$]+)/(?P<groupid>[a-zA-Z0-9@.$]+)/(?P<submail>[a-zA-Z0-9@.$]+)$',views.mobileimages),
   url(r"error/(?P<Email>[a-zA-Z0-9@.$]+)/",views.notfound)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

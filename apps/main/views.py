from django.shortcuts import render
from django.conf import settings
from django.views import View
from django.db.models import Q
from . models import *
import os

#================================== Worldwide Content ==========================================
def worldwide_content(request):
    img_list= os.listdir(settings.MEDIA_ROOT + "/images")
    media_url= settings.MEDIA_URL
    
    if not request.user.is_authenticated:
         request.session["display_name"]= "کاربر مهمان"     
    else:
        if request.user.first_name != "" and request.user.last_name != "":
            request.session["display_name"]= f"{request.user.first_name} {request.user.last_name}" 
        else:
            request.session["display_name"]= request.user.cell_num 
    
    return {"media_url": media_url,
            "img_list": img_list}

#============================================================================
def index(request):
    template_name = "main/index.html"
    return render(request,template_name,)


#============================================================================
def handler404_view(request,exceptiom=None,):
    template_name = "main/404.html"
    return render(request,template_name,)


#============================================================================
class set_slider_view(View):
    template_name = "main/slider.html"

    def get(self,request,*args,**kwargs):
        sliders = Slider.objects.filter(Q(is_active=True))
        return render(request,self.template_name,{"sliders":sliders})


#============================================================================
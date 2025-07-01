from django.urls import path
from .views import * 
# from apps.main.views import * 

app_name="main"
urlpatterns = [
    path("",index,name="index"),
    path("set_slider",set_slider_view.as_view(),name="set_slider"),
]

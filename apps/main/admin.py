from django.contrib import admin
from .models import *


@admin.register(Slider)
class Slider_Admin(admin.ModelAdmin):
    list_display = ("img_slider","heading_1","link","is_active","craete_at",)
    list_filter = ("heading_1",)
    search_fields = ("heading_1",)
    ordering = ("updated_at",)
    readonly_fields = ("img_slider",)
    
    
    
         
    
    

     
     
     
     
     
     
    

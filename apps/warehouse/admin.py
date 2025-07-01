from django.contrib import admin
from .models import *



#=======================================================================
@admin.register(Warehouse_Types)
class WarehouseTypesAdmin(admin.ModelAdmin):
    list_display = ["id","title"]
    

#=======================================================================    
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["product", "count", "warehouse_type", "price", "logged_date"]


#=======================================================================
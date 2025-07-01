from django.contrib import admin
from .models import *



#=======================================================================
class Details_Of_OrderInLine(admin.TabularInline):
    model = Details_Of_Order
    extra = 1

@admin.register(Orders)
class Orders_Admin(admin.ModelAdmin):
    list_display = ["order_customer","logged_date","is_paid","discount","order_state","order_payment","order_code",]
    ordering = ("id",)
    search_fields = ("id",)
    inlines = [Details_Of_OrderInLine]
    
    
#=======================================================================
@admin.register(Payment_Types)
class Payment_Types_Admin(admin.ModelAdmin):
    list_display = ["id","title"]
    ordering = ("id",)
    search_fields = ("id",)

    
#=======================================================================
@admin.register(OederState)
class Oeder_State_Admin(admin.ModelAdmin):
    list_display = ["id","title"]
    
    
#=======================================================================

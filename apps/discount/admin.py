from django.contrib import admin
from .models import *



#=======================================================================
@admin.register(Discounts)
class DiscountsAdmin(admin.ModelAdmin):
    list_display=["discount_code","discount_percentage","is_active","start_date","expiry_date",]
    ordering=("is_active",)


#=======================================================================
class DiscountBasketDetailsInLine(admin.TabularInline):
    model=DiscountBasketDetails
    
@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display=["title","discount_basket_percentage","is_active","start_date","expiry_date",]
    ordering=("is_active",)
    inlines=[DiscountBasketDetailsInLine,]
    

#=======================================================================

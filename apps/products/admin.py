from typing import Any
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models.aggregates import *
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter
from .models import *



#================================= Actions ======================================

def deactivating_values(modeladmin,request,queryset):
    res = queryset.update(is_active=False)
    message = f"تعداد {res} مقدار غیرفعال شد"
    modeladmin.message_user(request,message)

def activating_values(modeladmin,request,queryset):
    res = queryset.update(is_active=True)
    message = f"تعداد {res} مقدار فعال شد"
    modeladmin.message_user(request,message)
    
def JSON_Convertor(modeladmin,request,queryset):
    res = HttpResponse(content_type="application/json")
    serializers.serialize("json",queryset,stream=res)
    return res    

    
#================================= Group Admin ======================================

# class GroupInline(admin.TabularInline):
#     model = Groups
#     extra = 1


class GroupFilter(SimpleListFilter):
    title = "گروه محصولات"
    parameter_name = "group_id"
    
    def lookups(self, request, modeladmin):
        sub_groups = Groups.objects.filter(~Q(groups=None))
        groupsAdmin = set([item.groups for item in sub_groups])
        return [(item.id, item.title) for item in groupsAdmin]
    
    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(Q(groups=self.value()))
        return queryset
    
     
@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ("title","groups","is_active","displaying_sub_groups","displaying_products","slug","logged_date","updated_date",)
    list_filter = (GroupFilter,"is_active",)
    list_editable = ("is_active",)
    search_fields = ("title",)
    ordering = ("groups","title",)
    # inlines = [GroupInline,]
    actions = [deactivating_values,activating_values,JSON_Convertor]
    
    
    def get_queryset(self, *args, **kwargs):
        qs = super(GroupsAdmin,self).get_queryset(*args, **kwargs)
        qs = qs.annotate(sub_groups=Count("group"))
        qs = qs.annotate(products_in_each_group=Count("productGroup"))
        return qs
    
    def displaying_sub_groups(self,obj):
        return obj.sub_groups
    
    #ali's code
    # def displaying_sub_groups(self,obj):
    #     set_list=(len(set([i for i in obj.productGroup.all()])))
    #     return set_list
    
    def displaying_products(self,obj):
        return obj.products_in_each_group
    
    
    displaying_sub_groups.short_description = "تعداد زیر گروه ها"
    displaying_products.short_description = "تعداد کالاهای هر گروه"
    deactivating_values.short_description = "غیرفعال کردن گروهای انتخاب شده"
    activating_values.short_description = "فعال کردن گروهای انتخاب شده"
    JSON_Convertor.short_description = "تبدل کننده JSON"


#================================= Brand Admin ======================================

@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ("title","slug",)
    list_filter = ("title",)
    search_fields = ("title",)
    ordering = ("title",)
    actions = [deactivating_values,activating_values,JSON_Convertor]
    

    deactivating_values.short_description = "غیرفعال کردن برندهای انتخاب شده"
    activating_values.short_description = "فعال کردن برندهای انتخاب شده"
    JSON_Convertor.short_description = "تبدل کننده JSON"
    
    
#================================= Feature Admin ======================================

class Feature_ValueInline(admin.TabularInline):
    model = Feature_Value
    extra = 2

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ("title","displaying_groups","displaying_features")
    list_filter = ("title",)
    search_fields = ("title",)
    ordering = ("title",)
    inlines = [Feature_ValueInline,]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "product_groups":
            kwargs["queryset"]=Groups.objects.filter(~Q(groups=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def displaying_groups(self, obj):
        return ", ".join([group.title for group in obj.groups.all()])
    
    def displaying_features(self, obj):
        return ", ".join([feature.value_title for feature in obj.featureValue_Feature.all()]) 

    displaying_groups.short_description="گروهای دارای این ویژگی"
    displaying_features.short_description="مقدارها"
    
    
#================================= Product Admin ======================================

class Features_ProductsInline(admin.TabularInline):
    model = Features_Products
    extra = 2

    class Media :
        # cs= {
        #     'all': ('',)
        # }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin.js',
        )
        
class Product_GallerysInline(admin.TabularInline):
    model = Product_Gallery
    extra = 1  
    
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("title","displaying_groups","is_active","price","product_brands","slug","updated_date",)
    list_filter = (("product_brands__title",DropdownFilter),("product_groups__title",DropdownFilter),)
    list_editable = ("is_active",)
    search_fields = ("title",)
    ordering = ("updated_date","title",)
    inlines = [Features_ProductsInline,Product_GallerysInline,]
    actions = [deactivating_values,activating_values,JSON_Convertor]
    
    
    def displaying_groups(self, obj):
        return ", ".join([group.title for group in obj.product_groups.all()]) 
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "product_groups":
            kwargs["queryset"]=Groups.objects.filter(~Q(groups=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    


    displaying_groups.short_description="گروه"
    deactivating_values.short_description = "غیرفعال کردن محصول های انتخاب شده"
    activating_values.short_description = "فعال کردن محصول های انتخاب شده"
    JSON_Convertor.short_description = "تبدل کننده JSON"


#=======================================================================    


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseForbidden
from .models import *
from .forms import *
from django.utils.translation import gettext_lazy as _


#======================================= Users =======================================

# class PermissionInline(admin.TabularInline):
#     model = Permission
#     list_display=("is_admin","is_superuser",)
#     list_editable = ("is_admin","is_superuser",)
#     extra = 0
#     can_delete = False

        

class CreatingAdminUserAdmin(UserAdmin):
    
    add_form=CreatingAdminUserForm
    form=EditAdminUserForm
    
    
    list_display=("id","first_name","last_name","cell_num","email","gender","is_active","is_admin","is_superuser",)
    list_filter=("is_superuser","is_admin","is_active","gender",)
    
    
    add_fieldsets=(
        ("اطلاعات کاربری",{"fields":("cell_num","password1","password2",)}),
        ("اطلاعات شخصی",{"fields":("first_name","last_name","email","gender",)}),
    )
    
    fieldsets=(
        ("اطلاعات کاربری",{"fields":("cell_num","password",)}),
        ("اطلاعات شخصی",{"fields":("first_name","last_name","email","gender",)}),
        ("دسترسی ها",{"fields":("is_active","is_admin","is_superuser","groups","user_permissions",)}),
    )
    
    list_editable = ("is_admin","is_active",)
    sreach_fields = ("cell_num",)
    ordering = ("is_superuser","is_admin","is_active","last_name","first_name",)
    filter_horizontal = ("groups","user_permissions",)
    # inlines = (PermissionInline,)

    def change_view(self, request, object_id, form_url='', extra_context=None):
         
        if CustomUser.objects.filter(pk=object_id, is_superuser=True).exists() and request.user.is_superuser is False: 
            return HttpResponseForbidden('<h1 style="color:red; text-align:center;">شما مجاز به مشاهده این صفحه نیستید</h1>') 
        if CustomUser.objects.filter(pk=object_id, is_admin=True).exists() and request.user.is_superuser is False: 
            return HttpResponseForbidden('<h1 style="color:red; text-align:center;">شما مجاز به مشاهده این صفحه نیستید</h1>') 
        if CustomUser.objects.filter(pk=object_id, is_superuser=True).exists() and request.user.is_superuser is True: 
            return HttpResponseForbidden('<h1 style="color:black; text-align:center;">شما مجاز به مشاهده این صفحه نیستید</h1>') 
         
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(CustomUser,CreatingAdminUserAdmin)




#========================================================================================================================
@admin.register(Customer)
class Customer_Admin(admin.ModelAdmin):
    list_display = ["user","address"]



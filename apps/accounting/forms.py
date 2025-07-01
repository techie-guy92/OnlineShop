from django import forms 
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *


#======================================= Users Admin =======================================

class CreatingAdminUserForm(forms.ModelForm):
    password1=forms.CharField(label="رمز عبور",widget=forms.PasswordInput)
    password2=forms.CharField(label="تکرار رمز عبور ",widget=forms.PasswordInput)
    
    class Meta:
        model=CustomUser
        fields=["first_name","last_name","cell_num","email","gender"]
        
        
    def clean_password2(self):
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن یکی نیست")
        return pass2
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    
#====================================================   
    
class EditAdminUserForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text="برای تغییر رمز عبور روی <a href='../password'>لینک</a> کلیک کنید")
    
    # password = ReadOnlyPasswordHashField(
    #     label=_("Password"),
    #     help_text=_(
    #         "برای تغییر رمز عبور روی <a href='../password'>لینک</a> کلیک کنید"
    #     ),)
    
    class Meta:
        model=CustomUser
        fields=["cell_num","email","password","is_active",]
        # fields=["cell_num","email","password","is_active","is_admin"]
 
            
#======================================= Users =======================================

class RegisterUserForm(ModelForm):
    password1= forms.CharField(label="رمز عبور",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))
    password2= forms.CharField(label="تکرار رمز عبور",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز را وارد کنید'}))
    
    class Meta:
        model=CustomUser
        fields=["cell_num",]
        widgets={"cell_num": forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید'})}
 
    def clean_password2(self):
        pass1= self.cleaned_data["password1"]
        pass2= self.cleaned_data["password2"]
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن یکی نیست")
        return pass2
    

#====================================================
    
class VerifyingCellNumberForm(forms.Form):
    activation_code=forms.CharField(label="کد فعال سازی",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد فعال سازی را وارد کنید'}))


#====================================================

class LoginUserForm(forms.Form):
    cell_num=forms.CharField(label="شماره موبایل",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید'}))
    
    password=forms.CharField(label="رمز عبور",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))
    
    
#====================================================   

class ChangingPasswordForm(forms.Form):   
    password1=forms.CharField(label="رمز عبور",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))
    
    password2=forms.CharField(label="تکرار رمز عبور",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز را وارد کنید'}))
    
    def clean_password2(self):
        pass1=self.cleaned_data["password1"]
        pass2=self.cleaned_data["password2"]
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن یکی نیست")
        return pass2
    
    
#====================================================
    
class RememberPasswordForm(forms.Form):
    cell_num=forms.CharField(label="شماره موبایل",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید'}))
    
    
#====================================================

class Update_Profile_Form(forms.Form):
    
    first_name=forms.CharField(label="نام",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خود را وارد کنید'}))
    
    last_name=forms.CharField(label="نام خانوادگی",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خانوادگی خود را وارد کنید'}))
    
    cell_num=forms.CharField(label="شماره موبایل",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل خود را وارد کنید','readonly':'readonly'}))
    
    email=forms.EmailField(label="ایمیل",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'ایمیل خود را وارد کنید'}))
    
    address=forms.EmailField(label="آدرس",
                                    error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                                    widget=forms.Textarea(attrs={'class':'form-control','placeholder':'آدرس خود را وارد کنید','rows':"3",'cols':'3'}))
    
    image=forms.ImageField(label="عکس",
                           required=False)
    

    
#====================================================
    
    
    
    
    
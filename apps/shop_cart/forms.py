from django import forms
from .models import Payment_Types
from django.db.models import Q
from django.core.validators import RegexValidator

class Order_Form(forms.Form):
    
    first_name = forms.CharField(label="نام",
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خود را وارد کنید'}),
                            error_messages={'required':'این فیلد نمیتواند خالی باشد'})
    
    last_name = forms.CharField(label="نام خانوادگی",
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خانوادگی خود را وارد کنید'}),
                            error_messages={'required':'این فیلد نمیتواند خالی باشد'})
    
    phone_num = forms.CharField(label="شماره موبایل",
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل خود را وارد کنید'}),
                            required=False,
                            validators=[RegexValidator(r'^\d{11}$', message='شماره موبایل وارد شده معتبر نیست')])
        
    email = forms.CharField(label="ایمیل",
                            widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'ایمیل خود را وارد کنید'}),
                            error_messages={'required':'این فیلد نمیتواند خالی باشد'})
            
    address = forms.CharField(label="آدرس",
                            widget=forms.Textarea(attrs={'class':'form-control','placeholder':'آدرس خود را وارد کنید','rows':'3'}),
                            error_messages={'required':'این فیلد نمیتواند خالی باشد'})
    
    description = forms.CharField(label="توضیحات",
                            widget=forms.Textarea(attrs={'class':'form-control','placeholder':'توضیحات را وارد کنید','rows':'5'}),
                            required=False)
        
    payment_type_choices = [(item.id, item.title) for item in Payment_Types.objects.all()] 
    payment_type = forms.ChoiceField(label="شیوه پرداخت",
                            # choices=[(item.id, item.title) for item in Payment_Types.objects.all()],
                            choices = (reversed(payment_type_choices)),
                            widget=forms.RadioSelect(attrs={'checked': True}),)
    
    # payment_type_choices = [(item.id, item.title) for item in Payment_Types.objects.all()] 
    # payment_type_choices[0] = (payment_type_choices[0][1], {payment_type_choices[0]})
    # payment_type = forms.ChoiceField(label="شیوه پرداخت", choices=payment_type_choices, widget=forms.RadioSelect())
    




 

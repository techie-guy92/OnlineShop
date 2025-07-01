
from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils import timezone
from utiles import *
from .models import * 
from .forms import * 
from apps.shop_cart.models import *
from apps.payments.models import Payments



#======================================= Users =======================================
class RegisterUserView(View):
    template_name="accounting/register_user.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form=RegisterUserForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self, request, *args, **kwargs):
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            activation_code=generating_random_code(5)
            passed_time=str(timezone.now())
            
            CustomUser.objects.create_user(
                cell_num=data["cell_num"],
                activation_code=activation_code,
                password=data["password1"],
            )
           
            send_sms(data["cell_num"],f"کد فعال سازی: {activation_code}")
            
            request.session["user_session"]= {
                "activation_code":str(activation_code),
                "cell_num":data["cell_num"],
                "passed_time":passed_time,
                "remember_pass_status":False,
                }
            
            messages.success(request,"اطلاعات شما ثبت شد، برای تکمیل ثبت نام کد ارسال شده را وارد کنید","success")
            return redirect("accounting:verufy_cell_num")
  
        messages.error(request,"خطا در انجام ثبت نام","danger")
        return render(request,self.template_name,{"form":form}) 

        
#====================================================
class VerifyingCellNumberView(View):
    template_name="accounting/verifying_cell_number.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form=VerifyingCellNumberForm()
        return render(request,self.template_name,{"form":form})

    def post(self, request, *args, **kwargs):
        form=VerifyingCellNumberForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            
            user_session=request.session["user_session"]
            user_db= CustomUser.objects.get(cell_num= user_session["cell_num"])
            passed_time_2= user_session["passed_time"]
            passed_time_3= datetime.strptime(passed_time_2, "%Y-%m-%d %H:%M:%S.%f")
            time_diff = timezone.now() - passed_time_3
            total_seconds = time_diff.total_seconds()
            
            # pattern=re.compile(r"\s(\d.+)")
            # time_string="".join(re.findall(pattern,time))
            # time_obj = datetime.strptime(time_string, "%H:%M:%S.%f")
            # total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1000000
            
            if total_seconds <= 60:
                  
                if data["activation_code"] == user_session["activation_code"]:
                    
                    if user_session["remember_pass_status"] == False:
                        user_db.is_active= True
                        user_db.activation_code=generating_random_code(5)
                        user_db.save()
                        
                        messages.success(request,"ثبت نام با موفقیت انجام شد","success")
                        return redirect("main:index")
                    
                    else:
                        return redirect("accounting:changing_pass")
                else:
                    messages.error(request,"کد وارد شده صحیح نمیباشد","danger")
                    return render(request,self.template_name,{"form":form})
            else:
                messages.error(request,"اعتبار کد ارسال شده منقضی شده، کد جدید را وارد کنید","danger")
                activation_code=generating_random_code(5)
                user_db.activation_code=activation_code
                user_db.save()
                send_sms(user_session["cell_num"],f"کد فعال سازی: {activation_code}")   
                return render(request,self.template_name,{"form":form})
        else:
            messages.error(request,"اطلاعات وارد شده معتبر نمیباشد","danger")
            return render(request,self.template_name,{"form":form})
            
            
#====================================================
class LoginUserView(View):
    template_name="accounting/login_user.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form=LoginUserForm()
        return render(request,self.template_name,{"form":form})

    def post(self, request, *args, **kwargs):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_auth=authenticate(username=data["cell_num"],password=data["password"])
            
            if user_auth is not None:
                db_uesr=CustomUser.objects.get(cell_num=data["cell_num"])
                
                if db_uesr.is_admin == False:
                    messages.success(request,"ورود موفق","success")
                    login(request,user_auth)
                    next_url=request.GET.get("next")
                    
                    if next_url is not None:
                        return redirect(next_url)
                    else:
                        return redirect("main:index")
                    
                messages.error(request,"کاربر ادمین نمیتواند وارد شود","warning")
                return render(request,self.template_name,{"form":form})
            
            messages.error(request,"اطلاعات وارد شده صحیح نمیباشد","danger")
            return render(request,self.template_name,{"form":form}) 
        
        messages.error(request,"مشکلی رخ داده","danger")
        return render(request,self.template_name,{"form":form})


#====================================================
class LogoutUserView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        shopping_cart = request.session.get("shopping_cart")
        logout(request)
        request.session["shopping_cart"] = shopping_cart
        return redirect("main:index")


#====================================================
class ChangingPasswordView(View):
    template_name="accounting/changing_password.html"

    def get(self, request, *args, **kwargs):
        form=ChangingPasswordForm()
        return render(request,self.template_name,{"form":form})


    def post(self, request, *args, **kwargs):
        form=ChangingPasswordForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session["user_session"]
            user=CustomUser.objects.get(cell_num=user_session["cell_num"])
            user.set_password(data["password1"])
            user.activation_code=generating_random_code(5)
            user.save()
            messages.success(request,"رمز عبور با موفقیت تغییر کرد","success")
            return redirect("accounting:login_user")
        
        messages.error(request,"کد وارد شده صحیح نمیباشد","danger")
        return render(request,self.template_name,{"form":form})
            
    
#====================================================
class RememberPasswordView(View):
    template_name="accounting/remember_password.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form=RememberPasswordForm()
        return render(request,self.template_name,{"form":form})
    
    def post(self, request, *args, **kwargs):
        form=RememberPasswordForm(request.POST)
        if form.is_valid():
            try:
                data=form.cleaned_data
                user=CustomUser.objects.get(cell_num=data["cell_num"])
                activation_code=generating_random_code(5)
                user.activation_code=activation_code
                user.save()
                
                send_sms(data["cell_num"],f"برای بازیابی رمز عبور کد زیر را وارد نمایید\n{activation_code}")
                passed_time=str(timezone.now())
                
                request.session["user_session"]= {
                    "activation_code":str(activation_code),
                    "cell_num":data["cell_num"],
                    "passed_time":passed_time,
                    "remember_pass_status":True,
                }
                messages.success(request,"کد دریافتی را وارد نمایید","success")
                return redirect("accounting:verufy_cell_num")
            
            except:
                messages.error(request,"شماره موبایل وارد شده صحیح نمیباشد","danger")
                return render(request,self.template_name,{"form":form})


#====================================================
class DashboardView(LoginRequiredMixin,View):
    template_name = "accounting/dashboard.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
     
     
    def get(self, request, *args, **kwargs):
        client = request.user
        custom_user = Customer.objects.get(user=client)
        
        try:
            user_info = {
                "fname":client.first_name,
                "lname":client.last_name,
                "cell_num":client.cell_num,
                "email":client.email,
                "address":custom_user.address,
                "image":custom_user.image,
            }
    
        except ObjectDoesNotExist:
            user_info = {
                "fname":client.first_name,
                "lname":client.last_name,
                "cell_num":client.cell_num,
            }
            
        return render(request,self.template_name,{"user_info":user_info})


#===================================================================================
class Update_Profile_View(LoginRequiredMixin,View):
    template_name = "accounting/update_profile.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        client = request.user
        custom_user = Customer.objects.get(user=client)
        
        try:
            user_info_dict = {
                "first_name":client.first_name,
                "last_name":client.last_name,
                "cell_num":client.cell_num,
                "email":client.email,
                "address":custom_user.address,
            }
    
        except ObjectDoesNotExist:
            user_info_dict = {
                "first_name":client.first_name,
                "last_name":client.last_name,
                "cell_num":client.cell_num,
                "email":client.email,
            }
        
        form = Update_Profile_Form(initial=user_info_dict)
        
        context = {
            "form":form,
            "image":custom_user.image,
        }
        
        return render(request,self.template_name,context)
    
    
    def post(self,request):
        form = Update_Profile_Form(request.POST, request.FILES)
        client = request.user
        custom_user = Customer.objects.get(user=client)
        
        if form.is_valid():
            data = form.cleaned_data
            
            client.first_name = data["first_name"]
            client.last_name = data["last_name"]
            client.cell_num = data["cell_num"]
            client.email = data["email"]
            client.save()
            
            try:
                custom_user.address = data["address"]
                custom_user.image = data["image"]
                custom_user.save()
                
            except ObjectDoesNotExist:
                Customer.object.create(
                    user = client,
                    address = data["address"],
                    image = data["image"],
                )
            messages.success(request,"اظلاعات شما با موفقیت ویرایش شد","success")
            return redirect("accounting:dashboard")
        
        else:
            messages.error(request,"اطلاعات وارد شده معتبر نمیباشد","danger")
            return render(request,self.template_name,{"form":form})
    
    
#===================================================================================
@login_required
def fetch_orders(request):
    template_name = "accounting/fetch_orders.html"
    orders = Orders.objects.filter(order_customer_id=request.user.id).order_by("-logged_date")[:5]
    order_state_6 = OederState.objects.get(id=6)
    return render(request,template_name,{"orders":orders,"order_state_6":order_state_6})


#===================================================================================
@login_required
def fetch_payments(request):
    template_name = "accounting/fetch_payments.html"
    payments = Payments.objects.filter(payment_customer_id=request.user.id).order_by("-logged_date")[:5]
    return render(request,template_name,{"payments":payments})


#===================================================================================
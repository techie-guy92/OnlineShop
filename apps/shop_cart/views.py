from django.shortcuts import render,redirect,get_object_or_404
from .shop_cart import *
from .models import *
from .forms import *
from utiles import *
from apps.discount.forms import DiscountForm
from apps.products.models import Products
from apps.accounting.models import Customer
from apps.discount.models import Discounts

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime
from django.contrib import messages



class Shopping_Cart_View(View):
    
    def get(self,request,*args,**kwargs):
        template_name = "shopping_cart/shopping_cart.html"
        shopping_cart = Shopping_Cart(request)
        return render(request,template_name,{"shopping_cart":shopping_cart})
    
    
#==================================================================  
def show_shopping_cart_view(request):
    template_name = "shopping_cart/partials/show_shopping_cart.html"
    shopping_cart = Shopping_Cart(request)
    total_price = shopping_cart.cal_total_price()
    final_price, delivery, tax = cal_product_price(total_price)
    
    # delivery = 25000
    # if total_price > 500000:
    #     delivery = 0
    # tax = int(0.09 * total_price)
    # final_price = int(total_price+delivery+tax)
    
    # fp=Products.price - Products.fetch_discount_basket()
    
    context = {
            "shopping_cart":shopping_cart,
            "shopping_cart_count":shopping_cart.count,
            "total_price":total_price,
            "final_price":final_price,
            "delivery":delivery,
            "tax":tax,
            }
    return render(request,template_name,context)


#==================================================================  
def status_of_cart(request):
    shopping_cart = Shopping_Cart(request)
    return HttpResponse(shopping_cart.count)


#==================================================================   
def add_to_cart(request):
    product_id = request.GET.get("product_id")
    product = get_object_or_404(Products,id=product_id)
    qty = request.GET.get("qty")
         
    shopping_cart = Shopping_Cart(request)
    shopping_cart.add_to_shopping_cart(product,qty)
    return HttpResponse(shopping_cart.count)
    
    
#==================================================================
def del_from_cart(request):
    product_id = request.GET.get("product_id") 
    product = get_object_or_404(Products,id=product_id)
    shopping_cart = Shopping_Cart(request)
    shopping_cart.delete_from_shopping_cart(product)
    return redirect("Shopping_Cart:show_shopping_cart")


#==================================================================
def update_cart(request):
    list_of_product_id = request.GET.getlist("list_of_product_id[]") 
    list_of_qty = request.GET.getlist("list_of_qty[]") 
    shopping_cart = Shopping_Cart(request)
    shopping_cart.update_shopping_cart(list_of_product_id,list_of_qty)
    return redirect("Shopping_Cart:show_shopping_cart")


#==================================================================
class Create_Order_View(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounting:login_user")
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self,request):
        try:
            customer =  Customer.objects.get(user=request.user)  
        except ObjectDoesNotExist:
            customer =  Customer.objects.create(user=request.user)
            
        # order = Orders.objects.create(order_customer=customer, order_payment=get_object_or_404(Payment_Types,id=1)) #order==details_order_id , equal
        order = Orders.objects.create(order_customer=customer) 
        shopping_cart = Shopping_Cart(request)
        
        for item in shopping_cart:
                Details_Of_Order.objects.create( 
                    details_order = order,
                    # details_product =get_object_or_404(Products, slug=item["product"]["slug"]),
                    details_product_id = item["product"]["id"],
                    count = item["qty"],
                    price = item["price"],
                ) 
        # return redirect("Shopping_Cart:checkout", order.id)
        return redirect("Shopping_Cart:checkout", order.order_code)
    
        
#==================================================================
class Checkout_View(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounting:login_user")
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self,request,order_id):
        template_name = "shopping_cart/chekout.html"
        applicant = request.user
        customer = get_object_or_404(Customer, user=applicant)
        # order = get_object_or_404(Orders, id=order_id) 
        order = get_object_or_404(Orders, order_code=order_id) 
       
        shopping_cart = Shopping_Cart(request)
        total_price = shopping_cart.cal_total_price()
        final_price, delivery, tax = cal_product_price(total_price, order.discount)
        
        # delivery = 25000
        # if total_price > 500000:
        #     delivery = 0
        # tax = int(0.09 * total_price)
        # final_price = int(total_price+delivery+tax)
        
        # if order.discount > 0:
        #     final_price = final_price - ((final_price * order.discount)/100)
        
        customer_data = {
            "first_name":applicant.first_name,
            "last_name":applicant.last_name,
            "phone_num":applicant.cell_num,
            "email":applicant.email,
            "address":customer.address,
            "description":order.description,
            "payment_type":order.order_payment,
        }
        form = Order_Form(customer_data)
        form_discount = DiscountForm()
        
        context={
            "order":order,
            "shopping_cart":shopping_cart,
            "total_price":total_price,
            "final_price":final_price,
            "delivery":delivery,
            "tax":tax,
            "form":form,
            "form_discount":form_discount,
        }
        return render(request,template_name,context)
    
    
    def post(self, request, order_id):
        # Orders.objects.get(id=order_id)
        order = Orders.objects.get(order_code=order_id)
        applicant = request.user
        customer = Customer.objects.get(user=applicant) 
         
        form = Order_Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            try:
                order.description = cd["description"]    
                order.order_payment = Payment_Types.objects.get(id=cd["order_payment"])   
                order.save()
                 
                applicant.first_name = cd["first_name"]    
                applicant.last_name = cd["last_name"]    
                applicant.email = cd["email"]
                applicant.save()
                
                customer.phone_num = cd["phone_num"]    
                customer.address = cd["address"]    
                customer.save()
                
                return redirect("Shopping_Cart:checkout", order.order_code)
                # return redirect("Shopping_Cart:checkout", order_id)
                # return redirect("Shopping_Cart:checkout", order.order_code)
                
            except ObjectDoesNotExist:
                messages.error(request,"سفارش موجود نمیباشد ","danger")
                return redirect("Shopping_Cart:checkout", order.order_code)
                # return redirect("Payments:zarinpal_payment", order_id)
                
        return redirect("Shopping_Cart:checkout", order.order_code)
        # return redirect("Shopping_Cart:checkout", order_id)
        
        
#==================================================================
class ConfirmDiscountView(View):
    
    def post(self, request, *args, **kwargs):
        order_id = kwargs["order_id"]
        form_discount = DiscountForm(request.POST)
        if form_discount.is_valid():
            cd = form_discount.cleaned_data
            discount_code = cd["discount_code"]
        
        
        discount = Discounts.objects.filter(
                Q(discount_code=discount_code) &
                Q(is_active=True) &
                Q(start_date__lte=datetime.now()) &
                Q(expiry_date__gte=datetime.now()) 
            )
        
        discount_percentage = 0
        try:
            # Orders.objects.get(id=order_id)
            order = Orders.objects.get(order_code=order_id)
            
            if discount:
                discount_percentage = discount[0].discount_percentage
                order.discount = discount_percentage
                order.save()
                messages.success(request,"کد تخفیف اعمال شد","success")
                return redirect("Shopping_Cart:checkout", order.order_code)
                # return redirect("Shopping_Cart:checkout", order_id)
            
            else:
                messages.error(request,"کد وارد شده معتبر نمیباشد","danger")
                order.discount = discount_percentage
                order.save()
                 
        except ObjectDoesNotExist:
            messages.error(request,"سفارش موجود نمیباشد ","danger")
            
        return redirect("Shopping_Cart:checkout", order.order_code)
        # return redirect("Shopping_Cart:checkout", order_id)
        

#==================================================================
            
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from apps.shop_cart.models import *
from apps.warehouse.models import *
from .models import Payments
import requests
import json


#==================================================================
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


ZP_API_REQUEST = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8080/payments/verify/'

class ZarinpalPaymentView(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounting:login_user")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, order_id):
        try:
            order = Orders.objects.get(order_code=order_id)
            aplicant = request.user 
            description = "پرداخت از طریق درگاه زرین پال"
            payment = Payments.objects.create(
                payment_order = order,
                payment_customer = Customer.objects.get(user=aplicant),
                amount_paid = order.fetch_data_price(),
                description = description,
            )
            payment.save()
            
            request.session["payment_session"] = {
                "order_id":order.order_code,
                "payment_id":payment.id,
            }
            
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": order.fetch_data_price(),
                "Description": description,
                "Phone": aplicant.cell_num,
                "CallbackURL": CallbackURL,
            }
            
            data = json.dumps(data)
            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            try:
                response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

                if response.status_code == 200:
                    response = response.json()
                    if response['Status'] == 100:
                        order.is_paid = True
                        order.save()
                        
                        for soldItem in order.details_Order.all():
                            Warehouse.objects.create(
                                product = soldItem.product,
                                count = soldItem.count,
                                warehouse_type = Warehouse_Types.objects.get(id=2),
                                logged_user = request.user,
                                price = soldItem.price,
                            )
                            
                        return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                    else:
                        return {'status': False, 'code': str(response['Status'])}
                return response
    
            except requests.exceptions.Timeout:
                return {'status': False, 'code': 'timeout'}
            except requests.exceptions.ConnectionError:
                return {'status': False, 'code': 'connection error'}
            
        except ObjectDoesNotExist:
                order = Orders.objects.get(order_code=order_id)
                return redirect("Shopping_Cart:checkout", order.order_code)   
                # return redirect("Shopping_Cart:checkout", order_id)   
        
        
#==================================================================
class ZarinpalVerifyPaymentView(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounting:login_user")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request,):
        order_id = request.session["payment_session"]["order_id"] 
        payment_id = request.session["payment_session"]["payment_id"]
        order = Orders.objects.get(order_code=order_id) 
        payment = Payments.objects.get(id=payment_id) 
        
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.fetch_data_price(),
            "Authority": "",
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            
            order.is_paid = True
            payment.is_paid = True
            payment.status_code = response 
            payment.ref_id = str(response['RefID']),
            order.save()
            payment.save()
            
            if response['Status'] == 100:
                order.is_paid = True
                payment.is_paid = True
                payment.status_code = response 
                payment.ref_id = str(response['RefID']),
                order.save()
                payment.save()
                # return {'status': True, 'RefID': response['RefID']}
                return redirect("Payments:return_payment_gateway", f"'RefID': {response['RefID']}")
            
            else:
                payment.status_code = response 
                payment.save()
                # return {'status': False, 'code': str(response['Status'])}
                return redirect("Payments:return_payment_gateway", f"'code': {str(response['Status'])}")

        return response
    
    
#==================================================================
def Return_Payment_Gateway(request, message):
    return render(request,"payments/verify.html",{"message":message})


#==================================================================
from django.urls import path,re_path
from .views import *


app_name="Payments"
urlpatterns = [
    # path("zarinpal_payment/<int:order_id>/",ZarinpalPaymentView.as_view(),name="zarinpal_payment"),
    re_path(r'^zarinpal_payment/(?P<order_id>[\w\-]+)/$', ZarinpalPaymentView.as_view(), name='zarinpal_payment'),
    path("verify/",ZarinpalVerifyPaymentView.as_view(),name="zarinpal_verify_payment"),
    path("return_payment_gateway/",Return_Payment_Gateway,name="return_payment_gateway"),
]

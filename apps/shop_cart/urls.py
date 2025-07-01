from django.urls import path,re_path
from .views import *


app_name="Shopping_Cart"
urlpatterns = [
    path("shopping_cart/",Shopping_Cart_View.as_view(),name="shopping_cart"),
    path("show_shopping_cart/",show_shopping_cart_view,name="show_shopping_cart"),
    path("status_of_cart/",status_of_cart,name="status_of_cart"),
    path("add_to_cart/",add_to_cart,name="add_to_cart"),
    path("del_from_cart/",del_from_cart,name="del_from_cart"),
    path("update_cart/",update_cart,name="update_cart"),
    path("create_order/",Create_Order_View.as_view(),name="create_order"),
    # path("checkout/<int:order_id>/",Checkout_View.as_view(),name="checkout"),
    re_path(r'^checkout/(?P<order_id>[\w\-]+)/$', Checkout_View.as_view(), name='checkout'),
    re_path(r'^confirm_discount/(?P<order_id>[\w\-]+)/$', ConfirmDiscountView.as_view(), name='confirm_discount'),
]

from django.urls import path
from .views import *


app_name="accounting"
urlpatterns = [
    path("register_user/",RegisterUserView.as_view(),name="register_user"),
    path("verufy_cell_num/",VerifyingCellNumberView.as_view(),name="verufy_cell_num"),
    path("login_user/",LoginUserView.as_view(),name="login_user"),
    path("logout_user/",LogoutUserView.as_view(),name="logout_user"),
    path("changing_pass/",ChangingPasswordView.as_view(),name="changing_pass"),
    path("remember_pass/",RememberPasswordView.as_view(),name="remember_pass"),
    path("dashboard/",DashboardView.as_view(),name="dashboard"),
    path("update_profile/",Update_Profile_View.as_view(),name="update_profile"),
    path("fetch_orders/",fetch_orders,name="fetch_orders"),
    path("fetch_payments/",fetch_payments,name="fetch_payments"),
]



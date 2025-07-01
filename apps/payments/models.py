from django.db import models
from apps.shop_cart.models import *
from apps.accounting.models import *
from django.utils import timezone


class Payments(models.Model):
    payment_order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="paymentOrder", verbose_name="سفارش")
    payment_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="paymentsCustomer", verbose_name="مشتری")
    description = models.TextField(verbose_name="توضیحات")
    amount_paid = models.IntegerField(verbose_name="مبلغ")
    is_paid = models.BooleanField(default=False, verbose_name="وضعیت")
    status_code = models.IntegerField(blank=True, null=True, verbose_name="کد وضیت پرداخت")
    ref_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="کد پیگیری")
    logged_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    def __str__(self):
        return f"{self.payment_order} {self.payment_customer} {self.ref_id}"
    
    class Meta:
        verbose_name="پرداخت"
        verbose_name_plural="پرداخت ها"
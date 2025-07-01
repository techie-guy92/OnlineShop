from django.db import models
from django.utils import timezone
from apps.accounting.models import Customer
from apps.products.models import Products
from utiles import *
import uuid



#=======================================================================
class Payment_Types(models.Model):
    title = models.CharField(max_length=100,verbose_name="شیوه پرداخت")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "شیوه پرداخت"
        verbose_name_plural = "شیوه های پرداخت"
        
        
#=======================================================================
class OederState(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان وضعیت سفارش")
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = "وضعیت صفارش"
        verbose_name_plural =  "انواع وضعیت سفارش"
        
        
#=======================================================================
class Orders(models.Model):
    order_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="order_Customer", verbose_name="مشتری")
    order_payment = models.ForeignKey(Payment_Types, on_delete=models.CASCADE, default=1, blank=True, null=True, related_name="order_Payment", verbose_name="شیوه پرداخت")
    order_state = models.ForeignKey(OederState, on_delete=models.CASCADE, related_name="order_State", blank=True, null=True, verbose_name="وضعیت سفارش")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    logged_date = models.DateTimeField(default=timezone.now,verbose_name="تاریخ ثبت")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    is_paid = models.BooleanField(default=False, verbose_name="وضعیت پرداخت")
    order_code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="کد سفارش")
    discount = models.IntegerField(default=0, blank=True, null=True, verbose_name="تخفیف")
    
    def __str__(self) -> str:
        return f"{self.order_customer}\t{self.id}\t{self.is_paid}"
    
    
    def fetch_data_price(self):
        sum = 0
        for item in self.details_Order.all():
            sum+= item.details_product.fetch_discount_basket() * item.count    
        # for item in self.details_Order.all():
        #     sum+= item.price * item.count  
             
        final_price, delivery, tax = cal_product_price(sum, self.discount)
        return int(final_price * 10)
    
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"
        
        
#=======================================================================
class Details_Of_Order(models.Model):
    details_order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="details_Order", verbose_name="سفارش")
    details_product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="details_Product", verbose_name="محصول")
    count = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    price = models.IntegerField(verbose_name="مبلغ",)
    
    def __str__(self):
        return f"{self.details_order}\t{self.details_product}\t{self.count}\t{self.price}"
    
    class Meta:
        verbose_name = "جزییات سفارش"
        verbose_name_plural = "جزِییات سفارش ها"
        
        
#=======================================================================    
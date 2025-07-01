from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from apps.products.models import *
import uuid

#=======================================================================
class Discounts(models.Model):
    # discount_code = models.UUIDField(max_length=100,unique=True,default=uuid.uuid4,verbose_name="کد تخفیف")
    discount_code = models.CharField(max_length=100,unique=True,verbose_name="کد تخفیف")
    discount_percentage = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(50)],verbose_name="درصد تخفیف")
    is_active = models.BooleanField(default=False,verbose_name="وضعیت")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    expiry_date = models.DateTimeField(verbose_name="تاریخ انقضا")
    
    class Meta:
        verbose_name="تخفیف"
        verbose_name_plural="تخفیف ها"
        
        
    def __str__(self):
        return f"{self.discount_code} {self.discount_percentage} {self.is_active} {self.start_date} {self.expiry_date}"
    
    
#=======================================================================
class DiscountBasket(models.Model):
    title = models.CharField(max_length=100,verbose_name="عنوان سبد تخفیف")
    discount_basket_percentage = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(50)],verbose_name="درصد تخفیف")
    is_active = models.BooleanField(default=False,verbose_name="وضعیت")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    expiry_date = models.DateTimeField(verbose_name="تاریخ انقضا")
    
    class Meta:
        verbose_name="سبد تخفیف"
        verbose_name_plural="سبدهای تخفیف"
        
        
    def __str__(self):
        return f"{self.title} {self.discount_basket_percentage} {self.is_active} {self.start_date} {self.expiry_date}"
    
    
    
#=======================================================================
class DiscountBasketDetails(models.Model):
    discount_basket = models.ForeignKey(DiscountBasket,on_delete=models.CASCADE,related_name="discountBasket",verbose_name="سبد تخفیف")
    discount_product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="discountProducts",verbose_name="کالاهای تخفیف دار")
    
    class Meta:
        verbose_name="جزییات سبد تخفیف"

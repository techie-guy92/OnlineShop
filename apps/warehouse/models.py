from django.db import models
from apps.products.models import Products
from apps.accounting.models import CustomUser



#=======================================================================
class Warehouse_Types(models.Model):
    title = models.CharField(max_length=50,verbose_name="عنوان")
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name="نوع انبار"
        verbose_name_plural="نوع انبار"
        
        
#=======================================================================
class Warehouse(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="warhouseProduct",verbose_name="کالا")
    count = models.IntegerField(verbose_name="تعداد")
    warehouse_type = models.ForeignKey(Warehouse_Types,on_delete=models.CASCADE,related_name="warhouseType",verbose_name="انبار")
    logged_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="loggedUser",verbose_name="کاربر")
    price = models.IntegerField(blank=True,null=True,verbose_name="قیمت")
    logged_date = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت")
    
    
    def __str__(self):
        return f"{self.warehouse_type} {self.product}"
    
    class Meta:
        verbose_name="انبار"
        verbose_name_plural="انبار"
        

#=======================================================================
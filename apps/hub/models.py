from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from apps.accounting.models import CustomUser
from apps.products.models import Products


#============================================================================
class Comments(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="Commetnt_Product",verbose_name="کالا")
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="Comment_User",verbose_name="کاربر")
    admin = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="Comment_Admin",verbose_name="ادمین",blank=True,null=True)
    comment = models.TextField(verbose_name="نظر")
    comment_parent = models.ForeignKey("Comments",on_delete=models.CASCADE,related_name="Comment_Parent",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تارخ ثبت")
    is_active = models.BooleanField(default=False,verbose_name="وضعیت فعال بودن")
    
    def __str__(self):
        return f"{self.product} {self.user}"
    
    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        
        
#============================================================================
class Scores(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="Score_Product",verbose_name="کالا")
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="Score_User",verbose_name="کاربر")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تارخ ثبت")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],verbose_name="امتیاز")

    def __str__(self):
        return f"{self.product} {self.user}"
    
    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازات"


#============================================================================
class UserWishlist(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="Wishlist_Product",verbose_name="کالا")
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="Wishlist_User",verbose_name="کاربر")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تارخ ثبت")

    def __str__(self):
        return f"{self.product} {self.user}"
    
    class Meta:
        verbose_name = "علاقه مندی"
        verbose_name_plural = "علاقه مندی ها"

#============================================================================

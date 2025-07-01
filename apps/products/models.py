from django.db import models
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Sum,Avg
from django.utils.text import slugify
from unidecode import unidecode
from utiles import *
from middlewares.middlewares import * 
from datetime import datetime



#=======================================================================
class Groups(models.Model):
    title = models.CharField(max_length=50,verbose_name="گروه")
    short_description = models.TextField(default="",blank=True,null=True,verbose_name="خلاصه توضیحات")
    description = RichTextUploadingField(config_name="special",blank=True,null=True,verbose_name="توضیحات")
    folder_path = Uploading_Files("images","groups")  
    image = models.ImageField(upload_to=folder_path.file_name,verbose_name="تصویر")
    is_active = models.BooleanField(default=True,blank=True,verbose_name="وضعیت فعال بودن")
    slug = models.SlugField(blank=True,null=True)
    logged_date = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ درج")
    published_date = models.DateTimeField(default=timezone.now,verbose_name="تاریخ انتشار")
    updated_date = models.DateTimeField(auto_now=True,verbose_name="آخرین بروزرسانی")
    groups = models.ForeignKey("Groups",on_delete=models.CASCADE,blank=True,null=True,related_name="group",verbose_name="گروه")
    
    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "گروه"
        verbose_name_plural = "گروه ها"
        
        
#=======================================================================
class Brands(models.Model):
    title = models.CharField(max_length=50,verbose_name="برند")
    folder_path = Uploading_Files("images","brands")  
    image = models.ImageField(upload_to=folder_path.file_name,verbose_name="تصویر")
    slug = models.SlugField(blank=True,null=True)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"
        
        
#=======================================================================
class Features(models.Model):
    title = models.CharField(max_length=100,verbose_name="ویژگی")
    groups = models.ManyToManyField(Groups,related_name="featureGroup",verbose_name="گروه")        
    
    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی ها"
        
        
#=======================================================================
class Products(models.Model):
    title = models.CharField(max_length=250,verbose_name="نام کالا")
    short_description = models.TextField(default="",blank=True,null=True,verbose_name="خلاصه توضیحات")
    description = RichTextUploadingField(config_name="special",blank=True,null=True,verbose_name="توضیحات")
    folder_path = Uploading_Files("images","products")  
    image = models.ImageField(upload_to=folder_path.file_name,verbose_name="تصویر")
    is_active = models.BooleanField(default=True,blank=True,verbose_name="وضعیت فعال بودن")
    price = models.PositiveIntegerField(default=0,verbose_name="قیمت")
    slug = models.SlugField(max_length=250,blank=True,null=True)
    logged_date = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ درج")
    published_date = models.DateTimeField(default=timezone.now,verbose_name="تاریخ انتشار")
    updated_date = models.DateTimeField(auto_now=True,verbose_name="آخرین بروزرسانی")
    product_groups = models.ManyToManyField(Groups,related_name="productGroup",verbose_name="گروه کالا")
    product_brands = models.ForeignKey(Brands,on_delete=models.CASCADE,null=True,related_name="productBrand",verbose_name="برند")
    product_features = models.ManyToManyField(Features,through="Features_Products")
    
    def __str__(self):
        return self.title
    
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         new_slug = reaplace_dash_to_space(self.title)
    #         self.slug = slugify(unidecode(new_slug))
    #     super().save(*args, **kwargs)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title)
        super().save(*args, **kwargs)
       
       
    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})
        
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image.url,
            "price": self.price,
            "slug": self.slug,
        }
        
        
    def fetch_discount_basket(self):
        discount_basket_list = []
        for product in self.discountProducts.all():
            if (product.discount_basket.is_active == True and
                product.discount_basket.start_date <= datetime.now() and
                datetime.now() <= product.discount_basket.expiry_date):
                
                discount_basket_list.append(product.discount_basket.discount_basket_percentage)
        discount = 0
        if len(discount_basket_list) > 0:
            discount = max(discount_basket_list)
        return self.price - ((self.price * discount) / 100)
            
    
    def fetch_count_of_product(self):
        increment = self.warhouseProduct.filter(warehouse_type_id=1).aggregate(Sum("count"))
        decrement = self.warhouseProduct.filter(warehouse_type_id=2).aggregate(Sum("count"))
        
        input = 0 
        if increment["count__sum"] != None:
            input = increment["count__sum"]
            
        output = 0
        if decrement["count__sum"] != None:
            output = decrement["count__sum"]
        
        final_count = input - output
        return final_count
    
    
    def fetch_score(self):
        request = RequestMiddleWare(get_response=None)
        request = request.thread_local.current_request
        client = self.Score_Product.filter(user=request.user)
        score = 0
        
        if client.count() > 0:
            score = client[0].score
            
        return score


    def cal_avg_score(self):
        avg_score = self.Score_Product.all().aggregate(Avg("score"))["score__avg"]
        
        if avg_score == None:
            avg_score = 0
            
        return avg_score
    
    
    def fetch_wish_list(self):
        request = RequestMiddleWare(get_response=None)
        request = request.thread_local.current_request
        products = self.Wishlist_Product.filter(user=request.user).exists()
        return products
    
    
    def fetch_main_group(self):
        return self.product_groups.all()[0].id
        
        
    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالا ها"
    
          
#=======================================================================
class Feature_Value(models.Model):
    value_title = models.CharField(max_length=100,verbose_name="مقدار")
    feature = models.ForeignKey(Features,on_delete=models.CASCADE,blank=True,null=True,related_name="featureValue_Feature",verbose_name="ویژگی")

    def __str__(self):
        return f"{self.id} - {self.value_title}"
    
    class Meta:
        verbose_name = "مقدار ویژگی"
        verbose_name_plural = "مقادیر ویژگی ها"
        
        
#=======================================================================
class Features_Products(models.Model):
    features = models.ForeignKey(Features,on_delete=models.CASCADE,verbose_name="ویژگی")
    products = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="productFeature",verbose_name="کالا")
    value = models.CharField(max_length=100,verbose_name="مقدار ویژگی (اختیاری)") 
    filter_value = models.ForeignKey(Feature_Value,on_delete=models.CASCADE,blank=True,null=True,related_name="productFeature_featureValue",verbose_name="مقدار")
    
    def __str__(self):
        return f"{self.features} - {self.products} - {self.value}"
    
    class Meta:
        verbose_name = "ویژگی محصول"
        verbose_name_plural = "ویژگی های های محصول"


#=======================================================================
class Product_Gallery(models.Model):
    folder_path = Uploading_Files("images","product_gallery")  
    image = models.ImageField(upload_to=folder_path.file_name,verbose_name="تصویر کالا")
    products = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="productImages",verbose_name="کالا")
    
    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصویرها"
        
        
#=======================================================================





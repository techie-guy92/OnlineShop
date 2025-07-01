from django.db import models
from utiles import *
from django.utils import timezone
from django.utils.html import mark_safe



class Slider(models.Model):
    heading_1 = models.CharField(max_length=500, blank=True, null=True, verbose_name="تیتر یک")
    heading_2 = models.CharField(max_length=500, blank=True, null=True, verbose_name="تیتر دو")
    heading_3 = models.CharField(max_length=500, blank=True, null=True, verbose_name="تیتر سه")
    folder_path = Uploading_Files("images","sliders")  
    image = models.ImageField(upload_to=folder_path.file_name, verbose_name="اسلایدر")
    link_slider = models.URLField(max_length=200, blank=True, null=True, verbose_name="لینک")
    is_active = models.BooleanField(default=True, blank=True, verbose_name="وضعیت فغال بودن")
    craete_at = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت")
    published_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    
    
    def __str__(self):
        return f"{self.heading_1}"
    
    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدرها"
    
    def img_slider(self):
        return mark_safe(f'<img src="/media/{self.image}" style="width:80px; height:60px;">')
    
    
    def link(self):
        return mark_safe(f'<a href="{self.link_slider}" target="_blank">link</a>')
    
    
    img_slider.short_description = "تصویر اسلایدر"
    link.short_description = "پیوند"
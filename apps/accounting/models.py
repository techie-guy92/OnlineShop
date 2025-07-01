from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from utiles import *


#======================================= Users =======================================
class CustomUserManage(BaseUserManager):
    
    def create_user(self,cell_num,first_name="",last_name="",email="",activation_code=None,gender=None,password=None):
        
        if not cell_num:
            raise ValueError("وارد کردن شماره موبایل اجباری است")
        
        user=self.model(
            cell_num=cell_num,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            activation_code=activation_code,
            gender=gender,
        )
        # user.make_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,cell_num,first_name,last_name,email,activation_code=None,gender=None,password=None):
        
        user=self.create_user(
            cell_num=cell_num,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            activation_code=activation_code,
            gender=gender,
            password=password,
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    
    
#====================================================
class CustomUser(AbstractBaseUser,PermissionsMixin):
    first_name=models.CharField(max_length=50,blank=True,verbose_name="نام")
    last_name=models.CharField(max_length=50,blank=True,verbose_name="نام خانوادگی")
    cell_num=models.CharField(max_length=12,unique=True,verbose_name="شماره موبایل")
    email=models.EmailField(max_length=50,blank=True,verbose_name="ایمیل")
    gender_optins=(("rather not to say","اعلام نکردن"),("male","آقا"),("female","خانم"))
    gender=models.CharField(max_length=50,choices=gender_optins,default="rather not to say",blank=True,null=True,verbose_name="جنسیت")
    date_joined=models.DateTimeField(default=timezone.now)
    activation_code=models.CharField(max_length=20,blank=True,null=True)
    is_active=models.BooleanField(default=False,verbose_name="وضعیت فغال بودن")
    is_admin = models.BooleanField(default=False,verbose_name="وضعیت کارمند بودن")
    is_superuser = models.BooleanField(default=False,verbose_name="وضعیت ابرکارمند بودن")
    
    USERNAME_FIELD="cell_num"
    REQUIRED_FIELDS=["email","first_name","last_name",]
    
    objects=CustomUserManage()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # def is_activation_code_valid(self):
    #     return (timezone.now() - self.date_joined).total_seconds() <= 60

    class Meta:
    #   db_table = "جدول کاربر"
      verbose_name = "کاربر"
      verbose_name_plural = "کاربر ها"

    @property
    def is_staff(self):
        return self.is_admin
    
      
#====================================================
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True ,verbose_name="نام مشتری")
    phone_num=models.CharField(max_length=12, blank=True, null=True ,verbose_name="شماره موبایل")
    address = models.TextField(blank=True ,null=True ,verbose_name="آدرس")
    folder_path = Uploading_Files("images","customer")  
    image = models.ImageField(upload_to=folder_path.file_name, blank=True, null=True ,verbose_name="تصویر پروفایل")

    def __str__(self):
        return f"{self.user}" 
    
    class Meta:
      verbose_name = "مشتری"
      verbose_name_plural = "مشتری ها"


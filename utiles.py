#=======================================================================
from random import randint

def generating_random_code(count):

    count-= 1
    generator= randint(10**count, 10**(count + 1)-1)
    return generator


#=======================================================================
def send_sms(cell_num, messages):
    
    pass    
    # try:
    #     api= KavenegarAPI("")
    #     params= {"sender":"","receptor":"","message":""}
    #     response= api.sms_send(params)
    #     return response
    
    # except APIException as error:
    #     print(f"error1:{error}")
        
    # except HTTPException as error:
    #     print(f"error2:{error}")
    
    
#=======================================================================    
import os
from uuid import uuid4

class Uploading_Files:
    def __init__(self, prefix_dir, suffix_dir):
      self.prefix_dir = prefix_dir
      self.suffix_dir = suffix_dir
      
    def file_name(self,instance,filename):
        filename, ext = os.path.split(filename)
        new_filename = f"{uuid4()}{ext}"
        return f"{self.prefix_dir}/{self.suffix_dir}/{new_filename}"

#sample
# folder_path = Uploading_Files("images","group")  


#=======================================================================
# Both modules can be used, but 'slugify' will convert the slug to Finglish, 
# while 'django.utils.text' can save Persian slugs when the 'allow_unicode=True' option is enabled.

from django.utils.text import slugify
# from slugify import slugify

def replace_dash_to_space(title):
        new_title="".join([eliminator.replace(" ","-") for eliminator in title])
        return new_title.lower()
    
# def generate_slug(title):
#     new_title = replace_dash_to_space(title)
#     return slugify(new_title)

def generate_slug(title):
    new_title = replace_dash_to_space(title)
    return slugify(new_title, allow_unicode=True)
   
# print(generate_slug("soheil Daliri TEHRAN"))


#=======================================================================
import sys
import django

def django_path():
    sys.path = sys.path[1:]
    print(f"Django's path:\n{django.__path__}\n")


# django_path()


#=======================================================================
def cal_product_price(price, discount=0):
    delivery = 25000
    if price > 500000:
        delivery = 0
    tax = int(0.003 * (price + delivery))
    agg = int(price + delivery + tax)
    agg = int(agg - ((agg * discount)/100))
    
    return agg,delivery,tax    


#=======================================================================

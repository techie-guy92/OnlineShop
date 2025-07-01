from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os
from .models import Products



@receiver(post_delete, sender=Products)
def del_product_img(sender,**kwargs):
    img = str(kwargs["instance"].image)
    img_path = settings.MEDIA_ROOT + img
    
    if os.path.isfile(img_path):
        os.remove(img_path)
        print(f"***** '{img}' has been deleted *****")
        
        
# post_delete.connect(receiver=del_product_img,sender=Products)


#'images/products/21e4b273-e9dd-4379-a6bf-7c6fda7bac5alogo.png'
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from .forms import *
from .models import *


#============================================================================
class Making_CommentsView(View):
    template_name = "hub/making_comment.html"
    
    def get(self,request,*args,**kwargs):
        product_Id = request.GET.get("product_Id")    
        comment_Id = request.GET.get("comment_Id")
        slug = kwargs["slug"]
        
        initial_values = {
            "product_id" : product_Id,
            "comment_id" : comment_Id,
        }    
        form = CommentForm(initial=initial_values)
        
        context = {
            "form":form,
            "slug":slug,
        }
        
        return render(request,self.template_name,context)
        
        
    def post(self,request,*args,**kwargs):
        slug = kwargs.get("slug")
        product = get_object_or_404(Products,slug=slug)                   
        parent = None  
        
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            comment_id = data["comment_id"]
            if comment_id:
                parent = Comments.objects.get(id=comment_id)
                 
            Comments.objects.create(
                product = product,
                user = request.user,
                comment = data["comment"],
                comment_parent = parent,
            )
    
            messages.success(request,"نظر شما ثبت شد")
            return redirect("products:product_detail",product.slug)
        
        messages.error(request,"خطا در ارسال نظر","danger")
        return redirect("products:product_detail",product.slug)
    
    
#============================================================================
def Giving_Score_View(request):
    product_Id = request.GET.get("product_Id")
    score = request.GET.get("score")
    product = Products.objects.get(id=product_Id)
    
    Scores.objects.create(
        product = product,
        user = request.user,
        score = score, 
    )
    
    response_data = {
        'success': True,
        'message': 'امتیاز شما ثبت شد'
    }

    messages.success(request,"امتیاز شما ثبت شد","success")
    return JsonResponse(response_data)
    

#============================================================================
def Add_To_Wish_List_View(request):
    product_Id = request.GET.get("product_Id")
    product = Products.objects.get(id=product_Id)
    client = request.user
    wish_list = UserWishlist.objects.filter(Q(user_id=client.id) & Q(product_id=product_Id)).exists()
    
    response_data = {
        "success": True,
        "message_1": "این کالا به لیست علاقه مندی های شما اضافه شد",
        "message_2": "این کالا لیست علاقه مندی های شما وجود داشت",
    }
    
    if not wish_list:
        UserWishlist.objects.create(
            product = product,
            user = client
        )
        
        messages.success(request,"این کالا به لیست علاقه مندی های شما اضافه شد","success")
        return JsonResponse(response_data)
    
    messages.success(request,"این کالا لیست علاقه مندی های شما وجود داشت","success")
    return JsonResponse(response_data)
    

#============================================================================
class Wish_List_View(View):
    template_name = "hub/wish_list.html"
    
    def get(self,request,*args,**kwargs):
        user_wish_list = UserWishlist.objects.filter(Q(user_id=request.user.id))
        context = {
            "user_wish_list":user_wish_list,
        }
        return render(request,self.template_name,context)
    
    
#============================================================================
# def Confirm_Comments_View(self, request):

#     comments = Comments.objects.all()
#     admin_user = CustomUser.objects.get(is_admin=True)
    
#     for comment in comments:
#         if comment.is_active:
#             Comments.objects.create(
#                 admin = admin_user
#             )


#============================================================================



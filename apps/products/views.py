from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.db.models import Q,Count,Min,Max
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator
from .models import *
from .filters import *
from .comparison import *


#==================================================================================================
def fetching_root_groops_view():
    return Groups.objects.filter(Q(is_active=True) & Q(groups=None))


#==================================================================
# def fetch_cheapest_products_view(request, category_slug=None):
def fetch_cheapest_products_view(request):
    template_name = "products/cheapest_products.html"
    
    products=Products.objects.filter(is_active=True).order_by("price")[:5] #""
    groups=fetching_root_groops_view()
    context={
        "products":products,
        "groups":groups,
    }
    return render(request,template_name,context)
    
    
#==================================================================
def fetching_latest_products_view(request):
    template_name = "products/latest_products.html"
    
    products=Products.objects.filter(is_active=True).order_by("-published_date")[:5] 
    groups=fetching_root_groops_view()
    context={
        "products":products,
        "groups":groups,
    }
    return render(request,template_name,context)


#==================================================================
def fetching_popular_groups_view(request):
    template_name = "products/popular_groups.html"
    
    groups=Groups.objects.filter(Q(is_active=True))\
        .annotate(count=Count("productGroup")).order_by("-count")[:5]
    context={
        "groups":groups,
    }
    return render(request,template_name,context)


#==================================================================
# In this part of code, two functions were mixed as one class to not use 'render partial'.
# All previous codes are available but their commented

class fetching_product_detail_view(View):
    template_name = "products/product_detail.html"
    
    def get(self,request,*args,**kwargs):
        
        current_product = get_object_or_404(Products,slug=kwargs["slug"])
        if current_product.is_active:
            product = current_product
            
        related_products=[]
        for group in current_product.product_groups.all():
            related_products.extend(Products.objects.filter(Q(is_active=True) & Q(product_groups=group) & ~Q(id=current_product.id)))
                    
        return render(request,self.template_name,{"product":product,"related_products":related_products})


#==================================================================
# class fetching_product_detail_view(View):
#     template_name = "products/product_detail.html"
    
#     def get(self,request,slug):
#         product = get_object_or_404(Products,slug=slug) #first procedure
#         if product.is_active:
#             return render(request,self.template_name,{"product":product})
        
    
#==================================================================
# def fetching_related_products_view(request,*args,**kwargs):
#     template_name = "products/product_partials/related_products.html"
    
#     current_product = get_object_or_404(Products,slug=kwargs["slug"]) #second procedure
#     related_products=[]
#     for group in current_product.product_groups.all():
#         related_products.extend(Products.objects.filter(Q(is_active=True) & Q(product_groups=group) & ~Q(id=current_product.id)))
#     return render(request,template_name,{"related_products":related_products})


#==================================================================
class feching_all_groups_view(View):
    template_name = "products/all_groups.html"
    
    def get(self,request):
        all_groups = Groups.objects.filter(Q(is_active=True))\
            .annotate(count=Count("productGroup")).order_by("-count")
        return render(request,self.template_name,{"all_groups":all_groups})


#==================================================================
def fetching_all_groups_2_view(request):
    template_name = "products/product_partials/groups_filter.html"
    
    all_groups_2 = Groups.objects.annotate(count=Count("productGroup"))\
        .filter(Q(is_active=True) & ~Q(count=0)).order_by("-count")
    return render(request ,template_name, {"all_groups_2":all_groups_2})


#==================================================================
def feching_all_brands_view(request,*args,**kwargs):
    template_name = "products/product_partials/brands.html"
    
    current_group = get_object_or_404(Groups, slug=kwargs["slug"])
    products_id = current_group.productGroup.filter(is_active=True).values("product_brands_id")
    brands = Brands.objects.filter(id__in=products_id)\
        .annotate(count=Count("productBrand")).filter(~Q(count=0))\
            .order_by("-count")
    brands_count = Brands.objects.filter(id__in=products_id)        
    return render(request,template_name,{"brands":brands,"brands_count":brands_count})


#==================================================================
def fetching_filters_for_features_view(request, *args,**kwargs):
    template_name = "products/product_partials/filters_for_features.html"
    
    current_group = get_object_or_404(Groups, slug=kwargs["slug"])
    features = current_group.featureGroup.all()
    feature_dict = dict()
    for feature in features:
        feature_dict[feature] = feature.featureValue_Feature.all()
    return render(request, template_name, {"feature_dict":feature_dict,})


#================================================================== 
class feching_products_view(View):
    template_name = "products/products.html"
    
    def get(self,request,*args,**kwargs):
        slug = kwargs["slug"]
        current_group = get_object_or_404(Groups,slug=slug)
        products = Products.objects.filter(Q(is_active=True) & Q(product_groups=current_group))

        res_agg = products.aggregate(min=Min("price"),max=Max("price"))
        
        price_filter = ProductFilter(request.GET,queryset=products)
        products = price_filter.qs
        
        
        brands_filter = request.GET.getlist("brand")
        if brands_filter:
            products = products.filter(brand__id__in = brands_filter)
         
            
        features_filter = request.GET.getlist("feature")
        if features_filter:
            products = products.filter(productFeature__filter_value__id__in = features_filter).distinct()
            
            
        sort_type = request.GET.get("sort_type")
        if not sort_type:
            sort_type = "0"
            
        if sort_type == "1":
            products = products.order_by("price")
            
        elif sort_type == "2":
            products = products.order_by("-price")
            
            
        group_slug = slug
        product_per_page = 5
        paginator = Paginator(products,product_per_page)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        product_count = products.count()
        
        
        show_count_product = []
        i = product_per_page
        while i < product_count:
            show_count_product.append(i)
            i*=2
        show_count_product.append(i)
        
        
        context={
            "group_slug":group_slug,
            "products":products,
            "current_group":current_group,
            "res_agg":res_agg,
            "price_filter":price_filter,
            "product_count":product_count,
            "page_obj":page_obj,
            "sort_type":sort_type,
            "show_count_product":show_count_product,         
        }
            
        return render(request,self.template_name,context)


#==================================================================
def fetching_features_in_admin_view(request):
    if request.method == "GET":
        feature_id = request.GET["feature_id"]
        feature_values = Feature_Value.objects.filter(feature_id=feature_id)
        res = {fv.value_title:fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False)

    
#==================================================================
# def dict_converter_of_products(request):
#     template_name = ""
    
#     product_groups = Groups.objects.filter(Q(is_active=True) & Q(groups=None))
#     product_dict = {}
    
#     for group in product_groups:
#         sub_groups = Groups.objects.filter(Q(is_active=True) & Q(groups=group.id))
#         product_dict[group] = sub_groups
        
#     context = {
#         "product_groups":product_groups,
#         "product_dict":product_dict,
#     }
    
#     return render (request,template_name,context)


#==================================================================
class Search_Products_View(View):
    template_name = "products/search_products.html"
    
    def get(self, request, *args, **kwargs):
        looking_up = self.request.GET.get("q") #search/?q=
        products = Products.objects.filter(Q(title__icontains=looking_up) | Q(description__icontains=looking_up)) 

        context = {
            "products":products,
        }

        return render(request,self.template_name,context)


#==================================================================
class Show_Comparison_List_View(View):
    template_name = "products/comparison_list.html"
    
    def get(self,request,*args,**kwargs):
        comparison_list = Comparison_Of_Products(request)
        
        context = {
            "comparison_list":comparison_list,
        }
        
        return render(request,self.template_name,context)
    
    
#==================================================================
def Comparison_Table_View(request):
    template_name = "products/product_partials/comparison_table.html"
    
    comparison_product_list = Comparison_Of_Products(request)
    product_list = []
    feature_list = []
    
    for productId in comparison_product_list.comparison_list:
        product = Products.objects.get(id=productId)
        product_list.append(product)
        
    for product in product_list:
        for item in product.productFeature.all():
            if item.features not in feature_list:
                feature_list.append(item.features)
                
                
    context = {
        "product_list":product_list,
        "feature_list":feature_list,
    }
    
    return render(request,template_name,context)


#==================================================================
def Status_Of_Comparison_List_View(request):
    comparison_list = Comparison_Of_Products(request)
    return HttpResponse(comparison_list.count)


#==================================================================
def Add_To_Comparison_List_VIEW(request):
    product_Id = request.GET.get("product_Id")
    groupId = request.GET.get("groupId")
    comparison_list = Comparison_Of_Products(request)
    comparison_list.add_to_comparison_list(product_Id)
    return HttpResponse("کالا برای مقایسه اضافه شد")


#==================================================================
def Del_From_Comparison_List_VIEW(request):
    product_Id = request.GET.get("product_Id")
    comparison_list = Comparison_Of_Products(request)
    comparison_list.delete_from_comparison_list(product_Id)
    return redirect("products:comparison_table")


#==================================================================
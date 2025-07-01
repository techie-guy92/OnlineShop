from django.urls import path,re_path
from .views import *



app_name="products" 
urlpatterns = [
    path("cheapest_products/",fetch_cheapest_products_view,name="cheapest_products"),
    path("latest_products/",fetching_latest_products_view,name="latest_products"),
    path("popular_groups/",fetching_popular_groups_view,name="popular_groups"),
    re_path(r'^product_detail/(?P<slug>[\w\-]+)/$', fetching_product_detail_view.as_view(), name='product_detail'),
    # path("product_detail/<slug:slug>/",fetching_product_detail_view.as_view(),name="product_detail"),
    # path("related_products/<slug:slug>/",fetching_related_products_view,name="related_products"),
    path("all_groups/",feching_all_groups_view.as_view(),name="all_groups"),
    
    re_path(r'^products/(?P<slug>[\w\-]+)/$', feching_products_view.as_view(), name='products'),
    # path("products/<slug:slug>/",feching_products_view.as_view(),name="products"),
    path("all_groups_2/",fetching_all_groups_2_view,name="all_groups_2"),
    re_path(r'^all_brands/(?P<slug>[\w\-]+)/$', feching_all_brands_view, name='all_brands'),
    # path("all_brands/<slug:slug>/",feching_all_brands_view,name="all_brands"),
    re_path(r'^filters_for_features/(?P<slug>[\w\-]+)/$', fetching_filters_for_features_view, name='filters_for_features'),
    # path("filters_for_features/<slug:slug>/",fetching_filters_for_features_view,name="filters_for_features"),
    
    path("features_admin/",fetching_features_in_admin_view,name="features_admin"),
    
    path("search/",Search_Products_View.as_view(),name="search"),
    
    path("comparison_list/",Show_Comparison_List_View.as_view(),name="comparison_list"),
    path("comparison_table/",Comparison_Table_View,name="comparison_table"),
    path("status_of_comparison_list/",Status_Of_Comparison_List_View,name="status_of_comparison_list"),
    path("add_to_comparison_list/",Add_To_Comparison_List_VIEW,name="Add_to_comparison_list"),
    path("del_from_comparison_list/",Del_From_Comparison_List_VIEW,name="Del_from_comparison_list"),
]






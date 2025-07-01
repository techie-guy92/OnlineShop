from django.urls import path,re_path
from .views import *

app_name="Hub"
urlpatterns = [
    re_path(r'^making_comment/(?P<slug>[\w\-]+)/$',Making_CommentsView.as_view(), name='making_comment'),
    path("giving_score/",Giving_Score_View, name='giving_score'),
    path("add_to_wish_list/",Add_To_Wish_List_View, name='add_to_wish_list'),
    path("wish_list/",Wish_List_View.as_view(), name='wish_list'),
]

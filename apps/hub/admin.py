from django.contrib import admin
from .models import *



#============================================================================
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["user","comment","product","comment_parent","is_active","created_at"]
    list_editable = ["is_active"]
    
    
#============================================================================
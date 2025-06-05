from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.
admin.site.register([offerProduct,Category,SubCategory,Brand])

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','display_image','brand','category','desc']
    list_display_links=['name']
    list_editable=['desc']
    list_per_page=5
    list_filter=['price','brand']
    search_fields=['price','name']
    ordering=['name']

    def display_image(self,obj):
      if obj.image:
         return format_html('<img src="{}" height="100px" weight="100px">',obj.image.url)
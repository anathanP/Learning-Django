from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline 
from Store.admin import ProductAdmin
from Tags.models import TaggedItem
from Store.models import Product

# Register your models here.
class TaggedItemsInline(GenericTabularInline):
    autocomplete_fields = ["tag"]
    model = TaggedItem
    extra = 0
    

class CustomeProductAdmin(ProductAdmin):
    inlines = [TaggedItemsInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomeProductAdmin)

from django.contrib import admin, messages
from django.http import HttpRequest
from django.utils import html
from django.utils.http import urlencode
from django.urls import reverse
from django.db.models import Count
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"
    
    def lookups(self, request, model_admin):
        return [
            ("<10", "Low")
        ] 
        
    def queryset(self, request, queryset):
        if self.value == "<10":
            return queryset.filter(inventory__lt=10)

# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["Product"]

    prepopulated_fields = {
        "slug": ["title"]
    }
    actions = ["clear_inventory"]
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = ["Product"]
    list_filter = ["Product", "last_update", InventoryFilter]
    
    @admin.display(ordering="Product__title")    
    def collection_title(self, product):
        return product.Product.title
    
    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        
        return "OK"
    
    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        update_quety = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{update_quety} product were successfully updated.",
            messages.ERROR
        )
    

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ["first_name__istartswith", "last_name__istartswith"]
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    list_per_page = 10
    search_fields = ["first_name__istartswith", "last_name__istartswith", "orders_count"]
    
    @admin.display(ordering="orders_count")
    def orders_count(self, custmer):
        url = (
            reverse("admin:Store_order_changelist")
            + "?"
            + urlencode({
                "customer__id": str(custmer.id)
            })
        )
        return html.format_html(f"<a href={url}>{custmer.orders_count}</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count = Count("order")
        )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    list_display = ["id", "placed_at", "customer"]
    list_per_page = 10

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "products_count"]
    list_per_page = 10
    
    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (reverse('admin:Store_product_changelist')
               + "?"
               + urlencode({"Product__id": str(collection.id)}))        
        return html.format_html(f"<a href={url}>{collection.products_count}</a>")
        

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            products_count = Count("product")
        )

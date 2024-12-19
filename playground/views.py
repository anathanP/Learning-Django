from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Count, Sum
from Store.models import Collection, Customer, Product

# Create your views here.
def say_hello(request) -> HttpResponse:
    orders = Product.objects.annotate(
        total_sale=Sum(
            F('orderitem__quantity')*F("orderitem__unit_price")
        )
    ).order_by("-total_sale")[:5]

    return render(request, 'hello.html', {'name': 'Abbas', "orders": list(orders)})


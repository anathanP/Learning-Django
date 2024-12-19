from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField()
    unit_price = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="You need to enter a value more than 1")
     ]
    )
    inventory = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0, message="You need to enter a value more than 0")
        ]
    )
    last_update = models.DateTimeField(auto_now=True)
    Product = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, related_name="products", blank=True)
    
    def __str__(self):
        return self.title
    

    class Meta: 
        ordering = ["title"]


class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES = {
        MEMBERSHIP_BRONZE: "Bronze",
        MEMBERSHIP_SILVER: "Silver",
        MEMBERSHIP_GOLD: "Gold"
    }

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True)
    phone = models.CharField(max_length=13)
    membership = models.CharField(max_length=1 ,choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
    class Meta: 
        ordering = ["first_name", "last_name"]


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    

class Order(models.Model):
    PAYMENT_PENDING = "P"
    PAYMENT_COMPLETE = "C"
    PAYMENT_FAILED = "C"

    PAYMENT_STATUS_CHOICES = {
        PAYMENT_PENDING: "Pending",
        PAYMENT_COMPLETE: "Complete",
        PAYMENT_FAILED: "Failed"
    }

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
    class Meta: 
        ordering = ['placed_at']


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)


class CartItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=20, default="0000")
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)


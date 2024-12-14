from django.db import models

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(default="-")
    unit_price = models.PositiveIntegerField()
    inventory = models.PositiveSmallIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    Product = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, related_name="products")


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


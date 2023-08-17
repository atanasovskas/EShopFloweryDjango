
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('Orchids', 'Orchids'),
    ('Peony', 'Peony'),
    ('Roses', 'Roses'),
    ('Tulips', 'Tulips'),
    ('Lilies', 'Lilies'),
    ('Magnolia', 'Magnolia'),
    ('Cyclamen', 'Cyclamen'),
    ('Hyacinth', 'Hyacinth'),
    ('Bamboo', 'Bamboo'),
    ('Succulent','Succulent')
)
COLOR_CHOICES=(
    ("pink","pink"),
    ("violet","violet"),
    ("white","white"),
    ("blue","blue"),
    ("red","red"),
    ("yellow","yellow"),
    ("mix","mix")
)
OCCASSION_CHOICES=(
    ("Birthday","Birthday"),
    ("Graduation","Graduation"),
    ("Weeding","Weeding"),
    ("Motherday","Motherday"),
    ("Anniversary","Anniversary")
)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    code = models.CharField(unique=True,max_length=50,primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    description = models.TextField()
    image = models.ImageField()
    color = models.CharField(choices=COLOR_CHOICES, max_length=50)
    occasion = models.CharField(choices=OCCASSION_CHOICES, max_length=50)
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.code+" "+self.name




class Favorite(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)



class FavoriteItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name



class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
class CartItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=3)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name

    def subtotal(self):
        return self.item.price



class Address(models.Model):
    name=models.CharField(max_length=100)
    surname=models.CharField(max_length=100)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city= models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, choices=([('On Delivery', 'On Delivery'), ('Card', 'Card')]))

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Addresses'

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100,
                                    choices=(
                                        [('Created', 'Created'), ('InDelivery', 'InDelivery'),
                                         ('Finished', 'Finished')]))

    def __str__(self):
        return f"{self.user} of {self.cart.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=3)

    def subtotal(self):
        return self.item.price
    def __str__(self):
        return f" {self.item.name} x {self.item.price} ден."
class Payment(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=100,
                                 choices=(
                                     [('Visa', 'Visa'), ('MasterCard', 'MasterCard')]))
    card_number = models.CharField(max_length=255)
    exp_mm = models.IntegerField()
    exp_yy = models.IntegerField()
    security_code = models.IntegerField()
    card_holder_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)



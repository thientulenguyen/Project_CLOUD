from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=255)
    customer_phonenumber = models.CharField(max_length=20)
    customer_email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.customer_id)
    
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.category_id)

class Product(models.Model):
    product_id_size = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_size = models.CharField(max_length=20)
    product_image = models.ImageField(upload_to='product_images/')
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_id = models.IntegerField()

    def __str__(self):
        return str(self.product_id_size)
    
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id_size = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_quantity = models.IntegerField()
    #cart_transaction_id = models.CharField(max_length=200, null=True)
    cart_complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cart_id)
    
# class CartItem(models.Model):
#     cart_item_id = models.AutoField(primary_key=True)
#     product_id_size = models.ForeignKey(Product, on_delete=models.CASCADE)
#     cart_item_order = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     cart_quantity = models.IntegerField()

#     def __str__(self):
#         return str(self.cart_item_id)
    
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    #order_status = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.order_id)
    
class OrderDetails(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id_size = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_detail_quantity = models.PositiveIntegerField()
    order_detail_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.order_detail_id)
    
class Shipping(models.Model):
    Shipping_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    shipping_email = models.EmailField()
    shipping_address = models.CharField(max_length=255)
    shipping_phonenumber = models.CharField(max_length=20)
    shipping_description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.Shipping_id)
    
class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=100)
    emp_age = models.PositiveIntegerField()
    emp_address = models.CharField(max_length=255)
    emp_phonenumber = models.CharField(max_length=20)
    emp_email = models.EmailField()
    emp_position = models.CharField(max_length=100)
    Status_of_work = models.BooleanField(default=True)

    def __str__(self):
        return str(self.emp_id)

class Revenue(models.Model):
    revenue_id = models.AutoField(primary_key=True)
    revenue_month = models.DateField()
    revenue_Total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.revenue_id)
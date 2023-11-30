from django.contrib import admin
from .models import *

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'customer_id', 'product_id_size', 'cart_quantity', 'cart_complete')
    search_fields = ['cart_id']
    list_filter = ('cart_id', 'customer_id', 'product_id_size', 'cart_quantity', 'cart_complete')
admin.site.register(Cart, CartAdmin)

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('Shipping_id', 'order_id', 'first_name', 'last_name', 'shipping_email', 'shipping_address', 'shipping_phonenumber', 'shipping_description')
    search_fields = ['emp_name']
    list_filter = ('Shipping_id', 'order_id', 'first_name', 'last_name', 'shipping_email', 'shipping_address', 'shipping_phonenumber', 'shipping_description')
admin.site.register(Shipping, ShippingAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'emp_name', 'emp_age', 'emp_address', 'emp_phonenumber', 'emp_email', 'emp_position', 'Status_of_work')
    search_fields = ['emp_name']
    list_filter = ('emp_id', 'emp_name', 'emp_age', 'emp_address', 'emp_phonenumber', 'emp_email', 'emp_position', 'Status_of_work')
admin.site.register(Employee, EmployeeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id_size', 'product_name', 'product_description', 'product_size', 'product_image', 'product_price', 'category_id', 'product_id')
    search_fields = ['product_name']
    list_filter = ('product_id_size', 'product_name', 'product_description', 'product_size', 'product_image', 'product_price', 'category_id', 'product_id')
admin.site.register(Product, ProductAdmin)    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name')
    search_fields = ['category_id']
    list_filter = ('category_id', 'category_name')
admin.site.register(Category, CategoryAdmin)    

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'customer_name', 'customer_address', 'customer_phonenumber', 'customer_email')
    search_fields = ['customer_name']
    list_filter = ('customer_id', 'customer_name', 'customer_address', 'customer_phonenumber', 'customer_email')
admin.site.register(Customer, CustomerAdmin)

# class CustomerAccountAdmin(admin.ModelAdmin):
#     list_display = ('customer_acc_id', 'customer_username', 'customer_password', 'customer_id')
#     search_fields = ['customer_username']
#     list_filter = ('customer_acc_id', 'customer_username', 'customer_password', 'customer_id')
# admin.site.register(CustomerAccount, CustomerAccountAdmin)
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_id', 'order_date', 'order_total')
    search_fields = ['order_id']
    list_filter =('order_id', 'customer_id', 'order_date', 'order_total')
admin.site.register(Orders, OrderAdmin)

class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order_detail_id', 'order_id', 'product_id_size', 'order_detail_quantity', 'order_detail_total')
    search_fields = ['order_detail_id']
    list_filter = ('order_detail_id', 'order_id', 'product_id_size', 'order_detail_quantity', 'order_detail_total')
admin.site.register(OrderDetails, OrderDetailsAdmin)

# class EmployeeAccountAdmin(admin.ModelAdmin):
#     list_display = ('emp_acc_id', 'emp_id', 'emp_username', 'emp_password')
#     search_fields = ['emp_acc_id']
#     list_filter = ('emp_acc_id', 'emp_id', 'emp_username', 'emp_password')
# admin.site.register(EmployeeAccount, EmployeeAccountAdmin)

class RevenueAdmin(admin.ModelAdmin):
    list_display = ('revenue_id', 'revenue_month', 'revenue_Total')
    search_fields = ['revenue_id']
    list_filter = ('revenue_id', 'revenue_month', 'revenue_Total')
admin.site.register(Revenue, RevenueAdmin)
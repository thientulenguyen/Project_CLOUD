from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime
from django.db.models import Sum, F

products = Product.objects.none()
cart = Cart.objects.none()
categories = Category.objects.none()

def index(request):
    context = {}
    categories = Category.objects.all()
    for i in range(1, 10):  # Từ cate_id 1 đến 9
        pro_cate = Product.objects.filter(category_id=i).values('product_id', 'product_name', 'product_image', 'product_price').distinct()[:4]
        context[f'pro_cate_{i}'] = pro_cate
    context[f'categories'] = categories
    return render(request, 'app/index.html', context)

def shop(request, pk=None):
    context = {}
    products = Product.objects.values('product_id', 'product_name', 'product_image', 'product_price').distinct()
    categories = Category.objects.all()

    items_per_page = 20
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page', 1)

    try:
        current_page = paginator.page(page_number)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context['current_page'] = current_page
    context['categories'] = categories

    return render(request, 'app/shop.html', context)

def category(request, pk=None):
    context = {}
    categories = Category.objects.all()
    context['categories'] = categories

    if pk is not None:
        products = Product.objects.filter(category_id=pk).values('product_id', 'product_name', 'product_image', 'product_price').distinct()
        context['products'] = products

    return render(request, 'app/category.html', context)

def product(request, pk):
    context = {}
    categories = Category.objects.all()
    context[f'categories'] = categories

    product = Product.objects.filter(product_id=pk).first()
    context['product'] = product

    return render(request, 'app/product.html', context)

def blog(request):
    context = {}
    categories = Category.objects.all()
    context[f'categories'] = categories
    return render(request, 'app/blog.html', context)

def about(request):
    context = {}
    categories = Category.objects.all()
    context[f'categories'] = categories
    return render(request, 'app/about.html', context)

def contact(request):
    context = {}
    categories = Category.objects.all()
    context[f'categories'] = categories
    return render(request, 'app/contact.html', context)

def user(request):
    context = {}
    categories = Category.objects.all()
    context[f'categories'] = categories

    if request.user.is_authenticated:
        user = request.user
        customer_info = Customer.objects.get(user_id=user.id)
        #context[f'customer_info'] = customer_info

        customer = request.user.customer
        try:
            cart = Cart.objects.filter(customer_id=customer, cart_complete=True)
            #cart_items = cart.cart_set.all()

            # Lấy thông tin sản phẩm cho mỗi CartItem
            products_info = []
            cart_total = 0  # Tổng số tiền của tất cả sản phẩm
            quantity_total = 0  # Tổng số lượng của tất cả các mục
            for cart_item in cart:
                # Lấy thông tin sản phẩm từ Product
                product = Product.objects.get(product_id_size=cart_item.product_id_size_id)
                
                product_info = {
                    'cart_id' : cart_item.cart_id,
                    'product_name': product.product_name,
                    'product_size': product.product_size,
                    'product_image': product.product_image,  # Đường dẫn hình ảnh
                    'product_price': product.product_price,
                    'cart_quantity': cart_item.cart_quantity,
                    'price_total': product.product_price * cart_item.cart_quantity,  # Tính tổng tiền của từng sản phẩm
                }
                products_info.append(product_info)

                # Cập nhật tổng số tiền của tất cả sản phẩm
                cart_total += product_info['price_total']
                # Cập nhật tổng số lượng của tất cả các mục
                quantity_total += cart_item.cart_quantity

        except Cart.DoesNotExist:
            products_info = []
            cart_total = 0
            quantity_total = 0

        context = {
        'customer_info' : customer_info,
        'products_info': products_info,
        'cart_total': cart_total,
        'quantity_total': quantity_total,
        }
        
    else:
        products_info = []
        cart_total = 0
        quantity_total = 0

    

    return render(request, 'app/user.html', context)

def checkout(request):
    context = {}
    categories = Category.objects.all()
    context[f'categories'] = categories

    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            cart = Cart.objects.filter(customer_id=customer, cart_complete=False)
            #cart_items = cart.cart_set.all()

            # Lấy thông tin sản phẩm cho mỗi CartItem
            products_info = []
            cart_total = 0  # Tổng số tiền của tất cả sản phẩm
            quantity_total = 0  # Tổng số lượng của tất cả các mục
            for cart_item in cart:
                # Lấy thông tin sản phẩm từ Product
                product = Product.objects.get(product_id_size=cart_item.product_id_size_id)
                
                product_info = {
                    'cart_id' : cart_item.cart_id,
                    'product_name': product.product_name,
                    'product_size': product.product_size,
                    'product_image': product.product_image,  # Đường dẫn hình ảnh
                    'product_price': product.product_price,
                    'cart_quantity': cart_item.cart_quantity,
                    'price_total': product.product_price * cart_item.cart_quantity,  # Tính tổng tiền của từng sản phẩm
                }
                products_info.append(product_info)

                # Cập nhật tổng số tiền của tất cả sản phẩm
                cart_total += product_info['price_total']
                # Cập nhật tổng số lượng của tất cả các mục
                quantity_total += cart_item.cart_quantity

        except Cart.DoesNotExist:
            products_info = []
            cart_total = 0
            quantity_total = 0
    else:
        products_info = []
        cart_total = 0
        quantity_total = 0

    context = {
        'products_info': products_info,
        'cart_total': cart_total,
        'quantity_total': quantity_total,
    }

    if request.method == "POST":
        # Lấy thông tin từ form
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phonenumber = request.POST.get('phonenumber')
        description = request.POST.get('description')

        # Kiểm tra xem các trường bắt buộc đã được điền đầy đủ hay không
        if not first_name or not last_name or not email or not phonenumber or not address:
            error_message = 'Please fill in all required fields.'
            messages.error(request, error_message)
        else:
            # Tạo mới Order
            order = Orders.objects.create(
                customer_id=request.user.customer,
                order_date=datetime.date.today(),
                order_total=0,
            )

            # Lấy các sản phẩm trong giỏ hàng chưa thanh toán
            cart_items = Cart.objects.filter(customer_id=request.user.customer, cart_complete=False)

            # Tạo mới OrderDetails cho mỗi sản phẩm trong giỏ hàng
            for cart_item in cart_items:
                OrderDetails.objects.create(
                    order_id=order,
                    product_id_size=cart_item.product_id_size,
                    order_detail_quantity=cart_item.cart_quantity,
                    order_detail_total=cart_item.cart_quantity * cart_item.product_id_size.product_price,
                )

            # Tạo mới Shipping
            shipping = Shipping.objects.create(
                order_id=order,
                first_name=first_name,
                last_name=last_name,
                shipping_email=email,
                shipping_address=address,
                shipping_phonenumber=phonenumber,
                shipping_description=description,
            )

            # Tính tổng của order_detail_total trong bảng OrderDetails
            order_total = OrderDetails.objects.filter(order_id=order).aggregate(Sum('order_detail_total'))['order_detail_total__sum']

            # Cập nhật lại order_total trong bảng Orders
            order.order_total = order_total
            order.save()

            # Cập nhật cart_complete của Cart thành True
            cart_items.update(cart_complete=True)

            # Lấy tháng của ngày hiện tại
            current_month = datetime.date.today().month

            # Kiểm tra và thực hiện tính toán nếu orderdate và revenue month giống nhau
            revenue_month_match = Revenue.objects.get(revenue_month__month=current_month)
            
            if revenue_month_match:
                # Cập nhật revenue total của revenue cộng thêm order total của order
                revenue_month_match.revenue_Total = F('revenue_Total') + order_total
                revenue_month_match.save()

            messages.success(request, 'Your order has been placed successfully!')

    return render(request, 'app/checkout.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            cart = Cart.objects.filter(customer_id=customer, cart_complete=False)
            #cart_items = cart.cart_set.all()

            # Lấy thông tin sản phẩm cho mỗi CartItem
            products_info = []
            cart_total = 0  # Tổng số tiền của tất cả sản phẩm
            quantity_total = 0  # Tổng số lượng của tất cả các mục
            for cart_item in cart:
                # Lấy thông tin sản phẩm từ Product
                product = Product.objects.get(product_id_size=cart_item.product_id_size_id)
                
                product_info = {
                    'cart_id' : cart_item.cart_id,
                    'product_name': product.product_name,
                    'product_size': product.product_size,
                    'product_image': product.product_image,  # Đường dẫn hình ảnh
                    'product_price': product.product_price,
                    'cart_quantity': cart_item.cart_quantity,
                    'price_total': product.product_price * cart_item.cart_quantity,  # Tính tổng tiền của từng sản phẩm
                }
                products_info.append(product_info)

                # Cập nhật tổng số tiền của tất cả sản phẩm
                cart_total += product_info['price_total']
                # Cập nhật tổng số lượng của tất cả các mục
                quantity_total += cart_item.cart_quantity

        except Cart.DoesNotExist:
            products_info = []
            cart_total = 0
            quantity_total = 0
    else:
        products_info = []
        cart_total = 0
        quantity_total = 0

    context = {
        'products_info': products_info,
        'cart_total': cart_total,
        'quantity_total': quantity_total,
    }
    return render(request, 'app/cart.html', context)

def cart_add(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart = Cart.objects.filter(customer_id=customer, cart_complete=False)

        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            size = request.POST.get('size')
            quantity = request.POST.get('quantity')
            user = request.user

            customer_id = Customer.objects.get(user_id=user.id)
            product = Product.objects.get(product_id=product_id, product_size=size)
            
            for cart_item in cart:
                # Lấy id từ product_id_size của cart_item (kiểu Product)
                cart_product_id_size = cart_item.product_id_size_id
                if cart_product_id_size == product.product_id_size:
                    # Nếu trùng, cập nhật cart_quantity
                    cart_item.cart_quantity += int(quantity)
                    cart_item.save()
                    return redirect('cart')

            cart_item, created = Cart.objects.get_or_create(
                    cart_quantity=quantity,
                    cart_complete=0,
                    customer_id=customer_id,
                    product_id_size=product
                )

    return redirect('cart')

def cart_delete(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        # Lấy đối tượng CartItem cần xóa
        cart_item = get_object_or_404(Cart, pk=cart_id)
        # Thực hiện xóa cart item
        cart_item.delete()
    return redirect('cart')

def registerPage(request):
    context = {}
    categories = Category.objects.all()
    context[f'categories'] = categories

    form = CreateUser()

    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()

            # Tạo đối tượng Customer tương ứng
            customer_name = f"{user.first_name} {user.last_name}"
            customer_address = "_"
            customer_phonenumber = "_"
            customer_email = user.email

            # Tạo Customer mới
            customer = Customer.objects.create(
                customer_name=customer_name,
                customer_address=customer_address,
                customer_phonenumber=customer_phonenumber,
                customer_email=customer_email,
                user=user
            )

            return redirect('login')

    context[f'form'] = form
    return render(request, 'app/register.html', context)

def loginPage(request):
    context = {}
    categories = Category.objects.all()
    context[f'categories'] = categories
    
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'username or password is incorrect !')

    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('index')
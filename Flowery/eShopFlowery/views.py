from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def index(request):
      return render(request,'index.html')
def all_products(request):
    qs=Product.objects.all()
    context = {"products": qs}
    return render(request, 'products.html', context=context)

def products(request):

    occasion = request.GET.get('occasion', 'all')
    if occasion == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(occasion=occasion)

    context = {
        'products': products,
        'occasion': occasion,
    }

    return render(request,'products.html',context=context)


def description(request,code):
    products = Product.objects.filter(code=code)
    context = {'products': products}
    return render(request, 'description.html', context)


def  customer_login(request):
    if request.user.is_superuser:
        customer_logout(request)
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user :
                login(request, user)
                Cart.objects.get_or_create(user=user.userprofile)
                return redirect('products')  # Redirect to the products page
    else:
        form = CustomerLoginForm()
    return render(request, 'customer_login.html', {'form': form})

def customer_registration(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        print("Form data:", form.data)
        if form.is_valid():
            print("Form is valid")
            user = form.save(commit=False)
            user.save()

            UserProfile.objects.create(user=user)

            login(request, user)
            Cart.objects.create(user=user.userprofile)
            Favorite.objects.create(user=user.userprofile)

            return redirect('customer_login')

    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer_registration.html', {'form': form})
def customer_logout(request):
    #if request.method == 'POST':
    logout(request)
    return redirect('customer_login')

@login_required(login_url='customer_login')
def favorite(request):
    user_profile = request.user.userprofile
    if request.user.is_authenticated:
        try:
            favorite = Favorite.objects.get(user=user_profile)
            favitems = FavoriteItem.objects.filter(favorite=favorite)
            items = [favitem.item for favitem in favitems]
            context = {'products': items}
            return render(request, 'favorite.html', context)
        except Favorite.DoesNotExist:
            pass

    return render(request,'favorite.html')



def order(request):
    user = request.user.userprofile
    if request.user.is_authenticated:

            cart = Cart.objects.get(user=request.user.userprofile)
            cartitems = CartItem.objects.filter(cart=cart)
            address=Address.objects.get(user=request.user.userprofile)
            total = sum(cartitem.subtotal() for cartitem in cartitems)

            if request.method == 'POST':
                order = Order.objects.create(
                    user=request.user.userprofile,
                    cart=cart,
                    address=address,
                    order_status='Created'
                    )
                for cartitem in cartitems:
                    OrderItem.objects.create(
                        order=order,
                        item=cartitem.item,
                        quantity=cartitem.quantity,
                    )
                    product = cartitem.item
                    product.quantity -= cartitem.quantity
                    product.save()

                cartitems.delete()


                return redirect("finish")
            context = {'cartitems': cartitems, 'total': total}
            return render(request, 'order.html', context)
    return redirect("login")



def address(request):
    user_profile = request.user.userprofile
    try:
        existing_address = Address.objects.get(user=user_profile)
        form_data = AddressForm(instance=existing_address)
    except Address.DoesNotExist:
        existing_address = None
        form_data = AddressForm()

    if request.method == "POST":
        form_data = AddressForm(data=request.POST, files=request.FILES, instance=existing_address)
        if form_data.is_valid():
            address = form_data.save(commit=False)
            address.user = user_profile
            address.save()
            if address.payment_method == "Card":
                return redirect("payment")
            else:
                return redirect("order")

    return render(request, 'address.html', {'form': form_data})

@login_required(login_url='customer_login')
def add_to_favorite(request,code):
    if request.method == "POST":
        product = get_object_or_404(Product, code=code)

        favorite=Favorite.objects.get(user=request.user.userprofile)
        fav_item=FavoriteItem.objects.filter(favorite=favorite)

        if not fav_item.filter(item=product).exists():
            favorite_item = FavoriteItem.objects.create(item=product, favorite=favorite)
            return JsonResponse({"message": "Item added to favorites"}, status=200)
        else:
            return JsonResponse({"message": "Item is already in favorites"}, status=400)


def add_to_cart(request,code):
    if request.method == "POST":
        product = get_object_or_404(Product, code=code)
        quantity = int(request.POST.get('quantity'))
        updated_price = int(request.POST.get('updated_price'))
        print(updated_price)
        cart=Cart.objects.get(user=request.user.userprofile)
        c_item = CartItem.objects.filter(cart=cart)


        if not c_item.filter(item=product,quantity=quantity).exists():

            cart_item = CartItem.objects.create(item=product, cart=cart,quantity=quantity)
            item=CartItem.objects.get(item=product,cart=cart,quantity=quantity)
            item.item.price=updated_price
            cart_item.item.price=updated_price
            print(cart_item.item.price)
            cart_item.save()
            item.save()
            return JsonResponse({"message": "Item added to cart"}, status=200)
        else:
            return JsonResponse({"message": "Item is already in cart"},status=400)



@login_required(login_url='customer_login')
def view_cart(request):
    user = request.user.userprofile
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user)
            try:
                cartitems = CartItem.objects.filter(cart=cart)
                product_quantity = [(cartitem.item, cartitem.quantity) for cartitem in cartitems]
                total = sum(cartitem.subtotal() for cartitem in cartitems)
                context = {'product_quantity': product_quantity,'total':total,'cartitems':cartitems
                           }
                return render(request, 'view_cart.html', context)
            except CartItem.DoesNotExist:
                # Handle the case where CartItem does not exist
                context = {'message': 'Your cart is empty.'}
                return render(request, 'view_cart.html', context)
        except Cart.DoesNotExist:
            pass
    return render(request, 'view_cart.html')

def remove_favorite(request):
    if request.method == 'POST':
        product_code= request.POST.get('product_code')
        try:
            order_item = FavoriteItem.objects.get(item__code=product_code, favorite__user=request.user.userprofile)
            order_item.delete()
            return JsonResponse({'success': True})
        except Favorite.DoesNotExist:
            pass
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
def remove_item(request):
    if request.method == 'POST':
        product_code= request.POST.get('product_code')
        quantity=request.POST.get('quantity')

        try:
            # Assuming you have a CartItem model and you need to delete an item from the cart
            cart_item = CartItem.objects.get(item__code=product_code, cart__user=request.user.userprofile,quantity=quantity)
            cart_item.delete()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            pass
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def payment(request):
    user_profile = request.user.userprofile
    try:
        existing_card = Payment.objects.get(user=user_profile)
        form_data = PaymentForm(instance=existing_card)
    except Payment.DoesNotExist:
        existing_card = None
        form_data = PaymentForm()
    user_cart = Cart.objects.get(user=user_profile)

    if request.method == "POST":
        form_data = PaymentForm(data=request.POST, files=request.FILES, instance=existing_card)
        if form_data.is_valid():
            card = form_data.save(commit=False)
            card.user = user_profile
            card.cart = user_cart
            card.save()
            return redirect("order")

    return render(request, 'payment.html', {'form': form_data})


def finish(request):
    return  render(request,'finish.html')

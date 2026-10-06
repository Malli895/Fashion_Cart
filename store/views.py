from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q

from .models import (
    User,
    Category,
    Product,
    Cart,
    CartItem,
    Address,
    Order,
    OrderItem,
    Payment,
    Wishlist,
)


# =========================================================
# HOME / DASHBOARD
# =========================================================

def dashboard(request):

    products = Product.objects.all()

    categories = Category.objects.all()

    user_id = request.session.get("user_id")

    user = None

    if user_id:
        user = User.objects.filter(
            user_id=user_id
        ).first()

    return render(
        request,
        "dashboard.html",
        {
            "products": products,
            "categories": categories,
            "user": user,
        }
    )


def home(request):
    return dashboard(request)


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        if User.objects.filter(email=email).exists():

            return HttpResponse(
                "Email already registered."
            )

        User.objects.create(
            full_name=full_name,
            email=email,
            password=make_password(password),
            phone=phone,
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(
            email=email
        ).first()

        if user and check_password(password, user.password):

            request.session["user_id"] = user.user_id

            return redirect("home")

        else:

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid email or password."
                }
            )

    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    request.session.flush()

    return redirect("home")


# =========================================================
# PRODUCTS
# =========================================================

def products(request):

    products = Product.objects.all()

    search = request.GET.get(
        "search",
        ""
    ).strip()

    gender = request.GET.get(
        "gender",
        ""
    ).strip()

    if search:

        if search.lower() == "men":

            products = products.filter(
                category__gender__iexact="Men"
            )

        elif search.lower() == "women":

            products = products.filter(
                category__gender__iexact="Women"
            )

        elif search.lower() == "kids":

            products = products.filter(
                category__gender__iexact="Kids"
            )

        else:

            products = products.filter(
                Q(
                    product_name__icontains=search
                )
                |
                Q(
                    category__category_name__icontains=search
                )
                |
                Q(
                    description__icontains=search
                )
                |
                Q(
                    color__icontains=search
                )
            )

    if gender:

        products = products.filter(
            category__gender__iexact=gender
        )

    return render(
        request,
        "products.html",
        {
            "products": products,
            "search": search,
            "gender": gender,
        }
    )


# =========================================================
# PRODUCT DETAILS
# =========================================================

def product_details(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        product_id=product_id
    )

    return render(
        request,
        "product-details.html",
        {
            "product": product
        }
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(
    request,
    product_id
):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")

    product = get_object_or_404(
        Product,
        product_id=product_id
    )

    cart_obj, created = Cart.objects.get_or_create(
        user_id=user_id
    )

    cart_item = CartItem.objects.filter(
        cart_id=cart_obj.cart_id,
        product_id=product.product_id
    ).first()

    if cart_item:

        cart_item.quantity += 1

        cart_item.save()

    else:

        CartItem.objects.create(
            cart_id=cart_obj.cart_id,
            product_id=product.product_id,
            quantity=1
        )

    return redirect("cart")


# =========================================================
# CART
# =========================================================

def cart(request):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")

    cart_obj = Cart.objects.filter(
        user_id=user_id
    ).first()

    cart_items = []

    total_amount = 0

    if cart_obj:

        cart_items = CartItem.objects.filter(
            cart_id=cart_obj.cart_id
        ).select_related("product")

        for item in cart_items:

            total_amount += (
                item.product.price
                * item.quantity
            )

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total_amount": total_amount,
        }
    )


# =========================================================
# INCREASE QUANTITY
# =========================================================

def increase_quantity(
    request,
    cart_item_id
):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")

    cart_item = get_object_or_404(
        CartItem,
        cart_item_id=cart_item_id,
        cart__user_id=user_id
    )

    if (
        cart_item.quantity
        < cart_item.product.stock_quantity
    ):

        cart_item.quantity += 1

        cart_item.save()

    return redirect("cart")


# =========================================================
# DECREASE QUANTITY
# =========================================================

def decrease_quantity(
    request,
    cart_item_id
):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")

    cart_item = get_object_or_404(
        CartItem,
        cart_item_id=cart_item_id,
        cart__user_id=user_id
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()

    return redirect("cart")


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(
    request,
    cart_item_id
):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")

    cart_item = get_object_or_404(
        CartItem,
        cart_item_id=cart_item_id,
        cart__user_id=user_id
    )

    cart_item.delete()

    return redirect("cart")


# =========================================================
# DELIVERY ADDRESS
# =========================================================

def address(request):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")

    saved_addresses = Address.objects.filter(
        user_id=user_id
    ).order_by("-address_id")

    if request.method == "POST":

        # ---------------------------------------------
        # EXISTING ADDRESS
        # ---------------------------------------------

        selected_address_id = request.POST.get(
            "selected_address"
        )

        if selected_address_id:

            selected_address = get_object_or_404(
                Address,
                address_id=selected_address_id,
                user_id=user_id
            )

            request.session[
                "selected_address_id"
            ] = selected_address.address_id

            return redirect("payment")


        # ---------------------------------------------
        # NEW ADDRESS
        # ---------------------------------------------

        full_name = request.POST.get(
            "full_name"
        )

        phone = request.POST.get(
            "phone"
        )

        address_text = request.POST.get(
            "address"
        )

        city = request.POST.get(
            "city"
        )

        state = request.POST.get(
            "state"
        )

        pincode = request.POST.get(
            "pincode"
        )

        new_address = Address.objects.create(

            user_id=user_id,

            full_name=full_name,

            phone=phone,

            address=address_text,

            city=city,

            state=state,

            pincode=pincode,

        )

        request.session[
            "selected_address_id"
        ] = new_address.address_id

        return redirect("payment")

    return render(
        request,
        "address.html",
        {
            "saved_addresses":
                saved_addresses
        }
    )


# =========================================================
# PAYMENT
# =========================================================

def payment(
    request,
    order_id=None
):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")


    # =====================================================
    # EXISTING ORDER PAYMENT
    # =====================================================

    if order_id:

        order = get_object_or_404(
            Order,
            order_id=order_id,
            user_id=user_id
        )

        address_obj = order.address

        if request.method == "POST":

            payment_method = request.POST.get(
                "payment_method"
            )

            if not payment_method:

                return HttpResponse(
                    "Please select a payment method."
                )


            # Check existing payment

            payment_obj = Payment.objects.filter(
                order_id=order.order_id
            ).first()


            if payment_obj:

                payment_obj.payment_method = (
                    payment_method
                )

                payment_obj.payment_status = (
                    "Success"
                )

                payment_obj.save()

            else:

                Payment.objects.create(

                    order_id=order.order_id,

                    payment_method=payment_method,

                    payment_status="Success"

                )


            # Update order

            order.order_status = "Confirmed"

            order.save()


            return redirect(
                "order_details",
                order_id=order.order_id
            )


        return render(
            request,
            "payment.html",
            {
                "order": order,
                "address_obj": address_obj,
            }
        )


    # =====================================================
    # NEW ORDER PAYMENT
    # =====================================================

    selected_address_id = request.session.get(
        "selected_address_id"
    )

    if not selected_address_id:

        return redirect("address")


    address_obj = Address.objects.filter(
        address_id=selected_address_id,
        user_id=user_id
    ).first()

    if not address_obj:

        return redirect("address")


    # Get cart

    cart_obj = Cart.objects.filter(
        user_id=user_id
    ).first()

    if not cart_obj:

        return redirect("cart")


    cart_items = CartItem.objects.filter(
        cart_id=cart_obj.cart_id
    ).select_related("product")


    if not cart_items.exists():

        return redirect("cart")


    # Calculate total

    total_amount = 0

    for item in cart_items:

        total_amount += (
            item.product.price
            * item.quantity
        )


    # ---------------------------------------------
    # PAYMENT SUBMISSION
    # ---------------------------------------------

    if request.method == "POST":

        payment_method = request.POST.get(
            "payment_method"
        )

        if not payment_method:

            return HttpResponse(
                "Please select a payment method."
            )


        # -----------------------------------------
        # CREATE ORDER
        # -----------------------------------------

        order = Order.objects.create(

            user_id=user_id,

            address_id=address_obj.address_id,

            total_amount=total_amount,

            order_status="Confirmed"

        )


        # -----------------------------------------
        # CREATE ORDER ITEMS
        # -----------------------------------------

        for item in cart_items:

            OrderItem.objects.create(

                order_id=order.order_id,

                product_id=item.product.product_id,

                quantity=item.quantity,

                price=item.product.price

            )


        # -----------------------------------------
        # CREATE PAYMENT
        # -----------------------------------------

        Payment.objects.create(

            order_id=order.order_id,

            payment_method=payment_method,

            payment_status="Success"

        )


        # -----------------------------------------
        # EMPTY CART
        # -----------------------------------------

        cart_items.delete()


        # -----------------------------------------
        # REMOVE SELECTED ADDRESS FROM SESSION
        # -----------------------------------------

        request.session.pop(
            "selected_address_id",
            None
        )


        # -----------------------------------------
        # OPEN ORDER DETAILS
        # -----------------------------------------

        return redirect(
            "order_details",
            order_id=order.order_id
        )


    # GET REQUEST

    return render(
        request,
        "payment.html",
        {
            "address_obj": address_obj,

            "total_amount":
                total_amount,

            "order": None,
        }
    )


# =========================================================
# CREATE ORDER
# =========================================================

def create_order(request):

    # This URL is kept for compatibility.
    # New orders now go through Payment first.

    return redirect("address")


# =========================================================
# ORDER DETAILS
# =========================================================

def order_details(
    request,
    order_id
):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")


    order = get_object_or_404(

        Order,

        order_id=order_id,

        user_id=user_id

    )


    order_items = OrderItem.objects.filter(

        order_id=order.order_id

    ).select_related("product")


    for item in order_items:

        item.item_total = (
            item.price
            * item.quantity
        )


    payment_obj = Payment.objects.filter(

        order_id=order.order_id

    ).first()


    return render(

        request,

        "order-details.html",

        {

            "order": order,

            "order_items":
                order_items,

            "payment_obj":
                payment_obj,

        }

    )


# =========================================================
# MY ORDERS
# =========================================================

def orders(request):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")


    user_orders = Order.objects.filter(

        user_id=user_id

    ).prefetch_related(

        "orderitem_set__product"

    ).order_by("-order_id")


    for order in user_orders:

        for item in order.orderitem_set.all():

            item.item_total = (
                item.price
                * item.quantity
            )


        order.payment_obj = Payment.objects.filter(
            order_id=order.order_id
        ).first()


    return render(

        request,

        "orders.html",

        {
            "orders":
                user_orders
        }

    )


# =========================================================
# PROFILE
# =========================================================

def profile(request):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")


    user = get_object_or_404(

        User,

        user_id=user_id

    )


    return render(

        request,

        "profile.html",

        {
            "user": user
        }

    )


# =========================================================
# WISHLIST
# =========================================================

def add_to_wishlist(
    request,
    product_id
):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")


    product = get_object_or_404(

        Product,

        product_id=product_id

    )


    Wishlist.objects.get_or_create(

        user_id=user_id,

        product_id=product.product_id

    )


    return redirect("wishlist")


def wishlist(request):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")


    wishlist_items = Wishlist.objects.filter(

        user_id=user_id

    ).select_related("product")


    return render(

        request,

        "wishlist.html",

        {
            "wishlist_items":
                wishlist_items
        }

    )


def remove_from_wishlist(
    request,
    wishlist_id
):

    user_id = request.session.get(
        "user_id"
    )

    if not user_id:

        return redirect("login")


    wishlist_item = get_object_or_404(

        Wishlist,

        wishlist_id=wishlist_id,

        user_id=user_id

    )


    wishlist_item.delete()


    return redirect("wishlist")
from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # HOME / DASHBOARD
    # =====================================================

    path(
        "",
        views.dashboard,
        name="home"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),


    # =====================================================
    # LOGIN / REGISTER
    # =====================================================

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    # =====================================================
    # PRODUCTS
    # =====================================================

    path(
        "products/",
        views.products,
        name="products"
    ),

    path(
        "product/<int:product_id>/",
        views.product_details,
        name="product_details"
    ),


    # =====================================================
    # CART
    # =====================================================

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/increase/<int:cart_item_id>/",
        views.increase_quantity,
        name="increase_quantity"
    ),

    path(
        "cart/decrease/<int:cart_item_id>/",
        views.decrease_quantity,
        name="decrease_quantity"
    ),

    path(
        "cart/remove/<int:cart_item_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),


    # =====================================================
    # ADDRESS
    # =====================================================

    path(
        "address/",
        views.address,
        name="address"
    ),


    # =====================================================
    # ORDER
    # =====================================================

    path(
        "order/create/",
        views.create_order,
        name="create_order"
    ),

    path(
        "order/<int:order_id>/",
        views.order_details,
        name="order_details"
    ),

    path(
        "orders/",
        views.orders,
        name="orders"
    ),


    # =====================================================
    # PAYMENT
    # =====================================================

    path("payment/", views.payment, name="payment"),

    path(
        "payment/<int:order_id>/",
        views.payment,
        name="order_payment"
    ),


    # =====================================================
    # PROFILE / ACCOUNT
    # =====================================================

    path(
        "profile/",
        views.profile,
        name="profile"
    ),


    # =====================================================
    # WISHLIST
    # =====================================================

    path(
        "wishlist/",
        views.wishlist,
        name="wishlist"
    ),

    path(
        "wishlist/add/<int:product_id>/",
        views.add_to_wishlist,
        name="add_to_wishlist"
    ),

    path(
        "wishlist/remove/<int:wishlist_id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist"
    ),

]
from django.db import models
image = models.CharField(max_length=255, null=True, blank=True)


# =========================
# CATEGORY
# =========================

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.category_name


# =========================
# PRODUCT
# =========================

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_column="category_id"
    )

    product_name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    image = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.product_name


# =========================
# USER
# =========================

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email


# =========================
# CART
# =========================

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart"

    def __str__(self):
        return f"Cart {self.cart_id}"


# =========================
# CART ITEMS
# =========================

class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        db_column="cart_id"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="product_id"
    )

    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = "cart_items"

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"


# =========================
# ADDRESS
# =========================

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id"
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    class Meta:
        db_table = "addresses"

    def __str__(self):
        return f"{self.city} - {self.pincode}"


# =========================
# ORDER
# =========================

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id"
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        db_column="address_id"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    order_status = models.CharField(
        max_length=30,
        default="Pending"
    )

    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"Order {self.order_id}"


# =========================
# ORDER ITEMS
# =========================

class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column="order_id"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="product_id"
    )

    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        db_table = "order_items"

    def __str__(self):
        return f"Order {self.order.order_id} - {self.product.product_name}"


# =========================
# PAYMENT
# =========================

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column="order_id"
    )

    payment_method = models.CharField(max_length=30)

    payment_status = models.CharField(
        max_length=30,
        default="Pending"
    )

    transaction_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"Payment {self.payment_id}"

class Wishlist(models.Model):

    wishlist_id = models.AutoField(
        primary_key=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="product_id"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "wishlist"

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.product.product_name}"
        )
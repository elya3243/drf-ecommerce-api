from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'id']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CartItemSerializer(serializers.ModelSerializer):
    product= serializers.StringRelatedField()
    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['items', 'total_price']
    def get_total_price(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.product.price * item.quantity
        return total

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['items', 'id', 'created_at']

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
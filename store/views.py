from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Category, CartItem, Cart, Product, Order, OrderItem
from .serializers import ( ProductSerializer, CategorySerializer, AddToCartSerializer, CartSerializer,
                          UpdateCartItemSerializer, OrderSerializer, OrderDetailSerializer, ProductCreateSerializer)
from rest_framework import generics, status
from .permissions import IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



class ProductListCreateView(generics.ListCreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend,]
    search_fields = ['title']
    ordering_fields = ['title', 'price']
    filterset_fields = ['category',]

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class AddToCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=['quantity'])
        return Response({'message': 'Product added to cart'})


class CartDetailView(APIView):
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)

class CartItemView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk, cart__user=request.user)
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data['quantity']
        cart_item.quantity = quantity
        cart_item.save()
        return Response({'message': 'cart item updated'}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk, cart__user=request.user)
        cart_item.delete()
        return Response({'message': 'cart item deleted'}, status=status.HTTP_200_OK)

class CartOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        order = Order.objects.create(user=request.user)
        cart_items = cart.items.all()
        for item in cart_items:
            OrderItem.objects.create(order=order,
                                     product=item.product,
                                     quantity=item.quantity,
                                     price=item.product.price)
        cart_items.delete()
        return Response({'message': 'order created'},status=status.HTTP_201_CREATED)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
       return Order.objects.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
       return Order.objects.filter(user=self.request.user)
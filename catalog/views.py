from rest_framework import viewsets

from .models import Category, Product
from .paginators import StandardResultsSetPagination
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
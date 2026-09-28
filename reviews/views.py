"""Views для приложения reviews."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from catalog.paginators import StandardResultsSetPagination
from .models import Review
from .permissions import IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review.

    Поддерживает:
    - CRUD отзывов
    - поиск по тексту (?search=...)
    - фильтрацию по товару (?product=...), рейтингу (?rating=...)
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['product', 'rating', 'is_approved']
    search_fields = ['text']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """При создании отзыва подставляет текущего пользователя."""
        serializer.save(user=self.request.user)

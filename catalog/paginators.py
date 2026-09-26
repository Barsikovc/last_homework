from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Кастомный пагинатор: 10 элементов на страницу, можно менять через ?page_size=."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
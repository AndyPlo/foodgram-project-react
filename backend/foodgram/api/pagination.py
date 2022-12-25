from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    page_size_query_param = 'limit'

from django.core import paginator
from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    django_paginator_class = paginator.Paginator
    page_query_param = 'page'
    page_size_query_param = 'limit'

from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    last_page_strings = ('last',)
    invalid_page_message = 'Invalid page number.'
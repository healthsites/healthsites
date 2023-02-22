__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '21/05/19'

from django.core.paginator import EmptyPage, Paginator
from rest_framework.views import APIView


class NotANumberException(Exception):
    """ Class exception if it is not a number
    """

    def __init__(self):
        error = 'page is not a number'
        super(NotANumberException, self).__init__(error)
        self.errors = error


class LessThanOneException(Exception):
    """ Class exception if less than one
    """

    def __init__(self):
        error = 'page less than 1'
        super(LessThanOneException, self).__init__(error)
        self.errors = error


class PaginationAPI(APIView):
    """
    Base API for Facilities in pagination
    """
    page = None

    def get_query_by_page(self, query):
        """ Get query by page request
        :param query: query that will be paginated
        :type query: Queryset

        :return: Paginated query
        """
        data = self.request.GET
        page = data.get('page', 1)
        limit = data.get('limit', 100)
        try:
            self.page = int(page)
            if self.page <= 0:
                raise LessThanOneException()
        except ValueError:
            raise NotANumberException()
        try:
            paginator = Paginator(query, limit)
            return paginator.page(self.page)
        except EmptyPage:
            return []

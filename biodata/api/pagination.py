from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

LIMIT_MAX = 100


class CustomPagination(LimitOffsetPagination):
    max_limit = LIMIT_MAX
    default_limit = LIMIT_MAX

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.count,
            'limit': self.limit,
            'offset': self.offset,
            'results': data
        })

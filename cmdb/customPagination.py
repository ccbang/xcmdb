from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    ''' 自定义分页信息
    如果某个view list不想使用这种数据返回列表
    可以使用
    pagination_class = None
    来覆盖分页方法
    '''

    page_size_query_param = 'pageSize'

    def get_paginated_response(self, data):
        print(self.__dict__)
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'pagination': {
                'total': self.page.paginator.count,
                'pageSize': self.get_page_size(self.request),
                'current': self.page.number
            },
            'list': data
        })

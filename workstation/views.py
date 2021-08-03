from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.filters import WeldinggunsFilter
from workstation.models import MyLocation, BladeApply
from workstation.serializers import LocationSerializer, BladeItemSerializer


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10  # default limit per age
    page_size_query_param = 'pageSize'  # default param is offset
    max_limit = 15  # max limit per age


class LocationsViewset(ModelViewSet):
    queryset = MyLocation.objects.all()
    serializer_class = LocationSerializer

    '''
    cph_location_tree:
    返回一级地点带'CPH'字段的工位信息
    '''

    # 1,获取所有一级地点带’CPH‘的工位信息
    @action(methods=['GET'], detail=False)  # 生成路由规则: 前缀/方法名/
    def cph_location_tree(self, request):
        list = []
        # 1,获取CPH工位号
        location = MyLocation.objects.filter(location_level_1__contains='CPH')
        # 2,创建序列化器对象
        serializer = self.get_serializer(instance=location, many=True)
        for item in serializer.data:
            if item not in list:
                list.append(item)
        # 3,返回响应
        return Response(list)


class BladeItemViewSet(ModelViewSet):
    queryset = BladeApply.objects.all()
    serializer_class = BladeItemSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filterset_class = WeldinggunsFilter
    ordering_fields = ('create_time',)
    ordering = ('-create_time')  # 默认排序

    @action(methods=['post'], detail=False)
    def check(self, request):
        id = request.data['id']
        print(id)
        return Response('ww')
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     # for t in queryset:
    #     #     print(t)
    #
    #     # page = self.paginate_queryset(queryset)
    #     # bladeitem = BladeApply.objects.all()
    #     serializer = self.get_serializer(queryset, many=True)
    #     for t in serializer:
    #         print(t)
    #     # print(serializer.data)
    #     return Response({'rows': serializer.data, 'total': 'iii'})
    # @action(methods=['GET'], detail=False)
    # def blade_item(self, request):
    #     pagination_class = MyPageNumberPagination
    #     query = request.query_params
    #     print(query)
    #     # 创建序列化器对象
    #     queryset = self.get_object()
    #     print(queryset)
    #     # 配置分页数据
    #     pagination = pagination_class.paginate_queryset(queryset, request, self)
    #     #序列化
    #     serializer = self.get_serializer(isinstance=pagination, many=True)
    #
    #     Response(serializer.data)

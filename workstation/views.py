import base64

from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.filters import WeldinggunsFilter
from workstation.models import MyLocation, BladeApply, Images
from workstation.serializers import LocationSerializer, BladeItemSerializer, ImageSerializer


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
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter,)
    filterset_class = WeldinggunsFilter
    ordering_fields = ('create_time',)
    ordering = ('-create_time',)  # 默认排序
    search_fields = ('weldinggun__weldinggun_num',)

    # @action(methods=['PATCH'], detail=True)
    # def upload_img(self, request, *args, **kwargs):
    #     data = request.data
    #     print(data)
    #     ser_data = data
    #     if data['sort'] == 'repair_order_img':  # 维修单图片
    #         bladeitem = BladeApply.objects.get(pk=data['itemid'])
    #         ser_data = {
    #             'img_name': 'roimg-' + str(bladeitem.repair_order_num),
    #             'img': data['img'],
    #         }
    #         serializer = self.get_serializer(data=ser_data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             bladeitem.repair_order_img.id = self.get_object()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     serializer = self.get_serializer(data=ser_data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class ImagesViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        ser_data = data
        if data['sort'] == 'repair_order_img':  # 维修单图片
            bladeitem = BladeApply.objects.get(pk=data['itemid'])
            ser_data = {
                'img_name': 'roimg-' + str(bladeitem.repair_order_num),
                'img': data['img'],
            }
            serializer = self.get_serializer(data=ser_data)
            if serializer.is_valid():
                serializer.save()
                bladeitem.repair_order_img.id = self.get_object()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer = self.get_serializer(data=ser_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

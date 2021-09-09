import base64
import re

from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from utils.filters import WeldinggunsFilter, MaintenanceRecordsFilter
from workstation.models import MyLocation, BladeApply, Images, WeldingGun, Robot, MaintenanceRecords, Parts, MySort
from workstation.serializers import LocationSerializer, BladeItemSerializer, ImageSerializer, WeldinggunSerializer, \
    MaintenanceRecordsSerializer, PartsSerializer, SortSerializer


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10  # default limit per age
    page_size_query_param = 'pageSize'  # default param is offset
    max_limit = 15  # max limit per age


class PartsViewSet(ModelViewSet):
    queryset = Parts.objects.all()
    serializer_class = PartsSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter,)
    filter_fields = ('sort__type_layer', 'tag', 'users')  # 逗号必加,缺点无法模糊查询
    ordering_fields = ('hot',)
    ordering = ('-hot',)  # 默认排序
    search_fields = ('part_num', 'my_spec', 'order_num', 'brand__company_name', 'supplier__company_name')


class LocationsViewSet(ModelViewSet):
    queryset = MyLocation.objects.all()
    serializer_class = LocationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('weldinggun__weldinggun_num',)

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

    # 1,获取所有一级地点带’CPH‘的工位信息
    #  /workstation/location/back_by_target/?location=all&target=weldinggun
    @action(methods=['GET'], detail=False)  # 生成路由规则: 前缀/方法名/
    def back_by_target(self, request):
        print(request.query_params)
        query = request.query_params
        data = []
        if query['target'] == 'local':
            locations = MyLocation.objects.filter(location_level_1__contains='CPH')
            for location in locations:
                data.append({
                    'value': location.location_level_4,
                    'area': location.location_level_1 + '-' + location.location_level_2 + '-' + location.location_level_3
                })
            return Response(data)
        if query['target'] == 'robot':
            robots = Robot.objects.filter(location__location_level_1__contains='CPH')
            for robot in robots:
                data.append({
                    'value': robot.robot_num,
                    'area': robot.location.location_level_1 + '-' + robot.location.location_level_2 + '-' + robot.location.location_level_3
                })
            return Response(data)
        if query['target'] == 'weldinggun':
            weldingguns = WeldingGun.objects.filter(location__location_level_1__contains='CPH')
            for weldinggun in weldingguns:
                data.append({
                    'value': weldinggun.weldinggun_num,
                    'area': weldinggun.location.location_level_1 + '-' + weldinggun.location.location_level_2 + '-' + weldinggun.location.location_level_3
                })
            return Response(data)


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


class WeldingGunViewSet(ModelViewSet):
    queryset = WeldingGun.objects.all()
    serializer_class = WeldinggunSerializer


class MaintenanceRecordsViewSet(ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = (authentication.JWTAuthentication,)
    queryset = MaintenanceRecords.objects.all()
    serializer_class = MaintenanceRecordsSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter,)
    filterset_class = MaintenanceRecordsFilter
    ordering_fields = ('create_time',)
    ordering = ('-create_time',)  # 默认排序
    # search_fields = ('',)


class SortViewSet(ModelViewSet):
    queryset = MySort.objects.all()
    serializer_class = SortSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter,)
    search_fields = ('type_name',)
    ordering_fields = ('type_layer',)
    ordering = ('type_layer',)  # 默认排序

    def destroy(self, request, *args, **kwargs):
        try:
            del_sort = MySort.objects.get(pk=kwargs['pk'])
            del_sort_layer = re.findall(r'\w{2}', del_sort.type_layer)
            if del_sort_layer[2] == '00':
                if del_sort_layer[1] == '00':
                    MySort.objects.filter(type_layer__startswith=del_sort_layer[0]).delete()
                else:
                    # print(del_sort_layer[0] + del_sort_layer[1])
                    MySort.objects.filter(type_layer__startswith=(del_sort_layer[0] + del_sort_layer[1])).delete()
            else:
                del_sort.delete()
            data = {
                'code': 30,
                'msg': '删除成功！'
            }
        except Exception as e:
            data = {
                'code': 31,
                'msg': '无法删除，存在级联关系！'
            }
        return Response(data)

    @action(methods=['get'], detail=False)
    def listsort_device(self, request):
        data = request.query_params
        device_sort = MySort.objects.filter(type_layer__startswith='02')
        device_sort_ser = self.get_serializer(device_sort, many=True)
        return Response({
            'results': device_sort_ser.data,
            'code': 40
        })

import base64
import re

from django.db.models import Q
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
from rest_framework_simplejwt import authentication

from utils.filters import WeldinggunsFilter, MaintenanceRecordsFilter, PartSearch
from utils.utils import SortListAndList
from workstation.models import MyLocation, BladeApply, Images, WeldingGun, Robot, MaintenanceRecords, Parts, MySort, \
    DevicesType, Stock
from workstation.serializers import LocationSerializer, BladeItemSerializer, ImageSerializer, WeldinggunSerializer, \
    MaintenanceRecordsSerializer, PartsSerializer, SortSerializer, DevicesTypeSerializer
import numpy as np


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'results': serializer.data
        })


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
        # print(request.query_params)
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

    @action(methods=['GET'], detail=False)
    def analyse_data(self, request, *args, **kwargs):

        workstationsData = {}
        # --------------------------数据收集--------------------------#
        bladeitems_querysets = BladeApply.objects.filter(order_status=4)
        bladeitems = list(bladeitems_querysets)
        for bladeitem in bladeitems:
            if bladeitem.weldinggun.weldinggun_num in workstationsData:
                workstationsData[bladeitem.weldinggun.weldinggun_num]['frequency'] += 1
            else:
                workstationsData[bladeitem.weldinggun.weldinggun_num] = {'frequency': 1}
                workstationsData[bladeitem.weldinggun.weldinggun_num]['bladetypeset'] = []
                workstationsData[bladeitem.weldinggun.weldinggun_num]['price'] = []
                workstationsData[bladeitem.weldinggun.weldinggun_num]['timeset'] = []
            workstationsData[bladeitem.weldinggun.weldinggun_num]['bladetypeset'].append(
                bladeitem.bladetype_received.my_spec)
            workstationsData[bladeitem.weldinggun.weldinggun_num]['price'].append(
                bladeitem.bladetype_received.price)
            workstationsData[bladeitem.weldinggun.weldinggun_num]['timeset'].append(bladeitem.create_time)

        # print(workstationsData)
        # --------------------------数据解析--------------------------#
        top_receive = {
            'workstations': [],
            'workstations_freq': [],
        }
        service_data = {
            'blade_type': [],
            'blade_price': [],
            'average_life': [],
            'cost_effective': [],
            'temple_num': [],
        }
        blade_service_status = []
        for w in workstationsData:
            top_receive['workstations'].append(w)
            top_receive['workstations_freq'].append(len(workstationsData[w]['timeset']))
            for i in range(0, len(workstationsData[w]['bladetypeset'])):
                if i < len(workstationsData[w]['bladetypeset']) - 1:
                    delta = workstationsData[w]['timeset'][i + 1] - workstationsData[w]['timeset'][i]
                    delta_day = delta.days
                    if len(workstationsData[w]['bladetypeset']) is not 1:
                        if workstationsData[w]['bladetypeset'][i] in service_data['blade_type']:
                            index = service_data['blade_type'].index(workstationsData[w]['bladetypeset'][i])
                            service_data['average_life'][index] = round(
                                ((service_data['average_life'][index] * service_data[
                                    'temple_num'][index] + delta_day) / (service_data['temple_num'][index] + 1)), 2)
                            service_data['temple_num'][index] += 1
                        else:
                            service_data['blade_type'].append(workstationsData[w]['bladetypeset'][i])
                            service_data['blade_price'].append(workstationsData[w]['price'][i])
                            service_data['average_life'].append(delta_day)
                            service_data['cost_effective'].append(0)
                            service_data['temple_num'].append(1)
        for i in range(len(service_data['blade_type'])):
            service_data['cost_effective'][i] = round(
                service_data['average_life'][i] * 10 / service_data['blade_price'][i],
                2)
            # service_data['total_receive'].append(len(bladeitems_querysets.filter(
            #     bladetype_received__my_spec=service_data['blade_type'][i])))

        # --------------------------top10--------------------------#
        top_receive['workstations'], top_receive['workstations_freq'] = SortListAndList(top_receive['workstations'],
                                                                                        top_receive[
                                                                                            'workstations_freq'],
                                                                                        reverse=True)
        # --------------------------库存与总领用量--------------------------#
        blades = Parts.objects.filter(tag=1)
        for blade in blades:
            blade_stock = Stock.objects.filter(part__part_num=blade.part_num)
            blade_stock_nb = 0
            for b in blade_stock:
                if b.location.location_level_1 == '宁波':
                    blade_stock_nb += b.part_stock
            blade_service_status.append({
                'blade_spec': blade.my_spec.split('|', 1)[0],
                'total_receive': len(bladeitems_querysets.filter(
                    bladetype_received__my_spec=blade.my_spec)),
                'blade_stock_nb': blade_stock_nb
            })

        return Response({
            'top_receive': top_receive,
            'service_data': service_data,
            'blade_service_status': blade_service_status
        })


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
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (authentication.JWTAuthentication,)
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
        # data = request.query_params
        device_sort = MySort.objects.filter(type_layer__startswith='02')
        device_sort_ser = self.get_serializer(device_sort, many=True)
        return Response({
            'results': device_sort_ser.data,
            'code': 40
        })


class DevicesTypeViewSet(ModelViewSet):
    queryset = DevicesType.objects.all()
    serializer_class = DevicesTypeSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter,)
    filter_fields = ('device_sort__type_layer',)  # 逗号必加,缺点无法模糊查询
    ordering_fields = ('create_time',)
    ordering = ('-create_time',)  # 默认排序

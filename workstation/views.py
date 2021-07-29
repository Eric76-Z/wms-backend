from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from workstation.models import MyLocation
from workstation.serializers import LocationSerializer


class LocationsViewset(ModelViewSet):
    queryset = MyLocation.objects.all()
    serializer_class = LocationSerializer

    # 1,获取阅读量大于20的书籍
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
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
    def main_location(self, request):
        print('wwwwwwwwwwwwwwww')
        # 1,获取指定书籍
        location = MyLocation.objects.filter(location_level_1='CPH2.1')
        print(location)
        # 2,创建序列化器对象
        serializer = self.get_serializer(instance=location, many=True)
        # 3,返回响应
        return Response(serializer.data)

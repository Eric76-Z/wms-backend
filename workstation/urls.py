from django.urls import path
from . import views, views_fc

urlpatterns = [

]

from rest_framework.routers import SimpleRouter, DefaultRouter

# 1,创建路由对象
router = SimpleRouter()

# 2,注册视图集
router.register('location', views.LocationsViewSet, basename='location')
router.register('parts', views.PartsViewSet, basename='parts')
router.register('bladeitem', views.BladeItemViewSet, basename='bladeitem')
router.register('images', views.ImagesViewSet, basename='images')
router.register('weldinggun', views.WeldingGunViewSet, basename='weldinggun')
router.register('maintenance', views.MaintenanceRecordsViewSet, basename='maintenance')
router.register('sort', views.SortViewSet, basename='sort')


urlpatterns += router.urls

# 3,输出结果
# print(urlpatterns)

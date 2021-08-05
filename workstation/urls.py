from django.urls import path
from . import views

urlpatterns = [
    # url(r'^books/$',views.BookInfoModelViewSet.as_view({"get":"list","post":"create"})),
    # url(r'^books/(?P<pk>\d+)/$',views.BookInfoModelViewSet.as_view({"get":"retrieve","put":"update","delete":"destory"})),
    #
    # url(r'^books/bread/$',views.BookInfoModelViewSet.as_view({"get":"bread_book"})),
    # url(r'^books/bread/(?P<pk>\d+)/$',views.BookInfoModelViewSet.as_view({"put":"update_book_bread"})),

    # path(r'^test/$', views.TestView.as_view()),
]

from rest_framework.routers import SimpleRouter, DefaultRouter

# 1,创建路由对象
router = SimpleRouter()

# 2,注册视图集
router.register('location', views.LocationsViewset, basename='location')
router.register('bladeitem', views.BladeItemViewSet, basename='bladeitem')
router.register('images', views.ImagesViewSet, basename='images')
urlpatterns += router.urls

# 3,输出结果
# print(urlpatterns)

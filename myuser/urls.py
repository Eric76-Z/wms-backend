
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from myuser import views
from myuser.views import MyTokenObtainPairView, RegisterView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(r'login/', MyTokenObtainPairView.as_view()),
    path('register/', RegisterView.as_view())
]

# 1,创建路由对象
router = SimpleRouter()

# 2,注册视图集
router.register('user', views.UsersViewSet, basename='user')

urlpatterns += router.urls

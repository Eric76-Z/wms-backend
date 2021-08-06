
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from myuser.views import MyTokenObtainPairView, RegisterView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'login/', MyTokenObtainPairView.as_view()),
    path('register/', RegisterView.as_view())
]


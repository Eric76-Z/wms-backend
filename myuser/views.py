from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from myuser.models import UserProfile
from myuser.serializers import UserRegSerializer, MyTokenObtainPairSerializer, UserProfileSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegSerializer
    # 注意需要指定permission_classes = []为空列表或者允许所有权限[rest_framework.permissions.AllowAny]
    permission_classes = []

    # def post(self, request):
    #     data = request.data
    #     username = data['username']
    #     password = data['passowrd']
    #     phonenum = data['phonenum']
    #     email = data['email']
    #
    #     if all([username, password]):
    #         pass
    #     else:
    #         return Response({'msg': '请输入用户名或密码'})
    #     user= UserProfile
    # email = request.data.get('username')
    # passwrod = request.data.get('password')
    # if all([email, passwrod]):
    #     pass
    # else:
    #     return Response({'code': 9999, 'msg': '参数不全'})
    # rand_name = self.randomUsername()
    # user = User(username=rand_name, email=email)
    # user.set_password(passwrod)
    # user.save()
    # return Response({'code': 0, 'msg': '注册成功'})


class UsersViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    read_only_fields = []


#     @action(methods=['post'], detail=True)
#     def set_password(self, request, pk=None):
#         user = self.get_object()
#         serializer = PasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             user.set_password(serializer.data['password'])
#             user.save()
#             return Response({'status': 'password set'})
#         else:
#             return Response(serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)
# #
#     @action(detail=False)
#     def recent_users(self, request):
#         recent_users = User.objects.all().order('-last_login')
#
#         page = self.paginate_queryset(recent_users)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(recent_users, many=True)
#         return Response(serializer.data)

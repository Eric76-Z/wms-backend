from rest_framework import generics

from myuser.serializers import UserRegSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['token'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        data['userId'] = self.user.id
        data['isSuper'] = self.user.is_superuser
        try:
            data['realname'] = self.user.last_name + self.user.first_name
            data['phonenum'] = self.user.phonenum
            data['email'] = self.user.email
        except:
            data['realname'] = 'null'
            data['phonenum'] = 'null'
            data['phonenum'] = 'null'
        return data


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

#
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

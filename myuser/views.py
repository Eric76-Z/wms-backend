import datetime

from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from myuser.models import UserProfile
from myuser.serializers import UserRegSerializer, MyTokenObtainPairSerializer, UserProfileSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

from utils.utils import CodeRandom, SendEmailCode
from wms import settings
from workstation.models.base_models import EmailVerifyRecord


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegSerializer
    # 注意需要指定permission_classes = []为空列表或者允许所有权限[rest_framework.permissions.AllowAny]
    permission_classes = []

    def create(self, request, *args, **kwargs):
        print(request.data)
        user_serializer = self.get_serializer(data=request.data)
        if request.data['password'] != request.data['password1']:
            return Response({
                'code': 11,
                'msg': '密码与确认密码不一致!'
            })
        else:
            if user_serializer.is_valid():
                user_serializer.save()
                new_user = UserProfile.objects.get(phonenum=request.data['phonenum'])
                # new_user.is_active = 1
                new_user.set_password(request.data['password'])
                new_user.save()
                return Response({'msg': '注册成功！', 'code': 10})
            else:
                return Response({'msg': user_serializer.errors, 'code': 12})


class UsersViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    read_only_fields = []


class GetCode(APIView):

    def get(self, request):
        data = request.query_params
        data = SendEmailCode(data['email'], 'reset')
        return Response(data)


class ResetPwd(APIView):
    def post(self, request):
        data = request.data
        print(data)
        # 删除超过30天的数据
        nowday = datetime.date.today()
        deltaday = datetime.timedelta(days=30)
        delete_day = nowday - deltaday
        EmailVerifyRecord.objects.filter(send_time__lte=delete_day).delete()

        email_record = EmailVerifyRecord.objects.get(code=data['code'])

        nowtime = datetime.datetime.now()
        expire_time = nowtime - datetime.timedelta(minutes=5)
        if email_record.send_time > expire_time:
            user = UserProfile.objects.get(email=data['email'])
            if user:
                user.set_password(data['password'])
                user.save()
                return Response({
                    'code': 20,
                    'msg': '重置密码成功！'
                })
            else:
                return Response({
                    'code': 21,
                    'msg': '邮箱输入有误！'
                })
        else:
            return Response({
                'code': 23,
                'msg': '验证码过期！'
            })

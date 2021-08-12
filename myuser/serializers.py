import datetime

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from myuser.models import UserProfile



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
            data['lastname'] = self.user.last_name
            data['firstname'] = self.user.first_name
            data['realname'] = self.user.last_name + self.user.first_name
            data['phonenum'] = self.user.phonenum
            data['email'] = self.user.email
        except:
            data['lastname'] = 'null'
            data['firstname'] = 'null'
            data['realname'] = 'null'
            data['phonenum'] = 'null'
            data['phonenum'] = 'null'
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['password']

    def to_representation(self, value):
        """重写返回的数据（添加额外字段）"""
        # print('eeeeeeee')
        # print(value)
        data = super().to_representation(value)
        user = UserProfile.objects.get(phonenum=data['phonenum'])
        try:
            data['realname'] = user.last_name + user.first_name
        except:
            data['realname'] = 'null'
        # 返回处理之后的数据
        data['id'] = user.id
        data['isSuper'] = user.is_superuser
        data['groups'] = user.groups.values_list('name', flat=True)
        data_back={
            'email': data['email'],
            'firstname': data['first_name'],
            'lastname': data['last_name'],
            'realname': data['realname'],
            'groups': data['groups'],
            'isSuper': data['isSuper'],
            'phonenum': data['phonenum'],
            'userId': data['id'],
            'username': data['username']
        }
        return data_back

class UserRegSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(label='确认密码', help_text='确认密码',
                                      min_length=6, max_length=12,
                                      write_only=True,
                                      error_messages={
                                          'min_length': '仅允许6~12个字符的确认密码',
                                          'max_length': '仅允许6~12个字符的确认密码', })
    token = serializers.CharField(label='生成token', read_only=True)
    refresh = serializers.CharField(label='生成token', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'phonenum', 'password', 'password1', 'token', 'refresh']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError('密码与确认密码不一致')
        if UserProfile.objects.filter(email=attrs.get('email')):
            raise serializers.ValidationError('邮箱已存在')
        if UserProfile.objects.filter(email=attrs.get('phonenum')):
            raise serializers.ValidationError('手机号已存在')

        return attrs

    def create(self, validated_data):
        validated_data.pop('password1')
        # 创建user模型对象
        user = UserProfile.objects.create_user(**validated_data)
        user.last_login = datetime.datetime.now()
        # 创建token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        user.token = access_token
        user.refresh = refresh
        return user

    def to_representation(self, value):
        """重写返回的数据（添加额外字段）"""
        print(value)
        data = super().to_representation(value)
        user = UserProfile.objects.get(phonenum=data['phonenum'])
        try:
            data['realname'] = user.last_name + user.first_name
        except:
            data['realname'] = 'null'
        # 返回处理之后的数据
        data.pop('password')
        data['id'] = user.id
        data['isSuper'] = user.is_superuser
        data['groups'] = user.groups.values_list('name', flat=True)
        return data

    # def perform_create(self):

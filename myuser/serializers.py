import datetime

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from myuser.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['password']


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

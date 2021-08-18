import datetime

import jwt
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from rest_framework import serializers

from myuser.models import UserProfile
from utils.utils import SecondToLast
from wms import settings
from workstation.models import MyLocation, BladeApply, Images, WeldingGun, MaintenanceRecords, Parts, Articles, MySort


@receiver(pre_delete, sender=Images)  # sender=你要删除或修改文件字段所在的类**
def file_delete(instance, **kwargs):  # 函数名随意
    print('进入文件删除方法，删的是', instance.img)  # 用于测试
    instance.img.delete(False)  # file是保存文件或图片的字段名**


class LocationSerializer(serializers.ModelSerializer):
    localLv1 = serializers.CharField(source='location_level_1')
    localLv2 = serializers.CharField(source='location_level_2')
    localLv3 = serializers.CharField(source='location_level_3')

    class Meta:
        model = MyLocation
        fields = ('localLv1', 'localLv2', 'localLv3')
        read_only_fields = ('localLv1', 'localLv2', 'localLv3')
        extra_kwargs = {
            'localLv1': {
                'help_text': '车间'
            }
        }


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('img_name', 'img')


class WeldinggunSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeldingGun
        fields = '__all__'
        depth = 1  # 外键的序列化


class BladeItemSerializer(serializers.ModelSerializer):
    localLv1 = serializers.CharField(source='weldinggun.location.location_level_1', required=False)
    localLv2 = serializers.CharField(source='weldinggun.location.location_level_2', required=False)
    localLv3 = serializers.CharField(source='weldinggun.location.location_level_3', required=False)
    repair_order_img = ImageSerializer(required=False)

    class Meta:
        model = BladeApply
        fields = '__all__'
        # fields = (
        #     'weldinggun', 'bladetype_apply', 'applicant', 'bladetype_received', 'receiver', 'cycle_num', 'pressure',
        #     'oldblade_img', 'polestatus_img', 'repair_order_num', 'repair_order_img', 'order_status', 'order_comments',
        #     'receive_time', 'complete_time', 'create_time', 'update_time', 'localLv1', 'localLv2', 'localLv3',
        #     'last_receive_time')
        depth = 1  # 外键的序列化

    def to_representation(self, value):
        """重写返回的数据（添加额外字段）"""
        data = super().to_representation(value)
        # 获取接口权重数据进行组装

        dicts = BladeApply.objects.filter(
            Q(order_status=4) & Q(weldinggun__weldinggun_num=data['weldinggun']['weldinggun_num'])).order_by(
            '-create_time')
        last_replace = '首次领用'
        if dicts.exists():
            if data['order_status'] == 4:
                index = 0
                for dict in dicts.values():
                    index = index + 1
                    if dict['id'] == data['id']:
                        try:
                            last_replace = dicts.values()[index]['create_time']
                        except:
                            last_replace = '首次领用'
            else:
                for dict in dicts.values():

                    if BladeApply.objects.get(pk=data['id']).create_time > dict['create_time']:
                        last_replace = dicts.values()[0]['create_time']
                        break
        else:
            last_replace = '首次领用'

        if data['order_status'] == 2:
            try:
                order_comments = data['order_comments']
            except:
                order_comments = '可能短时间内再次领用！'
            data.update({"analyse": {
                'order_comments': order_comments
            }})
        elif data['order_status'] == 4:
            data.update({"analyse": {}})
        data.update({"analyse": {
            'last_replace': last_replace
        }})
        # 返回处理之后的数据
        return data

    def create(self, validated_data):

        blade = Parts.objects.get(pk=self.initial_data['bladetype_apply_id'])
        weldinggun = WeldingGun.objects.get(weldinggun_num=self.initial_data['weldinggunnum'])
        validated_data['bladetype_apply_id'] = blade.id
        validated_data['weldinggun_id'] = weldinggun.id

        bladeitem = BladeApply.objects.create(**validated_data)
        return bladeitem

    def update(self, instance, validated_data):
        # print(instance)
        # print(validated_data)
        try:  # 领用按钮
            validated_data['bladetype_received_id'] = self.initial_data['bladetype_received_id']
            validated_data['receiver_id'] = self.initial_data['receiver_id']
        except:
            pass
        super().update(instance, validated_data)
        return instance

    def is_valid(self, raise_exception=False):
        if self.initial_data.get("img"):
            bladeitem = BladeApply.objects.get(pk=self.initial_data['id'])
            if bladeitem.repair_order_img_id:
                image = Images.objects.get(pk=bladeitem.repair_order_img_id)
                file_delete(image)  # 删除文件
                image.delete()

            image = Images.objects.create(
                img_name='roimg-' + str(bladeitem.repair_order_num),
                img=self.initial_data['img'],
            )
            bladeitem.repair_order_img = image
            print(super(BladeItemSerializer, self).is_valid(raise_exception))
            self.validated_data['repair_order_img_id'] = image.id
            self.validated_data['complete_time'] = datetime.datetime.now()
        return super(BladeItemSerializer, self).is_valid(raise_exception)


class MaintenanceRecordsSerializer(serializers.ModelSerializer):
    # token = serializers.CharField(label='生成token', read_only=True)

    class Meta:
        model = MaintenanceRecords
        fields = '__all__'
        depth = 1  # 外键的序列化

    def is_valid(self, raise_exception=False):
        try:
            local = self.initial_data['MyLocation'].split('-')
            super(MaintenanceRecordsSerializer, self).is_valid(raise_exception)
            self.validated_data['applicant_id'] = self.initial_data['applicant_id']
            self.validated_data['localLv1'] = local[0]
            self.validated_data['localLv2'] = local[1]
            self.validated_data['localLv3'] = local[2]
        except:
            pass
        # print(self.validated_data)
        return super(MaintenanceRecordsSerializer, self).is_valid(raise_exception)

    def update(self, instance, validated_data):
        try:
            if self.initial_data['experience_summary']:
                validated_data['id'] = self.initial_data['id']
                validated_data['userId'] = self.initial_data['userId']
                validated_data['title'] = self.initial_data['title']
                validated_data['experience_summary'] = self.initial_data['experience_summary']
                # mtr = MaintenanceRecords.objects.get(pk=validated_data['id'])
                # 判断是否已存在总结
                if instance.experience_summary_id:
                    article = Articles.objects.get(id=instance.experience_summary_id)
                    article.title = validated_data['title']
                    article.body = validated_data['experience_summary']
                    article.save()
                else:
                    article = Articles.objects.create(title=validated_data['title'],
                                                      body=validated_data['experience_summary'],
                                                      main_author_id=validated_data['userId'], sort_id=44)
                    instance.experience_summary = article
                    instance.save()
        except:
            pass
        return instance



class PartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parts
        fields = '__all__'
        depth = 1  # 外键的序列化

from django.db.models import Q
from django.forms import model_to_dict
from rest_framework import serializers

from utils.utils import SecondToLast
from workstation.models import MyLocation, BladeApply


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


class BladeItemSerializer(serializers.ModelSerializer):
    weldinggun = serializers.CharField(source='weldinggun.weldinggun_num')
    bladetype_apply = serializers.CharField(source='bladetype_apply.my_spec')
    applicant = serializers.CharField(source='applicant.full_name', required=False)
    bladetype_received = serializers.CharField(source='bladetype_received.my_spec', default='null')
    receiver = serializers.CharField(source='receiver.full_name', required=False)
    localLv1 = serializers.CharField(source='weldinggun.location.location_level_1')
    localLv2 = serializers.CharField(source='weldinggun.location.location_level_2')
    localLv3 = serializers.CharField(source='weldinggun.location.location_level_3')
    repair_order_img_name = serializers.CharField(source='repair_order_img.file_name', default='null')
    repair_order_img = serializers.ImageField(source='repair_order_img.myfile', default='null')
    repair_order_img_sort = serializers.IntegerField(source='repair_order_img.sort.id',  required=False)

    # last_receive_time = 55

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
            Q(order_status=4) & Q(weldinggun__weldinggun_num=data['weldinggun'])).order_by('-create_time')
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
                last_replace = dicts.values()[0]['create_time']
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

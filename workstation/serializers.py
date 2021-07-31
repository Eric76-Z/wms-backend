from rest_framework import serializers

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

    class Meta:
        model = BladeApply
        fields = '__all__'
        depth = 1  # 外键的序列化

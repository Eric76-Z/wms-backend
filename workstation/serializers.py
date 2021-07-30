from rest_framework import serializers

from workstation.models import MyLocation, BladeApply


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyLocation
        fields = ('location_level_1', 'location_level_2', 'location_level_3')
        read_only_fields = ('location_level_1', 'location_level_2', 'location_level_3')
        extra_kwargs = {
            'location_level_1': {
                'help_text': '车间'
            }
        }



class BladeItemSerializer(serializers.ModelSerializer):
    weldinggun = serializers.CharField(source='weldinggun.weldinggun_num')
    bladetype_apply = serializers.CharField(source='bladetype_apply.my_spec')
    applicant = serializers.CharField(source='applicant.full_name', required=False)
    bladetype_received = serializers.CharField(source='bladetype_received.my_spec', default='null')
    receiver = serializers.CharField(source='receiver.full_name', required=False)
    Lv1 = serializers.CharField(source='weldinggun.location.location_level_1')
    Lv2 = serializers.CharField(source='weldinggun.location.location_level_2')
    Lv3 = serializers.CharField(source='weldinggun.location.location_level_3')

    class Meta:
        model = BladeApply
        fields = '__all__'
        print(fields)
        fields = fields + ['Lv1', 'Lv2', 'Lv3']
        depth = 1  # 外键的序列化

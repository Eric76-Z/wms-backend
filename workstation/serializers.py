from rest_framework import serializers

from workstation.models import MyLocation


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyLocation
        fields = ('location_level_1', 'location_level_2', 'location_level_3')
        read_only_fields = ('location_level_1', 'location_level_2', 'location_level_3')

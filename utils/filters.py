from itertools import chain

import django_filters
from django.db.models import Q

from workstation.models import BladeApply


class WeldinggunsFilter(django_filters.rest_framework.FilterSet):
    """用于焊枪工位查询的过滤器"""
    localLv1 = django_filters.CharFilter(field_name="weldinggun__location__location_level_1",
                                    help_text='车间', method='location_filter')
    localLv2 = django_filters.CharFilter(field_name="weldinggun__location__location_level_2", help_text='区域',
                                    method='location_filter')
    localLv3 = django_filters.CharFilter(field_name="weldinggun__location__location_level_3", help_text='线体',
                                    method='location_filter')

    def location_filter(self, queryset, name, value):
        datas = value.split(',')
        final_queryset = BladeApply.objects.none()
        for data in datas:
            if name == 'weldinggun__location__location_level_1':
                final_queryset = final_queryset | queryset.filter(weldinggun__location__location_level_1=data)
            elif name == 'weldinggun__location__location_level_2':
                final_queryset = final_queryset | queryset.filter(weldinggun__location__location_level_2=data)
            elif name == 'weldinggun__location__location_level_3':
                final_queryset = final_queryset | queryset.filter(weldinggun__location__location_level_3=data)
        return final_queryset

    class Meta:
        model = BladeApply
        # 用于查询的字段
        fields = ['localLv1', 'localLv2', 'localLv3']

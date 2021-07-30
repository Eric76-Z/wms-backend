import django_filters

from workstation.models import BladeApply

#
class WeldinggunsFilter(django_filters.rest_framework.FilterSet):
    """用于商品查询的过滤器"""
    Lv1 = django_filters.CharFilter(field_name="weldinggun.location.location_level_1", lookup_expr='icontains', help_text='车间')
    # Lv2 = django_filters.CharFilter(name="Lv2", lookup_expr='icontains', help_text='区域')
    # Lv3 = django_filters.CharFilter(name="Lv3", lookup_expr='icontains', help_text='线体')
    class Meta:
        model = BladeApply
        # 用于查询的字段
        # fields = ['Lv1', 'Lv2', 'Lv3']
        fields = 'Lv1'
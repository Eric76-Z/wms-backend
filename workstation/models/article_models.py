from django.db import models


class MaintenanceModel(models.Model):
    type_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='分类名')
    f_type_id = models.IntegerField(blank=True, null=True, verbose_name='父分类')
    type_layer = models.TextField(blank=True, null=True, verbose_name='层级')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'sort'

    def __str__(self):
        return self.type_name

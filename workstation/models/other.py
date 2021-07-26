

from django.db import models


class BladeConsumingV1(models.Model):
    WorkShop = models.CharField(max_length=32, verbose_name="领用车间")
    UseArea = models.CharField(max_length=32, verbose_name="领用区域")
    UseProductionLine = models.CharField(max_length=32, verbose_name="领用线体")
    UseNumSK = models.CharField(max_length=32, verbose_name="焊接控制柜编号")
    UserName = models.CharField(max_length=32, verbose_name="领用人")
    BladeType = models.CharField(max_length=16, null=True, blank=True, verbose_name="刀片型号")
    # UseNum = models.IntegerField(null=True, blank=True, verbose_name="领用数量")
    CycleNum = models.IntegerField(null=True, blank=True, verbose_name="修磨圈数")
    Pressure = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name="修磨压力")
    OldBladePicture = models.FileField(null=True, blank=True, upload_to='Blade/OldBlade/', verbose_name="旧刀片图片")
    PoleStatus = models.FileField(null=True, blank=True, upload_to='Blade/PoleStatus/', verbose_name="修磨后电极杆状态")
    RepairOrderNum = models.IntegerField(null=True, blank=True, verbose_name="维修单编号")
    RepairOrderPicture = models.FileField(null=True, blank=True, upload_to='Blade/RepairOrder/', verbose_name="维修单图片")
    OlderStatus = models.IntegerField(null=True, blank=True, verbose_name='订单状态')
    UseTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="领用时间")
    CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
    UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")


    class Meta:
        db_table = 'BladeConsumingV1'

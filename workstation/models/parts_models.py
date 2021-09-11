from django.db import models

from workstation.models import Company
from workstation.models.base_models import MySort, MyLog, MyTag, Images
from workstation.models.location_models import MyLocation
from workstation.models.device_models import DevicesType
from myuser.models import UserProfile


# 备件备案表


class Parts(models.Model):
    part_num = models.CharField(max_length=12, blank=True, null=True, verbose_name="物料号")
    my_spec = models.CharField(max_length=255, blank=True, null=True, verbose_name="M型号")
    price = models.FloatField(blank=True, null=True, verbose_name="价格")
    order_num = models.CharField(max_length=255, blank=True, null=True, verbose_name="订货号")
    setech_spec = models.CharField(max_length=255, blank=True, null=True, verbose_name="西泰克规格")
    brand = models.ForeignKey(Company, models.DO_NOTHING, related_name='brand_company', blank=True, null=True,
                              verbose_name="品牌")
    supplier = models.ForeignKey(Company, models.DO_NOTHING, related_name='supplier_company', blank=True, null=True,
                                 verbose_name="供应商")
    cordon = models.IntegerField(blank=True, null=True, verbose_name="警戒线")
    min_line = models.IntegerField(blank=True, null=True, verbose_name="底线")
    unit = models.CharField(max_length=16, blank=True, null=True, verbose_name="单位")
    part_img = models.ManyToManyField(Images, blank=True, verbose_name="备件图")
    mark = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注")
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="描述")
    device_type = models.ManyToManyField(DevicesType, blank=True, verbose_name="所属设备")
    f_part_id = models.IntegerField(blank=True, null=True, verbose_name="父备件id")
    sort = models.ManyToManyField(MySort, blank=True, verbose_name="分类")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
    log = models.ManyToManyField(MyLog, blank=True)
    tag = models.ManyToManyField(MyTag, blank=True)
    hot = models.IntegerField(default=0, blank=True, null=True, verbose_name='热度')
    users = models.ManyToManyField(UserProfile, blank=True, verbose_name="收藏")

    class Meta:
        db_table = 'parts'
        indexes = [models.Index(fields=['part_num'])]
        index_together = ['my_spec', 'setech_spec']

    def __str__(self):
        return self.my_spec


# 备件库存表
class Stock(models.Model):
    user = models.ForeignKey(UserProfile, models.DO_NOTHING, blank=True, null=True, verbose_name="人员")
    applicant = models.CharField(max_length=64, blank=True, null=True, verbose_name="申请人（char)")
    part = models.ForeignKey(Parts, models.DO_NOTHING, blank=True, null=True, verbose_name="备件")
    part_stock = models.IntegerField(blank=True, null=True, verbose_name="库存")
    location = models.ForeignKey(MyLocation, models.DO_NOTHING, blank=True, null=True, verbose_name="位置")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'stock'

    def __str__(self):
        return self.part.my_spec


# 备件上单表
class Orders(models.Model):
    user = models.ForeignKey(UserProfile, models.DO_NOTHING, blank=True, null=True, verbose_name="人员")
    part = models.ForeignKey(Parts, models.DO_NOTHING, blank=True, null=True, verbose_name="备件")
    part_stock = models.IntegerField(blank=True, null=True, verbose_name="库存")
    part_inorder = models.IntegerField(blank=True, null=True, verbose_name="上单")
    part_ontheway = models.IntegerField(blank=True, null=True, verbose_name="在途")
    arrival_date = models.DateField(blank=True, null=True, verbose_name="交货期")
    order_status = models.IntegerField(blank=True, null=True, verbose_name="订单状态")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return self.part.my_spec


# 备件领用表
class Consuming(models.Model):
    user = models.ForeignKey(UserProfile, models.DO_NOTHING, blank=True, null=True, verbose_name="人员")
    stock_id = models.ForeignKey(Stock, models.DO_NOTHING, blank=True, null=True, verbose_name="备件")
    consuming_num = models.IntegerField(blank=True, null=True, verbose_name="数量")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注")
    receive_time = models.DateTimeField(blank=True, null=True, verbose_name="领用时间")
    complete_time = models.DateTimeField(blank=True, null=True, verbose_name="完成时间")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'consuming'

    def __str__(self):
        return self.stock_id.part.my_spec

# class Part(models.Model):
#     MaterialNumSetec = models.CharField(max_length=16, null=True, blank=True, verbose_name='西泰克物料号')
#     PartType = models.CharField(max_length=128, null=True, blank=True, verbose_name='备件型号')
#     PartTypeSetec = models.CharField(max_length=128, null=True, blank=True, verbose_name='西泰克备件型号')
#     PartBrand = models.CharField(max_length=32, null=True, blank=True, verbose_name='备件品牌')
#     PartSupplier = models.CharField(max_length=32, null=True, blank=True, verbose_name='备件供应商')
#     PartPrice = models.IntegerField(null=True, blank=True, verbose_name='备件价格')
#     PartStock = models.IntegerField(null=True, blank=True, verbose_name='库存')
#     PartInorder = models.IntegerField(null=True, blank=True, verbose_name='上单')
#     PartOntheway = models.IntegerField(null=True, blank=True, verbose_name='在途')
#     PartCordon = models.IntegerField(null=True, blank=True, verbose_name='安全量')
#     PartInfo = models.TextField(max_length=1024, null=True, blank=True, verbose_name='备件简介')
#     PartPicture = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="备件图片")
#     PartAddress1 = models.CharField(max_length=32, null=True, blank=True, verbose_name='库位1')
#     PartAddress2 = models.CharField(max_length=32, null=True, blank=True, verbose_name='库位2')
#     PartAddress3 = models.CharField(max_length=32, null=True, blank=True, verbose_name='库位3')
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'Part'
#
#     def __str__(self):
#         return self.PartType
#
#
# class PartD(models.Model):
#     MaterialNumSetec = models.CharField(max_length=16, null=True, blank=True, verbose_name='西泰克物料号')
#     PartType = models.CharField(max_length=128, null=True, blank=True, verbose_name='备件型号')
#     PartTypeSetec = models.CharField(max_length=128, null=True, blank=True, verbose_name='西泰克备件型号')
#     PartBrand = models.CharField(max_length=32, null=True, blank=True, verbose_name='备件品牌')
#     PartU = models.ManyToManyField(Part, blank=True, verbose_name="父备件")
#     PartSupplier = models.CharField(max_length=32, null=True, blank=True, verbose_name='备件供应商')
#     PartPrice = models.IntegerField(null=True, blank=True, verbose_name='备件价格')
#     PartStock = models.IntegerField(null=True, blank=True, verbose_name='库存')
#     PartInorder = models.IntegerField(null=True, blank=True, verbose_name='上单')
#     PartOntheway = models.IntegerField(null=True, blank=True, verbose_name='在途')
#     PartCordon = models.IntegerField(null=True, blank=True, verbose_name='安全量')
#     PartInfo = models.TextField(max_length=1024, null=True, blank=True, verbose_name='备件简介')
#     PartPicture = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="备件图片")
#     PartAddress1 = models.CharField(max_length=32, null=True, blank=True, verbose_name='库位1')
#     PartAddress2 = models.CharField(max_length=32, null=True, blank=True, verbose_name='库位2')
#     PartAddress3 = models.CharField(max_length=32, null=True, blank=True, verbose_name='库位3')
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'PartD'
#
#     def __str__(self):
#         return self.PartType

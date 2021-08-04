from django.db import models
from workstation.models.base_models import MySort, Files


class Company(models.Model):
    company_name = models.CharField(max_length=64, blank=True, null=True, verbose_name="公司")
    abbreviation = models.CharField(max_length=64, blank=True, null=True, verbose_name="公司简写")
    icon = models.ForeignKey(Files, models.DO_NOTHING, blank=True, null=True, verbose_name="图标")
    introduction = models.CharField(max_length=255, blank=True, null=True, verbose_name="公司介绍")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'company'
        index_together = ['company_name', 'abbreviation']

    def __str__(self):
        return self.company_name


class MyLocation(models.Model):
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True, verbose_name="公司")
    department = models.CharField(max_length=64, blank=True, null=True, verbose_name="部门")
    location_level_1 = models.CharField(max_length=32, blank=True, null=True, verbose_name="一级地点")
    location_level_2 = models.CharField(max_length=32, blank=True, null=True, verbose_name="二级地点")
    location_level_3 = models.CharField(max_length=32, blank=True, null=True, verbose_name="三级地点")
    location_level_4 = models.CharField(max_length=32, blank=True, null=True, verbose_name="四级地点")
    sort = models.ForeignKey(MySort, models.DO_NOTHING, blank=True, null=True, verbose_name="地点类型")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'mylocation'
        indexes = [models.Index(fields=['location_level_4'])]

    def __str__(self):
        return self.location_level_4

#
# class Place(models.Model):
#     Company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="公司")
#     Department = models.CharField(max_length=32, null=True, blank=True, default='PFH2B', verbose_name="部门")
#     Workshop = models.CharField(max_length=32, null=True, blank=True, verbose_name="车间")
#     WorkArea = models.CharField(max_length=32, null=True, blank=True, verbose_name="区域")  # 哪个区域：UB
#     ProductionLine = models.CharField(max_length=32, null=True, blank=True, verbose_name="线体")  # 哪个区域：UB2.1
#     Controller = models.CharField(max_length=32, null=True, blank=True, verbose_name="控制柜")
#     ControllerIP = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
#     WorkStation = models.CharField(max_length=16, null=True, blank=True, verbose_name="工位")  # 哪个工位：3210
#     PlacePicture = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="图片")
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'Place'
#
#     def __str__(self):
#         return self.WorkStation

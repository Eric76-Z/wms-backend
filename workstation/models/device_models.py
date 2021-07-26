from django.db import models
from workstation.models import MySort, Files, MyTag, MyLog
from workstation.models.location_models import MyLocation, Company


class DevicesType(models.Model):
    parameter_1 = models.CharField(max_length=32, null=True, blank=True, verbose_name='设备参数1')
    parameter_2 = models.CharField(max_length=32, null=True, blank=True, verbose_name='设备参数2')
    parameter_3 = models.CharField(max_length=32, null=True, blank=True, verbose_name='设备参数3')
    parameter_4 = models.CharField(max_length=32, null=True, blank=True, verbose_name='设备参数4')
    parameter_5 = models.CharField(max_length=32, null=True, blank=True, verbose_name='设备参数5')
    device_info = models.TextField(max_length=1024, null=True, blank=True, verbose_name='设备简介')
    material = models.ManyToManyField(Files, blank=True, verbose_name="设备资料")
    device_sort = models.ForeignKey(MySort, models.DO_NOTHING, blank=True, null=True, verbose_name="设备分类")
    brand = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True, verbose_name="品牌")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
    tag = models.ManyToManyField(MyTag, blank=True)

    class Meta:
        db_table = 'devicestype'
        indexes = [models.Index(fields=['parameter_1'])]

    def __str__(self):
        return self.parameter_1


class Robot(models.Model):
    location = models.ForeignKey(MyLocation, models.DO_NOTHING, blank=True, null=True, verbose_name="地点")
    robot_type = models.ForeignKey(DevicesType, models.DO_NOTHING, blank=True, null=True, verbose_name="机器人型号")
    robot_num = models.CharField(max_length=64, blank=True, null=True, verbose_name="机器人编号")
    robot_serial = models.CharField(max_length=32, blank=True, null=True, verbose_name="机器人序列号")
    technology = models.ForeignKey(MySort, models.DO_NOTHING, blank=True, null=True, verbose_name="机器人工艺")
    start_time = models.DateTimeField(blank=True, null=True, verbose_name="投入运行时间")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
    is_inuse = models.BooleanField(default=True, verbose_name="是否在用")
    project = models.CharField(max_length=64, blank=True, null=True, verbose_name="项目")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
    log = models.ManyToManyField(MyLog, blank=True)
    tag = models.ManyToManyField(MyTag, blank=True)

    class Meta:
        db_table = 'robot'
        indexes = [models.Index(fields=['robot_num'])]

    def __str__(self):
        return self.robot_num

class RobotE7(models.Model):
    location = models.ForeignKey(MyLocation, models.DO_NOTHING, blank=True, null=True, verbose_name="地点")
    robotE7_type = models.ForeignKey(DevicesType, models.DO_NOTHING, blank=True, null=True, verbose_name="7轴型号")
    robotE7_num = models.CharField(max_length=64, blank=True, null=True, verbose_name="机器人编号")
    robotE7_serial = models.CharField(max_length=32, blank=True, null=True, verbose_name="机器人序列号")
    # technology = models.ForeignKey(MySort, models.DO_NOTHING, related_name='technology_mysort', blank=True, null=True, verbose_name="7轴工艺")
    start_time = models.DateTimeField(blank=True, null=True, verbose_name="投入运行时间")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
    is_inuse = models.BooleanField(default=True, verbose_name="是否在用")
    project = models.CharField(max_length=64, blank=True, null=True, verbose_name="项目")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
    log = models.ManyToManyField(MyLog, blank=True)
    tag = models.ManyToManyField(MyTag, blank=True)

    class Meta:
        db_table = 'robotE7'

    def __str__(self):
        return self.robotE7_num


class WeldingGun(models.Model):
    location = models.ForeignKey(MyLocation, models.DO_NOTHING, blank=True, null=True, verbose_name="地点")
    weldinggun_type = models.ForeignKey(DevicesType, models.DO_NOTHING, blank=True, null=True, verbose_name="焊枪型号")
    weldinggun_num = models.CharField(max_length=64, blank=True, null=True, verbose_name="焊枪编号")
    weldinggun_serial = models.CharField(max_length=32, blank=True, null=True, verbose_name="焊枪序列号")
    technology = models.ForeignKey(MySort, models.DO_NOTHING, blank=True, null=True, verbose_name="焊枪工艺")
    start_time = models.DateTimeField(blank=True, null=True, verbose_name="投入运行时间")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
    tcp = models.ForeignKey(Files, models.CASCADE, blank=True, null=True, verbose_name="焊枪Tcp")
    is_inuse = models.BooleanField(default=True, verbose_name="是否在用")
    project = models.CharField(max_length=64, blank=True, null=True, verbose_name="项目")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
    log = models.ManyToManyField(MyLog, blank=True)
    tag = models.ManyToManyField(MyTag, blank=True)
    class Meta:
        db_table = 'weldinggun'
        indexes = [models.Index(fields=['weldinggun_num'])]

    def __str__(self):
        return self.weldinggun_num

class TipDresser(models.Model):
    location = models.ForeignKey(MyLocation, models.DO_NOTHING, blank=True, null=True, verbose_name="地点")
    tipdresser_type = models.ForeignKey(DevicesType, models.DO_NOTHING, blank=True, null=True, verbose_name="修磨器型号")
    tipdresser_num = models.CharField(max_length=64, blank=True, null=True, verbose_name="修磨器编号")
    tipdresser_serial = models.CharField(max_length=32, blank=True, null=True, verbose_name="修磨器序列号")
    # technology = models.ForeignKey(MySort, models.DO_NOTHING, related_name='technology_mysort', blank=True, null=True, verbose_name="修磨器工艺")
    start_time = models.DateTimeField(blank=True, null=True, verbose_name="投入运行时间")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
    is_inuse = models.BooleanField(default=True, verbose_name="是否在用")
    project = models.CharField(max_length=64, blank=True, null=True, verbose_name="项目")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
    log = models.ManyToManyField(MyLog, blank=True)
    tag = models.ManyToManyField(MyTag, blank=True)

    class Meta:
        db_table = 'tipdresser'
        indexes = [models.Index(fields=['tipdresser_num'])]

    def __str__(self):
        return self.tipdresser_num



# class RobotType(models.Model):
#     RobotType = models.CharField(max_length=32, verbose_name='机器人型号')
#     RobotSpec = models.CharField(max_length=32, null=True, blank=True, verbose_name='机器人规格')
#     RobotInfo = models.TextField(max_length=1024, null=True, blank=True, verbose_name='机器人简介')
#     RobotPart = models.ManyToManyField(Part, blank=True, verbose_name="机器人备件")
#     RobotPicture = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="机器人图片")
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'RobotType'
#
#     def __str__(self):
#         return self.RobotType
#
#
# class WeldingGunType(models.Model):
#     WeldingGunType = models.CharField(max_length=32, null=True, blank=True, verbose_name='焊枪类型')
#     WeldingGunSpec = models.CharField(max_length=32, null=True, blank=True, verbose_name='焊枪型号')
#     WeldingGunCode = models.CharField(max_length=32, null=True, blank=True, verbose_name='焊枪枪号')
#     WeldingGunFactor = models.DecimalField(max_digits=3, decimal_locations=2, null=True, blank=True, verbose_name="焊枪系数")
#     WeldingGunInfo = models.TextField(max_length=1024, null=True, blank=True, verbose_name='焊枪简介')
#     WeldingGunDrawing = models.FileField(null=True, blank=True, upload_to='Device/WeldingGun/WeldingGunDrawing', verbose_name="焊枪图纸")
#     WeldingGunPicture = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.SET_NULL,
#                                           verbose_name="焊枪图片")
#     WeldingGunPart = models.ManyToManyField(Part, blank=True, verbose_name="焊枪备件")
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'WeldingGunType'
#
#     def __str__(self):
#         return self.WeldingGunSpec
#
#
# class Robot(models.Model):
#     Place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="地点")
#     RobotType = models.ForeignKey(RobotType, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="机器人型号")
#     RobotNum = models.CharField(max_length=64, null=True, blank=True, verbose_name="机器人编号")
#     RobotSerial = models.CharField(max_length=64, null=True, blank=True, verbose_name="机器人序列号")
#     StartTime = models.DateTimeField(null=True, blank=True, verbose_name="投入使用时间")
#     RobotIP = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
#     RobotLog = models.TextField(max_length=1024, null=True, blank=True, verbose_name='机器人log')
#     RobotTechnique = models.CharField(max_length=32, null=True, blank=True, verbose_name="机器人工艺")
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'Robot'
#
#     def __str__(self):
#         return self.RobotNum
#
#
# class WeldingGun(models.Model):
#     Place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="地点")
#     WeldingGunID = models.CharField(max_length=64, null=True, blank=True, verbose_name="焊枪ID")
#     WeldingGunType = models.ForeignKey(WeldingGunType, null=True, blank=True, on_delete=models.SET_NULL,
#                                        verbose_name="焊枪型号")
#     WeldingGunNum = models.CharField(max_length=64, null=True, blank=True, verbose_name="焊机编号")
#     WeldingGunSerial = models.CharField(max_length=64, null=True, blank=True, verbose_name="焊枪序列号")
#     StartTime = models.DateTimeField(null=True, blank=True, verbose_name="投入使用时间")
#     WeldingGunIP = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
#     WeldingGunLog = models.TextField(max_length=1024, null=True, blank=True, verbose_name='焊枪log')
#     WeldingGunTechnique = models.CharField(max_length=32, null=True, blank=True, verbose_name="焊枪工艺")
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'WeldingGun'
#
#     def __str__(self):
#         return self.WeldingGunNum

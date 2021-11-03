import os
import uuid

from django.db import models

from myuser.models.user_models import UserProfile
from workstation.models.base_models import Files, Images, Articles
from workstation.models.device_models import WeldingGun, Robot
from workstation.models.parts_models import Parts


# 使用uuid创建唯一的图片名，并保存的路径和文件名一并返回
def evaluation_directory_path(product_id, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("evaluations", filename)


class BladeApply(models.Model):
    weldinggun = models.ForeignKey(WeldingGun, models.DO_NOTHING, blank=True, null=True, verbose_name="焊枪")
    bladetype_apply = models.ForeignKey(Parts, models.DO_NOTHING, related_name='apply_parts', blank=True, null=True,
                                        verbose_name="申请刀片类型")
    applicant = models.ForeignKey(UserProfile, models.DO_NOTHING, related_name='bladetype_applicant_myuser', blank=True,
                                  null=True,
                                  verbose_name="申请人")
    bladetype_received = models.ForeignKey(Parts, models.DO_NOTHING, related_name='received_parts', blank=True,
                                           null=True, verbose_name="领用刀片类型")
    receiver = models.ForeignKey(UserProfile, models.DO_NOTHING, related_name='bladetype_receiver_myuser', blank=True,
                                 null=True,
                                 verbose_name="领用人")
    cycle_num = models.IntegerField(blank=True, null=True, verbose_name="圈数")
    pressure = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name="压力")
    oldblade_img = models.ForeignKey(Images, models.CASCADE, related_name='oldblade_imgs', blank=True, null=True,
                                     verbose_name="在用刀片图")
    polestatus_img = models.ForeignKey(Images, models.CASCADE, related_name='polestatus_imgs', blank=True, null=True,
                                       verbose_name="电极帽状态")
    repair_order_num = models.IntegerField(blank=True, null=True, verbose_name="维修单号")
    repair_order_img = models.ForeignKey(Images, models.CASCADE, related_name='repairorder_imgs', blank=True, null=True,
                                         verbose_name="维修单图")
    order_status = models.IntegerField(blank=True, null=True, verbose_name="订单状态")
    order_comments = models.CharField(max_length=255, blank=True, null=True, verbose_name="订单备注")
    receive_time = models.DateTimeField(blank=True, null=True, verbose_name="领用时间")
    complete_time = models.DateTimeField(blank=True, null=True, verbose_name="完成时间")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'blade_apply'

    def __str__(self):
        return self.weldinggun.weldinggun_num


class WeldingGunClothes(models.Model):
    applicant = models.ForeignKey(UserProfile, models.DO_NOTHING, related_name='weldinggunclothes_applicant_myuser',
                                  blank=True, null=True,
                                  verbose_name="申请人")
    replacer = models.ForeignKey(UserProfile, models.DO_NOTHING, related_name='weldinggunclothes_replacer_myuser',
                                 blank=True, null=True, verbose_name="更换人")
    weldinggun = models.ForeignKey(WeldingGun, models.DO_NOTHING, blank=True, null=True, verbose_name="焊枪")
    reason_replace = models.CharField(max_length=255, blank=True, null=True, verbose_name="更换原因")
    is_replace = models.BooleanField(default=False, verbose_name="是否更换")
    order_status = models.IntegerField(blank=True, null=True, verbose_name="订单状态")
    order_comments = models.CharField(max_length=255, blank=True, null=True, verbose_name="订单备注")
    receive_time = models.DateTimeField(blank=True, null=True, verbose_name="领用时间")
    complete_time = models.DateTimeField(blank=True, null=True, verbose_name="完成时间")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'weldinggun_clothes'

    def __str__(self):
        return self.weldinggun.weldinggun_num


class WeldingGunDamage(models.Model):
    applicant = models.ForeignKey(UserProfile, models.DO_NOTHING, related_name='weldinggundamage_applicant_myuser',
                                  blank=True, null=True,
                                  verbose_name="申请人")
    confirmer = models.ForeignKey(UserProfile, models.DO_NOTHING, related_name='weldinggundamage_confirmer_myuser',
                                  blank=True, null=True,
                                  verbose_name="确认人")
    weldinggun = models.ForeignKey(WeldingGun, models.DO_NOTHING, blank=True, null=True, verbose_name="焊枪")
    damage_part = models.CharField(max_length=255, blank=True, null=True, verbose_name="损坏部件")
    reason = models.IntegerField(blank=True, null=True, verbose_name="故障原因")
    to_replace = models.CharField(max_length=32, blank=True, null=True, verbose_name="待换备件")
    order_status = models.IntegerField(blank=True, null=True, verbose_name="订单状态")
    order_comments = models.CharField(max_length=255, blank=True, null=True, verbose_name="订单备注")
    is_complete = models.BooleanField(default=False, verbose_name="是否完成")
    complete_time = models.DateTimeField(blank=True, null=True, verbose_name="完成时间")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'weldinggun_damage'

    def __str__(self):
        return self.weldinggun.weldinggun_num


class MaintenanceRecords(models.Model):
    applicant = models.ForeignKey(UserProfile, models.DO_NOTHING, related_name='maintenancerecords_applicant_myuser',
                                  blank=True, null=True,
                                  verbose_name="上传人")
    inductor = models.ForeignKey(UserProfile, models.DO_NOTHING, related_name='maintenancerecords_inductor_myuser',
                                 blank=True, null=True,
                                 verbose_name="归纳人")
    maintenance_worker = models.ManyToManyField(UserProfile, blank=True, verbose_name="维修人员")
    sort = models.CharField(max_length=32, blank=True, null=True, verbose_name="故障类型")  # 设备故障、高频故障
    device_type = models.CharField(max_length=32, blank=True, null=True, verbose_name="设备")
    workstation = models.CharField(max_length=32, blank=True, null=True, verbose_name="工位")
    localLv1 = models.CharField(max_length=16, blank=True, null=True, verbose_name="一级地点")
    localLv2 = models.CharField(max_length=16, blank=True, null=True, verbose_name="二级地点")
    localLv3 = models.CharField(max_length=16, blank=True, null=True, verbose_name="三级地点")
    car_model = models.CharField(max_length=32, blank=True, null=True, verbose_name="车型")
    maintenance_record = models.TextField(blank=True, null=True, verbose_name="维修记录")
    need_summary = models.BooleanField(default=0, verbose_name="是否需要总结")
    experience_summary = models.ForeignKey(Articles, on_delete=models.SET_NULL, blank=True, null=True,
                                           verbose_name="经验总结")
    order_comments = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注")
    start_time = models.DateTimeField(blank=True, null=True, verbose_name="开始时间")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="结束时间")
    duration = models.IntegerField(blank=True, null=True, verbose_name="持续时间")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
    maintenance_status = models.IntegerField(blank=True, null=True, verbose_name="故障状态",
                                             choices=((1, '完全修复'), (2, '临时修复')))
    order_status = models.IntegerField(blank=True, null=True, verbose_name="订单状态")

    class Meta:
        db_table = 'maintenance_records'

    def __str__(self):
        return self.workstation


class EmsMaintenanceRecords(models.Model):
    applicant = models.ForeignKey(UserProfile, models.DO_NOTHING, related_name='emsmaintenancerecords_applicant_myuser',
                                  blank=True, null=True,
                                  verbose_name="上传人")
    localLv1 = models.CharField(max_length=16, blank=True, null=True, verbose_name="一级地点")
    localLv2 = models.CharField(max_length=16, blank=True, null=True, verbose_name="二级地点")
    localLv3 = models.CharField(max_length=16, blank=True, null=True, verbose_name="三级地点")
    car_model = models.CharField(max_length=32, blank=True, null=True, verbose_name="车型")
    ng_car = models.IntegerField(blank=True, null=True, verbose_name="NG小车")
    maintenance_record = models.TextField(blank=True, null=True, verbose_name="维修记录")
    order_comments = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注")
    closing_date = models.DateField( blank=True, null=True, verbose_name="节点")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
    order_status = models.IntegerField(blank=True, null=True, verbose_name="订单状态")

    class Meta:
        db_table = 'emsmaintenance_records'

    def __str__(self):
        return self.ng_car

# class WeldinggunTcp(models.Model):
#     uploader = models.ForeignKey(MyUser, models.DO_NOTHING, blank=True, null=True, verbose_name="上传人")
#     weldinggun = models.ForeignKey(Weldinggun, models.DO_NOTHING, blank=True, null=True, verbose_name="焊枪")
#     reason_replace = models.CharField(max_length=255, blank=True, null=True, verbose_name="故障原因")
#     order_status = models.IntegerField(blank=True, null=True, verbose_name="订单状态")
#     order_comments = models.CharField(max_length=255, blank=True, null=True, verbose_name="订单备注")
#     is_complete = models.BooleanField(default=False, verbose_name="是否完成")
#     complete_time = models.DateTimeField(blank=True, null=True, verbose_name="完成时间")
#     create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
#     update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'weldinggun_tcp'
#
#     def __str__(self):
#         return self.weldinggun.weldinggun_num

# class BladeConsuming(models.Model):
#     sid = models.IntegerField(auto_created=True, default='0')
#     Place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="地点")
#     # UseArea = models.CharField(max_length=32, verbose_name="领用区域")
#     # UseProductionLine = models.CharField(max_length=32, verbose_name="领用线体")
#     UseSK = models.ForeignKey(WeldingGun, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="焊接控制柜编号")
#     Applicant = models.CharField(max_length=32, null=True, blank=True, verbose_name="申请人")
#     Recipients = models.CharField(max_length=32, null=True, blank=True, verbose_name="领用人")
#     BladeTypeApply = models.CharField(max_length=32, null=True, blank=True, verbose_name="申请刀片")
#     BladeTypeReceived = models.CharField(max_length=32, null=True, blank=True, verbose_name="已领刀片")
#     CycleNum = models.IntegerField(null=True, blank=True, verbose_name="修磨圈数")
#     Pressure = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name="修磨压力")
#     OldBladePicture = models.FileField(null=True, blank=True, upload_to='Blade/OldBlade/', verbose_name="旧刀片图片")
#     PoleStatus = models.FileField(null=True, blank=True, upload_to='Blade/PoleStatus/', verbose_name="修磨后电极杆状态")
#     RepairOrderNum = models.IntegerField(null=True, blank=True, verbose_name="维修单编号")
#     RepairOrderPicture = models.FileField(null=True, blank=True, upload_to='Blade/RepairOrder/', verbose_name="维修单图片")
#     OlderStatus = models.IntegerField(null=True, blank=True, verbose_name='订单状态')
#     OlderComments = models.CharField(max_length=128, null=True, blank=True, verbose_name="状态备注")
#     UseTime = models.DateTimeField(null=True, blank=True, verbose_name="领用时间")
#     CompleteTime = models.DateTimeField(null=True, blank=True, verbose_name="完成时间")
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'BladeConsuming'
#
#
#
#
# class WeldingGunCylinderLog(models.Model):
#     sid = models.IntegerField(auto_created=True, default='0')
#     Place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="地点")
#     UseSK = models.ForeignKey(WeldingGun, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="焊接控制柜编号")
#     Declarant = models.CharField(max_length=32, null=True, blank=True, verbose_name="申报人")
#     DeclarTime = models.DateTimeField(null=True, blank=True, verbose_name="申报时间")
#     TargetValue = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="气缸目标值")
#     ActualValue = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="气缸实际值")
#     TestTime = models.CharField(max_length=32, null=True, blank=True, verbose_name="测试时间")
#     ReasonReplace = models.CharField(max_length=128, null=True, blank=True, verbose_name="更换原因")
#     is_replace = models.BooleanField(default=False)
#     Replacer = models.CharField(max_length=32, null=True, blank=True, verbose_name="更换人")
#     CompleteTime = models.DateTimeField(null=True, blank=True, verbose_name="完成时间")
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'WeldingGunCylinderLog'
#
#
# class WeldingGunClothesLog(models.Model):
#     sid = models.IntegerField(auto_created=True, default='0')
#     Place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="地点")
#     UseSK = models.ForeignKey(WeldingGun, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="焊接控制柜编号")
#     Declarant = models.CharField(max_length=32, null=True, blank=True, verbose_name="申报人")
#     DeclarTime = models.DateTimeField(null=True, blank=True, verbose_name="申报时间")
#     ReasonReplace = models.CharField(max_length=128, null=True, blank=True, verbose_name="更换原因")
#     ClothesDamagePicture = models.FileField(null=True, blank=True, upload_to='WeldingGunClothes/ClothesDamage/',
#                                             verbose_name="破损枪衣图")
#     NakedWeldingGun = models.FileField(null=True, blank=True, upload_to='WeldingGunClothes/NakedWeldingGun/',
#                                        verbose_name="裸枪图")
#     is_replace = models.BooleanField(default=False)
#     ClothesRecoverPicture = models.FileField(null=True, blank=True, upload_to='WeldingGunClothes/ClothesRecover/',
#                                              verbose_name="复原枪衣图")
#     Replacer = models.CharField(max_length=32, null=True, blank=True, verbose_name="更换人")
#     OlderStatus = models.IntegerField(null=True, blank=True, verbose_name='订单状态')
#     OlderComments = models.CharField(max_length=128, null=True, blank=True, verbose_name="状态备注")
#     CompleteTime = models.DateTimeField(null=True, blank=True, verbose_name="完成时间")
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#
#     class Meta:
#         db_table = 'WeldingGunClothesLog'
#
# class WeldingGunTCP(models.Model):
#     Place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="地点")
#     UseSK = models.ForeignKey(WeldingGun, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="焊接控制柜编号")
#     Uploader = models.CharField(max_length=32, null=True, blank=True, verbose_name="上传人")
#     UploadTime = models.DateTimeField(null=True, blank=True, verbose_name="上传时间")
#     WeldingGunTcpPicture = models.FileField(null=True, blank=True, upload_to='TCP/WeldingGunTCP',
#                                             verbose_name="TCP图")
#     OlderStatus = models.IntegerField(null=True, blank=True, verbose_name='订单状态')
#     OlderComments = models.CharField(max_length=128, null=True, blank=True, verbose_name="状态备注")
#     is_complete = models.BooleanField(default=False)
#     CreateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
#     UpdateTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="更新时间")
#     class Meta:
#         db_table = 'WeldingGunTCP'
#

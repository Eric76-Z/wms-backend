import xadmin
from myuser.models import UserProfile
from workstation import models
from workstation.models import WeldingGun, MyLocation, Parts, MaintenanceRecords
from xadmin import views
from xadmin.filters import MultiSelectFieldListFilter

class GlobalSiteSetting(object):
    # 设置后台顶部标题
    site_title = '修修'
    # 设置后台底部标题
    site_footer = 'xiuxiu.work'
    # 设置可折叠
    menu_style = 'accordion'


# 启用主题管理器
class BaseXadminSetting(object):
    enable_themes = True
    # 使用主题
    use_bootswatch = True


# 配置图标
class SafeAdmin(object):
    model_icon = 'fa fa-key'


# 注册
xadmin.site.register(views.CommAdminView, GlobalSiteSetting)
xadmin.site.register(views.BaseAdminView, BaseXadminSetting)


@xadmin.sites.register(models.MySort)
class MySortAdmin(object):
    list_display = ['id', 'type_name', 'f_type_id', 'type_layer']
    list_filter = ['f_type_id', 'type_layer']
    search_fields = ['type_name', 'type_layer']
    ordering = ['id']
    list_per_page = 25


@xadmin.sites.register(models.Company)
class CompanyAdmin(object):
    list_display = ['id', 'company_name', 'abbreviation', 'introduction']
    search_fields = ['company_name', 'abbreviation']
    ordering = ['id']
    list_per_page = 25


@xadmin.sites.register(models.MyLocation)
class MyLocationAdmin(object):
    list_display = ['id', 'company', 'department', 'location_level_1', 'location_level_2', 'location_level_3',
                    'location_level_4', 'sort']
    list_filter = ['location_level_1', 'location_level_3', 'location_level_4']
    search_fields = ['location_level_1', 'location_level_3', 'location_level_4']
    ordering = ['id']
    list_per_page = 25


@xadmin.sites.register(models.Parts)
class PartsAdmin(object):
    list_display = ['id', 'part_num', 'my_spec', 'order_num', 'price', 'brand', 'cordon', 'min_line', 'unit', 'mark',
                    'usefor', 'sort']
    list_filter = ['brand', 'sort']
    search_fields = ['id', 'part_num', 'my_spec', 'setech_spec', 'order_num', 'mark']
    ordering = ['id']
    list_per_page = 25


@xadmin.sites.register(models.Stock)
class StockAdmin(object):

    def PartNum(self, obj):
        return obj.part.part_num

    def Unit(self, obj):
        return obj.part.unit

    def Area(self, obj):
        return obj.location.location_level_1

    PartNum.short_description = u'物料号'
    Unit.short_description = u'单位'
    Area.short_description = u'基地'

    list_display = ['id', 'PartNum', 'part', 'part_stock', 'Unit', 'Area', 'location', 'applicant', 'comment']
    list_filter = ['location']
    search_fields = ['part__part_num', 'location__location_level_1', 'location__location_level_4']
    ordering = ['id']
    list_per_page = 25


@xadmin.sites.register(models.DevicesType)
class DevicesTypeAdmin(object):
    list_display = ['id', 'parameter_1', 'parameter_2', 'parameter_3', 'parameter_4', 'parameter_5', 'device_info',
                    'material', 'device_sort', 'brand']
    list_filter = ['device_sort', 'brand']
    search_fields = ['parameter_1', 'parameter_2']
    ordering = ['id']
    list_per_page = 25


@xadmin.sites.register(models.Robot)
class RobotAdmin(object):
    def Department(self, obj):
        return obj.location.department

    def Workshop(self, obj):
        return obj.location.location_level_1

    def WorkArea(self, obj):
        return obj.location.location_level_2

    def ProductionLine(self, obj):
        return obj.location.location_level_3

    Department.short_description = u'部门'
    Workshop.short_description = u'车间'
    WorkArea.short_description = u'区域'
    ProductionLine.short_description = u'线体'

    list_display = ['id', 'Department', 'Workshop', 'WorkArea', 'ProductionLine', 'robot_num', 'robot_type',
                    'technology', 'start_time', 'is_inuse', 'project']
    list_filter = (('location__location_level_1', MultiSelectFieldListFilter),
                   ('location__location_level_2', MultiSelectFieldListFilter),
                   'location__location_level_3',)
    search_fields = ['location__location_level_2', 'location__location_level_3', 'robot', 'technology']
    ordering = ['id']
    list_per_page = 25


@xadmin.sites.register(models.WeldingGun)
class WeldingGunAdmin(object):
    def Department(self, obj):
        return obj.location.department

    def Workshop(self, obj):
        return obj.location.location_level_1

    def WorkArea(self, obj):
        return obj.location.location_level_2

    def ProductionLine(self, obj):
        return obj.location.location_level_3

    Department.short_description = u'部门'
    Workshop.short_description = u'车间'
    WorkArea.short_description = u'区域'
    ProductionLine.short_description = u'线体'

    list_display = ['id', 'Department', 'Workshop', 'WorkArea', 'ProductionLine', 'weldinggun_num', 'weldinggun_type',
                    'technology', 'project', 'is_inuse']
    list_filter = (('location__location_level_1', MultiSelectFieldListFilter),
                   ('location__location_level_2', MultiSelectFieldListFilter),
                   'location__location_level_3',)
    search_fields = ['weldinggun_num', 'weldinggun_type__parameter_1']
    ordering = ['id']
    list_per_page = 25


@xadmin.sites.register(models.BladeApply)
class BladeApplyAdmin(object):

    # def getLocation(self, obj):
    #     Workshop = MyLocation.objects.get(id=obj.weldinggun.place_id)
    #     return Workshop.location_level_1

    # # location = getLocation(se)
    # getLocation[0].short_description = u'部门'
    # Workshop.short_description = u'车间'
    # WorkArea.short_description = u'区域'
    # ProductionLine.short_description = u'线体'

    # def BladeTypeApply(self, obj):
    #     spec = obj.bladetype_apply.my_spec
    #     spec = spec.split('|', 1)
    #     return spec[0]
    # def BladeTypeReceived(self, obj):
    #     spec = obj.bladetype_received.my_spec
    #     spec = spec.split('|', 1)
    #     return spec[0]
    # BladeTypeApply.short_description = u'申请型号'
    # BladeTypeReceived.short_description = u'领取型号'
    # 'BladeTypeApply', 'BladeTypeReceived',
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "bladetype_apply" or db_field.name == "bladetype_received":
            kwargs["queryset"] = Parts.objects.filter(tag=1).order_by("id")
        # else:
        #     kwargs["queryset"] = Parts.objects.all()
        # return super(BladeApplyAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        attrs = self.get_field_attrs(db_field, **kwargs)
        return db_field.formfield(**dict(attrs, **kwargs))
        # return db_field.formfield(**dict(**kwargs))

    list_display = ['id', 'bladetype_apply', 'applicant', 'bladetype_received', 'receiver', 'weldinggun', 'cycle_num',
                    'pressure', 'repair_order_num', 'order_status', 'order_comments']
    list_filter = [('bladetype_received__my_spec', MultiSelectFieldListFilter), 'order_status']
    search_fields = ['weldinggun__weldinggun_num']
    relfield_style = 'fk-ajax'
    ordering = ['-id']
    list_per_page = 25

@xadmin.sites.register(models.MaintenanceRecords)
class MaintenanceRecordsAdmin(object):

    # def getLocation(self, obj):
    #     Workshop = MyLocation.objects.get(id=obj.weldinggun.place_id)
    #     return Workshop.location_level_1

    # # location = getLocation(se)
    # getLocation[0].short_description = u'部门'
    # Workshop.short_description = u'车间'
    # WorkArea.short_description = u'区域'
    # ProductionLine.short_description = u'线体'

    # def BladeTypeApply(self, obj):
    #     spec = obj.bladetype_apply.my_spec
    #     spec = spec.split('|', 1)
    #     return spec[0]
    # def BladeTypeReceived(self, obj):
    #     spec = obj.bladetype_received.my_spec
    #     spec = spec.split('|', 1)
    #     return spec[0]
    # BladeTypeApply.short_description = u'申请型号'
    # BladeTypeReceived.short_description = u'领取型号'
    # 'BladeTypeApply', 'BladeTypeReceived',
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "bladetype_apply" or db_field.name == "bladetype_received":
            kwargs["queryset"] = Parts.objects.filter(tag=1).order_by("id")
        # else:
        #     kwargs["queryset"] = Parts.objects.all()
        # return super(BladeApplyAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        attrs = self.get_field_attrs(db_field, **kwargs)
        return db_field.formfield(**dict(attrs, **kwargs))
        # return db_field.formfield(**dict(**kwargs))

    list_display = ['id', 'maintenance_worker', 'rob', 'car_model', 'start_time', 'end_time', 'maintenance_record',
                    'experience_summary', 'order_comments']
    list_filter = ['rob',]
    search_fields = ['rob__rob_num']
    relfield_style = 'fk-ajax'
    ordering = ['-id']
    list_per_page = 25


@xadmin.sites.register(models.WeldingGunClothes)
class WeldingGunClothesAdmin(object):
    # def getLocation(self, obj):
    #     Workshop = MyLocation.objects.get(id=obj.weldinggun.place_id)
    #     return Workshop.location_level_1

    # # location = getLocation(se)
    # getLocation[0].short_description = u'部门'
    # Workshop.short_description = u'车间'
    # WorkArea.short_description = u'区域'
    # ProductionLine.short_description = u'线体'

    list_display = ['id', 'applicant', 'replacer', 'weldinggun', 'reason_replace', 'is_replace', 'order_status',
                    'order_comments', 'receive_time']
    # list_filter = []
    search_fields = ['weldinggun']
    ordering = ['-id']
    list_per_page = 25


@xadmin.sites.register(models.MyTag)
class MyTagAdmin(object):
    list_display = ['id', 'tag_name', 'create_time', 'update_time']
    list_filter = ['tag_name']
    search_fields = ['tag_name']
    ordering = ['-id']
    list_per_page = 25


@xadmin.sites.register(models.Files)
class MyFilesAdmin(object):
    list_display = ['id', 'file_name', 'myfile', 'sort', 'create_time', 'update_time']
    list_filter = ['file_name']
    search_fields = ['file_name']
    ordering = ['-id']
    list_per_page = 25

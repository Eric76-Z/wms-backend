from django.db import models


class PermissionType(models.Model):
    permission_type = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'permission_type'
        indexes = [models.Index(fields=['permission_type'])]


class FunctionOperation(models.Model):
    permission = models.ManyToManyField(PermissionType, blank=True, verbose_name="权限")
    operation_name = models.CharField(max_length=64)
    operation_code = models.CharField(max_length=64, blank=True, null=True)
    url_prefix = models.CharField(max_length=64, blank=True, null=True)  # Field name made lowercase.
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'function_operation'
        # indexes = [models.Index(fields=['operation_name'])]


class Menu(models.Model):
    permission = models.ManyToManyField(PermissionType, blank=True, verbose_name="权限")
    menu_name = models.CharField(max_length=32)
    menu_url = models.CharField(db_column='menu_URL', max_length=64, blank=True, null=True)  # Field name made lowercase.
    f_menu_id = models.IntegerField(blank=True, null=True, verbose_name="父菜单id")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'menu'
        # indexes = [models.Index(fields=['menu_name'])]


class PageElement(models.Model):
    permission = models.ManyToManyField(PermissionType, blank=True, verbose_name="权限")
    element_code = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'page_element'
        # indexes = [models.Index(fields=['element_code'])]

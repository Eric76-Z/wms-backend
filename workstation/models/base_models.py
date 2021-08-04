from django.db import models
from workstation.models import PermissionType
from utils.utils import FilePath


class MySort(models.Model):
    type_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='分类名')
    f_type_id = models.IntegerField(blank=True, null=True, verbose_name='父分类')
    type_layer = models.TextField(blank=True, null=True, verbose_name='层级')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'sort'

    def __str__(self):
        return self.type_name


class Files(models.Model):
    permission = models.ManyToManyField(PermissionType, blank=True, verbose_name="权限")
    file_name = models.CharField(max_length=64, verbose_name='文件名')
    myfile = models.FileField(null=True, blank=True, upload_to=FilePath, verbose_name="文件路径")
    sort = models.ForeignKey(MySort, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='分类')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'files'

    def __str__(self):
        return self.file_name


class Images(models.Model):
    permission = models.ManyToManyField(PermissionType, blank=True, verbose_name="权限")
    img_name = models.CharField(max_length=64, verbose_name='图片名')
    img = models.ImageField(null=True, blank=True, upload_to=FilePath,  verbose_name="图片")
    sort = models.ForeignKey(MySort, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='分类')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'Images'

    def __str__(self):
        return self.img_name


class MyLog(models.Model):
    log = models.CharField(max_length=255)
    sort = models.ForeignKey(MySort, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='分类')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'log'
        indexes = [models.Index(fields=['log'])]

    def __str__(self):
        return self.log


class MyTag(models.Model):
    tag_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='标签名')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'tag'
        indexes = [models.Index(fields=['tag_name'])]

    def __str__(self):
        return self.tag_name

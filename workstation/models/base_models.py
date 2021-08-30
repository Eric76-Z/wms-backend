from datetime import datetime

from django.db import models

from myuser.models import UserProfile
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
    img = models.ImageField(null=True, blank=True, upload_to=FilePath, verbose_name="图片")
    sort = models.ForeignKey(MySort, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='分类')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = 'images'

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


class Articles(models.Model):
    main_author = models.ForeignKey(UserProfile, related_name='main_author', on_delete=models.SET_NULL, blank=True,
                                    null=True,
                                    verbose_name="第一作者")
    authors = models.ManyToManyField(UserProfile, related_name='authors', blank=True, verbose_name="作者")
    title = models.CharField(max_length=64, verbose_name="标题")
    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()
    sort = models.ForeignKey(MySort, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="分类")
    log = models.ManyToManyField(MyLog, blank=True, verbose_name="日志")
    tag = models.ManyToManyField(MyTag, blank=True, verbose_name="标签")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        db_table = 'articles'
        ordering = ('-create_time',)

    def __str__(self):
        return self.title


class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10,
                                 choices=(("register", "注册"), ("forget", "找回密码"), ("reset", "重置密码")))
    send_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")

    class Meta:
        db_table = "emailcode"

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)

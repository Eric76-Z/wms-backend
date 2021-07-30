from django.contrib.auth.models import AbstractUser
from django.db import models
# from workstation.models.base_models import MyLog, MyTag, Files
# from workstation.models.permission_models import PermissionType
# from xadmin.plugins.auth import User


# class UserGroup(models.Model):
#     user_groupname = models.CharField(max_length=32, blank=True, null=True)
#     f_groupname_id = models.IntegerField(blank=True, null=True)
#     layer = models.IntegerField(blank=True, null=True)
#     create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
#     update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
#     log = models.ManyToManyField(MyLog, blank=True)
#     tag = models.ManyToManyField(MyTag, blank=True)
#
#     class Meta:
#         db_table = 'user_group'
#
#     def __str__(self):
#         return self.user_groupname
#
# class UserRole(models.Model):
#     permission = models.ManyToManyField(PermissionType, blank=True, verbose_name="权限")
#     rolename = models.CharField(max_length=32, blank=True, null=True)
#     create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
#     update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
#     log = models.ManyToManyField(MyLog, blank=True)
#     tag = models.ManyToManyField(MyTag, blank=True)
#
#     class Meta:
#         db_table = 'user_role'
#
#     def __str__(self):
#         return self.rolename


class UserProfile(AbstractUser):
    # myuser = models.OneToOneField(User,  on_delete=models.CASCADE, null= True, blank=True)
    # group = models.ManyToManyField(UserGroup1, blank=True, verbose_name="组名")
    # role = models.ManyToManyField(UserRole1, blank=True, verbose_name="角色")
    # realname = models.CharField(max_length=20, blank=True, null=True, verbose_name="真实姓名")
    # username = models.CharField(max_length=20, blank=True, null=True, verbose_name="昵称")
    # password = models.CharField(max_length=32, blank=True, null=True)
    phonenum = models.CharField(max_length=11, blank=True, null=True, verbose_name="手机号")
    worknum = models.IntegerField(blank=True, null=True, verbose_name="工号")
    # email = models.CharField(max_length=32, blank=True, null=True)
    # profile = models.ForeignKey(Files, models.CASCADE, blank=True, null=True, verbose_name="头像")
    is_onwork = models.BooleanField(default=False, verbose_name="是否在岗")
    # is_online = models.BooleanField(default=False, verbose_name="是否在线")
    is_delete = models.BooleanField(default=False, verbose_name="是否离职")
    # last_login = models.DateTimeField(blank=True, null=True, verbose_name="上次登陆")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="更新时间")
    # log = models.ManyToManyField(MyLog, blank=True)
    # tag = models.ManyToManyField(MyTag, blank=True)

    # class Meta:
    #     db_table = 'my_user'

    def __str__(self):
        return self.last_name + self.first_name
    def full_name(self):
        return self.last_name + self.first_name


#
# # class MyuserUsergroup(models.Model):
# #     my_user = models.ForeignKey(MyUser, models.DO_NOTHING, blank=True, null=True)
# #     user_group = models.ForeignKey(UserGroup, models.DO_NOTHING, blank=True, null=True)
# #
# #     class Meta:
# #         managed = False
# #         db_table = 'myuser_usergroup'
# #
# #
# # class MyuserUserrole(models.Model):
# #     my_user = models.ForeignKey(MyUser, models.DO_NOTHING, blank=True, null=True)
# #     userrole = models.ForeignKey(UserRole, models.DO_NOTHING, blank=True, null=True)
# #
# #     class Meta:
# #         managed = False
# #         db_table = 'myuser_userrole'
# #
# #
# # class UsergroupUserrole(models.Model):
# #     user_group = models.ForeignKey(UserGroup, models.DO_NOTHING, blank=True, null=True)
# #     userroler = models.ForeignKey(UserRole, models.DO_NOTHING, blank=True, null=True)
# #
# #     class Meta:
# #         managed = False
# #         db_table = 'usergroup_userrole'
#
#
#

# Generated by Django 3.2.5 on 2021-08-30 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workstation', '0009_rename_user_parts_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('send_type', models.CharField(choices=[('register', '注册'), ('forget', '找回密码')], max_length=10, verbose_name='验证码类型')),
                ('send_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
            ],
            options={
                'db_table': '邮箱验证码',
            },
        ),
    ]

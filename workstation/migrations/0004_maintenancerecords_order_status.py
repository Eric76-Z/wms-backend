# Generated by Django 3.2.5 on 2021-08-07 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workstation', '0003_auto_20210807_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancerecords',
            name='order_status',
            field=models.IntegerField(blank=True, null=True, verbose_name='订单状态'),
        ),
    ]

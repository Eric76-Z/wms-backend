# Generated by Django 3.2.5 on 2021-11-03 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workstation', '0007_alter_emsmaintenancerecords_closing_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emsmaintenancerecords',
            name='closing_date',
            field=models.DateField(blank=True, null=True, verbose_name='节点'),
        ),
    ]

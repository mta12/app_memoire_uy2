# Generated by Django 3.0.6 on 2020-06-16 09:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200616_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Date de Publication '),
        ),
    ]
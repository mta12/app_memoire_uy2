# Generated by Django 3.0.6 on 2020-06-12 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200612_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='Date de Publication '),
        ),
    ]

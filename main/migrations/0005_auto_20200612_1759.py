# Generated by Django 3.0.6 on 2020-06-12 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200610_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='note_soutenance',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
    ]

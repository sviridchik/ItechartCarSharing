# Generated by Django 3.2.5 on 2021-08-18 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210818_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('free', 'free'), ('booked', 'booked')], max_length=255),
        ),
    ]

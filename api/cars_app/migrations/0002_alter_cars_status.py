# Generated by Django 3.2.5 on 2021-10-08 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='status',
            field=models.CharField(choices=[('free', 'free'), ('active', 'active'), ('booked', 'booked'), ('unavaliable', 'unavaliable')], max_length=255),
        ),
    ]

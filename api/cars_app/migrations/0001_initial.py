# Generated by Django 3.2.5 on 2021-10-06 07:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('class_cars', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.TimeField(auto_now_add=True)),
                ('updated_at', models.TimeField(auto_now=True)),
                ('level_consumption', models.IntegerField()),
                ('mark', models.CharField(choices=[('Mercedes-Benz', 'Mercedes-Benz'), ('Toyota', 'Toyota'), ('Honda', 'Honda')], max_length=255)),
                ('reg_number', models.CharField(max_length=255)),
                ('color', models.CharField(choices=[('y', 'yellow'), ('w', 'white'), ('g', 'green')], max_length=255)),
                ('year', models.IntegerField()),
                ('latitude', models.FloatField(blank=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('free', 'free'), ('booked', 'booked')], max_length=255)),
                ('longitude', models.FloatField(blank=True)),
                ('car_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='class_cars.classcar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ViewedCars',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.TimeField(auto_now_add=True)),
                ('updated_at', models.TimeField(auto_now=True)),
                ('price_day', models.IntegerField()),
                ('price_night', models.IntegerField()),
                ('booking_price', models.IntegerField()),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars_app.cars')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
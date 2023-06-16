# Generated by Django 4.1.7 on 2023-04-01 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('face_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('job', models.CharField(max_length=15)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=20)),
                ('bio', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='profile_image')),
            ],
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-30 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=70)),
                ('password', models.CharField(max_length=70)),
                ('checkbox', models.CharField(max_length=70)),
            ],
        ),
        migrations.RenameModel(
            old_name='user',
            new_name='user1',
        ),
    ]

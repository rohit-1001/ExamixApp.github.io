# Generated by Django 4.2 on 2023-05-09 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0010_result_actual_result_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='marks',
            name='quiz_status',
            field=models.CharField(default='Successful', max_length=50),
            preserve_default=False,
        ),
    ]
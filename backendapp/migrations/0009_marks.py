# Generated by Django 4.2 on 2023-04-25 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0008_result_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.IntegerField()),
                ('quizid', models.IntegerField()),
                ('quiz_desc', models.CharField(max_length=400)),
                ('marks', models.IntegerField()),
            ],
        ),
    ]

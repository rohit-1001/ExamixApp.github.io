# Generated by Django 4.1.7 on 2023-04-08 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0006_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quizid', models.IntegerField()),
                ('question_no', models.IntegerField()),
                ('result', models.IntegerField()),
            ],
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-04 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0005_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quizid', models.IntegerField()),
                ('quiz_desc', models.CharField(max_length=400)),
                ('question_no', models.IntegerField()),
                ('question', models.CharField(max_length=400)),
                ('option1', models.CharField(max_length=400)),
                ('option2', models.CharField(max_length=400)),
                ('option3', models.CharField(max_length=400)),
                ('option4', models.CharField(max_length=400)),
                ('answer', models.IntegerField()),
            ],
        ),
    ]
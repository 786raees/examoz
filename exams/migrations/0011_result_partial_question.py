# Generated by Django 3.2 on 2022-06-18 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0010_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='partial_question',
            field=models.ManyToManyField(related_name='partial_question', to='exams.Question'),
        ),
    ]
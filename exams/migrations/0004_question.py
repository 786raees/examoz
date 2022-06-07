# Generated by Django 3.2 on 2022-06-07 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0003_auto_20220607_0214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(blank=True, choices=[('Multiple Choices (choose one)', 'Multiple Choices (choose one)'), ('Multiple Choices (choose many)', 'Multiple Choices (choose many)'), ('True/False', 'True/False'), ('Matching', 'Matching'), ('Fill in the blank', 'Fill in the blank'), ('Essay', 'Essay')], max_length=30, null=True)),
            ],
        ),
    ]

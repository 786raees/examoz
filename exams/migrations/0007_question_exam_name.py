# Generated by Django 3.2 on 2022-06-11 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0006_answer_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='exam_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exam_daata', to='exams.exam'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.2 on 2022-06-14 16:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0008_exam_is_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]

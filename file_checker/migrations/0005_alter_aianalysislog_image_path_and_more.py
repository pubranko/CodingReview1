# Generated by Django 4.2 on 2024-03-09 14:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('file_checker', '0004_aianalysislog_request_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aianalysislog',
            name='image_path',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='aianalysislog',
            name='request_timestamp',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='aianalysislog',
            name='response_timestamp',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='aianalysislog',
            name='success',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

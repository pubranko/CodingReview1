import uuid

from django.db import models
from datetime import datetime

from django.core.validators import MaxValueValidator
from django.utils import timezone

class AiAnalysisLog(models.Model):
    id = models.AutoField(
        null=False, primary_key=True)
    image_path = models.CharField(
        max_length=255, default=None, blank=False, null=True)
    success = models.BooleanField(
        default=False, blank=True, null=False)
    message = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    class_field = models.IntegerField(
        default=None, blank=True, null=True,)
    confidence = models.DecimalField(
        max_digits=5, decimal_places=4, default=None, blank=True, null=True)
    request_timestamp = models.DateTimeField(
        default=timezone.now, blank=True, null=False)
    response_timestamp = models.DateTimeField(
        default=timezone.now, blank=True, null=True)

    class Meta:
        db_table = "ai_analysis_log`"
        db_table_comment = "AI解析ログ"

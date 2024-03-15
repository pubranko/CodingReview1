from django.contrib import admin

# Register your models here.

from .models.ai_analysis_log import AiAnalysisLog


class AiAnalysisLogAdmin(admin.ModelAdmin):
    #fields = ["pub_date", "question_text"]
    list_display = ["image_path", "success", "request_timestamp"]

admin.site.register(AiAnalysisLog, AiAnalysisLogAdmin)
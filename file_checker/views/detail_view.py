from django.views import generic
from file_checker.models.ai_analysis_log import AiAnalysisLog


class DetailView(generic.DetailView):
    '''
    ai_analysisサーバーへリクエストした結果の詳細を表示。
    '''
    model = AiAnalysisLog
    template_name = "file_checker/detail.html"

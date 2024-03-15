from django.views import generic
from file_checker.models.ai_analysis_log import AiAnalysisLog


class IndexView(generic.ListView):
    '''
    ai_analysisサーバーへリクエストした結果を一覧で表示。
    リクエストタイムで降順に表示する。
    １ページに５件まで表示する。
    '''
    template_name = "file_checker/index.html"
    context_object_name = "ai_analysis_logs"
    paginate_by = 5 # １ページに表示する明細数

    def get_queryset(self):
        return AiAnalysisLog.objects.order_by("-request_timestamp")

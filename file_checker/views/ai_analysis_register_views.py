import requests
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from file_checker.models.ai_analysis_log import AiAnalysisLog


def ai_analysis_register(request: HttpRequest):
    '''
    indexページからのリクエストを受け取り、ai_analysisサーバーへpostメソッドでリクエストを送る。
    レスポンスを受け取りAiAnalysisLogテーブルへ保存する。
    indexページへリダイレクトして最新の結果を知らせる。
    '''
    request_timestamp = timezone.now()
    headers = {'x-api-key': 'test'}
    api_response = requests.post("http://127.0.0.1:4010/post-test", headers=headers)

    response_timestamp = timezone.now()
    api_response_data:dict = api_response.json()

    ai_analysis_log = AiAnalysisLog(
        # 画面入力値のパスを設定
        image_path=request.POST["image_path"],
        # APIサーバーからの戻り値を設定
        success=api_response_data['success'],
        message=api_response_data['message'],
        class_field=api_response_data['estimated_data']['class'] if 'class' in api_response_data['estimated_data'] else None,
        confidence=api_response_data['estimated_data']['confidence'] if 'confidence' in api_response_data['estimated_data'] else None,
        # リクエスト時、戻り値を受け取った時点のタイムス担保を設定
        request_timestamp=request_timestamp.isoformat(),
        response_timestamp=response_timestamp.isoformat(),
    )
    ai_analysis_log.save()
    
    return HttpResponseRedirect(reverse("file_checker:index"))

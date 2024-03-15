from django.urls import path

from .views.index_view import IndexView
from .views.detail_view import DetailView
from .views.ai_analysis_register_views import ai_analysis_register

app_name = 'file_checker'

urlpatterns = [
    # topページ：リクエストされた情報を一覧表示、リクエストの入力欄を提供。
    path("", IndexView.as_view(), name="index"),

    # topページで選択されたリクエストの明細情報を提供。
    path("<int:pk>/", DetailView.as_view(), name="detail"),

    # topページより入力されたイメージパスを受け取りDBへ登録する。
    # 登録後はtopページへリダイレクトする。
    path("ai_analysis_register/", ai_analysis_register, name="ai_analysis_register"),
]
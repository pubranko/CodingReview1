import random
import factory
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dateutil.parser import parse
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from file_checker.models.ai_analysis_log import AiAnalysisLog
from api_tester.settings import TIME_ZONE

faker:Faker = Faker('jp-JP')

class AiAnalysisLogFactory(factory.django.DjangoModelFactory):
    '''AiAnalysisLogモデル用データファクトリー'''
    class Meta:
        model = AiAnalysisLog

    image_path = faker.url()
    success = faker.boolean()
    message = faker.sentence()
    class_field = faker.random_int(min=0, max=999999999)
    confidence = round(random.uniform(0.0, 9.9999), 4)
    request_timestamp = datetime.now(ZoneInfo(TIME_ZONE))
    response_timestamp = datetime.now(ZoneInfo(TIME_ZONE))

class IndexViewTests(TestCase):
    def test_no_data(self):
        '''登録済みのデータがゼロ件の場合'''
        response = self.client.get(reverse("file_checker:index"))
        self.assertEqual(response.status_code, 200)

    def test_one_data(self):
        '''登録済みのデータが１件の場合'''
        ai_analysis_logs:list = []
        ai_analysis_logs.append(AiAnalysisLogFactory.create())
        response = self.client.get(reverse("file_checker:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["ai_analysis_logs"],
            ai_analysis_logs)

    def test_many_data(self):
        '''登録済みのデータが複数件（２ページ目以降あり）の場合'''
        # dummyデータを６件作成
        [ AiAnalysisLogFactory.create() for _ in range(6)]

        ai_analysis_logs = AiAnalysisLog.objects.order_by("-request_timestamp")[:5] # 降順で５件取得

        # １ページ目に最初の５件が表示されていることを確認
        response = self.client.get(reverse("file_checker:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["ai_analysis_logs"],
            ai_analysis_logs)

        url_with_query = "".join([reverse("file_checker:index"), "?", "page=2"])
        ai_analysis_log = AiAnalysisLog.objects.order_by("-request_timestamp")[5] # 最後の１件（６件目）を取得

        # 2ページ目に最後の１件が表示されていることを確認
        response = self.client.get(url_with_query)
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["ai_analysis_logs"],
            [ai_analysis_log])


class DetailViewTests(TestCase):
    def test_no_data(self):
        '''エラーケース（存在しないIDで検索）'''
        # 存在しないidで検索
        response = self.client.get(reverse('file_checker:detail', kwargs=dict(pk=999999999)))
        self.assertEqual(response.status_code, 404)

    def test_one_data(self):
        '''正常ケース'''
        # テストデータ仕込み
        time_stamp = datetime.now(ZoneInfo(TIME_ZONE))
        
        ai_analysis_log = AiAnalysisLog(
            # 画面入力値のパスを設定
            image_path="b" * 255,
            # APIサーバーからの戻り値を設定
            success=True,
            message="a" * 255,
            class_field=3,
            confidence=1.2345,
            # リクエスト時、戻り値を受け取った時点のタイムス担保を設定
            request_timestamp=time_stamp.isoformat(),
            response_timestamp=(time_stamp + timedelta(seconds=1)).isoformat(),
        )
        ai_analysis_log.save()

        # 明細の内容が想定のとおり表示さているか確認
        response = self.client.get(reverse('file_checker:detail', kwargs=dict(pk=ai_analysis_log.id)))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, str(ai_analysis_log.image_path))
        self.assertContains(response, ai_analysis_log.success)
        self.assertContains(response, str(ai_analysis_log.message))
        self.assertContains(response, str(ai_analysis_log.class_field))
        self.assertContains(response, str(ai_analysis_log.confidence))

        stmap: datetime = parse(str(ai_analysis_log.request_timestamp))
        date = f'{stmap.year}/{stmap.month}/{stmap.day}'    # 月日の頭のゼロを除去
        time = stmap.strftime("%H:%M:%S")
        self.assertContains(response, f'{date} {time}')    # 2024/3/1 01:02:03

        stmap: datetime = parse(str(ai_analysis_log.response_timestamp))
        date = f'{stmap.year}/{stmap.month}/{stmap.day}'    # 月日の頭のゼロを除去
        time = stmap.strftime("%H:%M:%S")
        self.assertContains(response, f'{date} {time}')


class AiAnalysisLogRegisterViewTests(TestCase):
    def test_register(self):
        '''AiAnalysisLog登録テスト'''
        # リクエストしたデータが登録されること、indexページへリダイレクトされることを確認
        response = self.client.post(reverse('file_checker:ai_analysis_register'), data={"image_path":"test_register"})
        self.assertRedirects(response, reverse('file_checker:index'), status_code=302, target_status_code=200)

        # 登録されたレコードがモデルに存在することを確認
        ai_analysis_log = AiAnalysisLog.objects.get(image_path="test_register")
        assert ai_analysis_log is not None
        
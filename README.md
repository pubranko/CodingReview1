# codingReview1

## 技術テスト結果報告
- pythonにて実施しました。

## 環境セットアップ

### 仮想環境作成 （pipenvライブラリーを利用）
- export PIPENV_VENV_IN_PROJECT=1 (ワークスペース内に.venvを作成させるよう設定)
- pipenv shell

### pipenvで必要ライブラリーのインストール
- pipenv install django==4.2 psycopg2-binary python-decouple pytest-factoryboy Faker
- RDBはpostgresを使用
- Django==4.2 LTS版を使用

### postgresDBコンテナーの操作コマンド
#### 起動
- docker-compose -f docker-compose-postgres.yml up -d
#### 停止
- docker-compose -f docker-compose-postgres.yml down

### prismの操作コマンド
- mock apiサーバーとしてprismを使用 （dockerコンテナー版を使用）
#### prismのサーバーを起動
- docker-compose -f docker-compose-prism.yml up
#### prismのサーバーを停止
- docker-compose -f docker-compose-prism.yml down
#### テストデータは以下のファイルを使用
- prism_api_test_data/response.yaml
- 上記ファイルのレスポンス値を手動で正常・エラーを切り替えることでレスポンスを制御

### Djangoプロジェクト作成
- django-admin startproject api_tester .

### Djangoアプリ追加
- python manage.py startapp file_checker

### 初回マイグレーション
- python manage.py migrate

### admin管理ユーザー作成
- python manage.py createsuperuser
- Username: admin_user
- Email address: admin@example.com
- Password: ********

### 管理ユーザーパスワードリセット
- python manage.py changepassword admin_user

### 技術テストに記載されているテーブル項目の誤りについて対応
- success項目がverchar255桁となっているが、真偽値であるためboolean型へ修正
- request_timestamp、response_timestampのタイムスタンプの定義が数値型になっているがdatetime型へ修正

## unit-test
### viewのテストを実装しています。modelのテストは今回不要と判断し見送り。
python manage.py test file_checker

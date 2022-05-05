#####################################################################################
# modelモジュール
# ファイル名：models.py
# ヒント：モデルは、makemigrate、migrateコマンドを通じて、データベースのテーブル定義と深いつながりがある。
# ヒント：このため、安易に項目の削除、追加を行わないこと。
# ヒント：ブラウザにPUTしブラウザからPOSTされるデータはフォーム、ブラウザにPUTするのみのデータはモデルが使い易い。
#####################################################################################
from django.db import models
#####################################################################################
# モデル名：AccountModel
# 処理概要：FILE_UPLOAD_ACCOUNTテーブル用のモデルを定義する。
# 使用ビュー：P01.LoginView等
#####################################################################################
class AccountModel(models.Model):
    ### id = models.CharField(max_length=50, default='')                                                # アカウント物理ＩＤ（物理主キー）
    ACCOUNT_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                    # アカウント論理ＩＤ（論理主キー）＝担当者ＩＤ
    ACCOUNT_TYPE = models.CharField(max_length=50, default='0', blank=True, null=True)                  # アカウント種別（１：都道府県、２：本省、３：運用業者）　
    ACCOUNT_PASSWORD = models.CharField(max_length=50, default='0', blank=True, null=True)              # アカウントパスワード
    ACCOUNT_LOCK_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)             # アカウントロックフラグ（０：未ロック、１：未ロック、５：ロック）
    OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 調査実施年
    FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                    # 対象水害年
    ORG_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                      # 組織コード
    ORG_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                      # 組織名
    DEPT_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                     # 部署コード
    DEPT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                     # 部署名
    ACCOUNT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                  # アカウント名＝担当者名
    MAIL_ADDRESS = models.CharField(max_length=50, default='0', blank=True, null=True)                  # メールアドレス 
    TEL_NO = models.CharField(max_length=51, default='0', blank=True, null=True)                        # 電話番号   
    ADD_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 登録日時
    ADD_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                      #　登録フラグ（０：登録中、１：登録中、５：登録済）   
    DELETE_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)              # 削除日時
    DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                   #　削除フラグ（０：未削除、１：未削除、５：削除済）
    LAST_LOGIN_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)          # 最終ログイン日時
    class Meta:
        db_table = 'file_upload_account'
#####################################################################################
# モデル名：InfoModel
# 処理概要：FILE_UPLOAD_INFOテーブル用のモデルを定義する。
# 使用ビュー：P02.TopView等
#####################################################################################
class InfoModel(models.Model):
    ### id = models.CharField(max_length=50, default='', blank=False, null=False)                       # お知らせ物理ＩＤ（物理主キー）
    OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 調査実施年
    FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                    # 対象水害年
    INFO_NUMBER = models.CharField(max_length=50, default='0', blank=True, null=True)                   # お知らせ番号
    SUMMARY = models.CharField(max_length=100, default='0', blank=True, null=True)                      # お知らせの要約
    BODY_1 = models.CharField(max_length=500, default='0', blank=True, null=True)                       # お知らせの全文
    BODY_2 = models.CharField(max_length=500, default='0', blank=True, null=True)                       # お知らせの全文
    BODY_3 = models.CharField(max_length=500, default='0', blank=True, null=True)                       # お知らせの全文
    BODY_4 = models.CharField(max_length=500, default='0', blank=True, null=True)                       # お知らせの全文
    BODY_5 = models.CharField(max_length=500, default='0', blank=True, null=True)                       # お知らせの全文
    BODY_6 = models.CharField(max_length=500, default='0', blank=True, null=True)                       # お知らせの全文
    BODY_7 = models.CharField(max_length=500, default='0', blank=True, null=True)                       # お知らせの全文
    BODY_8 = models.CharField(max_length=500, default='0', blank=True, null=True)                       # お知らせの全文
    BODY_9 = models.CharField(max_length=500, default='0', blank=True, null=True)                       # お知らせの全文
    BODY_10 = models.CharField(max_length=500, default='0', blank=True, null=True)                      # お知らせの全文
    HTML_FILE_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                # HTMLファイルのパス※必要な場合
    ADD_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                      # お知らせの登録年月日（YYYY/MM/DD、ゼロ埋めで登録すると想定、JOB_ADD_RSSで検索時に使用するため）
    DISPLAY_ORDER = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 一覧での表示順
    DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除フラグ（０：未削除、１：未削除、５：削除済）
    class Meta:
        db_table = 'file_upload_info'
#####################################################################################
# モデル名：P10UploadModel
# 処理概要：FILE_UPLOAD_P10Uploadテーブル用のモデルを定義する。
# 使用ビュー：P10.UploadListView等
#####################################################################################
class P10UploadModel(models.Model):
    ### id = models.CharField(max_length=50, default='')                                                # アップロード物理ＩＤ（物理主キー）
    KEN_UPLOAD_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                 # アップロード論理ＩＤ（論理主キー）
    KEN_KEN_HON_OPE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)          # 調査結果または確認結果フラグ（1：調査結果、2：確認結果）※これでこのデータが調査結果か確認結果かを区分する。
    KEN_OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)            # 調査実施
    KEN_FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 対象水害年
    KEN_ORG_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                  # 組織コード
    KEN_ORG_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                  # 組織名
    KEN_DEPT_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 部署コード
    KEN_DEPT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 部署名
    KEN_ACCOUNT_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                # アカウントＩＤ＝担当者ＩＤ
    KEN_ACCOUNT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)              # アカウント名＝担当者名
    KEN_ADD_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                  # 登録日
    KEN_ADD_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)             # 登録日時
    KEN_ADD_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                  # 登録フラグ（０：登録中、１：登録中、５：登録済）
    KEN_DELETE_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)               # 削除日
    KEN_DELETE_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)          # 削除日時
    KEN_DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)               # 削除フラグ（０：未削除、１：未削除、５：削除済）
    KEN_QUESTION_BODY = models.CharField(max_length=50, default='0', blank=True, null=True)             # 問合せ回答本文
    KEN_QUESTION_TO_HON_OPE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)  # 問合せ本省宛、問合せ運用業者宛フラグ
    HON_UPLOAD_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                 # アップロード論理ＩＤ（論理主キー）
    HON_KEN_HON_OPE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)          # 調査結果または確認結果フラグ（1：調査結果、2：確認結果）※これでこのデータが調査結果か確認結果かを区分する。
    HON_OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)            # 調査実施年
    HON_FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 対象水害年
    HON_ORG_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                  # 組織コード
    HON_ORG_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                  # 組織名
    HON_DEPT_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 部署コード
    HON_DEPT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 部署名
    HON_ACCOUNT_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                # アカウントＩＤ＝担当者ＩＤ
    HON_ACCOUNT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)              # アカウント名＝担当者名
    HON_ADD_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                  # 登録日
    HON_ADD_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)             # 登録日時
    HON_ADD_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                  # 登録フラグ（０：登録中、１：登録中、５：登録済）
    HON_DELETE_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)               # 削除日
    HON_DELETE_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)          # 削除日時
    HON_DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)               # 削除フラグ（０：未削除、１：未削除、５：削除済）
    HON_QUESTION_BODY = models.CharField(max_length=50, default='0', blank=True, null=True)             # 問合せ回答本文
    HON_QUESTION_TO_HON_OPE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)  # 問合せ本省宛、問合せ運用業者宛フラグ
#####################################################################################
# モデル名：UploadModel
# 処理概要：FILE_UPLOAD_UPLOADテーブル用のモデルを定義する。
# 使用ビュー：P11.UploadDetailView
# ヒント：調査結果または確認結果データは、調査結果で１件、確認結果で１件というように、別々に登録するものと想定する。
# ヒント：１画面で調査結果と確認結果を表示する画面があるため、SQLを工夫し、２件のデータを取得し、内部変数セット時にマージすること。
# ヒント：データ登録画面、データ登録確認画面で登録中のデータを保持するため、登録画面で登録時にＤＢに仮登録する。
# ヒント：データ登録画面、データ登録確認画面で登録中のデータを保持するため、登録確認画面で登録時にＤＢの登録フラグを仮登録済->本登録済に更新する。
# ヒント：データ削除画面、データ削除確認画面で削除中のデータを保持するため、削除画面で削除時にＤＢに仮削除する。
# ヒント：データ削除画面、データ削除確認画面で削除中のデータを保持するため、削除確認画面で削除時にＤＢの削除フラグを仮削除済->本削除済に更新する。
# ヒント：アップロードデータ＝調査結果とアップロードファイル＝調査結果添付ファイルには、親子関係が存在する。
# ヒント：アップロードファイルテーブルにアップロードテーブルの主キーを参照する外部キーを持たせることで、上記の親子関係を保持する。
# ヒント：djangoでは、idが物理テーブルの主キー暗黙の内に認識＝生成される。プログラムで意識してシーケンス番号を採番する。
# ヒント：このため、テーブルの物理主キーとは、別に、論理主キーを設けることで、
# ヒント：プログラムのロジックを簡潔（＝プログラム中にロジックをできるだけ含まないベタな状態）にしたまま、必要な機能を実現している。
#####################################################################################
class UploadModel(models.Model):
    ### id = models.CharField(max_length=50, default='')                                                # アップロード物理ＩＤ＝調査結果または確認結果物理ＩＤ（物理主キー）
    KEN_UPLOAD_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                 # アップロード論理ＩＤ＝調査結果ＩＤ＝都道府県登録データＩＤ※確認結果の場合に、元の調査結果の対応をセットする。（論理主キー）
    HON_UPLOAD_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                 # アップロード論理ＩＤ＝調査結果ＩＤ＝本省登録データＩＤ※確認結果の場合に、元の調査結果の対応をセットする。（論理主キー）
    KEN_HON_OPE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)              # アップロード種別・区分＝調査結果または確認結果種別・区分、１：都道府県登録データ＝調査結果、２：本省登録データ＝確認結果　※これでこのデータが調査結果か確認結果かを区分する。
    OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 調査実施年
    FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                    # 対象水害年
    ORG_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                      # 組織コード
    ORG_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                      # 組織名
    DEPT_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                     # 部署コード
    DEPT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                     # 部署名
    ACCOUNT_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                    # アカウントＩＤ＝ログインＩＤ＝担当者ＩＤ
    ACCOUNT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                  # アカウント名＝ログイン名＝担当者名
    ADD_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                      # 登録日
    ADD_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 登録日時
    ADD_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                      # 登録フラグ（０：登録中、１：登録中、５：登録済）
    DELETE_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除日
    DELETE_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)              # 削除日時
    DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除フラグ（０：未削除、１：未削除、５：削除済）
    QUESTION_BODY = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 問合せ回答本文
    QUESTION_TO_HON_OPE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)      # 問合せ本省宛、問合せ運用業者宛フラグ
    class Meta:
        db_table = 'file_upload_upload'
#####################################################################################
# モデル名：UploadFileModel
# 処理概要：FILE_UPLOAD_UPLOADFILEテーブル用のモデルを定義する。
# 使用ビュー：P11.UploadDetailView
# ヒント：データ登録画面、データ登録確認画面で登録中のデータを保持するため、登録画面で登録時にＤＢに仮登録する。
# ヒント：データ登録画面、データ登録確認画面で登録中のデータを保持するため、登録確認画面で登録時にＤＢの登録フラグを仮登録済->本登録済に更新する。
# ヒント：データ削除画面、データ削除確認画面で削除中のデータを保持するため、削除画面で削除時にＤＢに仮削除する。
# ヒント：データ削除画面、データ削除確認画面で削除中のデータを保持するため、削除確認画面で削除時にＤＢの削除フラグを仮削除済->本削除済に更新する。
# ヒント：アップロードデータ＝調査結果とアップロードファイル＝調査結果添付ファイルには、親子関係が存在する。
# ヒント：アップロードファイルテーブルにアップロードテーブルの主キーを参照する外部キーを持たせることで、上記の親子関係を保持する。
# ヒント：djangoでは、idが物理テーブルの主キー暗黙の内に認識＝生成される。プログラムで意識してシーケンス番号を採番する。
# ヒント：このため、テーブルの物理主キーとは、別に、論理主キーを設けることで、
# ヒント：プログラムのロジックを簡潔（＝プログラム中にロジックをできるだけ含まないベタな状態）にしたまま、必要な機能を実現している。
#####################################################################################
class UploadFileModel(models.Model):
    ### id = models.CharField(max_length=50, default='')                                                # アップロードファイル物理ＩＤ（物理主キー）
    KEN_UPLOAD_FILE_ID = models.CharField(max_length=50, default='0', blank=True, null=True)            # アップロードファイル論理ＩＤ（論理主キー）
    HON_UPLOAD_FILE_ID = models.CharField(max_length=50, default='0', blank=True, null=True)            # アップロードファイル論理ＩＤ（論理主キー）
    KEN_UPLOAD_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                 # アップロード論理ＩＤ：アップロードテーブルの論理主キーをセット（論理外部キー）
    HON_UPLOAD_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                 # アップロード論理ＩＤ：アップロードテーブルの論理主キーをセット（論理外部キー）
    KEN_HON_OPE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)              # アップロードファイル種別・区分：１：都道府県登録、２：本省登録、３：運用業者登録
    OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 調査実施年
    FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                    # 対象水害年
    KEN_UPLOAD_FILE_NAME = models.CharField(max_length=500, default='0', blank=True, null=True)         # アップロードファイル名　例　北海道.lzh
    HON_UPLOAD_FILE_NAME = models.CharField(max_length=500, default='0', blank=True, null=True)         # アップロードファイル名　例　本省.lzh
    KEN_UPLOAD_FILE_PATH = models.CharField(max_length=500, default='0', blank=True, null=True)         # アップロードファイルパス　例　F:\uplod\
    HON_UPLOAD_FILE_PATH = models.CharField(max_length=500, default='0', blank=True, null=True)         # アップロードファイルパス　例　F:\upload\
    ADD_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                      # 登録日
    ADD_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 登録日時
    ADD_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                      # 登録フラグ（０：登録中、１：登録中、５：登録済）
    DELETE_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除日
    DELETE_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)              # 削除日時
    DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除フラグ（０：未削除、１：未削除、５：削除済）
    DISPLAY_ORDER = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 未使用
    class Meta:
        db_table = 'file_upload_uploadfile'
#####################################################################################
# モデル名：QuestionModel
# 処理概要：FILE_UPLOAD_QUESTIONテーブル用のモデルを定義する。
# 使用ビュー：P25.QuestionReceiveListView
# ヒント：問合せまたは回答データは、問合せで１件、回答で１件というように、別々に登録するものと想定する。
# ヒント：１画面で調査結果と確認結果を表示する画面がはないため、、、、
#####################################################################################
class QuestionModel(models.Model):
    ### id = models.CharField(max_length=50, default='')                                                # 問合せ回答物理ＩＤ（物理主キー）
    QUESTION_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 問合せ回答論理ＩＤ（論理主キー）
    OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 調査実施年
    FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                    # 対象水害年
    SEND_ORG_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 送信組織コード
    SEND_ORG_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 送信組織名
    SEND_DEPT_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                # 送信部署コード
    SEND_DEPT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                # 送信部署名
    SEND_ACCOUNT_ID = models.CharField(max_length=50, default='0', blank=True, null=True)               # 送信アカウントＩＤ
    SEND_ACCOUNT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)             # 送信アカウント名　
    SEND_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                     # 送信日
    SEND_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)                # 送信日時
    SEND_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                     # 送信フラグ
    SUBJECT = models.CharField(max_length=50, default='0', blank=True, null=True)                       # 件名
    BODY = models.CharField(max_length=50, default='0', blank=True, null=True)                          # 本文
    RECEIVE_ORG_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)              # 受信組織コード
    RECEIVE_ORG_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)              # 受信組織名
    RECEIVE_DEPT_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)             # 受信部署コード
    RECEIVE_DEPT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)             # 受信部署名
    RECEIVE_ACCOUNT_ID = models.CharField(max_length=50, default='0', blank=True, null=True)            # 受信アカウントＩＤ
    RECEIVE_ACCOUNT_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)          # 受信アカウント名
    RECEIVE_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                  # 受信日
    RECEIVE_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)             # 受信日時
    RECEIVE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                  # 受信フラグ
    DELETE_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除日
    DELETE_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)              # 削除日時
    DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除フラグ
    RECEIVE_READ_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)             # 受信既読フラグ（０：未読、１：未読、５：既読）    
    class Meta:
        db_table = 'file_upload_question'
#####################################################################################
# モデル名：QuestionFileModel
# 処理概要：FILE_UPLOAD_QUESTIONFILEテーブル用のモデルを定義する。
# 使用ビュー：P25.QuestionReceiveListView
#####################################################################################
class QuestionFileModel(models.Model):
    ### id = models.CharField(max_length=50, default='')                                                # 問合せ回答ファイル物理ＩＤ（物理主キー）
    QUESTION_FILE_ID = models.CharField(max_length=50, default='0', blank=True, null=True)              # 問合せ回答ファイル論理ＩＤ（論理主キー）
    QUESTION_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 親問合せ回答論理ＩＤ（論理外部キー）
    OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 調査実施年
    FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                    # 対象水害年
    FILE_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                       # 問合せ回答ファイル論理ＩＤ（論理主キー）
    FILE_NAME = models.CharField(max_length=500, default='0', blank=True, null=True)                    # 問合せ回答ファイル名　例　北海道.lzh
    FILE_PATH = models.CharField(max_length=500, default='0', blank=True, null=True)                    # 問合せ回答ファイルパス　例　F:\uplod\
    SEND_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                     # 登録日
    SEND_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)                # 登録日時
    SEND_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                     # 登録フラグ（０：登録中、１：登録中、５：登録済）
    DELETE_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除日
    DELETE_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)              # 削除年月日
    DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除フラグ（０：未削除、１：未削除、５：削除済）
    class Meta:
        db_table = 'file_upload_questionfile'
#####################################################################################
# モデル名：P40FaqModel
# 処理概要：FILE_UPLOAD_P40Faqテーブル用のモデルを定義する。
# 使用ビュー：P40.FaqListView
#####################################################################################
class P40FaqModel(models.Model):
    ### id = models.CharField(max_length=50, default='', blank=False, null=False)                       # FAQ物理ＩＤ（物理主キー）
    FAQ_NUMBER = models.CharField(max_length=50, default='0', blank=True, null=True)                    # FAQ論理ＩＤ（論理主キー）
    OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 調査実施年
    FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                    # 対象水害年
    CATEGORY_1_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)               # 質問の大分類・区分コード（1：水害統計調査調査要領、2：水害統計入力システム）
    CATEGORY_2_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)               # 質問の小分類・区分コード（1000：一般資産水害統計調査、1010：被害区分の判断基準、1020：水害発生年月日、1030：水系・沿岸名、河川・海岸名、1040：被害建物の延床面積、1050：事業所従業者数、1060：農作物被害額、1070：水害区域図、1080：公共土木施設水害統計調査、1090：公益事業等水害統計調査、1100：その他、
    ###CATEGORY_1_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)            # 質問の大分類・区分名（1：水害統計調査調査要領、2：水害統計入力システム）
    CATEGORY_2_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)               # 質問の小分類・区分名（1000：一般資産水害統計調査、1010：被害区分の判断基準、、、）
    QUESTION_SUMMARY = models.CharField(max_length=500, default='0', blank=True, null=True)             # 質問の要約
    QUESTION_BODY = models.CharField(max_length=500, default='0', blank=True, null=True)                # 質問の全文
    ANSWER_SUMMARY = models.CharField(max_length=500, default='0', blank=True, null=True)               # 回答の要約 
    ANSWER_BODY_1 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_2 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_3 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_4 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_5 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_6 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_7 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_8 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_9 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_10 = models.CharField(max_length=500, default='0', blank=True, null=True)               # 回答の全文
    ANSWER_BODY_11 = models.CharField(max_length=500, default='0', blank=True, null=True)               # 回答の全文
    ANSWER_BODY_12 = models.CharField(max_length=500, default='0', blank=True, null=True)               # 回答の全文
    ANSWER_BODY_13 = models.CharField(max_length=500, default='0', blank=True, null=True)               # 回答の全文
    MANUAL_PAGE = models.CharField(max_length=50, default='0', blank=True, null=True)                   # マニュアルの該当ページ
    HTML_FILE_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                # HTMLファイルのパス※必要な場合
    DISPLAY_ORDER = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 一覧での表示順
    DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除フラグ
#####################################################################################
# モデル名：FaqModel
# 処理概要：FILE_UPLOAD_FAQテーブル用のモデルを定義する。
# 使用ビュー：P40.FaqListView
#####################################################################################
class FaqModel(models.Model):
    ### id = models.CharField(max_length=50, default='', blank=False, null=False)                       # FAQ物理ＩＤ（物理主キー）
    FAQ_NUMBER = models.CharField(max_length=50, default='0', blank=True, null=True)                    # FAQ論理ＩＤ（論理主キー）
    OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 調査実施年
    FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                    # 対象水害年
    CATEGORY_1_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)               # 質問の大分類・区分コード（1：水害統計調査調査要領、2：水害統計入力システム）
    CATEGORY_2_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)               # 質問の小分類・区分コード（1000：一般資産水害統計調査、1010：被害区分の判断基準、1020：水害発生年月日、1030：水系・沿岸名、河川・海岸名、1040：被害建物の延床面積、1050：事業所従業者数、1060：農作物被害額、1070：水害区域図、1080：公共土木施設水害統計調査、1090：公益事業等水害統計調査、1100：その他、
    QUESTION_SUMMARY = models.CharField(max_length=500, default='0', blank=True, null=True)             # 質問の要約
    QUESTION_BODY = models.CharField(max_length=500, default='0', blank=True, null=True)                # 質問の全文
    ANSWER_SUMMARY = models.CharField(max_length=500, default='0', blank=True, null=True)               # 回答の要約 
    ANSWER_BODY_1 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_2 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_3 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_4 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_5 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_6 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_7 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_8 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_9 = models.CharField(max_length=500, default='0', blank=True, null=True)                # 回答の全文
    ANSWER_BODY_10 = models.CharField(max_length=500, default='0', blank=True, null=True)               # 回答の全文
    ANSWER_BODY_11 = models.CharField(max_length=500, default='0', blank=True, null=True)               # 回答の全文
    ANSWER_BODY_12 = models.CharField(max_length=500, default='0', blank=True, null=True)               # 回答の全文
    ANSWER_BODY_13 = models.CharField(max_length=500, default='0', blank=True, null=True)               # 回答の全文
    MANUAL_PAGE = models.CharField(max_length=50, default='0', blank=True, null=True)                   # マニュアルの該当ページ
    HTML_FILE_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                # HTMLファイルのパス※必要な場合
    DISPLAY_ORDER = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 一覧での表示順（未使用）
    DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除フラグ（０：未削除、１：未削除、５：削除済）
    class Meta:
        db_table = 'file_upload_faq'
#####################################################################################
# モデル名：FaqCategoryModel
# 処理概要：FILE_UPLOAD_FAQCATEGORYテーブル用のモデルを定義する。
# 使用ビュー：P40.FaqListView
#####################################################################################
class FaqCategoryModel(models.Model):
    ### id = models.CharField(max_length=50, default='')                                                # FAQ CATEGORY物理ＩＤ（物理主キー）
    CATEGORY_CODE = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 質問の小分類・区分コード（1000：一般資産水害統計調査、1010：被害区分の判断基準、1020：水害発生年月日、1030：水系・沿岸名、河川・海岸名、1040：被害建物の延床面積、1050：事業所従業者数、1060：農作物被害額、1070：水害区域図、1080：公共土木施設水害統計調査、1090：公益事業等水害統計調査、1100：その他、
    CATEGORY_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 質問の小分類・区分名
    DISPLAY_ORDER = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 一覧での表示順
    DELETE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)                   # 削除フラグ（0：削除未、1：削除済）
    class Meta:
        db_table = 'file_upload_faqcategory'
#####################################################################################
# モデル名：RssModel
# 処理概要：FILE_UPLOAD_RSSテーブル用のモデルを定義する。
# 使用ビュー：P42.RdfView
# ヒント：未読、既読を管理するため、RSSを見る可能性のある人ごとにRSSテーブルのレコードを作成する。
# ヒント：バッチ処理で、操作履歴テーブル、元データのテーブルをもとに、RSSテーブルを定期的に更新する。
# ヒント：元データテーブルから、お知らせ、調査結果、問合せの登録のみを抽出し、対象データ、日時、誰から誰宛等の情報を生成し、RSSに追加する。
# ヒント：RSSに同じキー項目のデータが存在する場合は、前回バッチ時に処理済と考え、、、登録、更新しない。
# ヒント：InfoDetailView、UploadDetailView、QuestionDetailView処理時にレコードを追加する。
# ヒント：RSSは未読既読を管理せず、今日、昨日等に、アカウントＩＤ宛のお知らせ、調査結果、問合せ件数が何件あったかのみを管理する。
# ヒント：また、RSSのリンク先は詳細情報とせず、一覧にする。
# ヒント：つまり、未読既読の管理は人間にまかせる。今日新規に１０件きてれば、さすがに確認してみようか、、、という程度。
# ヒント：既読未読をRSSにも表示する場合、ログではなく、元のテーブルのRECEIVE_READ_FLAG等を使用する。
#####################################################################################
class RssModel(models.Model):
    ### id = models.CharField(max_length=50, default='')                                                # RSS物理ＩＤ（物理主キー）
    OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # RDF項目：調査実施年
    FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                    # RDF項目：対象水害年
    ABOUT = models.CharField(max_length=250, default='0', blank=True, null=True)                        # RDF項目：リンク（＝item rdf:about＝URL） 
    TITLE = models.CharField(max_length=100, default='0', blank=True, null=True)                        # RDF項目：題名（＝title）（お知らせ登録、調査結果または確認結果登録、問合せまたは回答登録）
    LINK = models.CharField(max_length=250, default='0', blank=True, null=True)                         # RDF項目：リンク（＝link）
    DESCRIPTION = models.CharField(max_length=250, default='0', blank=True, null=True)                  # RDF項目：説明（＝description）（お知らせ登録、調査結果または確認結果登録、問合せまたは回答登録）

    ADD_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                      # ＲＳＳテーブルにデータを登録する年月日
    COUNT_DATE = models.CharField(max_length=50, default='0', blank=True, null=True)                    # カウント対象年がtぅ日
    VIEW_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                     # バッチ等条件判定用項目：情報種別（InfoDetailView、UploadDetailView、QuestionDetailView）
    ACCOUNT_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                    # アカウントＩＤ
    DATA_COUNT = models.CharField(max_length=50, default='0', blank=True, null=True)                    # 件数のうち、正常範囲のデータ 
    class Meta:
        db_table = 'file_upload_rss'
#####################################################################################
# モデル名：LogModel
# 処理概要：FILE_UPLOAD_LOGテーブル用のモデルを定義する。
# 使用ビュー：P42.RdfView
# ヒント：未読、既読を管理するため、情報閲覧時に操作履歴テーブルに閲覧データの種類、ID、日時、閲覧者を追記していく。
# ヒント：操作履歴テーブルは、お知らせ、調査結果、問合せの閲覧のみを対象とする。
# ヒント：１０分毎で良い？
# ヒント：これらにより、現行のソースコードに手を加えることなく（操作テーブルへの追記のみ）、削除時等の消込なども気にすることなく単純なコードが記述できると想定する。
# ヒント：ログはログとしてのみ使用することとする。（RSSの未読既読管理と連携させると複雑なため）
#####################################################################################
class LogModel(models.Model):
    ### id = models.CharField(max_length=50, default='')                                                # 物理ＩＤ（物理主キー）
    OPERATION_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                # 調査実施年
    FLOOD_YEAR = models.CharField(max_length=50, default='0', blank=True, null=True)                    # 対象水害年
    LOG_DATE_TIME = models.CharField(max_length=50, default='0', blank=True, null=True)                 # 利用者の閲覧日時
    VIEW_NAME = models.CharField(max_length=50, default='0', blank=True, null=True)                     # バッチ等条件判定用項目：情報種別（InfoDetailView、UploadDetailView、QuestionDetailView） 
    FROM_ACCOUNT_ID = models.CharField(max_length=50, default='0', blank=True, null=True)               # バッチ等条件判定用項目：登録した担当者のアカウントＩＤ
    TO_ACCOUNT_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                 # バッチ等条件判定用項目：閲覧対象の担当者のアカウントＩＤ
    
    INFO_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                       # オプションRDF項目:
    KEN_UPLOAD_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                 # オプションRDF項目:
    HON_UPLOAD_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                 # オプションRDF項目:
    KEN_HON_OPE_FLAG = models.CharField(max_length=50, default='0', blank=True, null=True)              # オプションRDF項目:
    QUESTION_ID = models.CharField(max_length=50, default='0', blank=True, null=True)                   # オプションRDF項目:
    class Meta:
        db_table = 'file_upload_Log'

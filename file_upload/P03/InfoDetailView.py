#####################################################################################
# InfoDetailViewビューモジュール【ほぼ完成】
# ファイル：P03.InfoDetailView.py（Ｐ０３）
# ユースケース：都道府県の担当者は、INFOを閲覧する。
# ユースケース：本省の担当者は、INFOを閲覧する。
# ユースケース：運用業者の担当者は、INFOを閲覧する。
# TO-DO：引数チェックに引っかかった場合、ビュー関数でエラーが発生した場合、テンプレートでレンダリングでエラーが発生した場合に応じ、
# TO-DO：異なるエラー画面を表示することがＵＩ上好ましいと思われる。リリース後の課題として、TO-DO（保留）とする。
# ヒント：ここにこないはずの場合、ERRORとする。また、try exceptの場合も、ERRORとする。（判断基準１）
# ヒント：ユーザが入力した値のチェック、クエリストリング等で引っかかった場合、WARNとする。（判断基準１）
# ヒント：処理継続する場合はWARN、継続しない場合はERRORとする。（判断基準２）
#####################################################################################

#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：パイソンモジュールをインポートする。
# sys
#####################################################################################
import sys                                                 # sysモジュール
from datetime import datetime                              # datetimeモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：ジャンゴモジュールをインポートする。
# login_required
# render
# urlquote
#####################################################################################
from django.contrib.auth.decorators import login_required  # ログイン制御モジュール
from django.db import connection                           # ＤＢ接続モジュール
from django.db import transaction                          # トランザクション管理モジュール
from django.shortcuts import render                        # レンダリングモジュール
from django.utils.http import urlquote                     # URLエスケープモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# AccountModel
# InfoModel
# print_log
#####################################################################################
from file_upload.models import AccountModel                # アカウントモデル
from file_upload.models import InfoModel                   # お知らせモデル
from file_upload.CommonFunction import print_log           # ログ出力モジュール
#####################################################################################
# 関数名：P03.InfoDetailView（Ｐ０３Ａ）
# 関数概要：お知らせ詳細ページをブラウザに戻す。

# 引数[1]：request
# 引数[2]：accountType
# 引数[3]：accountId
# 引数[4]：operationYear
# 引数[5]：infoId

# 戻り値[1]：response
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def InfoDetailView(request, accountType, accountId, operationYear, infoId):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P03.InfoDetailView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ０３Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P03.InfoDetailView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P03.InfoDetailView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P03.InfoDetailView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P03.InfoDetailView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P03.InfoDetailView.infoId = {}'.format(infoId), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ０３Ａ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        # （７）本省アップロードＩＤをチェックする。　例　1
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        if accountId == str(request.user.username):
            pass
        else:
            print_log('[WARN] P03.InfoDetailView関数 P03A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P03.InfoDetailView関数 P03A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P03.InfoDetailView関数 P03A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P03.InfoDetailView関数 P03A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P03.InfoDetailView関数 P03A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P03.InfoDetailView関数 P03A20-5', 'WARN')
                return render(request, 'error.html')
        # （６）お知らせＩＤをチェックする。　例　1
        if infoId is None:
            print_log('[WARN] P03.InfoDetailView関数 P03A20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(infoId) == True:
                pass
            else:
                print_log('[WARN] P03.InfoDetailView関数 P03A20-4', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ０３Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print('[INFO] P03.InfoDetailView.method関数 P03A30', 'INFO')
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        localAccountModel = None
        try:
            localAccountModel = AccountModel.objects.raw("""
                SELECT 
                    * 
                FROM 
                    FILE_UPLOAD_ACCOUNT 
                WHERE 
                    ACCOUNT_ID=%s AND 
                    OPERATION_YEAR=%s 
                LIMIT 1
                """, 
                [ accountId, 
                  operationYear, 
                ])[0]
        except:
            localAccountModel = None
            print_log('[ERROR] P03.InfoDetailView関数 P03A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P03.InfoDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P03.InfoDetailView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P03.InfoDetailView関数 P03A30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P03.InfoDetailView関数 P03A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、お知らせデータ取得処理（Ｐ０３Ａ４０）
        # （１）お知らせデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、お知らせデータを取得する。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：rawでＤＢにアクセスした場合、検索結果が０件の場合、エクセプションが発生する。
        # ヒント：後々の拡張等を考慮し、場合分けをベタで記述し、明示されていないロジックを含まないコードとするため、
        # ヒント：あえて冗長な場合分けをしている。
        # ヒント：ＤＢのアップロードテーブル、アップロードファイルテーブルには、KEN_UPLOAD_ID、HON_UPLOAD_ID、KEN_HON_OPE_FLAGの項目がある。
        # ヒント：調査結果（親）と確認結果（子）を紐付けるために使用している。
        # ヒント：このため、調査結果（親）については、KEN_UPLOAD_ID（親アップロードデータのＩＤ）がセット、HON_UPLOAD_ID（子アップロードデータのＩＤ）が未セット、
        # ヒント：確認結果（子）については、KEN_UPLOAD_ID（親アップロードデータのＩＤ）がセット、HON_UPLOAD_ID（子アップロードデータのＩＤ）がセットされることを想定している。
        # ヒント：また、後々の拡張等を考慮し、調査結果（親）についても、KEN_UPLOAD_IDがセット、HON_UPLOAD_IDがセットされることも想定している。
        # ヒント：このため、調査結果、または確認結果を別々に検索する場合は、KEN_HON_OPE_FLAGも使用すること。
        ##########################################
        print_log('[INFO] P03.InfoDetailView関数 P03A40', 'INFO')
        # （１）お知らせデータを格納する局所変数を初期化する。
        localInfoModel = None
        # （２）ＤＢにアクセスし、お知らせデータを取得する。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                # ヒント：お知らせデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                try:
                    localInfoModel = InfoModel.objects.raw("""
                        SELECT 
                            * 
                        FROM 
                            FILE_UPLOAD_INFO 
                        WHERE 
                            OPERATION_YEAR=%s AND 
                            ID=%s 
                        LIMIT 1
                        """,
                        [ operationYear, 
                          infoId, 
                        ])[0]
                except:
                    localInfoModel = None        
                    print_log('[ERROR] P03.InfoDetailView関数 P03A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P03.InfoDetailView関数で警告が発生しました。', 'ERROR')
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                # ヒント：お知らせデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                try:
                    localInfoModel = InfoModel.objects.raw("""
                        SELECT 
                            * 
                        FROM 
                            FILE_UPLOAD_INFO 
                        WHERE 
                            OPERATION_YEAR=%s AND 
                            ID=%s 
                        LIMIT 1
                        """,
                        [ operationYear, 
                          infoId, 
                        ])[0]
                except:
                    localInfoModel = None        
                    print_log('[ERROR] P03.InfoDetailView関数 P03A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P03.InfoDetailView関数で警告が発生しました。', 'ERROR')
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                # ヒント：お知らせデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                try:
                    localInfoModel = InfoModel.objects.raw("""
                        SELECT 
                            * 
                        FROM 
                            FILE_UPLOAD_INFO 
                        WHERE 
                            OPERATION_YEAR=%s AND 
                            ID=%s 
                        LIMIT 1
                        """,
                        [ operationYear, 
                          infoId, 
                        ])[0]
                except:        
                    localInfoModel = None        
                    print_log('[ERROR] P03.InfoDetailView関数 P03A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P03.InfoDetailView関数で警告が発生しました。', 'ERROR')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P03.InfoDetailView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P03.InfoDetailView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P03.InfoDetailView関数 P03A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P03.InfoDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P03.InfoDetailView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、お知らせデータ取得処理（Ｐ０３Ａ４５）
        # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
        # （２）ＳＱＬ文を実行する。
        # （３）トランザクション管理でコミットする。
        # （４）ＤＢ接続を切断＝カーソルを閉じる。
        ##########################################
        print_log('[INFO] P03.InfoDetailView関数 P03A45', 'INFO')
        try:
            # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
            localCursor = connection.cursor()
            # （２）ＳＱＬ文を実行する。
            localCursor.execute("""
                INSERT INTO FILE_UPLOAD_LOG (
                    id, 
                    OPERATION_YEAR,
                    FLOOD_YEAR,
                    LOG_DATE_TIME,
                    VIEW_NAME,
                    INFO_ID
                ) VALUES (
                    (SELECT MAX(id + 1) FROM FILE_UPLOAD_LOG),
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                [ operationYear, 
                  operationYear,
                  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  'InfoDetailView',
                  infoId, 
                ])
            # （３）トランザクション管理でコミットする。
            transaction.commit()
        except:
            transaction.rollback()
            print_log('[ERROR] P03.InfoDetailView関数 P03A45', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P03.InfoDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P03.InfoDetailView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        finally:
            # （４）ＤＢ接続を切断＝カーソルを閉じる。
            localCursor.close()
        ##########################################
        # フォームセット処理（Ｐ０３Ａ５０）
        ##########################################
        print_log('[INFO] P03.InfoDetailView関数 P03A50', 'INFO')
        ##########################################
        # レスポンスセット処理（Ｐ０３Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        ##########################################
        print_log('[INFO] P03.InfoDetailView関数 P03A60', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            # ヒント：モデルの場合、len(list(localInfoModel))で件数を取得しようとするとエラーが発生する。
            # ヒント：そのため、以下では、if localInfoModel != Noneで条件分岐させている。
            if localInfoModel != None:
                response = {
                    'accountType': 1,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'accountId': accountId,                # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': True,                         # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': False,                        # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': False,                        # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': operationYear,        # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'infoModel': localInfoModel,           # お知らせデータのモデル
                    'infoLength': 1,                       # お知らせデータのモデルの件数
                }
            else:
                response = {
                    'accountType': 1,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'accountId': accountId,                # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': True,                         # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': False,                        # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': False,                        # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': operationYear,        # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'infoModel': localInfoModel,           # お知らせデータのモデル
                    'infoLength': 0,                       # お知らせデータのモデルの件数
                }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            # ヒント：モデルの場合、len(list(localInfoModel))で件数を取得しようとするとエラーが発生する。
            # ヒント：そのため、以下では、if localInfoModel != Noneで条件分岐させている。
            if localInfoModel != None:
                response = {
                    'accountType': 2,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'accountId': accountId,                # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': False,                        # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': True,                         # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': False,                        # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': operationYear,        # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'infoModel': localInfoModel,           # お知らせデータのモデル
                    'infoLength': 1,                       # お知らせデータのモデルの件数
                }
            else:
                response = {
                    'accountType': 2,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'accountId': accountId,                # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': False,                        # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': True,                         # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': False,                        # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': operationYear,        # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'infoModel': localInfoModel,           # お知らせデータのモデル
                    'infoLength': 0,                       # お知らせデータのモデルの件数
                }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            # ヒント：モデルの場合、len(list(localInfoModel))で件数を取得しようとするとエラーが発生する。
            # ヒント：そのため、以下では、if localInfoModel != Noneで条件分岐させている。
            if localInfoModel != None:
                response = {
                    'accountType': 3,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'accountId': accountId,                # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': False,                        # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': False,                        # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': True,                         # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': operationYear,        # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'infoModel': localInfoModel,           # お知らせデータのモデル
                    'infoLength': 1,                       # お知らせデータのモデルの件数
                }
            else:
                response = {
                    'accountType': 3,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'accountId': accountId,                # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': False,                        # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': False,                        # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': True,                         # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': operationYear,        # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'infoModel': localInfoModel,           # お知らせデータのモデル
                    'infoLength': 0,                       # お知らせデータのモデルの件数
                }
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P03.InfoDetailView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P03.InfoDetailView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P03.InfoDetailView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ０３Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P03.InfoDetailView関数 P02A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P03InfoDetailTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P03InfoDetailTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            return render(request, 'P03InfoDetailTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P03.InfoDetailView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P03.InfoDetailView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ０３Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。。
        print_log('[ERROR] P03.InfoDetailView関数 P03A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P03.InfoDetailView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P03.InfoDetailView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ０３Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P03.InfoDetailView関数 P03A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
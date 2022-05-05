#####################################################################################
# UploadDeleteConfirmViewビューモジュール【ほぼ完成】
# ファイル名：P15.UploadDeleteConfirmView.py（Ｐ１５）
# ユースケース：都道府県は、調査結果の削除を確認＝調査結果または確認結果の削除フラグをオンにする。
# ユースケース：本省は、確認結果の削除を確認＝調査結果または確認結果の削除フラグをオンにする。
# ヒント：調査結果と確認結果は同じフォーム、テーブル、モデル、テンプレートを使用する。
# ヒント：種別・区分フラグで調査結果と確認結果を識別する。
# ヒント：accountTypeはログインした人の種別・区分
# ヒント：KEN_HON_OPE_FLAGはデータ（データを登録した人）の種別・区分
# TO-DO：引数チェックに引っかかった場合、ビュー関数でエラーが発生した場合、テンプレートでレンダリングでエラーが発生した場合に応じ、
# TO-DO：異なるエラー画面を表示することがＵＩ上好ましいと思われる。リリース後の課題として、TO-DO（保留）とする。
# ヒント：ここにこないはずの場合、ERRORとする。また、try exceptの場合も、ERRORとする。（判断基準１）
# ヒント：ユーザが入力した値のチェック、クエリストリング等で引っかかった場合、WARNとする。（判断基準１）
# ヒント：処理継続する場合はWARN、継続しない場合はERRORとする。（判断基準２）
#####################################################################################

#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：パイソンモジュールをインポートする。
# sys：
# datetime：
#####################################################################################
import sys                                                 # sysモジュール
from datetime import datetime                              # datetimeモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：ジャンゴモジュールをインポートする。
# login_required：
# connection：
# transaction：
# render：
# urlquote：
#####################################################################################
from django.contrib.auth.decorators import login_required  # ログイン制御モジュール
from django.db import connection                           # ＤＢ接続モジュール
from django.db import transaction                          # ＤＢトランザクション管理モジュール
from django.shortcuts import render                        # レンダリングモジュール
from django.utils.http import urlquote                     # URLエスケープモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# UploadDeleteConfirmForm：
# AccountModel：
# UploadFileModel：
# print_log：
#####################################################################################
from file_upload.forms import UploadDeleteConfirmForm      # アップロード削除画面用のフォーム
from file_upload.models import AccountModel                # アカウントモデル
from file_upload.models import UploadFileModel             # アップロードファイルモデル
from file_upload.models import UploadModel                 # アップロードモデル
from file_upload.CommonFunction import print_log           # ログ出力モジュール
#####################################################################################
# 関数名：P15.UploadDeleteConfirmView（Ｐ１５Ａ）
# 関数概要：都道府県用調査結果削除確認ページをブラウザに戻す。（都道府県）
# 関数概要：本省用確認結果削除確認ページをブラウザに戻す。（本省）
#
# 引数[1]：request
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※アクセスは想定せず、不正アクセスとしてエラーページを返す。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
# 引数[5]：uploadId：都道府県用調査結果ＩＤ※ＤＢから都道府県用調査結果を取得し、本登録するために使用する。（都道府県）
# 引数[5]：uploadId：本省用確認結果ＩＤ※ＤＢから本省用確認結果を取得し、本登録するために使用する。（本省）
# 引数[5]：uploadId：調査結果または確認結果ＩＤ（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
#
# 戻り値[1]：response
#
# FORM：UploadDeleteConfirmForm：都道府県用調査結果削除確認ページ（都道府県）
# FORM：UploadDeleteConfirmForm：本省用確認結果削除確認ページ（本省）
# FORM：UploadDeleteConfirmForm：運用業者用確認結果削除確認ページ（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：UploadModel：調査結果または確認結果モデル（Ｕ）
# ※accountTypeが都道府県の場合、ページからフォーム経由でデータを取得し、ＤＢセットする。
# ※accountTypeが本省の場合、ページからフォーム経由でデータを取得し、ＤＢにセットする。
# ※accountTypeが運用業者の場合、この機能は提供しないため、エラーページを表示する。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def UploadDeleteConfirmView(request, accountType, accountId, operationYear, kenUploadId, honUploadId, kenHonOpeFlag):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１５Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P15.UploadDeleteConfirmView関数 P15A10', 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmView.kenUploadId = {}'.format(kenUploadId), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmView.honUploadId = {}'.format(honUploadId), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmView.kenHonOpeFlag = {}'.format(kenHonOpeFlag), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１５Ａ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        # （７）本省アップロードＩＤをチェックする。　例　1
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        # チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        if accountId == str(request.user.username):
            pass
        else:
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2':
            pass
        elif accountType == '3':
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-3', 'WARN')
            return render(request, 'error.html')
        else:
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P15.UploadDeleteConfirmlView関数 P15A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-5', 'WARN')
                return render(request, 'error.html')
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        if kenUploadId is None:
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenUploadId) == True:
                pass
            else:
                print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-6', 'WARN')
                return render(request, 'error.html')
        # （７）本省アップロードＩＤをチェックする。　例　1
        if honUploadId is None:
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-7', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(honUploadId) == True:
                pass
            else:
                print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-7', 'WARN')
                return render(request, 'error.html')
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        if kenHonOpeFlag is None:
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-8', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenHonOpeFlag) == True:
                pass
            else:
                print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-8', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ１５Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmView関数 P15A30', 'INFO')
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
                [accountId, operationYear, ])[0]
        except:
            localAccountModel = None
            print_log('[ERROR] P15.UploadDeleteConfirmView関数 P15A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、アップロードデータ取得処理（Ｐ１５Ａ４０）
        # （１）アップロードデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、アップロードデータ、アップロードファイルデータを取得する。
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
        print_log('[INFO] P15.UploadDeleteConfirmView関数 P15A40', 'INFO')
        # （１）アップロードデータ、アップロードファイルデータを格納する局所変数を初期化する。
        localKenUploadModel = None
        localHonUploadModel = None
        localKenUploadFileModel = None
        localHonUploadFileModel = None
        # （２）ＤＢにアクセスし、アップロードデータを取得する。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                if kenHonOpeFlag == '1':
                    # データの種別・区分＝１：都道府県の場合、、、
                    try:
                        localKenUploadModel = UploadModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOAD 
                            WHERE 
                                KEN_UPLOAD_ID=%s AND 
                                KEN_HON_OPE_FLAG='1' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """,
                            [kenUploadId, operationYear, ])[0]
                    except:        
                        localKenUploadModel = None
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数 P15A40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数で警告が発生しました。', 'ERROR')
                    try:    
                        localKenUploadFileModel = UploadFileModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOADFILE
                            WHERE 
                                KEN_UPLOAD_ID=%s AND 
                                KEN_HON_OPE_FLAG='1' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """,
                            [kenUploadId, operationYear, ])[0]
                    except:
                        localKenUploadFileModel = None        
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数 P15A40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数で警告が発生しました。', 'ERROR')
                elif kenHonOpeFlag == '2':
                    # データの種別・区分＝２：本省の場合、、、
                    try:
                        localHonUploadModel = UploadModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOAD
                            WHERE 
                                HON_UPLOAD_ID=%s AND 
                                KEN_HON_OPE_FLAG='2' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """,
                            [honUploadId, operationYear, ])[0]
                    except:
                        localHonUploadModel = None        
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数 P15A40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数で警告が発生しました。', 'ERROR')
                    try:    
                        localHonUploadFileModel = UploadFileModel.objects.raw("""
                            SELECT * FROM file_upload_uploadfile
                            WHERE HON_UPLOAD_ID=%s AND KEN_HON_OPE_FLAG='2' AND OPERATION_YEAR=%s LIMIT 1
                            """,
                            [honUploadId, operationYear, ])[0]
                    except:
                        localHonUploadFileModel = None
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数 P15A40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数で警告が発生しました。', 'ERROR')
                else:
                    # データの種別・区分＝その他の場合、、、
                    pass         
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                if kenHonOpeFlag == '1':
                    # データの種別・区分＝１：都道府県の場合、、、
                    try:
                        localKenUploadModel = UploadModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOAD
                            WHERE 
                                KEN_UPLOAD_ID=%s AND 
                                KEN_HON_OPE_FLAG='1' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """,
                            [kenUploadId, operationYear, ])[0]
                    except:
                        localKenUploadModel = None
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数 P15A40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数で警告が発生しました。', 'ERROR')
                    try:    
                        localKenUploadFileModel = UploadFileModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOADFILE
                            WHERE 
                                KEN_UPLOAD_ID=%s AND 
                                KEN_HON_OPE_FLAG='1' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """,
                            [kenUploadId, operationYear, ])[0]
                    except:
                        localKenUploadFileModel = None
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数 P15A40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数で警告が発生しました。', 'ERROR')
                elif kenHonOpeFlag == '2':
                    # データの種別・区分＝２：本省の場合、、、
                    try:
                        localHonUploadModel = UploadModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOAD
                            WHERE 
                                HON_UPLOAD_ID=%s AND 
                                KEN_HON_OPE_FLAG='2' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """,
                            [honUploadId, operationYear, ])[0]
                    except:
                        localHonUploadModel = None
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数 P15A40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P15.UploadDeleteConfirmView関数で警告が発生しました。', 'ERROR')
                    try:    
                        localHonUploadFileModel = UploadFileModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOADFILE
                            WHERE 
                                HON_UPLOAD_ID=%s AND 
                                KEN_HON_OPE_FLAG='2' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """,
                            [honUploadId, operationYear, ])[0]
                    except:
                        localHonUploadFileModel = None
                        print_log(sys.exc_info()[0], 'ERROR')
                else:
                    # データの種別・区分＝その他の場合、、、
                    pass         
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P15.UploadDeleteConfirmView関数 P12A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # フォームセット処理（Ｐ１５Ａ５０）
        # （１）局所変数のフォームを初期化する。
        # ヒント：ブラウザとのデータのやりとり、特にブラウザからPOSTデータがある場合、フォームを使用する。
        # ヒント：モデルはブラウザで参照用、かつタグをコーディングする場合等に使用する。
        # ヒント：フォームはブラウザで編集用、POSTでサーバにリクエストされる項目、かつタグを自動生成する場合等に使用する。
        # ヒント：表示画面の場合、URL+QUERY STRING、VIEW関数、GET、renderでテンプレートとレスポンスで目的の画面を表示する。
        # ヒント：追加、削除の場合、URL+QUERY STRING+フォーム値、DoVIEW関数、POST、redirect（URL+QUERY STRING）で次の画面に遷移する。
        # ヒント：または、追加、削除の場合、URL+QUERY STRING+フォーム値、DoVIEW関数、POST、renderでテンプレートとレスポンスで元の同じ画面を表示する。
        # ヒント：ただし、この場合、レスポンスに、追加、削除結果のフラグを返し、ブラウザ側（正確にはサーバでのレンダリング時＝HTML生成時）で通常画面と結果画面をフラグを見て分岐処理するようにテンプレートを記述する。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmView関数 P15A50', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localUploadDeleteConfirmForm = UploadDeleteConfirmForm()
        ##########################################            
        # フォームセット処理（Ｐ１５Ａ５２）
        # （１）局所変数のフォームにＤＢのアップロードテーブルから取得した値をセットする。（都道府県項目）
        # （２）局所変数のフォームにＤＢのアップロードファイルテーブルから取得した値をセットする。（都道府県項目）
        # ヒント：「!= None」でオブジェクトのインスタンスが生成済み＝存在していることを確認する。
        # ヒント：上記チェック処理を行い、実行時エラーの発生を防止する。
        # ヒント：これを実現するために、変数を初期化し、ＤＢアクセス時のエクセプション発生時にも、変数の初期化を確実に行う。
        ##########################################            
        # （１）局所変数のフォームにＤＢのアップロードテーブルから取得した値をセットする。（都道府県項目）
        if localKenUploadModel != None:
            localUploadDeleteConfirmForm.initial['KEN_UPLOAD_ID'] = localKenUploadModel.KEN_UPLOAD_ID
            localUploadDeleteConfirmForm.initial['KEN_KEN_HON_OPE_FLAG'] = localKenUploadModel.KEN_HON_OPE_FLAG
            localUploadDeleteConfirmForm.initial['KEN_OPERATION_YEAR'] = localKenUploadModel.OPERATION_YEAR
            localUploadDeleteConfirmForm.initial['KEN_FLOOD_YEAR'] = localKenUploadModel.FLOOD_YEAR
            localUploadDeleteConfirmForm.initial['KEN_ORG_CODE'] = localKenUploadModel.ORG_CODE
            localUploadDeleteConfirmForm.initial['KEN_ORG_NAME'] = localKenUploadModel.ORG_NAME
            localUploadDeleteConfirmForm.initial['KEN_DEPT_CODE'] = localKenUploadModel.DEPT_CODE
            localUploadDeleteConfirmForm.initial['KEN_DEPT_NAME'] = localKenUploadModel.DEPT_NAME
            localUploadDeleteConfirmForm.initial['KEN_ACCOUNT_ID'] = localKenUploadModel.ACCOUNT_ID
            localUploadDeleteConfirmForm.initial['KEN_ACCOUNT_NAME'] = localKenUploadModel.ACCOUNT_NAME
            localUploadDeleteConfirmForm.initial['KEN_ADD_DATE'] = localKenUploadModel.ADD_DATE
            localUploadDeleteConfirmForm.initial['KEN_ADD_DATE_TIME'] = localKenUploadModel.ADD_DATE_TIME
            localUploadDeleteConfirmForm.initial['KEN_ADD_FLAG'] = localKenUploadModel.ADD_FLAG
            localUploadDeleteConfirmForm.initial['KEN_DELETE_DATE'] = localKenUploadModel.DELETE_DATE
            localUploadDeleteConfirmForm.initial['KEN_DELETE_DATE_TIME'] = localKenUploadModel.DELETE_DATE_TIME
            localUploadDeleteConfirmForm.initial['KEN_DELETE_FLAG'] = localKenUploadModel.DELETE_FLAG
            localUploadDeleteConfirmForm.initial['KEN_QUESTION_BODY'] = localKenUploadModel.QUESTION_BODY
            localUploadDeleteConfirmForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = localKenUploadModel.QUESTION_TO_HON_OPE_FLAG
        else:
            localUploadDeleteConfirmForm.initial['KEN_UPLOAD_ID'] = ""
            localUploadDeleteConfirmForm.initial['KEN_KEN_HON_OPE_FLAG'] = ""
            localUploadDeleteConfirmForm.initial['KEN_OPERATION_YEAR'] = ""
            localUploadDeleteConfirmForm.initial['KEN_FLOOD_YEAR'] = ""
            localUploadDeleteConfirmForm.initial['KEN_ORG_CODE'] = ""
            localUploadDeleteConfirmForm.initial['KEN_ORG_NAME'] = ""
            localUploadDeleteConfirmForm.initial['KEN_DEPT_CODE'] = ""
            localUploadDeleteConfirmForm.initial['KEN_DEPT_NAME'] = ""
            localUploadDeleteConfirmForm.initial['KEN_ACCOUNT_ID'] = ""
            localUploadDeleteConfirmForm.initial['KEN_ACCOUNT_NAME'] = ""
            localUploadDeleteConfirmForm.initial['KEN_ADD_DATE'] = ""
            localUploadDeleteConfirmForm.initial['KEN_ADD_DATE_TIME'] = ""
            localUploadDeleteConfirmForm.initial['KEN_ADD_FLAG'] = ""
            localUploadDeleteConfirmForm.initial['KEN_DELETE_DATE'] = ""
            localUploadDeleteConfirmForm.initial['KEN_DELETE_DATE_TIME'] = ""
            localUploadDeleteConfirmForm.initial['KEN_DELETE_FLAG'] = ""
            localUploadDeleteConfirmForm.initial['KEN_QUESTION_BODY'] = ""
            localUploadDeleteConfirmForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = ""
        # （２）局所変数のフォームにＤＢのアップロードファイルテーブルから取得した値をセットする。（都道府県項目）
        if localKenUploadFileModel != None:
            localUploadDeleteConfirmForm.initial['KEN_UPLOAD_FILE_ID'] = localKenUploadFileModel.KEN_UPLOAD_FILE_ID
            localUploadDeleteConfirmForm.initial['KEN_UPLOAD_FILE_NAME'] = localKenUploadFileModel.KEN_UPLOAD_FILE_NAME
            localUploadDeleteConfirmForm.initial['KEN_UPLOAD_FILE_PATH'] = localKenUploadFileModel.KEN_UPLOAD_FILE_PATH
        else:
            localUploadDeleteConfirmForm.initial['KEN_UPLOAD_FILE_ID'] = ""
            localUploadDeleteConfirmForm.initial['KEN_UPLOAD_FILE_NAME'] = ""
            localUploadDeleteConfirmForm.initial['KEN_UPLOAD_FILE_PATH'] = ""
        ##########################################            
        # フォームセット処理（Ｐ１５Ａ５４）
        # （１）局所変数のフォームにＤＢのアップロードテーブルから取得した値をセットする。（本省項目）
        # （２）局所変数のフォームにＤＢのアップロードファイルテーブルから取得した値をセットする。（本省項目）
        # ヒント：「!= None」でオブジェクトのインスタンスが生成済み＝存在していることを確認する。
        # ヒント：上記チェック処理を行い、実行時エラーの発生を防止する。
        # ヒント：これを実現するために、変数を初期化し、ＤＢアクセス時のエクセプション発生時にも、変数の初期化を確実に行う。
        ##########################################
        # （１）局所変数のフォームにＤＢのアップロードテーブルから取得した値をセットする。（本省項目）
        if localHonUploadModel != None:    
            localUploadDeleteConfirmForm.initial['HON_UPLOAD_ID'] = localHonUploadModel.HON_UPLOAD_ID
            localUploadDeleteConfirmForm.initial['HON_KEN_HON_OPE_FLAG'] = localHonUploadModel.KEN_HON_OPE_FLAG
            localUploadDeleteConfirmForm.initial['HON_OPERATION_YEAR'] = localHonUploadModel.OPERATION_YEAR
            localUploadDeleteConfirmForm.initial['HON_FLOOD_YEAR'] = localHonUploadModel.FLOOD_YEAR
            localUploadDeleteConfirmForm.initial['HON_ORG_CODE'] = localHonUploadModel.ORG_CODE
            localUploadDeleteConfirmForm.initial['HON_ORG_NAME'] = localHonUploadModel.ORG_NAME
            localUploadDeleteConfirmForm.initial['HON_DEPT_CODE'] = localHonUploadModel.DEPT_CODE
            localUploadDeleteConfirmForm.initial['HON_DEPT_NAME'] = localHonUploadModel.DEPT_NAME
            localUploadDeleteConfirmForm.initial['HON_ACCOUNT_ID'] = localHonUploadModel.ACCOUNT_ID
            localUploadDeleteConfirmForm.initial['HON_ACCOUNT_NAME'] = localHonUploadModel.ACCOUNT_NAME
            localUploadDeleteConfirmForm.initial['HON_ADD_DATE'] = localHonUploadModel.ADD_DATE
            localUploadDeleteConfirmForm.initial['HON_ADD_DATE_TIME'] = localHonUploadModel.ADD_DATE_TIME
            localUploadDeleteConfirmForm.initial['HON_ADD_FLAG'] = localHonUploadModel.ADD_FLAG
            localUploadDeleteConfirmForm.initial['HON_DELETE_DATE'] = localHonUploadModel.DELETE_DATE
            localUploadDeleteConfirmForm.initial['HON_DELETE_DATE_TIME'] = localHonUploadModel.DELETE_DATE_TIME
            localUploadDeleteConfirmForm.initial['HON_DELETE_FLAG'] = localHonUploadModel.DELETE_FLAG
            localUploadDeleteConfirmForm.initial['HON_QUESTION_BODY'] = localHonUploadModel.QUESTION_BODY
            localUploadDeleteConfirmForm.initial['HON_QUESTION_TO_HON_OPE_FLAG'] = localHonUploadModel.QUESTION_TO_HON_OPE_FLAG
        else:
            localUploadDeleteConfirmForm.initial['HON_UPLOAD_ID'] = ""
            localUploadDeleteConfirmForm.initial['HON_KEN_HON_OPE_FLAG'] = ""
            localUploadDeleteConfirmForm.initial['HON_OPERATION_YEAR'] = ""
            localUploadDeleteConfirmForm.initial['HON_FLOOD_YEAR'] = ""
            localUploadDeleteConfirmForm.initial['HON_ORG_CODE'] = ""
            localUploadDeleteConfirmForm.initial['HON_ORG_NAME'] = ""
            localUploadDeleteConfirmForm.initial['HON_DEPT_CODE'] = ""
            localUploadDeleteConfirmForm.initial['HON_DEPT_NAME'] = ""
            localUploadDeleteConfirmForm.initial['HON_ACCOUNT_ID'] = ""
            localUploadDeleteConfirmForm.initial['HON_ACCOUNT_NAME'] = ""
            localUploadDeleteConfirmForm.initial['HON_ADD_DATE'] = ""
            localUploadDeleteConfirmForm.initial['HON_ADD_DATE_TIME'] = ""
            localUploadDeleteConfirmForm.initial['HON_ADD_FLAG'] = ""
            localUploadDeleteConfirmForm.initial['HON_DELETE_DATE'] = ""
            localUploadDeleteConfirmForm.initial['HON_DELETE_DATE_TIME'] = ""
            localUploadDeleteConfirmForm.initial['HON_DELETE_FLAG'] = ""
            localUploadDeleteConfirmForm.initial['HON_QUESTION_BODY'] = ""
            localUploadDeleteConfirmForm.initial['HON_QUESTION_TO_HON_OPE_FLAG'] = ""
        # （２）局所変数のフォームにＤＢのアップロードファイルテーブルから取得した値をセットする。（本省項目）
        if localHonUploadFileModel != None:
            localUploadDeleteConfirmForm.initial['HON_UPLOAD_FILE_ID'] = localHonUploadFileModel.HON_UPLOAD_FILE_ID
            localUploadDeleteConfirmForm.initial['HON_UPLOAD_FILE_NAME'] = localHonUploadFileModel.HON_UPLOAD_FILE_NAME
            localUploadDeleteConfirmForm.initial['HON_UPLOAD_FILE_PATH'] = localHonUploadFileModel.HON_UPLOAD_FILE_PATH
        else:
            localUploadDeleteConfirmForm.initial['HON_UPLOAD_FILE_ID'] = ""
            localUploadDeleteConfirmForm.initial['HON_UPLOAD_FILE_NAME'] = ""
            localUploadDeleteConfirmForm.initial['HON_UPLOAD_FILE_PATH'] = ""
        ##########################################            
        # フォームセット処理（Ｐ１５Ａ５６）
        # （１）フォームのウィジェットの属性に値をセットする。（都道府県項目）
        # （２）フォームのウィジェットの属性に値をセットする。（本省項目）
        # ヒント：利用者が編集できない項目は、disabled、readonlyのいずれかとする。
        # ヒント：フォームを使用した場合、ブラウザでタグが自動生成されるため、ブラウザのstyle、cssでdisable、readonlyをセットしにくい。
        # ヒント：そのため。ビュー関数でdisable、readonly等をセットする。
        # ヒント：フォームのフィールドは、非表示の項目もセットすることを推奨する。
        # ヒント：ステートレスなウェブアプリにおいて、ブラウザに送ったデータをPOST時にサーバ側のビュー関数で参照可能とするため。
        ##########################################            
        # （１）フォームのウィジェットの属性に値をセットする。（都道府県項目）
        localUploadDeleteConfirmForm.fields['KEN_UPLOAD_ID'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_KEN_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_OPERATION_YEAR'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_FLOOD_YEAR'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_ORG_CODE'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_ORG_NAME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_DEPT_CODE'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_DEPT_NAME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_ACCOUNT_ID'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_ACCOUNT_NAME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_ADD_DATE'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_ADD_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_ADD_FLAG'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_DELETE_DATE'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_DELETE_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_DELETE_FLAG'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_UPLOAD_FILE_ID'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_UPLOAD_FILE_NAME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_UPLOAD_FILE_PATH'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_QUESTION_BODY'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['KEN_QUESTION_TO_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        # （２）フォームのウィジェットの属性に値をセットする。（本省項目）
        localUploadDeleteConfirmForm.fields['HON_UPLOAD_ID'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_KEN_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_OPERATION_YEAR'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_FLOOD_YEAR'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_ORG_CODE'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_ORG_NAME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_DEPT_CODE'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_DEPT_NAME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_ACCOUNT_ID'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_ACCOUNT_NAME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_ADD_DATE'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_ADD_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_ADD_FLAG'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_DELETE_DATE'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_DELETE_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_DELETE_FLAG'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_UPLOAD_FILE_ID'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_UPLOAD_FILE_NAME'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_UPLOAD_FILE_PATH'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_QUESTION_BODY'].widget.attrs['readonly'] = True
        localUploadDeleteConfirmForm.fields['HON_QUESTION_TO_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        ##########################################
        # レスポンスセット処理（Ｐ１５Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmView関数 P15A60', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            response = {
                'accountType': 1,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': True,                             # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'wasDeleted': False,                       # 
                'operationYear': urlquote(operationYear),  #  調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'uploadDeleteConfirmForm': localUploadDeleteConfirmForm, # アップロードデータ削除確認画面用のフォーム
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'wasDeleted': False,                       # 削除済グラフ、０、１：未削除、５：削除済
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'uploadDeleteConfirmForm': localUploadDeleteConfirmForm, # アップロードデータ削除確認画面用のフォーム
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P15.UploadDeleteConfirmView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１５Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmView関数 P15A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P15UploadDeleteConfirmTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P15UploadDeleteConfirmTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ１５Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P15.UploadDeleteConfirmView関数 P15A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P15.UploadDeleteConfirmView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P15.UploadDeleteConfirmView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１５Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmView関数 P15A90', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
#####################################################################################
# 関数名：P15.UploadDeleteConfirmDoView（Ｐ１５Ｂ）
# 関数概要：都道府県用調査結果削除確認ページをでセットされた値をＤＢに本登録する。（都道府県）
# 関数概要：本省用確認結果削除確認ページをでセットされた値をＤＢに本登録する。（本省）
#
# 引数[1]：request
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※アクセスは想定せず、不正アクセスとしてエラーページを返す。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
# 引数[5]：uploadId：都道府県用調査結果ＩＤ（都道府県）※ＤＢから都道府県用調査結果を取得し、本登録するために使用する。（都道府県）
# 引数[5]：uploadId：本省用確認結果ＩＤ（本省）※ＤＢから本省用確認結果を取得し、本登録するために使用する。（本省）
# 引数[5]：uploadId：調査結果または確認結果ＩＤ（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
#
# 戻り値[1]：response
#
# FORM：UploadDeleteConfirmForm：都道府県用調査結果削除確認ページ（都道府県）
# FORM：UploadDeleteConfirmForm：本省用確認結果削除確認ページ（本省）
# FORM：UploadDeleteConfirmForm：運用業者用確認結果削除確認ページ（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：UploadModel：調査結果または確認結果モデル（Ｕ）
# ヒント：accountTypeが都道府県の場合、ページからフォーム経由でデータを取得し、ＤＢにセットする。
# ヒント：accountTypeが本省の場合、ページからフォーム経由でデータを取得し、ＤＢにセットする。
# ヒント：accountTypeが運用業者の場合、この機能は提供しないため、エラーページを表示する。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def UploadDeleteConfirmDoView(request, accountType, accountId, operationYear, kenUploadId, honUploadId, kenHonOpeFlag):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmDoView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１５Ｂ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P15.UploadDeleteConfirmDoView関数 P15B10', 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmDoView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmDoView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmDoView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmDoView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmDoView.kenUploadId = {}'.format(kenUploadId), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmDoView.honUploadId = {}'.format(honUploadId), 'INFO')
        print_log('[INFO] P15.UploadDeleteConfirmDoView.kenHonOpeFlag = {}'.format(kenHonOpeFlag), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１５Ｂ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        # （７）本省アップロードＩＤをチェックする。　例　1
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        # チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        if accountId == str(request.user.username):
            pass
        else:
            print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'POST':
            pass
        else:
            print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2':
            pass
        elif accountType == '3':
            print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-3', 'WARN')
            return render(request, 'error.html')
        else:
            print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-5', 'WARN')
                return render(request, 'error.html')
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        if kenUploadId is None:
            print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenUploadId) == True:
                pass
            else:
                print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-6', 'WARN')
                return render(request, 'error.html')
        # （７）本省アップロードＩＤをチェックする。　例　1
        if honUploadId is None:
            print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-7', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(honUploadId) == True:
                pass
            else:
                print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B20-7', 'WARN')
                return render(request, 'error.html')
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        if kenHonOpeFlag is None:
            print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-8', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenHonOpeFlag) == True:
                pass
            else:
                print_log('[WARN] P15.UploadDeleteConfirmView関数 P15A20-8', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ１５Ｂ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmDoView関数 P15B30', 'INFO')
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
                [accountId, operationYear, ])[0]
        except:
            localAccountModel = None
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数 P15B30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # アカウント種別がアカウントＩＤのアカウント種別と同じことをチェックする。            
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P15.UploadDeleteConfirmDoView関数 P15B30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # フォームデータチェック処理、局所変数セット処理（Ｐ１５Ｂ４０）
        # （１）ブラウザからポストされたデータを格納する変数を初期化する。
        # （２）画面からポストされた情報を取得する。（本省）
        # ※運用業者の場合は、ここにはこないと想定する。return済。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmDoView関数 P15B40', 'INFO')
        # （１）ブラウザからポストされたデータを格納する変数を初期化する。
        localForm = None
        localDeleteConfirmForm = UploadDeleteConfirmForm()
        # （２）バリデーション済のデータを局所変数にセットする。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                localForm = UploadDeleteConfirmForm(request.POST, request.FILES)
                if localForm.is_valid():
                    localDeleteConfirmForm.KEN_UPLOAD_ID = localForm.cleaned_data['KEN_UPLOAD_ID']
                    localDeleteConfirmForm.KEN_KEN_HON_OPE_FLAG = '1'
                    localDeleteConfirmForm.KEN_OPERATION_YEAR = localForm.cleaned_data['KEN_OPERATION_YEAR']
                    localDeleteConfirmForm.KEN_FLOOD_YEAR = localForm.cleaned_data['KEN_FLOOD_YEAR']
                    localDeleteConfirmForm.KEN_ORG_CODE = localForm.cleaned_data['KEN_ORG_CODE']
                    localDeleteConfirmForm.KEN_ORG_NAME = localForm.cleaned_data['KEN_ORG_NAME']
                    localDeleteConfirmForm.KEN_DEPT_CODE = localForm.cleaned_data['KEN_DEPT_CODE']
                    localDeleteConfirmForm.KEN_DEPT_NAME = localForm.cleaned_data['KEN_DEPT_NAME']
                    localDeleteConfirmForm.KEN_ACCOUNT_ID = localForm.cleaned_data['KEN_ACCOUNT_ID']
                    localDeleteConfirmForm.KEN_ACCOUNT_NAME = localForm.cleaned_data['KEN_ACCOUNT_NAME']
                    localDeleteConfirmForm.KEN_ADD_DATE = localForm.cleaned_data['KEN_ADD_DATE']
                    localDeleteConfirmForm.KEN_ADD_DATE_TIME = localForm.cleaned_data['KEN_ADD_DATE_TIME']
                    localDeleteConfirmForm.KEN_ADD_FLAG = localForm.cleaned_data['KEN_ADD_FLAG']
                    localDeleteConfirmForm.KEN_DELETE_DATE = localForm.cleaned_data['KEN_DELETE_DATE']
                    localDeleteConfirmForm.KEN_DELETE_DATE_TIME = localForm.cleaned_data['KEN_DELETE_DATE_TIME']
                    localDeleteConfirmForm.KEN_DELETE_FLAG = localForm.cleaned_data['KEN_DELETE_FLAG']
                    localDeleteConfirmForm.KEN_UPLOAD_FILE_ID = localForm.cleaned_data['KEN_UPLOAD_FILE_ID']
                    localDeleteConfirmForm.KEN_UPLOAD_FILE_NAME = localForm.cleaned_data['KEN_UPLOAD_FILE_NAME']
                    localDeleteConfirmForm.KEN_UPLOAD_FILE_PATH = localForm.cleaned_data['KEN_UPLOAD_FILE_PATH']
                    localDeleteConfirmForm.KEN_QUESTION_BODY = localForm.cleaned_data['KEN_QUESTION_BODY']
                    localDeleteConfirmForm.KEN_QUESTION_TO_HON_OPE_FLAG = localForm.cleaned_data['KEN_QUESTION_TO_HON_OPE_FLAG']
                else:
                    pass
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                localForm = UploadDeleteConfirmForm(request.POST, request.FILES)
                if localForm.is_valid():
                    localDeleteConfirmForm.HON_UPLOAD_ID = localForm.cleaned_data['HON_UPLOAD_ID']
                    localDeleteConfirmForm.HON_KEN_HON_OPE_FLAG = '2'
                    localDeleteConfirmForm.HON_OPERATION_YEAR = localForm.cleaned_data['HON_OPERATION_YEAR']
                    localDeleteConfirmForm.HON_FLOOD_YEAR = localForm.cleaned_data['HON_FLOOD_YEAR']
                    localDeleteConfirmForm.HON_ORG_CODE = localForm.cleaned_data['HON_ORG_CODE']
                    localDeleteConfirmForm.HON_ORG_NAME = localForm.cleaned_data['HON_ORG_NAME']
                    localDeleteConfirmForm.HON_DEPT_CODE = localForm.cleaned_data['HON_DEPT_CODE']
                    localDeleteConfirmForm.HON_DEPT_NAME = localForm.cleaned_data['HON_DEPT_NAME']
                    localDeleteConfirmForm.HON_ACCOUNT_ID = localForm.cleaned_data['HON_ACCOUNT_ID']
                    localDeleteConfirmForm.HON_ACCOUNT_NAME = localForm.cleaned_data['HON_ACCOUNT_NAME']
                    localDeleteConfirmForm.HON_ADD_DATE = localForm.cleaned_data['HON_ADD_DATE']
                    localDeleteConfirmForm.HON_ADD_DATE_TIME = localForm.cleaned_data['HON_ADD_DATE_TIME']
                    localDeleteConfirmForm.HON_ADD_FLAG = localForm.cleaned_data['HON_ADD_FLAG']
                    localDeleteConfirmForm.HON_DELETE_DATE = localForm.cleaned_data['HON_DELETE_DATE']
                    localDeleteConfirmForm.HON_DELETE_DATE_TIME = localForm.cleaned_data['HON_DELETE_DATE_TIME']
                    localDeleteConfirmForm.HON_DELETE_FLAG = localForm.cleaned_data['HON_DELETE_FLAG']
                    localDeleteConfirmForm.HON_UPLOAD_FILE_ID = localForm.cleaned_data['HON_UPLOAD_FILE_ID']
                    localDeleteConfirmForm.HON_UPLOAD_FILE_NAME = localForm.cleaned_data['HON_UPLOAD_FILE_NAME']
                    localDeleteConfirmForm.HON_UPLOAD_FILE_PATH = localForm.cleaned_data['HON_UPLOAD_FILE_PATH']
                    localDeleteConfirmForm.HON_QUESTION_BODY = localForm.cleaned_data['HON_QUESTION_BODY']
                    localDeleteConfirmForm.HON_QUESTION_TO_HON_OPE_FLAG = localForm.cleaned_data['HON_QUESTION_TO_HON_OPE_FLAG']
                else:
                    pass
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数 P15B40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # フォームセット処理（Ｐ１５Ｂ５０）
        # （１）画面からポストされた情報をチェックする。
        # ヒント：運用業者の場合は、ここにはこないと想定する。return済。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmDoView関数 P15B50', 'INFO')
        ##########################################
        # ＤＢアクセス処理、アップロードデータ削除処理（＝削除フラグを５にセット）（Ｐ１５Ａ６０）
        # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
        # （２）ＳＱＬ文を実行する。
        # （３）トランザクション管理でコミットする。
        # （４）ＤＢ接続を切断＝カーソルを閉じる。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：運用業者の場合は、ここにはこないと想定する。return済。
        # ヒント：rawはUPDATE文では使えないため、カーソルを利用する。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmDoView関数 P15B60', 'INFO')
        localDeleteDate = datetime.now().strftime("%Y/%m/%d")
        localDeleteDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        try:
            # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
            # （２）ＳＱＬ文を実行する。
            # （３）トランザクション管理でコミットする。
            localCursor = connection.cursor()
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                # ヒント：file_upload_uploadテーブルのレコードを更新する。（削除フラグの状態＝本削除済＝５）
                # ヒント：本削除済とは、レコードは登録済、ＩＤも発行済、削除フラグが本削除済＝５の状態をいう。
                try:
                    localCursor.execute("""
                        UPDATE FILE_UPLOAD_UPLOAD 
                            SET 
                            DELETE_DATE = %s,
                            DELETE_DATE_TIME = %s,  
                            DELETE_FLAG = '5'
                        WHERE 
                            KEN_UPLOAD_ID=%s AND 
                            KEN_HON_OPE_FLAG='1' AND 
                            OPERATION_YEAR=%s
                        """, 
                        [ localDeleteDate, 
                          localDeleteDateTime, 
                          kenUploadId, 
                          operationYear, ])
                    transaction.commit()
                except:
                    transaction.rollback()
                    print_log('[ERROR] P15.UploadDeleteConfirmDoView関数 P15B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P15.UploadDeleteConfirmDoView関数で警告が発生しました。', 'ERROR')
                try:    
                    localCursor.execute("""
                        UPDATE FILE_UPLOAD_UPLOADFILE 
                            SET 
                            DELETE_DATE = %s,
                            DELETE_DATE_TIME = %s,  
                            DELETE_FLAG = '5'
                        WHERE 
                            KEN_UPLOAD_ID=%s AND 
                            KEN_HON_OPE_FLAG='1' AND 
                            OPERATION_YEAR=%s 
                        """, 
                        [ localDeleteDate, 
                          localDeleteDateTime, 
                          kenUploadId, 
                          operationYear, ])
                    transaction.commit()
                except:    
                    transaction.rollback()
                    print_log('[ERROR] P15.UploadDeleteConfirmDoView関数 P15B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P15.UploadDeleteConfirmDoView関数で警告が発生しました。', 'ERROR')
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                # ヒント：file_upload_uploadテーブルのレコードを更新する。（削除フラグの状態＝本削除済＝５）
                # ヒント：本削除済とは、レコードは登録済、ＩＤも発行済、削除フラグが本削除済＝５の状態をいう。
                try:
                    localCursor.execute("""
                        UPDATE FILE_UPLOAD_UPLOAD 
                            SET 
                            DELETE_DATE = %s,
                            DELETE_DATE_TIME = %s,  
                            DELETE_FLAG = '5'
                        WHERE 
                            HON_UPLOAD_ID=%s AND 
                            KEN_HON_OPE_FLAG='2' AND 
                            OPERATION_YEAR=%s
                        """, 
                        [ localDeleteDate, 
                          localDeleteDateTime, 
                          honUploadId, 
                          operationYear, ])
                    transaction.commit()
                except:    
                    transaction.rollback()
                    print_log('[ERROR] P15.UploadDeleteConfirmDoView関数 P15B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P15.UploadDeleteConfirmDoView関数で警告が発生しました。', 'ERROR')
                try:    
                    localCursor.execute("""
                        UPDATE FILE_UPLOAD_UPLOADFILE 
                            SET 
                            DELETE_DATE = %s,
                            DELETE_DATE_TIME = %s,  
                            DELETE_FLAG = '5'
                        WHERE 
                            HON_UPLOAD_ID=%s AND 
                            KEN_HON_OPE_FLAG='2' AND 
                            OPERATION_YEAR=%s
                        """, 
                        [ localDeleteDate, 
                          localDeleteDateTime, 
                          honUploadId, 
                          operationYear, ])
                    transaction.commit()
                except:    
                    transaction.rollback()
                    print_log('[ERROR] P15.UploadDeleteConfirmDoView関数 P15B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P15.UploadDeleteConfirmDoView関数で警告が発生しました。', 'ERROR')
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数 P13B60', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        finally:
            # （４）ＤＢ接続を切断＝カーソルを閉じる。
            localCursor.close()
        ##########################################
        # レスポンスセット処理（Ｐ１５Ｂ７０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        # ヒント：accountType：１：都道府県、２：本省、３：運用業者
        # ヒント：accountId：　例　01hokkai
        # ヒント：isKen：True：都道府県でログインしている、False：都道府県でログインしていない
        # ヒント：isHon：True：本省でログインしている、False：本省でログインしていない
        # ヒント：isOpe：True：運用業者でログインしている、False：運用業者でログインしていない
        # ヒント：wasDeleted：GETとPOSTで同じテンプレートを使用し、テンプレート内で処理を分岐するために使用する。　例　True：POSTの結果、False：削除画面の表示＝GET
        # ヒント：operationYear：調査実施年
        # ヒント：message：元の削除確認画面で、このメッセージの文字列（＝ＤＢアクセス処理の結果）を表示する。
        # ヒント：DeleteConfirmForm：テンプレートで使用するフォームのデータをセットする。
        # ヒント：isKen、isHon、isOpeは１つが必ずTrue、２つが必ずFalseを想定する。
        ##########################################
        print_log('[INFO] P15.UpdateDeleteConfirmDoView関数 P15B70', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            response = {
                'accountType': 1,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': accountId,                    # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': True,                             # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'wasDeleted': True,                        # 削除済フラグをTrueにセットする。テンプレートで画面表示処理を分岐するために使用する。
                'operationYear': operationYear,            # 調査実施年
                'message': '都道府県が登録したファイルをデータベースから削除しました。', # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'DeleteConfirmForm': localDeleteConfirmForm, # アップロードデータ削除確認画面用のフォーム
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': accountId,                    # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'wasDeleted': True,                        # 削除済フラグをTrueにセットする。テンプレートで画面表示処理を分岐するために使用する。
                'operationYear': operationYear,            # 調査実施年
                'message': '本省が登録したファイルをデータベースから削除しました。', # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'DeleteConfirmForm': localDeleteConfirmForm, # アップロードデータ削除確認画面用のフォーム
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、    
            print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P15.UploadDeleteConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P15.UploadDeleteConfirmDoView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１５Ｂ８０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmDoView関数 P15B80', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P15UploadDeleteConfirmTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P15UploadDeleteConfirmTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P15.UploadDeleteConfirmDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ１５Ｂ９０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P15.UploadDeleteConfirmDoView関数 P15B90', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P15.UploadDeleteConfirmDoView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P15.UploadDeleteConfirmDoView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１５Ｂ１００）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P15.UploadDeleteConfirmDoView関数 P15B100', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
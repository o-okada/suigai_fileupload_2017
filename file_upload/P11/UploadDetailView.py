#####################################################################################
# UploadDetailViewビューモジュール【ほぼ完成】
# ファイル名：P11.UploadDetailView.py（Ｐ１１）
# ユースケース：都道府県は、調査結果または確認結果を閲覧する。
# ユースケース：本省は、調査結果または確認結果を閲覧する。
# ユースケース：運用業者は、調査結果または確認結果を閲覧する。
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
# os：
# shutil:ファイルコピー関数のshutil.copy2()を使用するためにインポートする。
# sys：
#####################################################################################
import os                                                  # osモジュール
import shutil                                              # shutilモジュール
import sys                                                 # sysモジュール
from datetime import datetime                              # datetimeモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：ジャンゴモジュールをインポートする。
# login_required：
# HttpResponse：
# render：
# smart_str：
# urlquote：
#####################################################################################
from django.contrib.auth.decorators import login_required  # ログイン制御モジュール
from django.db import connection                           # ＤＢ接続モジュール
from django.db import transaction                          # トランザクション管理モジュール
from django.http.response import HttpResponse              # レスポンスモジュール
from django.shortcuts import render                        # レンダリングモジュール
from django.utils.encoding import smart_str                # URLエスケープモジュール
from django.utils.http import urlquote                     # URLエスケープモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# print_log：
# UploadDetailForm：
# AccountModel：
# UploadFileModel：
# UploadModel：
#####################################################################################
from file_upload.CommonFunction import print_log           # ログ出力モジュール
from file_upload.forms import UploadDetailForm             # アップロード詳細画面用のフォーム
from file_upload.models import AccountModel                # アカウントデータモデル
from file_upload.models import UploadFileModel             # アップロードファイルデータモデル
from file_upload.models import UploadModel                 # アップロードデータモデル
#####################################################################################
# 関数名：P11.UploadDetailView（Ｐ１１Ａ）
# 関数概要：都道府県用調査結果または確認結果詳細ページをブラウザに戻す。（都道府県）
# 関数概要：本省用調査結果または確認結果詳細ページをブラウザに戻す。（本省）
# 関数概要：運用業者用調査結果または確認結果詳細ページをブラウザに戻す。（運用業者）
#
# 引数[1]：request：
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから運用業者名、運用部署名、運用業者名を取得するために使用する。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）
# 引数[5]：uploadId：都道府県用調査結果または確認結果詳細ＩＤ※ＤＢから都道府県用調査結果または確認結果を取得するために使用する。（都道府県）
# 引数[5]：uploadId：本省用調査結果または確認結果詳細ＩＤ※ＤＢから本省用調査結果または確認結果を取得するために使用する。（本省）
# 引数[5]：uploadId：運用業者用調査結果または確認結果詳細ＩＤ※ＤＢから運用業者用調査結果または確認結果を取得するために使用する。（運用業者）
#
# ※uploadIdには、都道府県がアップロードしたIDをセットすること
# ※DBではfile_upload_uploadテーブルの通り、都道府県がアップロードしたデータと本省がアップロードしたデータを別レコードとして扱うが、
# ※python、templateでは、これをペア、つまり２レコードで１レコードとして扱うことに注意すること。
# ※SQL文でparent_idを使用してAAAの項目をKEN_AAA、HON_AAA等と拡張する。
# ※SQL文で取得する場合、KENがアップロードしたデータのIDを仮のidとすること。model.object.raw等でidが必要とのエラーが表示されるため。
#
# 戻り値[1]：response：
#
# FORM：UploadDetailForm：都道府県用調査結果または確認結果詳細ページ（都道府県）
# FORM：UploadDetailForm：本省用調査結果または確認結果詳細ページ（本省）
# FORM：UploadDetailForm：運用業者用調査結果または確認結果詳細ページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：UploadModel：調査結果または確認結果モデル（Ｒ）
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def UploadDetailView(request, accountType, accountId, operationYear, kenUploadId, honUploadId, kenHonOpeFlag):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P11.UploadDetailView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１１Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P11.UploadDetailView関数 P11A10', 'INFO')
        print_log('[INFO] P11.UploadDetailView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P11.UploadDetailView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P11.UploadDetailView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P11.UploadDetailView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P11.UploadDetailView.kenUploadId = {}'.format(kenUploadId), 'INFO')
        print_log('[INFO] P11.UploadDetailView.honUploadId = {}'.format(honUploadId), 'INFO')
        print_log('[INFO] P11.UploadDetailView.kenHonOpeFlag = {}'.format(kenHonOpeFlag), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１１Ａ２０）
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
            print_log('[WARN] P11.UploadDetailView関数 P11A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P11.UploadDetailView関数 P11A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P11.UploadDetailView関数 P11A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P11.UploadDetailView関数 P11A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P11.UploadDetailView関数 P11A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P11.UploadDetailView関数 P11A20-5', 'WARN')
                return render(request, 'error.html')
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        if kenUploadId is None:
            print_log('[WARN] P11.UploadDetailView関数 P11A20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenUploadId) == True:
                pass
            else:
                print_log('[WARN] P11.UploadDetailView関数 P11A20-6', 'WARN')
                return render(request, 'error.html')
        # （７）本省アップロードＩＤをチェックする。　例　1
        if honUploadId is None:
            print_log('[WARN] P11.UploadDetailView関数 P11A20-7', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(honUploadId) == True:
                pass
            else:
                print_log('[WARN] P11.UploadDetailView関数 P11A20-7', 'WARN')
                return render(request, 'error.html')
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        if kenHonOpeFlag is None:
            print_log('[WARN] P11.UploadDetailView関数 P11A20-8', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenHonOpeFlag) == True:
                pass
            else:
                print_log('[WARN] P11.UploadDetailView関数 P11A20-8', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ１１Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P11.UploadDetailView関数 P11A30', 'INFO')
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
            print_log('[ERROR] P11.UploadDetailView関数 P11A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P11.UploadDetailView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P11.UploadDetailView関数 P11A30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P11.UploadDetailView関数 P11A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、アップロードデータ取得処理（Ｐ１１Ａ４０）
        # （１）アップロードデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、アップロードデータを取得する。
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
        print_log('[INFO] P11.UploadDetailView関数 P11A40', 'INFO')
        # （１）アップロードデータを格納する局所変数を初期化する。
        localKenUploadModel = None
        localHonUploadModel = None
        localKenUploadFileModel = None
        localHonUploadFileModel = None
        # （２）ＤＢにアクセスし、アップロードデータを取得する。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、（１０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、（２０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、（３０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、（４０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、（１０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                        [ kenUploadId, 
                          operationYear, 
                        ])[0]
                except:
                    localKenUploadModel = None
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、（２０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                        [ honUploadId, 
                          operationYear, 
                        ])[0]
                except:
                    localHonUploadModel = None
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、（３０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                        [ kenUploadId, 
                          operationYear, 
                        ])[0]
                except:
                    localKenUploadFileModel = None
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、（４０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                        [ honUploadId, 
                          operationYear, 
                        ])[0]
                except:
                    localHonUploadFileModel = None        
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、（１０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                        [ kenUploadId, 
                          operationYear, 
                        ])[0]
                except:
                    localKenUploadModel = None
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、（２０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                        [ honUploadId, 
                          operationYear, 
                        ])[0]
                except:
                    localHonUploadModel = None
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、（３０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                        [ kenUploadId, 
                          operationYear, 
                        ])[0]
                except:
                    localKenUploadFileModel = None
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、（４０）
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
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
                        [ honUploadId, 
                          operationYear, 
                        ])[0]
                except:
                    localHonUploadFileModel = None
                    print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
            else: 
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P11.UploadDetailView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P11.UploadDetailView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P11.UploadDetailView関数 P11A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P11.UploadDetailView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、お知らせデータ取得処理（Ｐ１１Ａ４５）
        # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
        # （２）ＳＱＬ文を実行する。
        # （３）トランザクション管理でコミットする。
        # （４）ＤＢ接続を切断＝カーソルを閉じる。
        ##########################################
        print_log('[INFO] P11.UploadDetailView関数 P11A45', 'INFO')
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
                    KEN_UPLOAD_ID,
                    HON_UPLOAD_ID
                ) VALUES (
                    (SELECT MAX(id + 1) FROM FILE_UPLOAD_LOG),
                    %s,
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
                  'UploadDetailView',
                  kenUploadId, 
                  honUploadId, 
                ])
            # （３）トランザクション管理でコミットする。
            transaction.commit()
        except:
            transaction.rollback()
            print_log('[ERROR] P11.UploadDetailView関数 P11A45', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P11.UploadDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P11.UploadDetailView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        finally:
            # （４）ＤＢ接続を切断＝カーソルを閉じる。
            localCursor.close()
        ##########################################
        # フォームセット処理（Ｐ１１Ａ５０）
        # （１）局所変数のフォームを初期化する。
        # ヒント：ブラウザとのデータのやりとり、特にブラウザからPOSTデータがある場合、フォームを使用する。
        # ヒント：モデルはブラウザで参照用、かつタグをコーディングする場合等に使用する。
        # ヒント：フォームはブラウザで編集用、POSTでサーバにリクエストされる項目、かつタグを自動生成する場合等に使用する。
        # ヒント：表示画面の場合、URL+QUERY STRING、VIEW関数、GET、renderでテンプレートとレスポンスで目的の画面を表示する。
        # ヒント：追加、削除の場合、URL+QUERY STRING+フォーム値、DoVIEW関数、POST、redirect（URL+QUERY STRING）で次の画面に遷移する。
        # ヒント：または、追加、削除の場合、URL+QUERY STRING+フォーム値、DoVIEW関数、POST、renderでテンプレートとレスポンスで元の同じ画面を表示する。
        # ヒント：ただし、この場合、レスポンスに、追加、削除結果のフラグを返し、ブラウザ側（正確にはサーバでのレンダリング時＝HTML生成時）で通常画面と結果画面をフラグを見て分岐処理するようにテンプレートを記述する。
        ##########################################
        print_log('[INFO] P11.UploadDetailView関数 P11A50', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localUploadDetailForm = UploadDetailForm()
        ##########################################            
        # フォームセット処理（Ｐ１１Ａ５２）
        # （１）局所変数のフォームにＤＢのアップロードテーブルから取得した値をセットする。（都道府県項目）
        # ヒント：「!= None」でオブジェクトのインスタンスが生成済み＝存在していることを確認する。
        # ヒント：上記チェック処理を行い、実行時エラーの発生を防止する。
        # ヒント：これを実現するために、変数を初期化し、ＤＢアクセス時のエクセプション発生時にも、変数の初期化を確実に行う。
        ##########################################            
        # （１）局所変数のフォームにＤＢのアップロードテーブルから取得した値をセットする。（都道府県項目）
        if localKenUploadModel != None:
            localUploadDetailForm.initial['KEN_UPLOAD_ID'] = localKenUploadModel.KEN_UPLOAD_ID
            localUploadDetailForm.initial['KEN_KEN_HON_OPE_FLAG'] = localKenUploadModel.KEN_HON_OPE_FLAG
            localUploadDetailForm.initial['KEN_OPERATION_YEAR'] = localKenUploadModel.OPERATION_YEAR
            localUploadDetailForm.initial['KEN_FLOOD_YEAR'] = localKenUploadModel.FLOOD_YEAR
            localUploadDetailForm.initial['KEN_ORG_CODE'] = localKenUploadModel.ORG_CODE
            localUploadDetailForm.initial['KEN_ORG_NAME'] = localKenUploadModel.ORG_NAME
            localUploadDetailForm.initial['KEN_DEPT_CODE'] = localKenUploadModel.DEPT_CODE
            localUploadDetailForm.initial['KEN_DEPT_NAME'] = localKenUploadModel.DEPT_NAME
            localUploadDetailForm.initial['KEN_ACCOUNT_ID'] = localKenUploadModel.ACCOUNT_ID
            localUploadDetailForm.initial['KEN_ACCOUNT_NAME'] = localKenUploadModel.ACCOUNT_NAME
            localUploadDetailForm.initial['KEN_ADD_DATE'] = localKenUploadModel.ADD_DATE
            localUploadDetailForm.initial['KEN_ADD_DATE_TIME'] = localKenUploadModel.ADD_DATE_TIME
            localUploadDetailForm.initial['KEN_ADD_FLAG'] = localKenUploadModel.ADD_FLAG
            localUploadDetailForm.initial['KEN_DELETE_DATE'] = localKenUploadModel.DELETE_DATE
            localUploadDetailForm.initial['KEN_DELETE_DATE_TIME'] = localKenUploadModel.DELETE_DATE_TIME
            localUploadDetailForm.initial['KEN_DELETE_FLAG'] = localKenUploadModel.DELETE_FLAG
            localUploadDetailForm.initial['KEN_QUESTION_BODY'] = localKenUploadModel.QUESTION_BODY
            localUploadDetailForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = localKenUploadModel.QUESTION_TO_HON_OPE_FLAG
        else:
            localUploadDetailForm.initial['KEN_UPLOAD_ID'] = ""
            localUploadDetailForm.initial['KEN_KEN_HON_OPE_FLAG'] = ""
            localUploadDetailForm.initial['KEN_OPERATION_YEAR'] = ""
            localUploadDetailForm.initial['KEN_FLOOD_YEAR'] = ""
            localUploadDetailForm.initial['KEN_ORG_CODE'] = ""
            localUploadDetailForm.initial['KEN_ORG_NAME'] = ""
            localUploadDetailForm.initial['KEN_DEPT_CODE'] = ""
            localUploadDetailForm.initial['KEN_DEPT_NAME'] = ""
            localUploadDetailForm.initial['KEN_ACCOUNT_ID'] = ""
            localUploadDetailForm.initial['KEN_ACCOUNT_NAME'] = ""
            localUploadDetailForm.initial['KEN_ADD_DATE'] = ""
            localUploadDetailForm.initial['KEN_ADD_DATE_TIME'] = ""
            localUploadDetailForm.initial['KEN_ADD_FLAG'] = ""
            localUploadDetailForm.initial['KEN_DELETE_DATE'] = ""
            localUploadDetailForm.initial['KEN_DELETE_DATE_TIME'] = ""
            localUploadDetailForm.initial['KEN_DELETE_FLAG'] = ""
            localUploadDetailForm.initial['KEN_QUESTION_BODY'] = ""
            localUploadDetailForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = ""
        if localKenUploadFileModel != None:
            localUploadDetailForm.initial['KEN_UPLOAD_FILE_ID'] = localKenUploadFileModel.KEN_UPLOAD_FILE_ID
            localUploadDetailForm.initial['KEN_UPLOAD_FILE_NAME'] = localKenUploadFileModel.KEN_UPLOAD_FILE_NAME
            localUploadDetailForm.initial['KEN_UPLOAD_FILE_PATH'] = localKenUploadFileModel.KEN_UPLOAD_FILE_PATH
        else:
            localUploadDetailForm.initial['KEN_UPLOAD_FILE_ID'] = ""
            localUploadDetailForm.initial['KEN_UPLOAD_FILE_NAME'] = ""
            localUploadDetailForm.initial['KEN_UPLOAD_FILE_PATH'] = ""
        ##########################################            
        # フォームセット処理（Ｐ１１Ａ５４）
        # （１）局所変数のフォームにＤＢのアップロードテーブルから取得した値をセットする。（本省項目）
        ##########################################            
        # （１）局所変数のフォームにＤＢのアップロードテーブルから取得した値をセットする。（本省項目）
        if localHonUploadModel != None:
            localUploadDetailForm.initial['HON_UPLOAD_ID'] = localHonUploadModel.HON_UPLOAD_ID
            localUploadDetailForm.initial['HON_KEN_HON_OPE_FLAG'] = localHonUploadModel.KEN_HON_OPE_FLAG
            localUploadDetailForm.initial['HON_OPERATION_YEAR'] = localHonUploadModel.OPERATION_YEAR
            localUploadDetailForm.initial['HON_FLOOD_YEAR'] = localHonUploadModel.FLOOD_YEAR
            localUploadDetailForm.initial['HON_ORG_CODE'] = localHonUploadModel.ORG_CODE
            localUploadDetailForm.initial['HON_ORG_NAME'] = localHonUploadModel.ORG_NAME
            localUploadDetailForm.initial['HON_DEPT_CODE'] = localHonUploadModel.DEPT_CODE
            localUploadDetailForm.initial['HON_DEPT_NAME'] = localHonUploadModel.DEPT_NAME
            localUploadDetailForm.initial['HON_ACCOUNT_ID'] = localHonUploadModel.ACCOUNT_ID
            localUploadDetailForm.initial['HON_ACCOUNT_NAME'] = localHonUploadModel.ACCOUNT_NAME
            localUploadDetailForm.initial['HON_ADD_DATE'] = localHonUploadModel.ADD_DATE
            localUploadDetailForm.initial['HON_ADD_DATE_TIME'] = localHonUploadModel.ADD_DATE_TIME
            localUploadDetailForm.initial['HON_ADD_FLAG'] = localHonUploadModel.ADD_FLAG
            localUploadDetailForm.initial['HON_DELETE_DATE'] = localHonUploadModel.DELETE_DATE
            localUploadDetailForm.initial['HON_DELETE_DATE_TIME'] = localHonUploadModel.DELETE_DATE_TIME
            localUploadDetailForm.initial['HON_DELETE_FLAG'] = localHonUploadModel.DELETE_FLAG
            localUploadDetailForm.initial['HON_QUESTION_BODY'] = localHonUploadModel.QUESTION_BODY
            localUploadDetailForm.initial['HON_QUESTION_TO_HON_OPE_FLAG'] = localHonUploadModel.QUESTION_TO_HON_OPE_FLAG
        else:
            localUploadDetailForm.initial['HON_UPLOAD_ID'] = ""
            localUploadDetailForm.initial['HON_KEN_HON_OPE_FLAG'] = ""
            localUploadDetailForm.initial['HON_OPERATION_YEAR'] = ""
            localUploadDetailForm.initial['HON_FLOOD_YEAR'] = ""
            localUploadDetailForm.initial['HON_ORG_CODE'] = ""
            localUploadDetailForm.initial['HON_ORG_NAME'] = ""
            localUploadDetailForm.initial['HON_DEPT_CODE'] = ""
            localUploadDetailForm.initial['HON_DEPT_NAME'] = ""
            localUploadDetailForm.initial['HON_ACCOUNT_ID'] = ""
            localUploadDetailForm.initial['HON_ACCOUNT_NAME'] = ""
            localUploadDetailForm.initial['HON_ADD_DATE'] = ""
            localUploadDetailForm.initial['HON_ADD_DATE_TIME'] = ""
            localUploadDetailForm.initial['HON_ADD_FLAG'] = ""
            localUploadDetailForm.initial['HON_DELETE_DATE'] = ""
            localUploadDetailForm.initial['HON_DELETE_DATE_TIME'] = ""
            localUploadDetailForm.initial['HON_DELETE_FLAG'] = ""
            localUploadDetailForm.initial['HON_QUESTION_BODY'] = ""
            localUploadDetailForm.initial['HON_QUESTION_TO_HON_OPE_FLAG'] = ""
        if localHonUploadFileModel != None:
            localUploadDetailForm.initial['HON_UPLOAD_FILE_ID'] = localHonUploadFileModel.HON_UPLOAD_FILE_ID
            localUploadDetailForm.initial['HON_UPLOAD_FILE_NAME'] = localHonUploadFileModel.HON_UPLOAD_FILE_NAME
            localUploadDetailForm.initial['HON_UPLOAD_FILE_PATH'] = localHonUploadFileModel.HON_UPLOAD_FILE_PATH
        else:
            localUploadDetailForm.initial['HON_UPLOAD_FILE_ID'] = ""
            localUploadDetailForm.initial['HON_UPLOAD_FILE_NAME'] = ""
            localUploadDetailForm.initial['HON_UPLOAD_FILE_PATH'] = ""
        ##########################################            
        # フォームセット処理（Ｐ１１Ａ５４）
        # （１）フォームのウィジェットの属性に値をセットする。（都道府県項目）
        # （２）フォームのウィジェットの属性に値をセットする。（本省項目）
        # ヒント：利用者が編集できない項目は、disabled、readonlyのいずれかとする。
        # ヒント：フォームを使用した場合、ブラウザでタグが自動生成されるため、ブラウザのstyle、cssでdisable、readonlyをセットしにくい。
        # ヒント：そのため。ビュー関数でdisable、readonly等をセットする。
        # ヒント：フォームのフィールドは、非表示の項目もセットすることを推奨する。
        # ヒント：ステートレスなウェブアプリにおいて、ブラウザに送ったデータをPOST時にサーバ側のビュー関数で参照可能とするため。
        ##########################################            
        # （１）フォームのウィジェットの属性に値をセットする。（都道府県項目）
        localUploadDetailForm.fields['KEN_UPLOAD_ID'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_KEN_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_OPERATION_YEAR'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_FLOOD_YEAR'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_ORG_CODE'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_ORG_NAME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_DEPT_CODE'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_DEPT_NAME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_ACCOUNT_ID'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_ACCOUNT_NAME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_ADD_DATE'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_ADD_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_ADD_FLAG'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_DELETE_DATE'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_DELETE_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_DELETE_FLAG'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_QUESTION_BODY'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_QUESTION_TO_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_UPLOAD_FILE_ID'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_UPLOAD_FILE_NAME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['KEN_UPLOAD_FILE_PATH'].widget.attrs['readonly'] = True
        # （２）フォームのウィジェットの属性に値をセットする。（本省項目）
        localUploadDetailForm.fields['HON_UPLOAD_ID'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_KEN_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_OPERATION_YEAR'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_FLOOD_YEAR'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_ORG_CODE'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_ORG_NAME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_DEPT_CODE'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_DEPT_NAME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_ACCOUNT_ID'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_ACCOUNT_NAME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_ADD_DATE'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_ADD_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_ADD_FLAG'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_DELETE_DATE'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_DELETE_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_DELETE_FLAG'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_QUESTION_BODY'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_QUESTION_TO_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_UPLOAD_FILE_ID'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_UPLOAD_FILE_NAME'].widget.attrs['readonly'] = True
        localUploadDetailForm.fields['HON_UPLOAD_FILE_PATH'].widget.attrs['readonly'] = True
        ##########################################
        # レスポンスセット処理（Ｐ１１Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        # ヒント：accountType：１：都道府県、２：本省、３：運用業者
        # ヒント：accountId：　例　01hokkai
        # ヒント：isKen：True：都道府県でログインしている、False：都道府県でログインしていない
        # ヒント：isHon：True：本省でログインしている、False：本省でログインしていない
        # ヒント：isOpe：True：運用業者でログインしている、False：運用業者でログインしていない
        # ヒント：operationYear：調査実施年
        # ヒント：message：ダミー、未使用
        # ヒント：uploadDetailForm：テンプレートで使用するフォームのデータをセットする。
        # ヒント：isKen、isHon、isOpeは１つが必ずTrue、２つが必ずFalseを想定する。
        ##########################################
        print_log('[INFO] P11.UploadDetailView関数 P11A60', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            response = {
                'accountType': 1,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。 
                'isKen': True,                             # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'uploadDetailForm': localUploadDetailForm, # アップロード詳細画面用のフォーム
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'uploadDetailForm': localUploadDetailForm, # アップロード詳細画面用のフォーム
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            response = {
                'accountType': 3,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': True,                             # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'uploadDetailForm': localUploadDetailForm, # アップロード詳細画面用のフォーム
            }
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P11.UploadDetailView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P11.UploadDetailView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P11.UploadDetailView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１１Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P11.UploadDetailView関数 P11A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P11UploadDetailTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P11UploadDetailTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            return render(request, 'P11UploadDetailTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P11.UploadDetailView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P11.UploadDetailView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ１１Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P11.UploadDetailView関数 P11A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P11.UploadDetailView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P11.UploadDetailView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング、戻り値セット処理（Ｐ１１Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P11.UploadDetailView関数 P11A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
#####################################################################################
# 関数名：P11.UploadDownloadView（Ｐ１１Ｂ）
# 関数概要：都道府県用調査結果または確認結果ファイルをブラウザに戻す。（都道府県）
# 関数概要：本省用調査結果または確認結果ファイルをブラウザに戻す。（本省）
# 関数概要：運用業者用調査結果または確認結果ファイルをブラウザに戻す。（運用業者）
#
# 引数[1]：request
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから運用業者名、運用業者部署名、運用業者名を取得するために使用する。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）
# 引数[5]：fileId：都道府県用調査結果または確認結果ファイルＩＤ※ＤＢから都道府県用調査結果または確認結果ファイルを取得するために使用する。（都道府県）
# 引数[5]：fileId：本省用調査結果または確認結果ファイルＩＤ※ＤＢから本省用調査結果または確認結果ファイルを取得するために使用する。（本省）
# 引数[5]：fileId：運用業者用調査結果または確認結果ファイルＩＤ※ＤＢから運用業者用調査結果または確認結果ファイルを取得するために使用する。（運用業者）
#
# 戻り値[1]：response：
#
# FORM：UploadDownloadForm：都道府県用調査結果または確認結果ダウンロードページ（都道府県）
# FORM：UploadDownloadForm：本省用調査結果または確認結果ダウンロードページ（本省）
# FORM：UploadDownloadForm：運用業者用調査結果または確認結果ダウンロードページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：UploadModel：調査結果または確認結果（Ｒ）
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def UploadDownloadView(request, accountType, accountId, operationYear, kenUploadFileId, honUploadFileId, kenHonOpeFlag):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P11.UploadDownloadView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１１Ｂ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P11.UploadDownloadView関数 P11B10', 'INFO')
        print_log('[INFO] P11.UploadDownloadView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P11.UploadDownloadView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P11.UploadDownloadView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P11.UploadDownloadView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P11.UploadDownloadView.kenUploadFileId = {}'.format(kenUploadFileId), 'INFO')
        print_log('[INFO] P11.UploadDownloadView.honUploadFileId = {}'.format(honUploadFileId), 'INFO')
        print_log('[INFO] P11.UploadDownloadView.kenHonOpeFlag = {}'.format(kenHonOpeFlag), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１１Ｂ２０）
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
            print_log('[WARN] P11.UploadDownloadView関数 P11B20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P11.UploadDownloadView関数 P11B20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P11.UploadDownloadView関数 P11B20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P11.UploadDownloadView関数 P11B20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P11.UploadDownloadView関数 P11B20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P11.UploadDownloadView関数 P11B20-5', 'WARN')
                return render(request, 'error.html')
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        if kenUploadFileId is None:
            print_log('[WARN] P11.UploadDownloadView関数 P11B20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenUploadFileId) == True:
                pass
            else:
                print_log('[WARN] P11.UploadDownloadView関数 P11B20-6', 'WARN')
                return render(request, 'error.html')
        # （７）本省アップロードＩＤをチェックする。　例　1
        if honUploadFileId is None:
            print_log('[WARN] P11.UploadDownloadView関数 P11B20-7', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(honUploadFileId) == True:
                pass
            else:
                print_log('[WARN] P11.UploadDownloadView関数 P11B20-7', 'WARN')
                return render(request, 'error.html')
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        if kenHonOpeFlag is None:
            print_log('[WARN] P11.UploadDownloadView関数 P11B20-8', 'WARN')
            return render(request, 'error.html')
        else:
            if kenHonOpeFlag == '1' or kenHonOpeFlag == '2' or kenHonOpeFlag == '3':
                pass
            else:
                print_log('[WARN] P11.UploadDownloadView関数 P11B20-8', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ１１Ｂ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P11.UploadDownloadView関数 P11B30', 'INFO')
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
            print_log('[ERROR] P11.UploadDownloadView関数 P11B30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P11.UploadDownloadView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P11.UploadDownloadView関数 P11B30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P11.UploadDownloadView関数 P11B30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、アップロードファイルデータ取得処理（Ｐ１１Ｂ４０）
        # （１）ファイルデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、ファイルデータを取得する。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：rawでＤＢにアクセスした場合、検索結果が０件の場合、エクセプションが発生する。
        # ヒント：後々の拡張等を考慮し、場合分けをベタで記述し、明示されていないロジックを含まないコードとするため、
        # ヒント：あえて冗長な場合分けをしている。
        ##########################################
        print_log('[INFO] P11.UploadDownloadView関数 P11B40', 'INFO')
        # （１）ファイルデータを格納する局所変数を初期化する。
        localKenUploadFileModel = None
        localHonUploadFileModel = None
        # （２）ＤＢにアクセスし、ファイルデータを取得する。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
                if kenHonOpeFlag == '1':
                    # データの種別・区分＝１：都道府県の場合、、、
                    try:
                        localKenUploadFileModel = UploadFileModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOADFILE 
                            WHERE 
                                KEN_UPLOAD_FILE_ID=%s AND 
                                KEN_HON_OPE_FLAG='1' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """, 
                            [ kenUploadFileId, 
                              operationYear, 
                            ])[0]
                    except:
                        localKenUploadFileModel = None
                        print_log('[ERROR] P11.UploadDownloadView関数 P11B40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
                elif kenHonOpeFlag == '2':
                    # データの種別・区分＝２：本省の場合、、、
                    try:
                        localHonUploadFileModel = UploadFileModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOADFILE 
                            WHERE 
                                HON_UPLOAD_FILE_ID=%s AND 
                                KEN_HON_OPE_FLAG='2' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """, 
                            [ honUploadFileId, 
                              operationYear, 
                            ])[0]
                    except:
                        localHonUploadFileModel = None
                        print_log('[ERROR] P11.UploadDownloadView関数 P11B40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
                else:
                    # データの種別・区分＝その他の場合、、、
                    pass        
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
                if kenHonOpeFlag == '1':
                    # データの種別・区分＝１：都道府県の場合、、、
                    try:
                        localKenUploadFileModel = UploadFileModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOADFILE 
                            WHERE 
                                KEN_UPLOAD_FILE_ID=%s AND 
                                KEN_HON_OPE_FLAG='1' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """, 
                            [kenUploadFileId, operationYear, ])[0]
                    except:
                        localKenUploadFileModel = None
                        print_log('[ERROR] P11.UploadDownloadView関数 P11B40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
                elif kenHonOpeFlag == '2':
                    # データの種別・区分＝２：本省の場合、、、
                    try:
                        localHonUploadFileModel = UploadFileModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOADFILE 
                            WHERE 
                                HON_UPLOAD_FILE_ID=%s AND 
                                KEN_HON_OPE_FLAG='2' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """, 
                            [ honUploadFileId, 
                              operationYear, 
                            ])[0]
                    except:
                        localHonUploadFileModel = None        
                        print_log('[ERROR] P11.UploadDownloadView関数 P11B40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
                else:
                    # データの種別・区分＝その他の場合、、、
                    pass
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場、、、
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：exceptが発生した場合でもreturnしない。
                if kenHonOpeFlag == '1':
                    # データの種別・区分＝１：都道府県の場合、、、
                    try:
                        localKenUploadFileModel = UploadFileModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOADFILE 
                            WHERE 
                                KEN_UPLOAD_FILE_ID=%s AND 
                                KEN_HON_OPE_FLAG='1' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """, 
                            [ kenUploadFileId, 
                              operationYear, 
                            ])[0]
                    except:
                        localKenUploadFileModel = None        
                        print_log('[ERROR] P11.UploadDownloadView関数 P11B40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
                elif kenHonOpeFlag == '2':
                    # データの種別・区分＝２：本省の場合、、、
                    try:
                        localHonUploadFileModel = UploadFileModel.objects.raw("""
                            SELECT 
                                * 
                            FROM 
                                FILE_UPLOAD_UPLOADFILE 
                            WHERE 
                                HON_UPLOAD_FILE_ID=%s AND 
                                KEN_HON_OPE_FLAG='2' AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """, 
                            [ honUploadFileId, 
                              operationYear, 
                            ])[0]
                    except:
                        localHonUploadFileModel = None
                        print_log('[ERROR] P11.UploadDownloadView関数 P11B40', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
                else:
                    # データの種別・区分＝その他の場合、、、
                    pass        
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P11.UploadDownloadView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P11.UploadDownloadView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P11.UploadDownloadView関数 P11B40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P11.UploadDownloadView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # 変数セット処理（Ｐ１１Ｂ５０）
        # （１）局所変数に値をセットする。
        ##########################################
        print_log('[INFO] P11.UploadDownloadView関数 P11B50', 'INFO')
        # （１）局所変数に値をセットする。
        localKenUploadFileName = ""
        localHonUploadFileName = ""
        localKenUploadFilePath = ""
        localHonUploadFilePath = ""
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            if kenHonOpeFlag == '1' and localKenUploadFileModel != None:
                # データの種別・区分＝１：都道府県の場合、、、
                localKenUploadFileName = localKenUploadFileModel.KEN_UPLOAD_FILE_NAME
                localKenUploadFilePath = localKenUploadFileModel.KEN_UPLOAD_FILE_PATH
            elif kenHonOpeFlag == '2' and localHonUploadFileModel != None:
                # データの種別・区分＝２：本省の場合、、、
                localHonUploadFileName = localHonUploadFileModel.HON_UPLOAD_FILE_NAME
                localHonUploadFilePath = localHonUploadFileModel.HON_UPLOAD_FILE_PATH
            else:
                # データの種別・区分＝その他の場合、、、
                pass        
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            if kenHonOpeFlag == '1' and localKenUploadFileModel != None:
                # データの種別・区分＝１：都道府県の場合、、、
                localKenUploadFileName = localKenUploadFileModel.KEN_UPLOAD_FILE_NAME
                localKenUploadFilePath = localKenUploadFileModel.KEN_UPLOAD_FILE_PATH
            elif kenHonOpeFlag == '2' and localHonUploadFileModel != None:
                # データの種別・区分＝２：本省の場合、、、
                localHonUploadFileName = localHonUploadFileModel.HON_UPLOAD_FILE_NAME
                localHonUploadFilePath = localHonUploadFileModel.HON_UPLOAD_FILE_PATH
            else:
                # データの種別・区分＝その他の場合、、、
                pass        
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            if kenHonOpeFlag == '1' and localKenUploadFileModel != None:
                # データの種別・区分＝１：都道府県の場合、、、
                localKenUploadFileName = localKenUploadFileModel.KEN_UPLOAD_FILE_NAME
                localKenUploadFilePath = localKenUploadFileModel.KEN_UPLOAD_FILE_PATH
            elif kenHonOpeFlag == '2' and localHonUploadFileModel != None:
                # データの種別・区分＝２：本省の場合、、、
                localHonUploadFileName = localHonUploadFileModel.HON_UPLOAD_FILE_NAME
                localHonUploadFilePath = localHonUploadFileModel.HON_UPLOAD_FILE_PATH
            else:
                # データの種別・区分＝その他の場合、、、
                pass        
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P11.UploadDownloadView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P11.UploadDownloadView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # レスポンスセット処理（Ｐ１１Ｂ６０）
        # （１）ファイルを格納しているディレクトリからダウンロード用のディレクトリにコピーする。
        # （２）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        # ヒント：後々の拡張等を考慮し、アカウント毎のダウンロード権限の制御を細かく行うことを可能とするため、
        # ヒント：また、データ項目をコーディング中に絞り過ぎないようにするため、冗長だが、条件式を組み合わせ毎に分けている。
        # ヒント：後々も不要であれば、正式リリースに向けて、短縮して記述しても良い。
        # ヒント：kenUploadFilePathに永続的にファイルを格納する。
        # ヒント：アップロードファイルの登録時に、ＤＢとkenUploadFilePathのディレクトリへのファイルの移動を行うことを想定している。
        # ヒント：ビュー関数を介さず、直接リンクからダウンロードできないようにこのように実装している。
        # ヒント：os.path.join(localBaseDir, 'download')に一時的にファイルを格納する。
        ##########################################
        print_log('[INFO] P11.UploadDownloadView関数 P11B60', 'INFO')
        # （１）ファイルを格納しているディレクトリからダウンロード用のディレクトリにコピーする。
        # （２）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            if kenHonOpeFlag == '1' and len(localKenUploadFileName) >= 1 and len(localKenUploadFilePath) >= 1:
                # データの種別・区分＝１：都道府県の場合、、、
                # ヒント：./01hokkai/aaa.lzhを./download/aaa.lzhにコピーする。
                # ヒント：./download/aaa.lzhブラウザに戻す。
                try:
                    shutil.copy2(os.path.join(localKenUploadFilePath), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download', localKenUploadFileName))
                    response = HttpResponse(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download', localKenUploadFileName), 'rb').read(), content_type="application/x-zip-compressed")
                    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(localKenUploadFileName)
                except:
                    print_log('[ERROR] P11.UploadDownloadView関数 P11B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
            elif kenHonOpeFlag == '2' and len(localHonUploadFileName) >= 1 and len(localHonUploadFilePath) >= 1:
                # データの種別・区分＝２：本省の場合、、、
                # ヒント：./keizai/aaa.lzhを./download/aaa.lzhにコピーする。
                # ヒント：./download/aaa.lzhブラウザに戻す。
                try:
                    shutil.copy2(os.path.join(localHonUploadFilePath), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download', localHonUploadFileName))
                    response = HttpResponse(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download', localHonUploadFileName), 'rb').read(), content_type="application/x-zip-compressed")
                    response["Content-Disposition"] = "attachment; filename=%s", [localHonUploadFileName]
                except:    
                    print_log('[ERROR] P11.UploadDownloadView関数 P11B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
            else:
                # データの種別・区分＝その他の場合、、、
                pass    
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            if kenHonOpeFlag == '1' and len(localKenUploadFileName) >= 1 and len(localKenUploadFilePath) >= 1:
                # データの種別・区分＝１：都道府県の場合、、、
                try:
                    print_log(localKenUploadFileName, 'INFO')
                    localBaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    shutil.copy2(os.path.join(localKenUploadFilePath, localKenUploadFileName), os.path.join(localBaseDir, 'download', localKenUploadFileName))
                    response = HttpResponse(open(os.path.join(os.path.join(localBaseDir, 'download'), localKenUploadFileName), 'rb').read(), content_type="application/x-zip-compressed")
                    response["Content-Disposition"] = "attachment; filename=%s", [localKenUploadFileName]
                except:
                    print_log('[ERROR] P11.UploadDownloadView関数 P11B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
            elif kenHonOpeFlag == '2' and len(localHonUploadFileName) >= 1 and len(localHonUploadFilePath) >= 1:
                # データの種別・区分＝２：本省の場合、、、
                try:
                    print_log(localHonUploadFileName, 'INFO')
                    localBaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    shutil.copy2(os.path.join(localHonUploadFilePath, localHonUploadFileName), os.path.join(localBaseDir, 'download', localHonUploadFileName))
                    response = HttpResponse(open(os.path.join(os.path.join(localBaseDir, 'download'), localHonUploadFileName), 'rb').read(), content_type="application/x-zip-compressed")
                    response["Content-Disposition"] = "attachment; filename=%s", [localHonUploadFileName]
                except:    
                    print_log('[ERROR] P11.UploadDownloadView関数 P11B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
            else:
                # データの種別・区分＝その他の場合、、、
                pass    
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            if kenHonOpeFlag == '1' and len(localKenUploadFileName) >= 1 and len(localKenUploadFilePath) >= 1:
                # データの種別・区分＝１：都道府県の場合、、、
                try:
                    localBaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    shutil.copy2(os.path.join(localKenUploadFilePath, localKenUploadFileName), os.path.join(localBaseDir, 'download', localKenUploadFileName))
                    response = HttpResponse(open(os.path.join(os.path.join(localBaseDir, 'download'), localKenUploadFileName), 'rb').read(), content_type="application/x-zip-compressed")
                    response["Content-Disposition"] = "attachment; filename=%s", [localHonUploadFileName]
                except:
                    print_log('[ERROR] P11.UploadDownloadView関数 P11B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
            elif kenHonOpeFlag == '2' and len(localHonUploadFileName) >= 1 and len(localHonUploadFilePath) >= 1:
                # データの種別・区分＝２：本省の場合、、、
                try:
                    localBaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    shutil.copy2(os.path.join(localHonUploadFilePath, localHonUploadFileName), os.path.join(localBaseDir, 'download', localHonUploadFileName))
                    response = HttpResponse(open(os.path.join(os.path.join(localBaseDir, 'download'), localHonUploadFileName), 'rb').read(), content_type="application/x-zip-compressed")
                    response["Content-Disposition"] = "attachment; filename=%s", [localHonUploadFileName]
                except:    
                    print_log('[ERROR] P11.UploadDownloadView関数 P11B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P11.UploadDownloadView関数で警告が発生しました。', 'ERROR')
                    response["Content-Disposition"] = "attachment; filename=%s", [localHonUploadFileName]
            else:
                # データの種別・区分＝その他の場合、、、
                pass    
        else:
            pass
        print_log('[INFO] P11.UploadDownloadView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１１Ｂ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P11.UploadDownloadView関数 P11B70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return response
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ１１Ｂ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P11.UploadDownloadView関数 P11B80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P11.UploadDownloadView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P11.UploadDownloadView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１１Ｂ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P11.UploadDownloadView関数 P11B90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
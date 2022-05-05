#####################################################################################
# UploadListViewビューモジュール【ほぼ完成】
# ファイル名：P10.UploadListView.py（Ｐ１０）
# ユースケース：都道府県の担当者は、調査結果または確認結果の一覧を閲覧する。
# ユースケース：本省の担当者は、調査結果または確認結果の一覧を閲覧する。
# ユースケース：運用業者の担当者は、問合せまたは回答の一覧を閲覧する。
# ヒント：調査結果と確認結果は同じテーブル、モデルを使用する。
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
# sys
#####################################################################################
import sys                                                 # sysモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：ジャンゴモジュールをインポートする。
# login_required
# render
# urlquote
#####################################################################################
from django.contrib.auth.decorators import login_required  # ログイン制御モジュール
from django.shortcuts import render                        # レンダリングモジュール
from django.utils.http import urlquote                     # URLエスケープモジュール   
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# print_log
# AccountModel
# P10UploadModel
#####################################################################################
from file_upload.CommonFunction import print_log           # ログ出力モジュール
from file_upload.models import AccountModel                # アカウントデータモデル
from file_upload.models import P10UploadModel              # アップロードデータ一覧表画面専用のアップロードデータモデル
#####################################################################################
# 関数名：P10.UploadListView（Ｐ１０Ａ）
# 関数概要：都道府県用調査結果または確認結果一覧ページをブラウザに戻す。（都道府県）
# 関数概要：本省用調査結果または確認結果一覧ページをブラウザに戻す。（本省）
# 関数概要：運用業者用調査結果または確認結果一覧ページをブラウザに戻す。（運用業者）
#
# 引数[1]：request：
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから運用業者名、運用部署名、運用業者名を取得するために使用する。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）
#
# 戻り値[1]：response
#
# FORM：UploadListForm：都道府県用調査結果または確認結果一覧ページ（都道府県）
# FORM：UploadListForm：本省用調査結果または確認結果一覧ページ（本省）
# FORM：UploadListForm：運用業者用調査結果または確認結果一覧ページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：UploadModel：調査結果または確認結果モデル（Ｒ）
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def UploadListView(request, accountType, accountId, operationYear, filterAccount):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P10.UploadListView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１０Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P10.UploadListView関数 P10A10', 'INFO')
        print_log('[INFO] P10.UploadListView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P10.UploadListView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P10.UploadListView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P10.UploadListView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P10.UploadListView.filterAccount = {}'.format(filterAccount), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１０Ａ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # （６）フィルタ種別をチェックする。　例　既読 + 未読、未読のみ、既読のみ、北海道、青森、、、沖縄、、、　
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        if accountId == str(request.user.username):
            pass
        else:
            print_log('[WARN] P10.UploadListView関数 P10A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P10.UploadListView関数 P10A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P10.UploadListView関数 P10A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P10.UploadListView関数 P10A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P10.UploadListView関数 P10A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P10.UploadListView関数 P10A20-5', 'WARN')
                return render(request, 'error.html')
        # （６）フィルタ種別をチェックする。　例　既読 ＋ 未読
        if filterAccount is None:
            print_log('[WARN] P10.UploadListViewListView関数 P25A20-6', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ１０Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # （４）局所変数に値をセットする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P10.UploadListView関数 P10A30', 'INFO')
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
            print_log('[ERROR] P10.UploadListView関数 P10A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P10.UploadListView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P10.UploadListView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P10.UploadListView関数P10A30', 'WARN')
            print_log('[WARN] localAccountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P10.UploadListView関数 P10A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        # （４）局所変数に値をセットする。
        # ヒント：アップロードデータの一覧をＤＢから取得するとき、組織コードで自分と同じ組織のアップロードデータのみを検索するために使用する。
        localOrgCode = ''
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            localOrgCode = localAccountModel.ORG_CODE
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            localOrgCode = localAccountModel.ORG_CODE
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            localOrgCode = localAccountModel.ORG_CODE
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P10.UploadListView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P10.UploadListView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、アップロードデータの一覧の取得処理（Ｐ１０Ａ４０）
        # （１）アップロードデータ、アップロードファイルデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、アップロードデータの一覧を取得する。
        # （３）ＤＢにアクセスし、アカウントデータを取得する。
        # SELECT K1.ID AS KEN_UPLOAD_ID,H1.ID AS HON_UPLOAD_ID FROM 
        # (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE OPERATION_YEAR='2016' AND ORG_CODE='1') K1 
        # LEFT OUTER JOIN 
        # (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE OPERATION_YEAR='2016' AND ORG_CODE='1') H1
        # ON K1.ID=H1.PARENT_ID        
        ##########################################
        print_log('[INFO] P10.UploadListView関数 P10A40', 'INFO')
        # （１）アップロードデータ、アップロードファイルデータを格納する局所変数を初期化する。
        localUploadArray = None
        # （２）ＤＢにアクセスし、アップロードデータの一覧を取得する。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                # ヒント：ＤＢのアップロードデータテーブルは、都道府県、本省で別々のレコードとして管理している。
                # ヒント：一覧では、スレッド形式で都道府県のアップロードデータの次に、本省のアップロードデータを表示させるため、LEFT OUTER JOINを使用している。
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                try:
                    if filterAccount == '' or filterAccount == '0' or filterAccount == 'NULL':
                        # ケース１：filterAccountが空欄、NULL、0の場合、、、
                        # ヒント：絞り込まない
                        localUploadArray = P10UploadModel.objects.raw("""
                            SELECT 
                                K1.id AS id,
                                K1.KEN_UPLOAD_ID AS KEN_UPLOAD_ID,
                                K1.KEN_HON_OPE_FLAG AS KEN_KEN_HON_OPE_FLAG,
                                K1.OPERATION_YEAR AS KEN_OPERATION_YEAR,
                                K1.FLOOD_YEAR AS KEN_FLOOD_YEAR,
                                K1.ORG_CODE AS KEN_ORG_CODE,
                                K1.ORG_NAME AS KEN_ORG_NAME,
                                K1.DEPT_CODE AS KEN_DEPT_CODE,
                                K1.DEPT_NAME AS KEN_DEPT_NAME,
                                K1.ACCOUNT_ID AS KEN_ACCOUNT_ID,
                                K1.ACCOUNT_NAME AS KEN_ACCOUNT_NAME,
                                K1.ADD_DATE AS KEN_ADD_DATE,
                                K1.ADD_DATE_TIME AS KEN_ADD_DATE_TIME,
                                K1.ADD_FLAG AS KEN_ADD_FLAG,
                                K1.DELETE_DATE AS KEN_DELETE_DATE,
                                K1.DELETE_DATE_TIME AS KEN_DELETE_DATE_TIME,
                                K1.DELETE_FLAG AS KEN_DELETE_FLAG,
                                K1.QUESTION_TO_HON_OPE_FLAG AS KEN_QUESTION_TO_HON_OPE_FLAG,
                                K1.QUESTION_BODY AS KEN_QUESTION_BODY,
                                H1.HON_UPLOAD_ID AS HON_UPLOAD_ID,
                                H1.KEN_HON_OPE_FLAG AS HON_KEN_HON_OPE_FLAG,
                                H1.OPERATION_YEAR AS HON_OPERATION_YEAR,
                                H1.FLOOD_YEAR AS HON_FLOOD_YEAR,
                                H1.ORG_CODE AS HON_ORG_CODE,
                                H1.ORG_NAME AS HON_ORG_NAME,
                                H1.DEPT_CODE AS HON_DEPT_CODE,
                                H1.DEPT_NAME AS HON_DEPT_NAME,
                                H1.ACCOUNT_ID AS HON_ACCOUNT_ID,
                                H1.ACCOUNT_NAME AS HON_ACCOUNT_NAME,
                                H1.ADD_DATE AS HON_ADD_DATE,
                                H1.ADD_DATE_TIME AS HON_ADD_DATE_TIME,
                                H1.ADD_FLAG AS HON_ADD_FLAG,
                                H1.DELETE_DATE AS HON_DELETE_DATE,
                                H1.DELETE_DATE_TIME AS HON_DELETE_DATE_TIME,
                                H1.DELETE_FLAG AS HON_DELETE_FLAG,
                                H1.QUESTION_TO_HON_OPE_FLAG AS HON_QUESTION_TO_HON_OPE_FLAG,
                                H1.QUESTION_BODY AS HON_QUESTION_BODY 
                            FROM 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='1' AND OPERATION_YEAR=%s AND ORG_CODE=%s) K1 
                                LEFT OUTER JOIN 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='2' AND OPERATION_YEAR=%s AND ORG_CODE=%s) H1 
                                ON K1.KEN_UPLOAD_ID=H1.KEN_UPLOAD_ID
                            WHERE
                                K1.ADD_FLAG='5'    
                            ORDER BY 
                                K1.ADD_DATE_TIME DESC
                            """,
                            [ operationYear, 
                              localOrgCode, 
                              operationYear, 
                              '8000', 
                            ])
                    else:    
                        # ケース２：filterAccountが有効なアカウントＩＤの場合、、、
                        # ヒント：絞り込む
                        localUploadArray = P10UploadModel.objects.raw("""
                            SELECT 
                                K1.id AS id,
                                K1.KEN_UPLOAD_ID AS KEN_UPLOAD_ID,
                                K1.KEN_HON_OPE_FLAG AS KEN_KEN_HON_OPE_FLAG,
                                K1.OPERATION_YEAR AS KEN_OPERATION_YEAR,
                                K1.FLOOD_YEAR AS KEN_FLOOD_YEAR,
                                K1.ORG_CODE AS KEN_ORG_CODE,
                                K1.ORG_NAME AS KEN_ORG_NAME,
                                K1.DEPT_CODE AS KEN_DEPT_CODE,
                                K1.DEPT_NAME AS KEN_DEPT_NAME,
                                K1.ACCOUNT_ID AS KEN_ACCOUNT_ID,
                                K1.ACCOUNT_NAME AS KEN_ACCOUNT_NAME,
                                K1.ADD_DATE AS KEN_ADD_DATE,
                                K1.ADD_DATE_TIME AS KEN_ADD_DATE_TIME,
                                K1.ADD_FLAG AS KEN_ADD_FLAG,
                                K1.DELETE_DATE AS KEN_DELETE_DATE,
                                K1.DELETE_DATE_TIME AS KEN_DELETE_DATE_TIME,
                                K1.DELETE_FLAG AS KEN_DELETE_FLAG,
                                K1.QUESTION_TO_HON_OPE_FLAG AS KEN_QUESTION_TO_HON_OPE_FLAG,
                                K1.QUESTION_BODY AS KEN_QUESTION_BODY,
                                H1.HON_UPLOAD_ID AS HON_UPLOAD_ID,
                                H1.KEN_HON_OPE_FLAG AS HON_KEN_HON_OPE_FLAG,
                                H1.OPERATION_YEAR AS HON_OPERATION_YEAR,
                                H1.FLOOD_YEAR AS HON_FLOOD_YEAR,
                                H1.ORG_CODE AS HON_ORG_CODE,
                                H1.ORG_NAME AS HON_ORG_NAME,
                                H1.DEPT_CODE AS HON_DEPT_CODE,
                                H1.DEPT_NAME AS HON_DEPT_NAME,
                                H1.ACCOUNT_ID AS HON_ACCOUNT_ID,
                                H1.ACCOUNT_NAME AS HON_ACCOUNT_NAME,
                                H1.ADD_DATE AS HON_ADD_DATE,
                                H1.ADD_DATE_TIME AS HON_ADD_DATE_TIME,
                                H1.ADD_FLAG AS HON_ADD_FLAG,
                                H1.DELETE_DATE AS HON_DELETE_DATE,
                                H1.DELETE_DATE_TIME AS HON_DELETE_DATE_TIME,
                                H1.DELETE_FLAG AS HON_DELETE_FLAG,
                                H1.QUESTION_TO_HON_OPE_FLAG AS HON_QUESTION_TO_HON_OPE_FLAG,
                                H1.QUESTION_BODY AS HON_QUESTION_BODY 
                            FROM 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='1' AND OPERATION_YEAR=%s AND ORG_CODE=%s) K1 
                                LEFT OUTER JOIN 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='2' AND OPERATION_YEAR=%s AND ORG_CODE=%s) H1 
                                ON K1.KEN_UPLOAD_ID=H1.KEN_UPLOAD_ID
                            WHERE      
                                (K1.ACCOUNT_ID=%s OR H1.ACCOUNT_ID=%s) AND K1.ADD_FLAG='5'
                            ORDER BY 
                                K1.ADD_DATE_TIME DESC
                            """,
                            [ operationYear, 
                              localOrgCode, 
                              operationYear, 
                              '8000', 
                              filterAccount, 
                              filterAccount, 
                            ])
                except:
                    localUploadArray = None
                    print_log('[ERROR] P10.UploadListView関数 P10A30', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P10.UploadListView関数で警告が発生しました。', 'ERROR')
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                # ヒント：ＤＢのアップロードデータテーブルは、都道府県、本省で別々のレコードとして管理している。
                # ヒント：一覧では、スレッド形式で都道府県のアップロードデータの次に、本省のアップロードデータを表示させるため、LEFT OUTER JOINを使用している。
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                try:
                    if filterAccount == '' or filterAccount == '0' or filterAccount == 'NULL':
                        # ケース３：filterAccountが空欄、NULL、0の場合、、、
                        # ヒント：絞り込まない
                        localUploadArray = P10UploadModel.objects.raw("""
                            SELECT 
                                K1.id AS id,
                                K1.KEN_UPLOAD_ID AS KEN_UPLOAD_ID,
                                K1.KEN_HON_OPE_FLAG AS KEN_KEN_HON_OPE_FLAG,
                                K1.OPERATION_YEAR AS KEN_OPERATION_YEAR,
                                K1.FLOOD_YEAR AS KEN_FLOOD_YEAR,
                                K1.ORG_CODE AS KEN_ORG_CODE,
                                K1.ORG_NAME AS KEN_ORG_NAME,
                                K1.DEPT_CODE AS KEN_DEPT_CODE,
                                K1.DEPT_NAME AS KEN_DEPT_NAME,
                                K1.ACCOUNT_ID AS KEN_ACCOUNT_ID,
                                K1.ACCOUNT_NAME AS KEN_ACCOUNT_NAME,
                                K1.ADD_DATE AS KEN_ADD_DATE,
                                K1.ADD_DATE_TIME AS KEN_ADD_DATE_TIME,
                                K1.ADD_FLAG AS KEN_ADD_FLAG,
                                K1.DELETE_DATE AS KEN_DELETE_DATE,
                                K1.DELETE_DATE_TIME AS KEN_DELETE_DATE_TIME,
                                K1.DELETE_FLAG AS KEN_DELETE_FLAG,
                                K1.QUESTION_TO_HON_OPE_FLAG AS KEN_QUESTION_TO_HON_OPE_FLAG,
                                K1.QUESTION_BODY AS KEN_QUESTION_BODY,
                                H1.HON_UPLOAD_ID AS HON_UPLOAD_ID,
                                H1.KEN_HON_OPE_FLAG AS HON_KEN_HON_OPE_FLAG,
                                H1.OPERATION_YEAR AS HON_OPERATION_YEAR,
                                H1.FLOOD_YEAR AS HON_FLOOD_YEAR,
                                H1.ORG_CODE AS HON_ORG_CODE,
                                H1.ORG_NAME AS HON_ORG_NAME,
                                H1.DEPT_CODE AS HON_DEPT_CODE,
                                H1.DEPT_NAME AS HON_DEPT_NAME,
                                H1.ACCOUNT_ID AS HON_ACCOUNT_ID,
                                H1.ACCOUNT_NAME AS HON_ACCOUNT_NAME,
                                H1.ADD_DATE AS HON_ADD_DATE,
                                H1.ADD_DATE_TIME AS HON_ADD_DATE_TIME,
                                H1.ADD_FLAG AS HON_ADD_FLAG,
                                H1.DELETE_DATE AS HON_DELETE_DATE,
                                H1.DELETE_DATE_TIME AS HON_DELETE_DATE_TIME,
                                H1.DELETE_FLAG AS HON_DELETE_FLAG,
                                H1.QUESTION_TO_HON_OPE_FLAG AS HON_QUESTION_TO_HON_OPE_FLAG,
                                H1.QUESTION_BODY AS HON_QUESTION_BODY 
                            FROM 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='1' AND OPERATION_YEAR=%s) K1 
                                LEFT OUTER JOIN 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='2' AND OPERATION_YEAR=%s AND ORG_CODE=%s) H1 
                                ON K1.KEN_UPLOAD_ID=H1.KEN_UPLOAD_ID 
                            WHERE
                                K1.ADD_FLAG='5'    
                            ORDER BY 
                                K1.ADD_DATE_TIME DESC
                            """, 
                            [ operationYear, 
                              operationYear, 
                              '8000', 
                            ])
                    else:    
                        # ケース４：filterAccountが有効なアカウントＩＤの場合、、、
                        # ヒント：絞り込む
                        localUploadArray = P10UploadModel.objects.raw("""
                            SELECT 
                                K1.id AS id,
                                K1.KEN_UPLOAD_ID AS KEN_UPLOAD_ID,
                                K1.KEN_HON_OPE_FLAG AS KEN_KEN_HON_OPE_FLAG,
                                K1.OPERATION_YEAR AS KEN_OPERATION_YEAR,
                                K1.FLOOD_YEAR AS KEN_FLOOD_YEAR,
                                K1.ORG_CODE AS KEN_ORG_CODE,
                                K1.ORG_NAME AS KEN_ORG_NAME,
                                K1.DEPT_CODE AS KEN_DEPT_CODE,
                                K1.DEPT_NAME AS KEN_DEPT_NAME,
                                K1.ACCOUNT_ID AS KEN_ACCOUNT_ID,
                                K1.ACCOUNT_NAME AS KEN_ACCOUNT_NAME,
                                K1.ADD_DATE AS KEN_ADD_DATE,
                                K1.ADD_DATE_TIME AS KEN_ADD_DATE_TIME,
                                K1.ADD_FLAG AS KEN_ADD_FLAG,
                                K1.DELETE_DATE AS KEN_DELETE_DATE,
                                K1.DELETE_DATE_TIME AS KEN_DELETE_DATE_TIME,
                                K1.DELETE_FLAG AS KEN_DELETE_FLAG,
                                K1.QUESTION_TO_HON_OPE_FLAG AS KEN_QUESTION_TO_HON_OPE_FLAG,
                                K1.QUESTION_BODY AS KEN_QUESTION_BODY,
                                H1.HON_UPLOAD_ID AS HON_UPLOAD_ID,
                                H1.KEN_HON_OPE_FLAG AS HON_KEN_HON_OPE_FLAG,
                                H1.OPERATION_YEAR AS HON_OPERATION_YEAR,
                                H1.FLOOD_YEAR AS HON_FLOOD_YEAR,
                                H1.ORG_CODE AS HON_ORG_CODE,
                                H1.ORG_NAME AS HON_ORG_NAME,
                                H1.DEPT_CODE AS HON_DEPT_CODE,
                                H1.DEPT_NAME AS HON_DEPT_NAME,
                                H1.ACCOUNT_ID AS HON_ACCOUNT_ID,
                                H1.ACCOUNT_NAME AS HON_ACCOUNT_NAME,
                                H1.ADD_DATE AS HON_ADD_DATE,
                                H1.ADD_DATE_TIME AS HON_ADD_DATE_TIME,
                                H1.ADD_FLAG AS HON_ADD_FLAG,
                                H1.DELETE_DATE AS HON_DELETE_DATE,
                                H1.DELETE_DATE_TIME AS HON_DELETE_DATE_TIME,
                                H1.DELETE_FLAG AS HON_DELETE_FLAG,
                                H1.QUESTION_TO_HON_OPE_FLAG AS HON_QUESTION_TO_HON_OPE_FLAG,
                                H1.QUESTION_BODY AS HON_QUESTION_BODY 
                            FROM 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='1' AND OPERATION_YEAR=%s) K1 
                                LEFT OUTER JOIN 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='2' AND OPERATION_YEAR=%s AND ORG_CODE=%s) H1 
                                ON K1.KEN_UPLOAD_ID=H1.KEN_UPLOAD_ID 
                            WHERE
                                (K1.ACCOUNT_ID=%s OR H1.ACCOUNT_ID=%s) AND K1.ADD_FLAG='5'
                            ORDER BY 
                                K1.ADD_DATE_TIME DESC
                            """, 
                            [ operationYear, 
                              operationYear, 
                              '8000', 
                              filterAccount, 
                              filterAccount, 
                            ])
                except:
                    localUploadArray = None
                    print_log('[ERROR] P10.UploadListView関数 P10A30', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P10.UploadListView関数で警告が発生しました。', 'ERROR')
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                # ヒント：ＤＢのアップロードデータテーブルは、都道府県、本省で別々のレコードとして管理している。
                # ヒント：一覧では、スレッド形式で都道府県のアップロードデータの次に、本省のアップロードデータを表示させるため、LEFT OUTER JOINを使用している。
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                try:
                    if filterAccount == '' or filterAccount == '0' or filterAccount == 'NULL':
                        # ケース５：filterAccountが空欄、NULL、0の場合、、、
                        # ヒント：絞り込まない
                        localUploadArray = P10UploadModel.objects.raw("""
                            SELECT 
                                K1.id AS id,
                                K1.KEN_UPLOAD_ID AS KEN_UPLOAD_ID,
                                K1.KEN_HON_OPE_FLAG AS KEN_KEN_HON_OPE_FLAG,
                                K1.OPERATION_YEAR AS KEN_OPERATION_YEAR,
                                K1.FLOOD_YEAR AS KEN_FLOOD_YEAR,
                                K1.ORG_CODE AS KEN_ORG_CODE,
                                K1.ORG_NAME AS KEN_ORG_NAME,
                                K1.DEPT_CODE AS KEN_DEPT_CODE,
                                K1.DEPT_NAME AS KEN_DEPT_NAME,
                                K1.ACCOUNT_ID AS KEN_ACCOUNT_ID,
                                K1.ACCOUNT_NAME AS KEN_ACCOUNT_NAME,
                                K1.ADD_DATE AS KEN_ADD_DATE,
                                K1.ADD_DATE_TIME AS KEN_ADD_DATE_TIME,
                                K1.ADD_FLAG AS KEN_ADD_FLAG,
                                K1.DELETE_DATE AS KEN_DELETE_DATE,
                                K1.DELETE_DATE_TIME AS KEN_DELETE_DATE_TIME,
                                K1.DELETE_FLAG AS KEN_DELETE_FLAG,
                                K1.QUESTION_TO_HON_OPE_FLAG AS KEN_QUESTION_TO_HON_OPE_FLAG,
                                K1.QUESTION_BODY AS KEN_QUESTION_BODY,
                                H1.HON_UPLOAD_ID AS HON_UPLOAD_ID,
                                H1.KEN_HON_OPE_FLAG AS HON_KEN_HON_OPE_FLAG,
                                H1.OPERATION_YEAR AS HON_OPERATION_YEAR,
                                H1.FLOOD_YEAR AS HON_FLOOD_YEAR,
                                H1.ORG_CODE AS HON_ORG_CODE,
                                H1.ORG_NAME AS HON_ORG_NAME,
                                H1.DEPT_CODE AS HON_DEPT_CODE,
                                H1.DEPT_NAME AS HON_DEPT_NAME,
                                H1.ACCOUNT_ID AS HON_ACCOUNT_ID,
                                H1.ACCOUNT_NAME AS HON_ACCOUNT_NAME,
                                H1.ADD_DATE AS HON_ADD_DATE,
                                H1.ADD_DATE_TIME AS HON_ADD_DATE_TIME,
                                H1.ADD_FLAG AS HON_ADD_FLAG,
                                H1.DELETE_DATE AS HON_DELETE_DATE,
                                H1.DELETE_DATE_TIME AS HON_DELETE_DATE_TIME,
                                H1.DELETE_FLAG AS HON_DELETE_FLAG,
                                H1.QUESTION_TO_HON_OPE_FLAG AS HON_QUESTION_TO_HON_OPE_FLAG,
                                H1.QUESTION_BODY AS HON_QUESTION_BODY 
                            FROM 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='1' AND OPERATION_YEAR=%s) K1 
                                LEFT OUTER JOIN 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='2' AND OPERATION_YEAR=%s AND ORG_CODE=%s) H1 
                                ON K1.KEN_UPLOAD_ID=H1.KEN_UPLOAD_ID
                            WHERE
                                K1.ADD_FLAG='5'    
                            ORDER BY 
                                K1.ADD_DATE_TIME DESC
                            """, 
                            [ operationYear, 
                              operationYear, 
                              '8000', 
                            ])
                    else:    
                        # ケース６：filterAccountが有効なアカウントＩＤの場合、、、
                        # ヒント：絞り込む
                        localUploadArray = P10UploadModel.objects.raw("""
                            SELECT 
                                K1.id AS id,
                                K1.KEN_UPLOAD_ID AS KEN_UPLOAD_ID,
                                K1.KEN_HON_OPE_FLAG AS KEN_KEN_HON_OPE_FLAG,
                                K1.OPERATION_YEAR AS KEN_OPERATION_YEAR,
                                K1.FLOOD_YEAR AS KEN_FLOOD_YEAR,
                                K1.ORG_CODE AS KEN_ORG_CODE,
                                K1.ORG_NAME AS KEN_ORG_NAME,
                                K1.DEPT_CODE AS KEN_DEPT_CODE,
                                K1.DEPT_NAME AS KEN_DEPT_NAME,
                                K1.ACCOUNT_ID AS KEN_ACCOUNT_ID,
                                K1.ACCOUNT_NAME AS KEN_ACCOUNT_NAME,
                                K1.ADD_DATE AS KEN_ADD_DATE,
                                K1.ADD_DATE_TIME AS KEN_ADD_DATE_TIME,
                                K1.ADD_FLAG AS KEN_ADD_FLAG,
                                K1.DELETE_DATE AS KEN_DELETE_DATE,
                                K1.DELETE_DATE_TIME AS KEN_DELETE_DATE_TIME,
                                K1.DELETE_FLAG AS KEN_DELETE_FLAG,
                                K1.QUESTION_TO_HON_OPE_FLAG AS KEN_QUESTION_TO_HON_OPE_FLAG,
                                K1.QUESTION_BODY AS KEN_QUESTION_BODY,
                                H1.HON_UPLOAD_ID AS HON_UPLOAD_ID,
                                H1.KEN_HON_OPE_FLAG AS HON_KEN_HON_OPE_FLAG,
                                H1.OPERATION_YEAR AS HON_OPERATION_YEAR,
                                H1.FLOOD_YEAR AS HON_FLOOD_YEAR,
                                H1.ORG_CODE AS HON_ORG_CODE,
                                H1.ORG_NAME AS HON_ORG_NAME,
                                H1.DEPT_CODE AS HON_DEPT_CODE,
                                H1.DEPT_NAME AS HON_DEPT_NAME,
                                H1.ACCOUNT_ID AS HON_ACCOUNT_ID,
                                H1.ACCOUNT_NAME AS HON_ACCOUNT_NAME,
                                H1.ADD_DATE AS HON_ADD_DATE,
                                H1.ADD_DATE_TIME AS HON_ADD_DATE_TIME,
                                H1.ADD_FLAG AS HON_ADD_FLAG,
                                H1.DELETE_DATE AS HON_DELETE_DATE,
                                H1.DELETE_DATE_TIME AS HON_DELETE_DATE_TIME,
                                H1.DELETE_FLAG AS HON_DELETE_FLAG,
                                H1.QUESTION_TO_HON_OPE_FLAG AS HON_QUESTION_TO_HON_OPE_FLAG,
                                H1.QUESTION_BODY AS HON_QUESTION_BODY 
                            FROM 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='1' AND OPERATION_YEAR=%s) K1 
                                LEFT OUTER JOIN 
                                (SELECT * FROM FILE_UPLOAD_UPLOAD WHERE KEN_HON_OPE_FLAG='2' AND OPERATION_YEAR=%s AND ORG_CODE=%s) H1 
                                ON K1.KEN_UPLOAD_ID=H1.KEN_UPLOAD_ID
                            WHERE
                                (K1.ACCOUNT_ID=%s OR H1.ACCOUNT_ID=%s) AND K1.ADD_FLAG='5'     
                            ORDER BY 
                                K1.ADD_DATE_TIME DESC
                            """,  
                            [ operationYear, 
                              operationYear, 
                              '8000', 
                              filterAccount, 
                              filterAccount, 
                            ])
                except:
                    localUploadArray = None
                    print_log('[ERROR] P10.UploadListView関数 P10A30', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P10.UploadListView関数で警告が発生しました。', 'ERROR')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P10.UploadListView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P10.UploadListView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P10.UploadListView関数 P10A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P10.UploadListView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P10.UploadListView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （３）ＤＢにアクセスし、アカウントデータを取得する。
        try:
            localAccountArray = AccountModel.objects.raw("""
                SELECT 
                    *
                FROM 
                    FILE_UPLOAD_ACCOUNT 
                WHERE 
                    OPERATION_YEAR=%s
                ORDER BY
                    ACCOUNT_ID    
                """, 
                [ operationYear, ])
        except:
            localAccountArray == None        
            print_log('[ERROR] P10.UploadListView関数 P10A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P10.UploadListView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P10.UploadListView関数を警告終了しました。', 'ERROR')
        ##########################################
        # フォームセット処理（Ｐ１０Ａ５０）
        # （１）局所変数のフォームを初期化する。
        ##########################################
        print_log('[INFO] P10.UploadListView関数 P10A50', 'INFO')
        ##########################################
        # レスポンスセット処理（Ｐ１０Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        ##########################################
        print_log('[INFO] P10.UploadListView関数 P10A60', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            if localUploadArray != None:
                response = {
                    'accountType': 1,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'accountId': urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。 
                    'isKen': True,                         # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': False,                        # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': False,                        # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': urlquote(operationYear), # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'uploadArray': localUploadArray,       # アップロードデータの一覧 
                    'uploadLength': len(list(localUploadArray)), # アップロードデータの一覧に含まれるアップロードデータの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                }
            else:
                response = {
                    'accountType': 1,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。   
                    'accountId': urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': True,                         # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': False,                        # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': False,                        # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': urlquote(operationYear), # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'uploadArray': localUploadArray,       # アップロードデータの一覧 
                    'uploadLength': 0,                     # アップロードデータの一覧に含まれるアップロードデータの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            if localUploadArray != None:
                response = {
                    'accountType': 2,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。   
                    'accountId': urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': False,                        # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': True,                         # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': False,                        # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': urlquote(operationYear), # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'uploadArray': localUploadArray,       # アップロードデータの一覧 
                    'uploadLength': len(list(localUploadArray)), # アップロードデータの一覧に含まれるアップロードデータの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                }
            else:
                response = {
                    'accountType': 2,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。    
                    'accountId': urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': False,                        # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': True,                         # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': False,                        # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': urlquote(operationYear), # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'uploadArray': localUploadArray,       # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'uploadLength': 0,                     # アップロードデータの一覧に含まれるアップロードデータの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                }        
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            if localUploadArray != None:
                response = {
                    'accountType': 3,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。    
                    'accountId': urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': False,                        # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': False,                        # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': True,                         # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': urlquote(operationYear), # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'uploadArray': localUploadArray,       # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'uploadLength': len(list(localUploadArray)), # アップロードデータの一覧に含まれるアップロードデータの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                }
            else:
                response = {
                    'accountType': 3,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。    
                    'accountId': urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': False,                        # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': False,                        # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': True,                         # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': urlquote(operationYear), # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'uploadArray': localUploadArray,       # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'uploadLength': 0,                     # アップロードデータの一覧に含まれるアップロードデータの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                }
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P10.UploadListView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P10.UploadListView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P10.UploadListView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１０Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P10.UploadListView関数 P10A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P10UploadListTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P10UploadListTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            return render(request, 'P10UploadListTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P10.UploadListView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P10.UploadListView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ１０Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P10.UploadListView関数 P10A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P10.UploadListView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P10.UploadListView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１０Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P10.UploadListView関数 P10A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
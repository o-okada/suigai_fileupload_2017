#####################################################################################
# UploadAddViewビューモジュール【ほぼ完成】
# ファイル名：P12.UploadAddView.py（Ｐ１２）
# ユースケース：都道府県は、調査結果を仮登録＝調査結果または確認結果を仮登録する。
# ユースケース：本省は、確認結果を仮登録＝調査結果または確認結果を仮登録する。
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
# os
# sys
# namedtuple
# datetime
#####################################################################################
import os                                                  # osモジュール
import sys                                                 # sysモジュール
from collections import namedtuple                         # namedtupleモジュール
from datetime import datetime                              # datetimeモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：ジャンゴモジュールをインポートする。
# login_required
# connection
# transaction
# HttpResponseRedirect
# render
# urlquote
#####################################################################################
from django.contrib.auth.decorators import login_required  # ログイン制御モジュール
from django.db import connection                           # ＤＢ接続モジュール
from django.db import transaction                          # トランザクション管理モジュール
from django.http import HttpResponseRedirect               # HTTPリダイレクトモジュール
from django.shortcuts import render                        # レンダリングモジュール
from django.utils.http import urlquote                     # URLエスケープモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# UploadAddForm
# AccountModule
# UploadFileModule
# UploadModule
# print_log
#####################################################################################
from file_upload.CommonFunction import print_log           # ログ出力モジュール
from file_upload.forms import UploadAddForm                # アップロードデータ登録画面用フォーム
from file_upload.models import AccountModel                # アカウントデータモデル
from file_upload.models import UploadFileModel             # アップロードファイルデータモデル
from file_upload.models import UploadModel                 # アップロードデータモデル
#####################################################################################
# 処理名：大域変数定義（０００）
# 処理概要：大域変数を定義する。
#####################################################################################
def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
#####################################################################################
# 関数名：P12.UploadAddView（Ｐ１２Ａ）
# 関数概要：都道府県用調査結果登録ページをブラウザに戻す。（都道府県）
# 関数概要：本省用確認結果登録ページをブラウザに戻す。（本省）
# 関数概要：運用業者用閲覧ページをブラウザに戻す。（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
#
# 引数[1]：request：
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※アクセスは想定せず、不正アクセスとしてエラーページを返す。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
# 引数[5]：parentUploadId：調査結果または確認結果ＩＤ（都道府県）：nullを想定する。
# 引数[5]：parentUploadId：調査結果または確認結果ＩＤ（本省）：必須を想定する。※一覧から選択してこの画面に遷移すると想定する。
# 引数[5]：parentUploadId：調査結果または確認結果ＩＤ（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
#
# 戻り値[1]：response：
#
# FORM：UploadAddForm：都道府県用調査結果登録ページ（都道府県）
# FORM：UploadAddForm：本省用確認結果登録ページ（本省）
# FORM：UploadAddForm：運用業者用調査結果登録ページ（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：UploadModel：調査結果または確認結果モデル（Ｒ）
#
# ヒント：accountTypeが都道府県の場合、新規に調査結果データを生成し、都道府県名等をセットし、ページに表示する。
# ヒント：accountTypeが本省の場合、引数のparentUploadIdをキーに、ＤＢから調査結果データを取得し、ページに表示する。
# ヒント：accountTypeが運用業者の場合、この機能は提供しないため、エラーページを表示する。
# ヒント：都道府県からの呼び出しの場合、parentUploadIdはNull
# ヒント：本省からの呼び出しの場合、parentUploadIdはNot Null
# ヒント：運用業者からの呼び出しの場合、アクセスは想定せず、不正アクセスとしてエラーページを返す。
# ヒント：理由
# ヒント：都道府県からの呼び出しの場合、新規に調査結果を生成するので、また、parentUploadIDはテーブルのユニークキーのため、Do関数内でDBのSEQを使用して生成する。
# ヒント：都道府県からの調査結果に対して本省が確認結果を登録するため、本省からの呼び出しの場合、どの調査結果に対する確認結果を示すparentUploadIdがセットされていると想定する。
# ヒント：調査結果と確認結果は同じテーブルを用いる。
# ヒント：調査結果と確認結果はペアになるが、レコードは別々のレコードとする。
# ヒント：１件の調査結果に対して、確認結果は１件とする。後で拡張する可能性あり。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def UploadAddView(request, accountType, accountId, operationYear, kenUploadId, honUploadId, kenHonOpeFlag):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P12.UploadAddView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１２Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P12.UploadAddView関数 P12A10', 'INFO')
        print_log('[INFO] P12.UploadAddView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P12.UploadAddView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P12.UploadAddView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P12.UploadAddView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P12.UploadAddView.kenUploadId = {}'.format(kenUploadId), 'INFO')
        print_log('[INFO] P12.UploadAddView.honUploadId = {}'.format(honUploadId), 'INFO')
        print_log('[INFO] P12.UploadAddView.kenHonOpeFlag = {}'.format(kenHonOpeFlag), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１２Ａ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        # （７）本省アップロードＩＤをチェックする。　例　1
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        # ヒント：都道府県アップロードＩＤ、本省アップロードＩＤは、本来、ビジネスロジックとしては、いずれかがセットされているものである。
        # ヒント：この方法の場合、urls.pyの記述を複数用意しなければならないこと、関数を最悪複数用意しなければならないこと等、デメリットがある。
        # ヒント：そこで、未セットのＩＤには０をダミーとしてセットし、どちらが有効かをkenHonOpeFlagで判別するようにした。
        # ヒント：したがって、以下のチェック処理でもいずれにもセットされていることを正常とし、それ以外を異常としている。
        ##########################################
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        if accountId == str(request.user.username):
            pass
        else:
            print_log('[WARN] P12.UploadAddView関数 P12A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P12.UploadAddView関数 P12A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2':
            pass
        elif accountType == '3':
            print_log('[WARN] P12.UploadAddView関数 P12A20-3', 'WARN')
            return render(request, 'error.html')
        else:
            print_log('[WARN] P12.UploadAddView関数 P12A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P12.UploadAddView関数 P12A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P12.UploadAddView関数 P12A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P12.UploadAddView関数 P12A20-5', 'WARN')
                return render(request, 'error.html')
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        # ヒント：都道府県の場合、調査結果を新規で登録するため、kenUploadIdにはダミーの値がセットされていると想定する。
        # ヒント：本省の場合、都道府県からの調査結果に対して確認結果を新規で登録するため、kenUploadIdには有効な値がセットされていると想定する。
        if kenUploadId is None:
            print_log('[WARN] P12.UploadAddView関数 P12A20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenUploadId) == True:
                pass
            else:
                print_log('[WARN] P12.UploadAddView関数 P12A20-6', 'WARN')
                return render(request, 'error.html')
        # （７）本省アップロードＩＤをチェックする。　例　1
        if honUploadId is None:
            print_log('[WARN] P12.UploadAddView関数 P12A20-7', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(honUploadId) == True:
                pass
            else:
                print_log('[WARN] P12.UploadAddView関数 P12A20-7', 'WARN')
                return render(request, 'error.html')
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        if kenHonOpeFlag is None:
            print_log('[WARN] P12.UploadAddView関数 P12A20-8', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenHonOpeFlag) == True:
                pass
            else:
                print_log('[WARN] P12.UploadAddView関数 P12A20-8', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ１２Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P12.UploadAddView関数 P12A30', 'INFO')
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
            print_log('[ERROR] P12.UploadAddView関数 P12A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P12.UploadAddView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。         
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P12.UploadAddView関数 P12A30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P12.UploadAddView関数 P12A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、アップロードデータ取得処理（Ｐ１２Ａ４０）
        # （１）アップロードデータ、アップロードファイルデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、アップロードデータ、アップロードファイルデータを取得する。
        # ヒント：都道府県の場合は、調査結果データを生成する。
        # ヒント：本省の場合は、既に都道府県が調査結果を登録済と想定し、画面表示用に、ＤＢからこのデータを取得する。
        # ヒント：運用業者の場合は、ここにはこないと想定する。return済。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：KEN_UPLOAD_ID、HON_UPLOAD_IDが親子関係を示すものとしてＤＢに格納されているため、
        # ヒント：データの取得時には、KEN_HON_OPE_FLAGも検索のキーにセットすることを想定している。
        ##########################################
        print_log('[INFO] P12.UploadAddView関数 P12A40', 'INFO')
        # （１）アップロードデータ、アップロードファイルデータを格納する局所変数を初期化する。
        localUploadModel = None
        localUploadFileModel = None
        # （２）ＤＢにアクセスし、アップロードデータ、アップロードファイルデータを取得する。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                localUploadModel = UploadModel()
                localUploadFileModel = UploadFileModel()
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                try:
                    localUploadModel = UploadModel.objects.raw("""
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
                    localUploadModel = None        
                    print_log('[ERROR] P12.UploadAddView関数 P12A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P12.UploadAddView関数で警告が発生しました。', 'ERROR')
                    print_log('[ERROR] P12.UploadAddView関数を警告終了しました。', 'ERROR')
                try:    
                    localUploadFileModel = UploadFileModel.objects.raw("""
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
                    localUploadFileModel = None        
                    print_log('[ERROR] P12.UploadAddView関数 P12A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P12.UploadAddView関数で警告が発生しました。', 'ERROR')
                    print_log('[ERROR] P12.UploadAddView関数を警告終了しました。', 'ERROR')
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                print_log('[ERROR] P12.UploadAddView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P12.UploadAddView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P12.UploadAddView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P12.UploadAddView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P12.UploadAddView関数 P12A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P12.UploadAddView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # フォームセット処理（Ｐ１２Ａ５０）
        # （１）局所変数のフォームを初期化する。
        # ヒント：ブラウザとのデータのやりとり、特にブラウザからPOSTデータがある場合、フォームを使用する。
        # ヒント：モデルはブラウザで参照用、かつタグをコーディングする場合等に使用する。
        # ヒント：フォームはブラウザで編集用、POSTでサーバにリクエストされる項目、かつタグを自動生成する場合等に使用する。
        ##########################################
        print_log('[INFO] P12.UploadAddView関数 P12A50', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localAddDate = datetime.now().strftime("%Y/%m/%d")
        localAddDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        localUploadAddForm = UploadAddForm()
        ##########################################
        # フォームセット処理（Ｐ１２Ａ５１）
        # （１）局所変数のフォームに初期値をセットする。
        ##########################################
        # （１）局所変数のフォームに初期値をセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            # ヒント：アップロードデータ項目に初期値をセットする。
            localUploadAddForm.initial['KEN_UPLOAD_ID'] = "NULL"                                   # P12-1
            localUploadAddForm.initial['KEN_KEN_HON_OPE_FLAG'] = "1"                               # P12-2
            localUploadAddForm.initial['KEN_OPERATION_YEAR'] = urlquote(operationYear)             # P12-3
            localUploadAddForm.initial['KEN_FLOOD_YEAR'] = urlquote(operationYear)                 # P12-4
            
            if localAccountModel != None:
                localUploadAddForm.initial['KEN_ORG_CODE'] = localAccountModel.ORG_CODE            # P12-6
                localUploadAddForm.initial['KEN_ORG_NAME'] = localAccountModel.ORG_NAME            # P12-7
                localUploadAddForm.initial['KEN_DEPT_CODE'] = localAccountModel.DEPT_CODE          # P12-8
                localUploadAddForm.initial['KEN_DEPT_NAME'] = localAccountModel.DEPT_NAME          # P12-9
                localUploadAddForm.initial['KEN_ACCOUNT_ID'] = localAccountModel.ACCOUNT_ID        # P12-10
                localUploadAddForm.initial['KEN_ACCOUNT_NAME'] = localAccountModel.ACCOUNT_NAME    # P12-11
            else:
                localUploadAddForm.initial['KEN_ORG_CODE'] = "NULL"                                # P12-6
                localUploadAddForm.initial['KEN_ORG_NAME'] = "NULL"                                # P12-7
                localUploadAddForm.initial['KEN_DEPT_CODE'] = "NULL"                               # P12-8
                localUploadAddForm.initial['KEN_DEPT_NAME'] = "NULL"                               # P12-9
                localUploadAddForm.initial['KEN_ACCOUNT_ID'] = "NULL"                              # P12-10
                localUploadAddForm.initial['KEN_ACCOUNT_NAME'] = "NULL"                            # P12-11
                
            localUploadAddForm.initial['KEN_ADD_DATE'] = localAddDate                              # P12-12
            localUploadAddForm.initial['KEN_ADD_DATE_TIME'] = localAddDateTime                     # P12-13
            localUploadAddForm.initial['KEN_ADD_FLAG'] = "1"                                       # P12-14
            localUploadAddForm.initial['KEN_DELETE_DATE'] = "NULL"                                 # P12-15
            localUploadAddForm.initial['KEN_DELETE_DATE_TIME'] = "NULL"                            # P12-16
            localUploadAddForm.initial['KEN_DELETE_FLAG'] = "0"                                    # P12-17
            localUploadAddForm.initial['KEN_QUESTION_BODY'] = "NULL"                               # P12-19
            localUploadAddForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = "NULL"                    # P12-20
            localUploadAddForm.initial['KEN_UPLOAD_FILE_NAME'] = "NULL"                            # P12-18
            localUploadAddForm.initial['KEN_UPLOAD_FILE_ID'] = "NULL"                              # P12-18
            localUploadAddForm.initial['KEN_UPLOAD_FILE_PATH'] = "NULL"                            # P12-18

            localUploadAddForm.initial['HON_UPLOAD_ID'] = "NULL"                                   # P12-1
            localUploadAddForm.initial['HON_KEN_HON_OPE_FLAG'] = "NULL"                            # P12-2
            localUploadAddForm.initial['HON_OPERATION_YEAR'] = "NULL"                              # P12-3
            localUploadAddForm.initial['HON_FLOOD_YEAR'] = "NULL"                                  # P12-4
            localUploadAddForm.initial['HON_ORG_CODE'] = "NULL"                                    # P12-6
            localUploadAddForm.initial['HON_ORG_NAME'] = "NULL"                                    # P12-7
            localUploadAddForm.initial['HON_DEPT_CODE'] = "NULL"                                   # P12-8
            localUploadAddForm.initial['HON_DEPT_NAME'] = "NULL"                                   # P12-9
            localUploadAddForm.initial['HON_ACCOUNT_ID'] = "NULL"                                  # P12-10
            localUploadAddForm.initial['HON_ACCOUNT_NAME'] = "NULL"                                # P12-11
            localUploadAddForm.initial['HON_ADD_DATE'] = "NULL"                                    # P12-12
            localUploadAddForm.initial['HON_ADD_DATE_TIME'] = "NULL"                               # P12-13
            localUploadAddForm.initial['HON_ADD_FLAG'] = "NULL"                                    # P12-14
            localUploadAddForm.initial['HON_DELETE_DATE'] = "NULL"                                 # P12-15
            localUploadAddForm.initial['HON_DELETE_DATE_TIME'] = "NULL"                            # P12-16
            localUploadAddForm.initial['HON_DELETE_FLAG'] = "NULL"                                 # P12-17
            localUploadAddForm.initial['HON_QUESTION_BODY'] = "NULL"                               # P12-21
            localUploadAddForm.initial['HON_QUESTION_TO_HON_OPE_FLAG'] = "NULL"                    # P12-
            localUploadAddForm.initial['HON_UPLOAD_FILE_NAME'] = "NULL"                            # P12-
            localUploadAddForm.initial['HON_UPLOAD_FILE_ID'] = "NULL"                              # P12-
            localUploadAddForm.initial['HON_UPLOAD_FILE_PATH'] = "NULL"                            # P12-
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            # ヒント：アップロードデータ項目に初期値をセットする。
            if localUploadModel != None:
                localUploadAddForm.initial['KEN_UPLOAD_ID'] = localUploadModel.KEN_UPLOAD_ID # M1
                localUploadAddForm.initial['KEN_KEN_HON_OPE_FLAG'] = localUploadModel.KEN_HON_OPE_FLAG # M2
                localUploadAddForm.initial['KEN_OPERATION_YEAR'] = localUploadModel.OPERATION_YEAR # M3
                localUploadAddForm.initial['KEN_FLOOD_YEAR'] = localUploadModel.FLOOD_YEAR # M4
                localUploadAddForm.initial['KEN_ORG_CODE'] = localUploadModel.ORG_CODE # M6
                localUploadAddForm.initial['KEN_ORG_NAME'] = localUploadModel.ORG_NAME # M7
                localUploadAddForm.initial['KEN_DEPT_CODE'] = localUploadModel.DEPT_CODE # M8
                localUploadAddForm.initial['KEN_DEPT_NAME'] = localUploadModel.DEPT_NAME # M9
                localUploadAddForm.initial['KEN_ACCOUNT_ID'] = localUploadModel.ACCOUNT_ID # M10
                localUploadAddForm.initial['KEN_ACCOUNT_NAME'] = localUploadModel.ACCOUNT_NAME # M11
                localUploadAddForm.initial['KEN_ADD_DATE'] = localUploadModel.ADD_DATE # M12
                localUploadAddForm.initial['KEN_ADD_DATE_TIME'] = localUploadModel.ADD_DATE_TIME # M13
                localUploadAddForm.initial['KEN_ADD_FLAG'] = localUploadModel.ADD_FLAG # M14
                localUploadAddForm.initial['KEN_DELETE_DATE'] = localUploadModel.DELETE_DATE # M15
                localUploadAddForm.initial['KEN_DELETE_DATE_TIME'] = localUploadModel.DELETE_DATE_TIME # M16
                localUploadAddForm.initial['KEN_DELETE_FLAG'] = localUploadModel.DELETE_FLAG # M17
                localUploadAddForm.initial['KEN_QUESTION_BODY'] = localUploadModel.QUESTION_BODY # M18
                localUploadAddForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = localUploadModel.QUESTION_TO_HON_OPE_FLAG # M19
            else:
                localUploadAddForm.initial['KEN_UPLOAD_ID'] = "NULL" # M1
                localUploadAddForm.initial['KEN_KEN_HON_OPE_FLAG'] = "NULL" # M2
                localUploadAddForm.initial['KEN_OPERATION_YEAR'] = "NULL" # M3
                localUploadAddForm.initial['KEN_FLOOD_YEAR'] = "NULL" # M4
                localUploadAddForm.initial['KEN_ORG_CODE'] = "NULL" # M6
                localUploadAddForm.initial['KEN_ORG_NAME'] = "NULL" # M7
                localUploadAddForm.initial['KEN_DEPT_CODE'] = "NULL" # M8
                localUploadAddForm.initial['KEN_DEPT_NAME'] = "NULL" # M9
                localUploadAddForm.initial['KEN_ACCOUNT_ID'] = "NULL" # M10
                localUploadAddForm.initial['KEN_ACCOUNT_NAME'] = "NULL" # M11
                localUploadAddForm.initial['KEN_ADD_DATE'] = "NULL" # M12
                localUploadAddForm.initial['KEN_ADD_DATE_TIME'] = "NULL" # M13
                localUploadAddForm.initial['KEN_ADD_FLAG'] = "NULL" # M14
                localUploadAddForm.initial['KEN_DELETE_DATE'] = "NULL" # M15
                localUploadAddForm.initial['KEN_DELETE_DATE_TIME'] = "NULL" # M16
                localUploadAddForm.initial['KEN_DELETE_FLAG'] = "NULL" # M17
                localUploadAddForm.initial['KEN_QUESTION_BODY'] = "NULL" # M18
                localUploadAddForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = "NULL" # M19
            if localUploadFileModel != None:
                localUploadAddForm.initial['KEN_UPLOAD_FILE_NAME'] = localUploadFileModel.KEN_UPLOAD_FILE_NAME # M1
                localUploadAddForm.initial['KEN_UPLOAD_FILE_ID'] = localUploadFileModel.KEN_UPLOAD_FILE_ID # M1
                localUploadAddForm.initial['KEN_UPLOAD_FILE_PATH'] = localUploadFileModel.KEN_UPLOAD_FILE_PATH # M1
            else:
                localUploadAddForm.initial['KEN_UPLOAD_FILE_NAME'] = "NULL" # M1
                localUploadAddForm.initial['KEN_UPLOAD_FILE_ID'] = "NULL"
                localUploadAddForm.initial['KEN_UPLOAD_FILE_PATH'] = "NULL"

            localUploadAddForm.initial['HON_UPLOAD_ID'] = "NULL" # M1
            localUploadAddForm.initial['HON_KEN_HON_OPE_FLAG'] = "2" # M2
            localUploadAddForm.initial['HON_OPERATION_YEAR'] = urlquote(operationYear) # M3
            localUploadAddForm.initial['HON_FLOOD_YEAR'] = urlquote(operationYear) # M4
            if localAccountModel != None:
                localUploadAddForm.initial['HON_ORG_CODE'] = localAccountModel.ORG_CODE # M6
                localUploadAddForm.initial['HON_ORG_NAME'] = localAccountModel.ORG_NAME # M7
                localUploadAddForm.initial['HON_DEPT_CODE'] = localAccountModel.DEPT_CODE # M8
                localUploadAddForm.initial['HON_DEPT_NAME'] = localAccountModel.DEPT_NAME # M9
                localUploadAddForm.initial['HON_ACCOUNT_ID'] = localAccountModel.ACCOUNT_ID # N10
                localUploadAddForm.initial['HON_ACCOUNT_NAME'] = localAccountModel.ACCOUNT_NAME # M11
            else:
                localUploadAddForm.initial['HON_ORG_CODE'] = "NULL"                                # M6
                localUploadAddForm.initial['HON_ORG_NAME'] = "NULL"                                # M7
                localUploadAddForm.initial['HON_DEPT_CODE'] = "NULL"                               # M8
                localUploadAddForm.initial['HON_DEPT_NAME'] = "NULL"                               # M9
                localUploadAddForm.initial['HON_ACCOUNT_ID'] = "NULL"                              # N10
                localUploadAddForm.initial['HON_ACCOUNT_NAME'] = "NULL"                            # M11
            localUploadAddForm.initial['HON_ADD_DATE'] = localAddDate                              # M12
            localUploadAddForm.initial['HON_ADD_DATE_TIME'] = localAddDateTime                     # M13
            localUploadAddForm.initial['HON_ADD_FLAG'] = "1"                                       # M14
            localUploadAddForm.initial['HON_DELETE_DATE'] = "NULL"                                 # M15
            localUploadAddForm.initial['HON_DELETE_DATE_TIME'] = "NULL"                            # M16
            localUploadAddForm.initial['HON_DELETE_FLAG'] = "0"                                    # M17
            localUploadAddForm.initial['HON_QUESTION_BODY'] = "NULL"                               # M18
            localUploadAddForm.initial['HON_QUESTION_TO_HON_OPE_FLAG'] = "NULL"                    # M19
            localUploadAddForm.initial['HON_UPLOAD_FILE_NAME'] = "NULL"                            # M1
            localUploadAddForm.initial['HON_UPLOAD_FILE_ID'] = "NULL"                              # M1
            localUploadAddForm.initial['HON_UPLOAD_FILE_PATH'] = "NULL"                            # M1
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P12.UploadAddView関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddView関数が異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # 調査結果または確認結果フラグ＝上記以外の場合、、、
            print_log('[ERROR] P12.UploadAddView関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddView関数が異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################            
        # フォームセット処理（Ｐ１２Ａ５２）
        # （１）フォームのウィジェットの属性に値をセットする。（都道府県項目）
        # （２）フォームのウィジェットの属性に値をセットする。（本省項目）
        # ヒント：利用者が編集できない項目は、disabled、readonlyのいずれかとする。
        # ヒント：フォームを使用した場合、ブラウザでタグが自動生成されるため、ブラウザのstyle、cssでdisable、readonlyをセットしにくい。
        # ヒント：そのため。ビュー関数でdisable、readonly等をセットする。
        # ヒント：フォームのフィールドは、非表示の項目もセットすることを推奨する。
        # ヒント：ステートレスなウェブアプリにおいて、ブラウザに送ったデータをPOST時にサーバ側のビュー関数で参照可能とするため。
        ##########################################            
        localUploadAddForm.fields['KEN_UPLOAD_ID'].widget.attrs['readonly'] = True                 # P12-
        localUploadAddForm.fields['KEN_KEN_HON_OPE_FLAG'].widget.attrs['readonly'] = True          # P12- 
        localUploadAddForm.fields['KEN_OPERATION_YEAR'].widget.attrs['readonly'] = True            # P12- 
        localUploadAddForm.fields['KEN_FLOOD_YEAR'].widget.attrs['readonly'] = True                # P12- 
        localUploadAddForm.fields['KEN_ORG_CODE'].widget.attrs['readonly'] = True                  # P12- 
        localUploadAddForm.fields['KEN_ORG_NAME'].widget.attrs['readonly'] = True                  # P12-     
        localUploadAddForm.fields['KEN_DEPT_CODE'].widget.attrs['readonly'] = True                 # P12- 
        localUploadAddForm.fields['KEN_DEPT_NAME'].widget.attrs['readonly'] = True                 # P12-     
        localUploadAddForm.fields['KEN_ACCOUNT_ID'].widget.attrs['readonly'] = True                # P12-     
        localUploadAddForm.fields['KEN_ACCOUNT_NAME'].widget.attrs['readonly'] = True              # P12- 
        localUploadAddForm.fields['KEN_ADD_DATE'].widget.attrs['readonly'] = True                  # P12- 
        localUploadAddForm.fields['KEN_ADD_DATE_TIME'].widget.attrs['readonly'] = True             # P12-     
        localUploadAddForm.fields['KEN_ADD_FLAG'].widget.attrs['readonly'] = True                  # P12- 
        localUploadAddForm.fields['KEN_DELETE_DATE'].widget.attrs['readonly'] = True               # P12- 
        localUploadAddForm.fields['KEN_DELETE_DATE_TIME'].widget.attrs['readonly'] = True          # P12- 
        localUploadAddForm.fields['KEN_DELETE_FLAG'].widget.attrs['readonly'] = True               # P12- 
        localUploadAddForm.fields['KEN_QUESTION_BODY'].widget.attrs['readonly'] = False            # P12- 
        localUploadAddForm.fields['KEN_QUESTION_TO_HON_OPE_FLAG'].widget.attrs['readonly'] = True  # P12- 
        localUploadAddForm.fields['KEN_UPLOAD_FILE_NAME'].widget.attrs['readonly'] = False         # P12- 
        localUploadAddForm.fields['KEN_UPLOAD_FILE_ID'].widget.attrs['readonly'] = False           # P12- 
        localUploadAddForm.fields['KEN_UPLOAD_FILE_PATH'].widget.attrs['readonly'] = False         # P12- 
        localUploadAddForm.fields['HON_UPLOAD_ID'].widget.attrs['readonly'] = True                 # P12- 
        localUploadAddForm.fields['HON_KEN_HON_OPE_FLAG'].widget.attrs['readonly'] = True          # P12- 
        localUploadAddForm.fields['HON_OPERATION_YEAR'].widget.attrs['readonly'] = True            # P12- 
        localUploadAddForm.fields['HON_FLOOD_YEAR'].widget.attrs['readonly'] = True                # P12- 
        localUploadAddForm.fields['HON_ORG_CODE'].widget.attrs['readonly'] = True                  # P12- 
        localUploadAddForm.fields['HON_ORG_NAME'].widget.attrs['readonly'] = True                  # P12-     
        localUploadAddForm.fields['HON_DEPT_CODE'].widget.attrs['readonly'] = True                 # P12- 
        localUploadAddForm.fields['HON_DEPT_NAME'].widget.attrs['readonly'] = True                 # P12- 
        localUploadAddForm.fields['HON_ACCOUNT_ID'].widget.attrs['readonly'] = True                # P12- 
        localUploadAddForm.fields['HON_ACCOUNT_NAME'].widget.attrs['readonly'] = True              # P12-     
        localUploadAddForm.fields['HON_ADD_DATE'].widget.attrs['readonly'] = True                  # P12- 
        localUploadAddForm.fields['HON_ADD_DATE_TIME'].widget.attrs['readonly'] = True             # P12- 
        localUploadAddForm.fields['HON_ADD_FLAG'].widget.attrs['readonly'] = True                  # P12- 
        localUploadAddForm.fields['HON_DELETE_DATE'].widget.attrs['readonly'] = True               # P12- 
        localUploadAddForm.fields['HON_DELETE_DATE_TIME'].widget.attrs['readonly'] = True          # P12- 
        localUploadAddForm.fields['HON_DELETE_FLAG'].widget.attrs['readonly'] = True               # P12- 
        localUploadAddForm.fields['HON_QUESTION_BODY'].widget.attrs['readonly'] = False            # P12- 
        localUploadAddForm.fields['HON_QUESTION_TO_HON_OPE_FLAG'].widget.attrs['readonly'] = True  # P12- 
        localUploadAddForm.fields['HON_UPLOAD_FILE_NAME'].widget.attrs['readonly'] = False         # P12- 
        localUploadAddForm.fields['HON_UPLOAD_FILE_ID'].widget.attrs['readonly'] = False           # P12- 
        localUploadAddForm.fields['HON_UPLOAD_FILE_PATH'].widget.attrs['readonly'] = False         # P12- 
        ##########################################
        # レスポンスセット処理（Ｐ１２Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        # ヒント：登録済フラグがTrueの場合、テンプレートでは、登録結果を表示する処理を想定する。
        # ヒント：登録済フラグがFalseの場合、テンプレートでは、これから登録するデータを表示し、利用者が編集を加えると想定する。
        # ヒント：必須項目の未入力等に対応するため、１画面で新規登録用の画面と、結果表示用の画面の両方が処理できたほうが効率が良いため。
        # ヒント：また、テンプレートファイルの記述は、それほど複雑にはならないためこのように実装する。
        ##########################################
        print_log('[INFO] P12.UploadAddView関数 P12A60', 'INFO')
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
                'uploadAddForm': localUploadAddForm,       # アップロードデータ登録画面用のフォーム
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区別＝２：本省の場合、、、
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'uploadAddForm': localUploadAddForm,       # アップロードデータ登録画面用のフォーム
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P12.UploadAddView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P12.UploadAddView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P12.UploadAddView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１２Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P12.UploadAddView関数 P12A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P12UploadAddTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P12UploadAddTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P12.UploadAddView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P12.UploadAddView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ１２Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P12.UploadAddView関数 P12A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P12.UploadAddView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P12.UploadAddView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１２Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P12.UploadAddView関数 P12A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
#####################################################################################
# 関数名：P12.UploadAddDoView（Ｐ１２Ｂ）
# 関数概要：都道府県用調査結果登録ページでセットされた値をＤＢに仮登録する。（都道府県）
# 関数概要：本省用確認結果登録ページでセットされた値をＤＢに仮登録する。（本省）
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
# FORM：UploadAddForm：都道府県用調査結果登録ページ（都道府県）
# FORM：UploadAddForm：本省用確認結果登録ページ（本省）
# FORM：UploadAddForm：運用業者用確認結果登録ページ（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：UploadModel：調査結果または確認結果モデル（Ｃ）
# ヒント：都道府県からの呼び出しの場合、parentUploadIdはNull
# ヒント：本省からの呼び出しの場合、parentUploadIdはNot Null
# ヒント：運用業者からの呼び出しの場合、アクセスは想定せず、不正アクセスとしてエラーページを返す。
# ヒント：理由
# ヒント：都道府県からの呼び出しの場合、新規に調査結果を生成するので、また、parentUploadIDはテーブルのユニークキーのため、Do関数内でDBのSEQを使用して生成する。
# ヒント：都道府県からの調査結果に対して本省が確認結果を登録するため、本省からの呼び出しの場合、どの調査結果に対する確認結果かを示すparentUploadIdがセットされていると想定する。
# ヒント：運用業者からの呼び出しの場合、アクセスは想定せず、不正アクセスとしてエラーページを返す。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def UploadAddDoView(request, accountType, accountId, operationYear, kenUploadId, honUploadId, kenHonOpeFlag):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P12.UploadAddDoView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１２Ｂ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P12.UploadAddDoView関数 P12B10', 'INFO')
        print_log('[INFO] P12.UploadAddDoView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P12.UploadAddDoView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P12.UploadAddDoView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P12.UploadAddDoView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P12.UploadAddDoView.kenUploadId = {}'.format(kenUploadId), 'INFO')
        print_log('[INFO] P12.UploadAddDoView.honUploadId = {}'.format(honUploadId), 'INFO')
        print_log('[INFO] P12.UploadAddDoView.kenHonOpeFlag = {}'.format(kenHonOpeFlag), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１２Ｂ２０）
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
            print_log('[WARN] P12.UploadAddDoView関数 P12B20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'POST':
            pass
        else:
            print_log('[WARN] P12.UploadAddDoView関数 P12B20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2':
            pass
        elif accountType == '3':
            print_log('[WARN] P12.UploadAddDoView関数 P12B20-3', 'WARN')
            return render(request, 'error.html')
        else:
            print_log('[WARN] P12.UploadAddDoView関数 P12B20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P12.UploadAddDoView関数 P12B20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P12.UploadAddDoView関数 P12B20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P12.UploadAddDoView関数 P12B20-5', 'WARN')
                return render(request, 'error.html')
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        if kenUploadId is None:
            print_log('[WARN] P12.UploadAddDoView関数 P23B20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenUploadId) == True:
                pass
            else:    
                print_log('[WARN] P12.UploadAddDoView関数 P12B20-6', 'WARN')
                return render(request, 'error.html')
        # （７）本省アップロードＩＤをチェックする。　例　1
        if honUploadId is None:
            print_log('[WARN] P12.UploadAddDoView関数 P12B20-7', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(honUploadId) == True:
                pass
            else:
                print_log('[WARN] P12.UploadAddDoView関数 P12B20-7', 'WARN')
                return render(request, 'error.html')
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        if kenHonOpeFlag is None:
            print_log('[WARN] P12.UploadAddoView関数 P12A20-8', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenHonOpeFlag) == True:
                pass
            else:
                print_log('[WARN] P12.UploadAddDoView関数 P12A20-8', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ１２Ｂ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P12.UploadAddDoView関数 P12B30', 'INFO')
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        localAccountModel = None
        # アカウントＩＤ、水害対象年（業務実施年）をキーにＤＢからアカウント情報を取得する。
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
            print_log('[ERROR] P12.UploadAddDoView関数 P12B30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P12.UploadAddDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P12.UploadAddDoView関数 P12B30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P12.UploadAddDoView関数 P12B30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # フォームセット処理（Ｐ１２Ｂ４０）
        # （１）局所変数のフォームを初期化する。
        # （２）画面からポストされた情報を取得する。
        # ヒント：運用業者の場合は、ここにはこないと想定する。return済。
        # ヒント：画面からポストされた情報をlocalFormに一時的に格納する。
        # ヒント：localFormの値をチェックしながら、格納用のlocalAddConfirmFormに値をチェットする。
        ##########################################
        print_log('[INFO] P12.UploadAddDoView関数 P12B40', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localForm = None
        localAddForm = UploadAddForm()
        # （２）画面からポストされた情報を取得する。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                localForm = UploadAddForm(request.POST, request.FILES)
                if localForm.is_valid():
                    localAddForm.KEN_UPLOAD_ID = localForm.cleaned_data['KEN_UPLOAD_ID']
                    localAddForm.KEN_KEN_HON_OPE_FLAG = '1'
                    localAddForm.KEN_OPERATION_YEAR = localForm.cleaned_data['KEN_OPERATION_YEAR']
                    localAddForm.KEN_FLOOD_YEAR = localForm.cleaned_data['KEN_FLOOD_YEAR']
                    localAddForm.KEN_ORG_CODE = localForm.cleaned_data['KEN_ORG_CODE']
                    localAddForm.KEN_ORG_NAME = localForm.cleaned_data['KEN_ORG_NAME']
                    localAddForm.KEN_DEPT_CODE = localForm.cleaned_data['KEN_DEPT_CODE']
                    localAddForm.KEN_DEPT_NAME = localForm.cleaned_data['KEN_DEPT_NAME']
                    localAddForm.KEN_ACCOUNT_ID = localForm.cleaned_data['KEN_ACCOUNT_ID']
                    localAddForm.KEN_ACCOUNT_NAME = localForm.cleaned_data['KEN_ACCOUNT_NAME']
                    localAddForm.KEN_ADD_DATE = localForm.cleaned_data['KEN_ADD_DATE']
                    localAddForm.KEN_ADD_DATE_TIME = localForm.cleaned_data['KEN_ADD_DATE_TIME']
                    localAddForm.KEN_ADD_FLAG = localForm.cleaned_data['KEN_ADD_FLAG']
                    localAddForm.KEN_DELETE_DATE = localForm.cleaned_data['KEN_DELETE_DATE']
                    localAddForm.KEN_DELETE_DATE_TIME = localForm.cleaned_data['KEN_DELETE_DATE_TIME']
                    localAddForm.KEN_DELETE_FLAG = localForm.cleaned_data['KEN_DELETE_FLAG']
                    # ヒント：./01hokkai/aaa.lzhにファイルを格納する。
                    # ヒント：事前に全アカウントＩＤについて、ディレクトリを作成しておくことを想定する。
                    # ヒント：ＤＢに登録するデータにも上記ディレクトリ、ファイル名をセットすることを想定する。
                    localAddForm.KEN_UPLOAD_FILE_NAME = localForm.cleaned_data['KEN_UPLOAD_FILE_NAME']
                    localAddForm.KEN_UPLOAD_FILE_ID = localForm.cleaned_data['KEN_UPLOAD_FILE_ID']
                    localAddForm.KEN_UPLOAD_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId)
                    localAddForm.KEN_QUESTION_BODY = localForm.cleaned_data['KEN_QUESTION_BODY']
                    localAddForm.KEN_QUESTION_TO_HON_OPE_FLAG = localForm.cleaned_data['KEN_QUESTION_TO_HON_OPE_FLAG']
                else:
                    pass
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                localForm = UploadAddForm(request.POST, request.FILES)
                if localForm.is_valid():
                    localAddForm.HON_UPLOAD_ID = localForm.cleaned_data['HON_UPLOAD_ID']
                    localAddForm.HON_KEN_HON_OPE_FLAG = '2'
                    localAddForm.HON_OPERATION_YEAR = localForm.cleaned_data['HON_OPERATION_YEAR']
                    localAddForm.HON_FLOOD_YEAR = localForm.cleaned_data['HON_FLOOD_YEAR']
                    localAddForm.HON_ORG_CODE = localForm.cleaned_data['HON_ORG_CODE']
                    localAddForm.HON_ORG_NAME = localForm.cleaned_data['HON_ORG_NAME']
                    localAddForm.HON_DEPT_CODE = localForm.cleaned_data['HON_DEPT_CODE']
                    localAddForm.HON_DEPT_NAME = localForm.cleaned_data['HON_DEPT_NAME']
                    localAddForm.HON_ACCOUNT_ID = localForm.cleaned_data['HON_ACCOUNT_ID']
                    localAddForm.HON_ACCOUNT_NAME = localForm.cleaned_data['HON_ACCOUNT_NAME']
                    localAddForm.HON_ADD_DATE = localForm.cleaned_data['HON_ADD_DATE']
                    localAddForm.HON_ADD_DATE_TIME = localForm.cleaned_data['HON_ADD_DATE_TIME']
                    localAddForm.HON_ADD_FLAG = localForm.cleaned_data['HON_ADD_FLAG']
                    localAddForm.HON_DELETE_DATE = localForm.cleaned_data['HON_DELETE_DATE']
                    localAddForm.HON_DELETE_DATE_TIME = localForm.cleaned_data['HON_DELETE_DATE_TIME']
                    localAddForm.HON_DELETE_FLAG = localForm.cleaned_data['HON_DELETE_FLAG']
                    # ヒント：./keizai/aaa.lzhにファイルを格納する
                    # ヒント：事前に全アカウントＩＤについて、ディレクトリを作成しておくことを想定する。
                    # ヒント：ＤＢに登録するデータにも上記ディレクトリ、ファイル名をセットすることを想定する。
                    localAddForm.HON_UPLOAD_FILE_NAME = localForm.cleaned_data['HON_UPLOAD_FILE_NAME']
                    localAddForm.HON_UPLOAD_FILE_ID = localForm.cleaned_data['HON_UPLOAD_FILE_ID']
                    localAddForm.HON_UPLOAD_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId)
                    localAddForm.HON_QUESTION_BODY = localForm.cleaned_data['HON_QUESTION_BODY']
                    localAddForm.HON_QUESTION_TO_HON_OPE_FLAG = localForm.cleaned_data['HON_QUESTION_TO_HON_OPE_FLAG']
                else:
                    pass
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                print_log('[ERROR] P12.UploadAddDoView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P12.UploadAddDoView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P12.UploadAddDoView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P12.UploadAddDoView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P12.UploadAddDoView関数 P12B40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P12.UploadAddDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # 局所変数セット処理（Ｐ１２Ｂ４５）
        # （１）問合せ回答データの局所変数に初期値をセットする。
        ##########################################
        print_log('[INFO] P12.UploadAddDoView関数 P12B45', 'INFO')
        localAddDate = datetime.now().strftime("%Y/%m/%d")
        localAddDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        ##########################################
        # ファイル受信処理（Ｐ１２Ｂ５０）
        # （１）画面からポストされたファイルを受信し、サーバに保存する。
        ##########################################
        print_log('[INFO] P12.UploadAddDoView関数 P12B50', 'INFO')
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                # ヒント：./01hokkai/aaa.lzhにファイルを格納する。
                # ヒント：事前に全アカウントＩＤについて、ディレクトリを作成しておくことを想定する。
                # ヒント：ＤＢに登録するデータにも上記ディレクトリ、ファイル名をセットすることを想定する。
                ### localTempDir = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId, (localAddForm.KEN_UPLOAD_FILE_NAME.name)), 'wb+')
                localTempDir = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId, (((localAddDateTime.replace(' ', '')).replace('/', '')).replace(':', '') + localAddForm.KEN_UPLOAD_FILE_NAME.name)), 'wb+')
                for localChunk in request.FILES['KEN_UPLOAD_FILE_NAME'].chunks():
                    localTempDir.write(localChunk)
                localTempDir.close()
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                # ヒント：./keizai/aaa.lzhにファイルを格納する
                # ヒント：事前に全アカウントＩＤについて、ディレクトリを作成しておくことを想定する。
                # ヒント：ＤＢに登録するデータにも上記ディレクトリ、ファイル名をセットすることを想定する。
                ### localTempDir = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId, (localAddForm.HON_UPLOAD_FILE_NAME.name)), 'wb+')
                localTempDir = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId, (((localAddDateTime.replace(' ', '')).replace('/', '')).replace(':', '') + localAddForm.HON_UPLOAD_FILE_NAME.name)), 'wb+')
                for localChunk in request.FILES['HON_UPLOAD_FILE_NAME'].chunks():
                    localTempDir.write(localChunk)
                localTempDir.close()
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                # ここでは何もしない。
                pass
            else:
                # ログインした利用者のアカウント種別・区分＝その他の場合、、、
                # ここでは何もしない。
                pass
        except:    
            print_log('[ERROR] P12.UploadAddDoView関数 P12B50', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P12.UploadAddDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、アップロードデータ登録処理（Ｐ１２Ｂ６０）
        # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
        # （２）ＳＱＬ文を実行する。
        # （３）トランザクション管理でコミットする。
        # （４）ＤＢ接続を切断＝カーソルを閉じる。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：運用業者の場合は、ここにはこないと想定する。return済。
        # ヒント：rawはUPDATE文では使えないため、カーソルを利用する。
        ##########################################
        print_log('[INFO] P12.UploadAddDoView関数 P12B60', 'INFO')
        try:
            # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
            # （２）ＳＱＬ文を実行する。
            # （３）トランザクション管理でコミットする。
            localCursor = connection.cursor()
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                # ヒント：file_upload_uploadテーブルにレコードを追加する。（登録フラグの状態＝仮登録済＝1）
                # ヒント：仮登録済とは、レコードは登録済、ＩＤも付与済、登録フラグが仮登録済＝1の状態をいう。
                # ヒント：ＩＤにＤＢから取得した最大値＋１をセットする。
                # ヒント：SELECT MAX(KEN_UPLOAD_ID + 0)としているが、KEN_UPLOAD_IDは文字列のため、0を足すことで、
                # ヒント：暗黙の型変換がＤＢ内で実行され、最大値を取得可能となる。
                # ヒント：+0しないと、暗黙の型変換が実行されず、エラーとなるので注意すること。                
                try:
                    localCursor.execute("""
                        INSERT INTO FILE_UPLOAD_UPLOAD (
                            id, 
                            KEN_UPLOAD_ID, 
                            HON_UPLOAD_ID,
                            KEN_HON_OPE_FLAG, 
                            OPERATION_YEAR, 
                            FLOOD_YEAR,
                            ORG_CODE, 
                            ORG_NAME,
                            DEPT_CODE, 
                            DEPT_NAME,
                            ACCOUNT_ID, 
                            ACCOUNT_NAME,
                            ADD_DATE,
                            ADD_DATE_TIME, 
                            ADD_FLAG,
                            DELETE_DATE, 
                            DELETE_DATE_TIME, 
                            DELETE_FLAG,
                            QUESTION_TO_HON_OPE_FLAG, 
                            QUESTION_BODY
                        ) VALUES (
                            (SELECT MAX(id + 1) FROM FILE_UPLOAD_UPLOAD), 
                            (SELECT MAX(KEN_UPLOAD_ID + 1) FROM FILE_UPLOAD_UPLOAD), 
                            '', 
                            %s, 
                            %s, 
                            %s,  
                            (SELECT ORG_CODE FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s), 
                            (SELECT ORG_NAME FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s),  
                            (SELECT DEPT_CODE FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s), 
                            (SELECT DEPT_NAME FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s), 
                            %s, 
                            (SELECT ACCOUNT_NAME FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s),  
                            %s, 
                            %s, 
                            %s,  
                            %s, 
                            %s, 
                            %s,  
                            %s, 
                            %s
                        )
                        """, 
                        [ '1',
                          localAddForm.KEN_OPERATION_YEAR, 
                          localAddForm.KEN_FLOOD_YEAR,
                          localAddForm.KEN_ACCOUNT_ID, 
                          localAddForm.KEN_ACCOUNT_ID,
                          localAddForm.KEN_ACCOUNT_ID, 
                          localAddForm.KEN_ACCOUNT_ID,
                          localAddForm.KEN_ACCOUNT_ID, 
                          localAddForm.KEN_ACCOUNT_ID,
                          localAddDate, 
                          localAddDateTime, 
                          '0', 
                          localAddForm.KEN_DELETE_DATE, 
                          localAddForm.KEN_DELETE_DATE_TIME, 
                          '0',
                          localAddForm.KEN_QUESTION_TO_HON_OPE_FLAG, 
                          localAddForm.KEN_QUESTION_BODY,  
                        ])
                    transaction.commit()
                except:
                    transaction.rollback()
                    print_log('[ERROR] P12.UploaAddDoView関数 P12B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P12.UploaAddDoView関数で警告が発生しました。', 'ERROR')
                try:    
                    localCursor.execute("""
                        SELECT 
                            MAX(KEN_UPLOAD_ID + 0) AS KEN_UPLOAD_ID 
                        FROM 
                            FILE_UPLOAD_UPLOAD 
                        WHERE 
                            ACCOUNT_ID=%s AND 
                            OPERATION_YEAR=%s 
                        LIMIT 1
                        """,
                        [ accountId, 
                          operationYear, 
                        ])
                    localResults = namedtuplefetchall(localCursor)
                    localUploadModel = UploadModel()
                    localUploadModel.KEN_UPLOAD_ID = localResults[0].KEN_UPLOAD_ID
                except:
                    localUploadModel = None
                    transaction.rollback()
                    print_log('[ERROR] P12.UploaAddDoView関数 P12B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P12.UploaAddDoView関数で警告が発生しました。', 'ERROR')
                # ヒント：file_upload_uploadfileテーブルの登録フラグを更新する。ファイルアップロードボタンでレコードは仮登録済と想定する。
                # ヒント：仮登録済とは、レコードは登録済、IDも付与済、登録フラグが仮登録済をいう。
                # ヒント：file_upload_uploadfileテーブルの登録スラグの状態＝仮登録済
                # ヒント：SELECT MAX(KEN_UPLOAD_ID + 0)としているが、KEN_UPLOAD_IDは文字列のため、0を足すことで、
                # ヒント：暗黙の型変換がＤＢ内で実行され、最大値を取得可能となる。
                # ヒント：+0しないと、暗黙の型変換が実行されず、エラーとなるので注意すること。                
                try:        
                    localCursor.execute("""
                        INSERT INTO FILE_UPLOAD_UPLOADFILE (
                            id, 
                            KEN_UPLOAD_FILE_ID, 
                            HON_UPLOAD_FILE_ID,
                            KEN_UPLOAD_ID, 
                            HON_UPLOAD_ID,
                            KEN_HON_OPE_FLAG,
                            OPERATION_YEAR, 
                            FLOOD_YEAR,
                            ADD_DATE, 
                            ADD_DATE_TIME, 
                            ADD_FLAG,
                            DELETE_DATE, 
                            DELETE_DATE_TIME, 
                            DELETE_FLAG,
                            KEN_UPLOAD_FILE_NAME, 
                            KEN_UPLOAD_FILE_PATH
                        ) VALUES (
                            (SELECT MAX(id + 1) FROM FILE_UPLOAD_UPLOADFILE), 
                            (SELECT MAX(KEN_UPLOAD_FILE_ID + 1) FROM FILE_UPLOAD_UPLOADFILE), 
                            '',
                            %s, 
                            '',
                            '1',
                            %s, 
                            %s,
                            %s, 
                            %s, 
                            %s,
                            %s, 
                            %s, 
                            %s,
                            %s, 
                            %s 
                        )
                        """,
                        [ localUploadModel.KEN_UPLOAD_ID,
                          localAddForm.KEN_OPERATION_YEAR, 
                          localAddForm.KEN_FLOOD_YEAR,
                          localAddDate, 
                          localAddDateTime, 
                          '0',
                          localAddForm.KEN_DELETE_DATE, 
                          localAddForm.KEN_DELETE_DATE_TIME, 
                          '0',
                          localAddForm.KEN_UPLOAD_FILE_NAME.name, 
                          os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId, (((localAddDateTime.replace(' ', '')).replace('/', '')).replace(':', '') + localAddForm.KEN_UPLOAD_FILE_NAME.name)),
                        ])
                    transaction.commit()
                except:    
                    transaction.rollback()
                    print_log('[ERROR] P12.UploaAddDoView関数 P12B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P12.UploaAddDoView関数で警告が発生しました。', 'ERROR')
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                # ヒント：file_upload_uploadテーブルにレコードを追加する。（登録フラグの状態＝仮登録済）
                # ヒント：仮登録済とは、レコードは登録済、IDも付与済、登録フラグが仮登録済をいう。
                # ヒント：IDにDBから取得した最大値＋１をセットする。
                # ヒント：SELECT MAX(KEN_UPLOAD_ID + 0)としているが、KEN_UPLOAD_IDは文字列のため、0を足すことで、
                # ヒント：暗黙の型変換がＤＢ内で実行され、最大値を取得可能となる。
                # ヒント：+0しないと、暗黙の型変換が実行されず、エラーとなるので注意すること。                
                try:
                    localCursor.execute("""
                        INSERT INTO FILE_UPLOAD_UPLOAD (
                            id, 
                            KEN_UPLOAD_ID, 
                            HON_UPLOAD_ID,
                            KEN_HON_OPE_FLAG, 
                            OPERATION_YEAR, 
                            FLOOD_YEAR,
                            ORG_CODE, 
                            ORG_NAME,
                            DEPT_CODE, 
                            DEPT_NAME,
                            ACCOUNT_ID, 
                            ACCOUNT_NAME,
                            ADD_DATE,
                            ADD_DATE_TIME, 
                            ADD_FLAG,
                            DELETE_DATE, 
                            DELETE_DATE_TIME, 
                            DELETE_FLAG,
                            QUESTION_TO_HON_OPE_FLAG, 
                            QUESTION_BODY
                        ) VALUES (
                            (SELECT MAX(id + 1) FROM FILE_UPLOAD_UPLOAD), 
                            %s, 
                            (SELECT MAX(HON_UPLOAD_ID + 1) FROM FILE_UPLOAD_UPLOAD), 
                            %s, 
                            %s, 
                            %s,  
                            (SELECT ORG_CODE FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s), 
                            (SELECT ORG_NAME FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s),  
                            (SELECT DEPT_CODE FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s), 
                            (SELECT DEPT_NAME FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s), 
                            %s, 
                            (SELECT ACCOUNT_NAME FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s),  
                            %s, 
                            %s, 
                            %s,  
                            %s, 
                            %s, 
                            %s,  
                            %s, 
                            %s
                        )
                        """, 
                        [ kenUploadId,
                          '2',
                          localAddForm.HON_OPERATION_YEAR, 
                          localAddForm.HON_FLOOD_YEAR,
                          localAddForm.HON_ACCOUNT_ID, 
                          localAddForm.HON_ACCOUNT_ID,
                          localAddForm.HON_ACCOUNT_ID, 
                          localAddForm.HON_ACCOUNT_ID,
                          localAddForm.HON_ACCOUNT_ID, 
                          localAddForm.HON_ACCOUNT_ID,
                          localAddDate, 
                          localAddDateTime, 
                          '0', 
                          localAddForm.HON_DELETE_DATE, 
                          localAddForm.HON_DELETE_DATE_TIME, 
                          '0', 
                          localAddForm.HON_QUESTION_TO_HON_OPE_FLAG, 
                          localAddForm.HON_QUESTION_BODY,  
                        ])
                    transaction.commit()
                except:    
                    transaction.rollback()
                    print_log('[ERROR] P12.UploaAddDoView関数 P12B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P12.UploaAddDoView関数で警告が発生しました。', 'ERROR')
                try:    
                    localCursor.execute("""
                        SELECT 
                            MAX(HON_UPLOAD_ID + 0) AS HON_UPLOAD_ID 
                        FROM 
                            FILE_UPLOAD_UPLOAD 
                        WHERE 
                            ACCOUNT_ID=%s AND 
                            OPERATION_YEAR=%s 
                        LIMIT 1
                        """,
                        [ accountId, 
                          operationYear, 
                        ])
                    localResults = namedtuplefetchall(localCursor)
                    localUploadModel = UploadModel()
                    localUploadModel.HON_UPLOAD_ID = localResults[0].HON_UPLOAD_ID
                except:    
                    localUploadModel = None
                    transaction.rollback()
                    print_log('[ERROR] P12.UploaAddDoView関数 P12B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P12.UploaAddDoView関数で警告が発生しました。', 'ERROR')
                # ヒント：file_upload_uploadfileテーブルの登録フラグを更新する。ファイルアップロードボタンでレコードは仮登録済と想定する。
                # ヒント：仮登録済とは、レコードは登録済、IDも付与済、登録フラグが仮登録済をいう。
                # ヒント：file_upload_uploadfileテーブルの登録フラグの状態＝仮登録済
                # ヒント：SELECT MAX(KEN_UPLOAD_ID + 0)としているが、KEN_UPLOAD_IDは文字列のため、0を足すことで、
                # ヒント：暗黙の型変換がＤＢ内で実行され、最大値を取得可能となる。
                # ヒント：+0しないと、暗黙の型変換が実行されず、エラーとなるので注意すること。                
                try:
                    localCursor.execute("""
                        INSERT INTO FILE_UPLOAD_UPLOADFILE (
                            id, 
                            KEN_UPLOAD_FILE_ID, 
                            HON_UPLOAD_FILE_ID,
                            KEN_UPLOAD_ID, 
                            HON_UPLOAD_ID,
                            KEN_HON_OPE_FLAG,
                            OPERATION_YEAR, 
                            FLOOD_YEAR,
                            ADD_DATE, 
                            ADD_DATE_TIME, 
                            ADD_FLAG,
                            DELETE_DATE, 
                            DELETE_DATE_TIME, 
                            DELETE_FLAG,
                            HON_UPLOAD_FILE_NAME, 
                            HON_UPLOAD_FILE_PATH 
                        ) VALUES (
                            (SELECT MAX(id + 1) FROM FILE_UPLOAD_UPLOADFILE), 
                            '', 
                            (SELECT MAX(HON_UPLOAD_FILE_ID + 1) FROM FILE_UPLOAD_UPLOADFILE),
                            %s, 
                            %s,
                            '2',
                            %s, 
                            %s,
                            %s, 
                            %s, 
                            '0',
                            %s, 
                            %s, 
                            '0',
                            %s, 
                            %s   
                        )
                        """, 
                        [ kenUploadId,
                          localUploadModel.HON_UPLOAD_ID, 
                          localAddForm.HON_OPERATION_YEAR, 
                          localAddForm.HON_FLOOD_YEAR,
                          localAddDate, 
                          localAddDateTime, 
                          localAddForm.HON_DELETE_DATE, 
                          localAddForm.HON_DELETE_DATE_TIME,
                          localAddForm.HON_UPLOAD_FILE_NAME.name, 
                          os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId, (((localAddDateTime.replace(' ', '')).replace('/', '')).replace(':', '') + localAddForm.HON_UPLOAD_FILE_NAME.name)),
                        ])
                    transaction.commit()
                except:    
                    transaction.rollback()
                    print_log('[ERROR] P12.UploaAddDoView関数 P12B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P12.UploaAddDoView関数で警告が発生しました。', 'ERROR')
            elif accountType == '3':
                # ログインしょた利用者のアカウント・区分＝３：運用業者の場合、、、
                print_log('[ERROR] P12.UploaAddDoView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P12.UploadAddDoView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P12.UploadAddDoView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P12.UploadAddDoView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            transaction.rollback()
            print_log('[ERROR] P12.UploadAddDoView関数 P12B60', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P12.UploadAddDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        finally:
            localCursor.close()
        ##########################################
        # ＤＢアクセス処理（Ｐ１２Ｂ６０）
        # （１）ＤＢからアップロードＩＤ、アップロードファイルＩＤを取得する。
        # ヒント：Ｐ１２Ｂ６０でＤＢへのレコードの登録時にMAX+1でＩＤを生成している。
        # ヒント：このため、この関数内ではアップロードＩＤ，アップロードファイルＩＤを保持しておらず、
        # ヒント：アップロードＩＤ、アップロードファイルＩＤをＤＢから取得し、
        # ヒント：次のＰ１３の確認画面をリクエストするクエリストリングにアップロードＩＤをセットする。
        ##########################################
        print_log('[INFO] P12.UploadAddDoView関数 P12B60', 'INFO')
        # （１）ＤＢからアップロードＩＤ、アップロードファイルＩＤを取得する。
        localUploadModel = None
        try:
            localCursor = connection.cursor()
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                # ヒント：SELECT MAX(KEN_UPLOAD_ID + 0)としているが、KEN_UPLOAD_IDは文字列のため、0を足すことで、
                # ヒント：暗黙の型変換がＤＢ内で実行され、最大値を取得可能となる。
                # ヒント：+0しないと、暗黙の型変換が実行されず、エラーとなるので注意すること。                
                try:
                    localCursor.execute("""
                        SELECT 
                            MAX(KEN_UPLOAD_ID + 0) AS KEN_UPLOAD_ID 
                        FROM 
                            FILE_UPLOAD_UPLOAD 
                        WHERE 
                            ACCOUNT_ID=%s AND 
                            OPERATION_YEAR=%s 
                        LIMIT 1
                        """,
                        [ accountId, 
                          operationYear, 
                        ])
                    localResults = namedtuplefetchall(localCursor)
                    localUploadModel = UploadModel()
                    localUploadModel.KEN_UPLOAD_ID = localResults[0].KEN_UPLOAD_ID
                except:    
                    localUploadModel = None
                    print_log('[ERROR] P12.UploaAddDoView関数 P12B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P12.UploaAddDoView関数で警告が発生しました。', 'ERROR')
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                # ヒント：SELECT MAX(KEN_UPLOAD_ID + 0)としているが、KEN_UPLOAD_IDは文字列のため、0を足すことで、
                # ヒント：暗黙の型変換がＤＢ内で実行され、最大値を取得可能となる。
                # ヒント：+0しないと、暗黙の型変換が実行されず、エラーとなるので注意すること。
                try:                
                    localCursor.execute("""
                        SELECT 
                            MAX(HON_UPLOAD_ID + 0) AS HON_UPLOAD_ID 
                        FROM 
                            FILE_UPLOAD_UPLOAD 
                        WHERE 
                            ACCOUNT_ID=%s AND 
                            OPERATION_YEAR=%s 
                        LIMIT 1
                        """,
                        [ accountId, 
                          operationYear, 
                        ])
                    localResults = namedtuplefetchall(localCursor)
                    localUploadModel = UploadModel()
                    localUploadModel.HON_UPLOAD_ID = localResults[0].HON_UPLOAD_ID
                except:    
                    localUploadModel = None
                    print_log('[ERROR] P12.UploaAddDoView関数 P12B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P12.UploaAddDoView関数で警告が発生しました。', 'ERROR')
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                print_log('[ERROR] P12.UploadAddDoView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P12.UploadAddDoView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P12.UploadAddDoView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P12.UploadAddDoView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P12.UploadAddDoView関数 P12B60', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P12.UploadAddDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P12.UploadAddDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        finally:
            localCursor.close()
        ##########################################
        # レスポンスセット処理（Ｐ１２Ｂ７０）
        # （１）局所変数のレスポンスにメッセージとフォームをセットする。
        # ヒント：運用業者の場合は、ここにはこないと想定する。return済。
        ##########################################
        print_log('[INFO] P12.UploadAddDoView関数 P12B70', 'INFO')
        # （１）局所変数のレスポンスにメッセージとフォームをセットする。
        print_log('[INFO] P12.UploadAddDoView関数が正常終了しました。', 'INFO')
        ##########################################
        # リダイレクト処理、レンダリング処理、戻り値セット処理（Ｐ１２Ｂ８０）
        # （１）リダイレクト関数をコールする。
        # （２）レンダリング関数をコールする。
        # （３）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P12.UploadAddDoView関数 P12B80', 'INFO')
        # （１）リダイレクト関数をコールする。
        # （２）レンダリング関数をコールする。
        # （３）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return HttpResponseRedirect('/file_upload/P13/UploadAddConfirm/'+urlquote(str(localAccountModel.ACCOUNT_TYPE))+'/'+urlquote(str(localAccountModel.ACCOUNT_ID))+'/'+urlquote(str(localAccountModel.OPERATION_YEAR))+'/'+urlquote(str(localUploadModel.KEN_UPLOAD_ID))+'/'+str(0)+'/'+'1')
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return HttpResponseRedirect('/file_upload/P13/UploadAddConfirm/'+urlquote(str(localAccountModel.ACCOUNT_TYPE))+'/'+urlquote(str(localAccountModel.ACCOUNT_ID))+'/'+urlquote(str(localAccountModel.OPERATION_YEAR))+'/'+str(0)+'/'+urlquote(str(localUploadModel.HON_UPLOAD_ID))+'/'+'2')
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P13.UploadAddDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P13.UploadAddDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ１２Ｂ９０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P12.UploadAddDoView関数 P12B90', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P12.UploadAddDoView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P12.UploadAddDoView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１２Ｂ１００）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P12.UploadAddDoView関数 P12B100', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
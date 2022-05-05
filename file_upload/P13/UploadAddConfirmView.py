#####################################################################################
# UploadAddConfirmViewビューモジュール【ほぼ完成】
# ファイル名：P13.UploadAddConfirmView.py（Ｐ１３）
# ユースケース：都道府県は、調査結果の登録内容を確認＝調査結果または確認結果を本登録する。
# ユースケース：本省は、確認結果の登録内容を確認＝調査結果または確認結果を本登録する。
# ヒント：調査結果と確認結果は同じテーブル、モデルを使用する。
# ヒント：種別・区分フラグで調査結果と確認結果を識別する。
# ヒント：accountTypeはログインした人の種別・区分
# ヒント：KEN_HON_OPE_FLAGはデータ（データを登録した人）の種別・区分
# ヒント：アップロードファイルは、UploadAddViewで既にアップロード済と想定する。
# ヒント：UplaodAddConfirmViewと関連するテンプレートの役割は、利用者にＤＢに登録されることを念押しすることにある。
# ヒント：また、確認ボタン押下時にエラーが出るよりも、前の段階で入力チェックと同じタイミングでエラーが出た方がＵＩとして優れていると考える。
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
# render
# urlquote
#####################################################################################
from django.contrib.auth.decorators import login_required  # ログイン制御モジュール
from django.db import connection                           # ＤＢコネクション管理モジュール
from django.db import transaction                          # ＤＢトランザクション管理モジュール
from django.shortcuts import render                        # レンダリングモジュール
from django.utils.http import urlquote                     # URLエスケープモジュール 
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# UploadAddConfirmForm
# AccountModel
# UploadFileModel
# UploadModel
# print_log
#####################################################################################
from file_upload.CommonFunction import print_log           # ログ出力モジュール
from file_upload.forms import UploadAddConfirmForm         # アップロードデータ登録確認画面用のフォーム
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
# 関数名：P13.UploadAddConfirmView（Ｐ１３Ａ）
# 関数概要：都道府県用調査結果登録確認ページをブラウザに戻す。（都道府県）
# 関数概要：本省用確認結果登録確認ページをブラウザに戻す。（本省）
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
# 引数[5]：uploadId：運用業者用確認結果ＩＤ：アクセスは想定せず、不正アクセスとしてエラーページを返す。（運用業者）
#
# 戻り値[1]：response
#
# FORM：UploadAddConfirmForm：都道府県用調査結果登録確認ページ（都道府県）
# FORM：UploadAddConfirmForm：本省用確認結果登録確認ページ（本省）
# FORM：UploadAddConfirmForm：運用業者用確認結果登録確認ページ（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：UploadModel：調査結果または確認結果モデル（Ｒ）
#
# ヒント：accountTypeが都道府県の場合、引数のkenAddIdをキーに、ＤＢから仮登録の調査結果データを取得し、ページに表示する。
# ヒント：accountTypeが本省の場合、引数のhonAddIdをキーに、ＤＢから仮登録の確認結果データを取得し、ページに表示する。
# ヒント：accountTypeが運用業者の場合、この機能は提供しないため、エラーページを表示する。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def UploadAddConfirmView(request, accountType, accountId, operationYear, kenUploadId, honUploadId, kenHonOpeFlag):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P13.UploadAddConfirmView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１３Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P13.UploadAddConfirmView関数 P13A10', 'INFO')
        print_log('[INFO] P13.UploadAddConfirmView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmView.kenUploadId = {}'.format(kenUploadId), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmView.honUploadId = {}'.format(honUploadId), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmView.kenHonOpeFlag = {}'.format(kenHonOpeFlag), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１３Ａ２０）
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
            print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2':
            pass
        elif accountType == '3':
            print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-3', 'WARN')
            return render(request, 'error.html')
        else:
            print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P13.UploadAddConfirmlView関数 P13A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        # ヒント：urls.pyの検索条件にヒットしないため、論理的な設定の有無にかかわらず、ダミーでも0等をセットすると想定する。
        # ヒント：つまり、ここではロジックを判定せず、ソース中にロジックを分散させずに、別の箇所で集中的にロジックを判定する。
        # ヒント：つまり、ロジック的にはあまり意味がないが、セキュリティ的に意味があるため、数字のみがセットされていることをチェックする。
        if operationYear is None:
            print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-5', 'WARN')
                return render(request, 'error.html')
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        # ヒント：urls.pyの検索条件にヒットしないため、論理的な設定の有無にかかわらず、ダミーでも0等をセットすると想定する。
        # ヒント：つまり、ここではロジックを判定せず、ソース中にロジックを分散させずに、別の箇所で集中的にロジックを判定する。
        # ヒント：つまり、ロジック的にはあまり意味がないが、セキュリティ的に意味があるため、数字のみがセットされていることをチェックする。
        if kenUploadId is None:
            print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenUploadId) == True:
                pass
            else:
                print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-6', 'WARN')
                return render(request, 'error.html')
        # （７）本省アップロードＩＤをチェックする。　例　1
        # ヒント：urls.pyの検索条件にヒットしないため、論理的な設定の有無にかかわらず、ダミーでも0等をセットすると想定する。
        # ヒント：つまり、ここではロジックを判定せず、ソース中にロジックを分散させずに、別の箇所で集中的にロジックを判定する。
        # ヒント：つまり、ロジック的にはあまり意味がないが、セキュリティ的に意味があるため、数字のみがセットされていることをチェックする。
        if honUploadId is None:
            print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-7', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(honUploadId) == True:
                pass
            else:
                print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-7', 'WARN')
                return render(request, 'error.html')
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        if kenHonOpeFlag is None:
            print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-8', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenHonOpeFlag) == True:
                pass
            else:
                print_log('[WARN] P13.UploadAddConfirmView関数 P13A20-8', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ１３Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P13.UploadAddConfirmView関数 P13A30', 'INFO')
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # ヒント：ＤＢアクセス前にlocalAccountModelをNoneに初期化することで、ここで、ＤＢからのデータ取得に成功したか否かを判定できる。
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
                  operationYear, ])[0]
        except:
            localAccountModel = None
            print_log('[ERROR] P13.UploadAddConfirmView関数 P13A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        # ヒント：ＤＢアクセス前にlocalAccountModelをNoneに初期化することで、ここで、ＤＢからのデータ取得に成功したか否かを判定できる。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P13.UploadAddConfirmView関数P13A30', 'WARN')
            print_log('[WARN] localAccountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P13.UploadAddConfirmView関数 P13A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、アップロードデータ取得処理（Ｐ１３Ａ４０）
        # （１）アップロードデータ、アップロードファイルデータを格納する局所変数を初期化する。
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
        print_log('[INFO] P13.UploadAddConfirmView関数 P13A40', 'INFO')
        # （１）アップロードデータ、アップロードファイルデータを格納する局所変数を初期化する。
        localUploadModel = None
        localUploadFileModel = None
        # （２）ＤＢにアクセスし、アップロードデータ、アップロードファイルデータを取得する。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
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
                        [kenUploadId, operationYear, ])[0]
                except:
                    localUploadModel = None        
                    print_log('[ERROR] P13.UploadAddConfirmView関数 P13A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P13.UploadAddConfirmView関数で警告が発生しました。', 'ERROR')
                # ヒント：アップロードファイルデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：アップロードファイルデータは１アップロードデータにつき、１件と想定している。
                # ヒント：アップロードファイルデータのみ削除する機能、アップロードファイルデータ、アップロードデータを更新する機能を提供していないためこの想定は破綻しない。
                # TO-DO：必要に応じ、上記制限を緩和することを検討すること。ただし、この場合、以下のＳＱＬ文は使用できなくなり、修正が必要である。
                # ヒント：アップロードデータを登録するというよりも、アップロードファイルデータを登録し、その付随として、その他の情報を登録するというユースケースを想定する。
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
                          operationYear, ])[0]
                except:
                    localUploadFileModel = None            
                    print_log('[ERROR] P13.UploadAddConfirmView関数 P13A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P13.UploadAddConfirmView関数で警告が発生しました。', 'ERROR')
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                try:
                    localUploadModel = UploadModel.objects.raw("""
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
                    localUploadModel = None
                    print_log('[ERROR] P13.UploadAddConfirmView関数 P13A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P13.UploadAddConfirmView関数で警告が発生しました。', 'ERROR')
                # ヒント：アップロードファイルデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                # ヒント：アップロードファイルデータは１アップロードデータにつき、１件と想定している。
                # ヒント：アップロードファイルデータのみ削除する機能、アップロードファイルデータ、アップロードデータを更新する機能を提供していないためこの想定は破綻しない。
                # TO-DO：必要に応じ、上記制限を緩和することを検討すること。ただし、この場合、以下のＳＱＬ文は使用できなくなり、修正が必要である。
                # ヒント：アップロードデータを登録するというよりも、アップロードファイルデータを登録し、その付随として、その他の情報を登録するというユースケースを想定する。
                try:    
                    localUploadFileModel = UploadFileModel.objects.raw("""
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
                    localUplodFileModel = None            
                    print_log('[ERROR] P13.UploadAddConfirmView関数 P13A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P13.UploadAddConfirmView関数で警告が発生しました。', 'ERROR')
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                print_log('[ERROR] P13.UploadAddConfirmView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P13.UploadAddConfirmView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P13.UploadAddConfirmView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P13.UploadAddConfirmView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P13.UploadAddConfirmView関数 P13A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # フォームセット処理（Ｐ１３Ａ５０）
        # （１）局所変数のフォームを初期化する。
        # ヒント：ブラウザとのデータのやりとり、特にブラウザからPOSTデータがある場合、フォームを使用する。
        # ヒント：モデルはブラウザで参照用、かつタグをコーディングする場合等に使用する。
        # ヒント：フォームはブラウザで編集用、POSTでサーバにリクエストされる項目、かつタグを自動生成する場合等に使用する。
        # ヒント：表示画面の場合、URL+QUERY STRING、VIEW関数、GET、renderでテンプレートとレスポンスで目的の画面を表示する。
        # ヒント：追加、削除の場合、URL+QUERY STRING+フォーム値、DoVIEW関数、POST、redirect（URL+QUERY STRING）で次の画面に遷移する。
        # ヒント：または、追加、削除の場合、URL+QUERY STRING+フォーム値、DoVIEW関数、POST、renderでテンプレートとレスポンスで元の同じ画面を表示する。
        # ヒント：ただし、この場合、レスポンスに、追加、削除結果のフラグを返し、ブラウザ側（正確にはサーバでのレンダリング時＝HTML生成時）で通常画面と結果画面をフラグを見て分岐処理するようにテンプレートを記述する。
        ##########################################
        print_log('[INFO] P13.UploadAddConfirmView関数 P13A50', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localAddDate = datetime.now().strftime("%Y/%m/%d")
        localAddDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        localUploadAddConfirmForm = UploadAddConfirmForm()
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            # ヒント：アップロードデータ項目に初期値をセットする。
            if localUploadModel != None:        
                localUploadAddConfirmForm.initial['KEN_UPLOAD_ID'] = localUploadModel.KEN_UPLOAD_ID # M1
                localUploadAddConfirmForm.initial['KEN_KEN_HON_OPE_FLAG'] = localUploadModel.KEN_HON_OPE_FLAG # M2
                localUploadAddConfirmForm.initial['KEN_OPERATION_YEAR'] = localUploadModel.OPERATION_YEAR # M3
                localUploadAddConfirmForm.initial['KEN_FLOOD_YEAR'] = localUploadModel.FLOOD_YEAR # M4
                localUploadAddConfirmForm.initial['KEN_ORG_CODE'] = localUploadModel.ORG_CODE # M6
                localUploadAddConfirmForm.initial['KEN_ORG_NAME'] = localUploadModel.ORG_NAME # M7
                localUploadAddConfirmForm.initial['KEN_DEPT_CODE'] = localUploadModel.DEPT_CODE # M8
                localUploadAddConfirmForm.initial['KEN_DEPT_NAME'] = localUploadModel.DEPT_NAME # M9
                localUploadAddConfirmForm.initial['KEN_ACCOUNT_ID'] = localUploadModel.ACCOUNT_ID # M10
                localUploadAddConfirmForm.initial['KEN_ACCOUNT_NAME'] = localUploadModel.ACCOUNT_NAME # M11
                localUploadAddConfirmForm.initial['KEN_ADD_DATE'] = localUploadModel.ADD_DATE # M12
                localUploadAddConfirmForm.initial['KEN_ADD_DATE_TIME'] = localUploadModel.ADD_DATE_TIME # M13
                localUploadAddConfirmForm.initial['KEN_ADD_FLAG'] = localUploadModel.ADD_FLAG # M14
                localUploadAddConfirmForm.initial['KEN_DELETE_DATE'] = localUploadModel.DELETE_DATE # M15
                localUploadAddConfirmForm.initial['KEN_DELETE_DATE_TIME'] = localUploadModel.DELETE_DATE_TIME # M16
                localUploadAddConfirmForm.initial['KEN_DELETE_FLAG'] = localUploadModel.DELETE_FLAG # M17
                localUploadAddConfirmForm.initial['KEN_QUESTION_BODY'] = localUploadModel.QUESTION_BODY # M18
                localUploadAddConfirmForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = localUploadModel.QUESTION_TO_HON_OPE_FLAG # M19
                localUploadAddConfirmForm.initial['HON_UPLOAD_ID'] = "" # M1
                localUploadAddConfirmForm.initial['HON_KEN_HON_OPE_FLAG'] = "" # M2
                localUploadAddConfirmForm.initial['HON_OPERATION_YEAR'] = "" # M3
                localUploadAddConfirmForm.initial['HON_FLOOD_YEAR'] = "" # M4
                localUploadAddConfirmForm.initial['HON_ORG_CODE'] = "" # M6
                localUploadAddConfirmForm.initial['HON_ORG_NAME'] = "" # M7
                localUploadAddConfirmForm.initial['HON_DEPT_CODE'] = "" # M8
                localUploadAddConfirmForm.initial['HON_DEPT_NAME'] = "" # M9
                localUploadAddConfirmForm.initial['HON_ACCOUNT_ID'] = "" # M10
                localUploadAddConfirmForm.initial['HON_ACCOUNT_NAME'] = "" # M11
                localUploadAddConfirmForm.initial['HON_ADD_DATE'] = "" # M12
                localUploadAddConfirmForm.initial['HON_ADD_DATE_TIME'] = "" # M13
                localUploadAddConfirmForm.initial['HON_ADD_FLAG'] = "" # M14
                localUploadAddConfirmForm.initial['HON_DELETE_DATE'] = "" # M15
                localUploadAddConfirmForm.initial['HON_DELETE_DATE_TIME'] = "" # M16
                localUploadAddConfirmForm.initial['HON_DELETE_FLAG'] = "" # M17
                localUploadAddConfirmForm.initial['HON_QUESTION_BODY'] = "" # M18
                localUploadAddConfirmForm.initial['HON_QUESTION_TO_HON_OPE_FLAG'] = "" # M19
            else:
                localUploadAddConfirmForm.initial['KEN_UPLOAD_ID'] = "" # M1
                localUploadAddConfirmForm.initial['KEN_KEN_HON_OPE_FLAG'] = "" # M2
                localUploadAddConfirmForm.initial['KEN_OPERATION_YEAR'] = "" # M3
                localUploadAddConfirmForm.initial['KEN_FLOOD_YEAR'] = "" # M4
                localUploadAddConfirmForm.initial['KEN_ORG_CODE'] = "" # M6
                localUploadAddConfirmForm.initial['KEN_ORG_NAME'] = "" # M7
                localUploadAddConfirmForm.initial['KEN_DEPT_CODE'] = "" # M8
                localUploadAddConfirmForm.initial['KEN_DEPT_NAME'] = "" # M9
                localUploadAddConfirmForm.initial['KEN_ACCOUNT_ID'] = "" # M10
                localUploadAddConfirmForm.initial['KEN_ACCOUNT_NAME'] = "" # M11
                localUploadAddConfirmForm.initial['KEN_ADD_DATE'] = "" # M12
                localUploadAddConfirmForm.initial['KEN_ADD_DATE_TIME'] = "" # M13
                localUploadAddConfirmForm.initial['KEN_ADD_FLAG'] = "" # M14
                localUploadAddConfirmForm.initial['KEN_DELETE_DATE'] = "" # M15
                localUploadAddConfirmForm.initial['KEN_DELETE_DATE_TIME'] = "" # M16
                localUploadAddConfirmForm.initial['KEN_DELETE_FLAG'] = "" # M17
                localUploadAddConfirmForm.initial['KEN_QUESTION_BODY'] = "" # M18
                localUploadAddConfirmForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = "" # M19
                localUploadAddConfirmForm.initial['HON_UPLOAD_ID'] = "" # M1
                localUploadAddConfirmForm.initial['HON_KEN_HON_OPE_FLAG'] = "" # M2
                localUploadAddConfirmForm.initial['HON_OPERATION_YEAR'] = "" # M3
                localUploadAddConfirmForm.initial['HON_FLOOD_YEAR'] = "" # M4
                localUploadAddConfirmForm.initial['HON_ORG_CODE'] = "" # M6
                localUploadAddConfirmForm.initial['HON_ORG_NAME'] = "" # M7
                localUploadAddConfirmForm.initial['HON_DEPT_CODE'] = "" # M8
                localUploadAddConfirmForm.initial['HON_DEPT_NAME'] = "" # M9
                localUploadAddConfirmForm.initial['HON_ACCOUNT_ID'] = "" # M10
                localUploadAddConfirmForm.initial['HON_ACCOUNT_NAME'] = "" # M11
                localUploadAddConfirmForm.initial['HON_ADD_DATE'] = "" # M12
                localUploadAddConfirmForm.initial['HON_ADD_DATE_TIME'] = "" # M13
                localUploadAddConfirmForm.initial['HON_ADD_FLAG'] = "" # M14
                localUploadAddConfirmForm.initial['HON_DELETE_DATE'] = "" # M15
                localUploadAddConfirmForm.initial['HON_DELETE_DATE_TIME'] = "" # M16
                localUploadAddConfirmForm.initial['HON_DELETE_FLAG'] = "" # M17
                localUploadAddConfirmForm.initial['HON_QUESTION_BODY'] = "" # M18
                localUploadAddConfirmForm.initial['HON_QUESTION_TO_HON_OPE_FLAG'] = "" # M19
            # アップロードデータファイル項目に初期値をセットする。
            if localUploadFileModel != None:
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_NAME'] = localUploadFileModel.KEN_UPLOAD_FILE_NAME # M1
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_ID'] = localUploadFileModel.KEN_UPLOAD_FILE_ID # M1
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_PATH'] = localUploadFileModel.KEN_UPLOAD_FILE_PATH # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_NAME'] = "" # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_ID'] = "" # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_PATH'] = "" # M1
            else:
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_NAME'] = "" # M1
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_ID'] = "" # M1
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_PATH'] = "" # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_NAME'] = "" # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_ID'] = "" # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_PATH'] = "" # M1
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            # ヒント：アップロードデータ項目に初期値をセットする。
            if localUploadModel != None:
                localUploadAddConfirmForm.initial['KEN_UPLOAD_ID'] = "" # M1
                localUploadAddConfirmForm.initial['KEN_KEN_HON_OPE_FLAG'] = "" # M2
                localUploadAddConfirmForm.initial['KEN_OPERATION_YEAR'] = "" # M3
                localUploadAddConfirmForm.initial['KEN_FLOOD_YEAR'] = "" # M4
                localUploadAddConfirmForm.initial['KEN_ORG_CODE'] = "" # M6
                localUploadAddConfirmForm.initial['KEN_ORG_NAME'] = "" # M7
                localUploadAddConfirmForm.initial['KEN_DEPT_CODE'] = "" # M8
                localUploadAddConfirmForm.initial['KEN_DEPT_NAME'] = "" # M9
                localUploadAddConfirmForm.initial['KEN_ACCOUNT_ID'] = "" # M10
                localUploadAddConfirmForm.initial['KEN_ACCOUNT_NAME'] = "" # M11
                localUploadAddConfirmForm.initial['KEN_ADD_DATE'] = "" # M12
                localUploadAddConfirmForm.initial['KEN_ADD_DATE_TIME'] = "" # M13
                localUploadAddConfirmForm.initial['KEN_ADD_FLAG'] = "" # M14
                localUploadAddConfirmForm.initial['KEN_DELETE_DATE'] = "" # M15
                localUploadAddConfirmForm.initial['KEN_DELETE_DATE_TIME'] = "" # M16
                localUploadAddConfirmForm.initial['KEN_DELETE_FLAG'] = "" # M17
                localUploadAddConfirmForm.initial['KEN_QUESTION_BODY'] = "" # M18
                localUploadAddConfirmForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = "" # M19
                localUploadAddConfirmForm.initial['HON_UPLOAD_ID'] = localUploadModel.HON_UPLOAD_ID # M1
                localUploadAddConfirmForm.initial['HON_KEN_HON_OPE_FLAG'] = localUploadModel.KEN_HON_OPE_FLAG # M2
                localUploadAddConfirmForm.initial['HON_OPERATION_YEAR'] = localUploadModel.OPERATION_YEAR # M3
                localUploadAddConfirmForm.initial['HON_FLOOD_YEAR'] = localUploadModel.FLOOD_YEAR # M4
                localUploadAddConfirmForm.initial['HON_ORG_CODE'] = localUploadModel.ORG_CODE # M6
                localUploadAddConfirmForm.initial['HON_ORG_NAME'] = localUploadModel.ORG_NAME # M7
                localUploadAddConfirmForm.initial['HON_DEPT_CODE'] = localUploadModel.DEPT_CODE # M8
                localUploadAddConfirmForm.initial['HON_DEPT_NAME'] = localUploadModel.DEPT_NAME # M9
                localUploadAddConfirmForm.initial['HON_ACCOUNT_ID'] = localUploadModel.ACCOUNT_ID # M10
                localUploadAddConfirmForm.initial['HON_ACCOUNT_NAME'] = localUploadModel.ACCOUNT_NAME # M11
                localUploadAddConfirmForm.initial['HON_ADD_DATE'] = localUploadModel.ADD_DATE # M12
                localUploadAddConfirmForm.initial['HON_ADD_DATE_TIME'] = localUploadModel.ADD_DATE_TIME # M13
                localUploadAddConfirmForm.initial['HON_ADD_FLAG'] = localUploadModel.ADD_FLAG # M14
                localUploadAddConfirmForm.initial['HON_DELETE_DATE'] = localUploadModel.DELETE_DATE # M15
                localUploadAddConfirmForm.initial['HON_DELETE_DATE_TIME'] = localUploadModel.DELETE_DATE_TIME # M16
                localUploadAddConfirmForm.initial['HON_DELETE_FLAG'] = localUploadModel.DELETE_FLAG # M17
                localUploadAddConfirmForm.initial['HON_QUESTION_BODY'] = localUploadModel.QUESTION_BODY # M18
                localUploadAddConfirmForm.initial['HON_QUESTION_TO_HON_OPE_FLAG'] = localUploadModel.QUESTION_TO_HON_OPE_FLAG # M19
            else:
                localUploadAddConfirmForm.initial['KEN_UPLOAD_ID'] = "" # M1
                localUploadAddConfirmForm.initial['KEN_KEN_HON_OPE_FLAG'] = "" # M2
                localUploadAddConfirmForm.initial['KEN_OPERATION_YEAR'] = "" # M3
                localUploadAddConfirmForm.initial['KEN_FLOOD_YEAR'] = "" # M4
                localUploadAddConfirmForm.initial['KEN_ORG_CODE'] = "" # M6
                localUploadAddConfirmForm.initial['KEN_ORG_NAME'] = "" # M7
                localUploadAddConfirmForm.initial['KEN_DEPT_CODE'] = "" # M8
                localUploadAddConfirmForm.initial['KEN_DEPT_NAME'] = "" # M9
                localUploadAddConfirmForm.initial['KEN_ACCOUNT_ID'] = "" # M10
                localUploadAddConfirmForm.initial['KEN_ACCOUNT_NAME'] = "" # M11
                localUploadAddConfirmForm.initial['KEN_ADD_DATE'] = "" # M12
                localUploadAddConfirmForm.initial['KEN_ADD_DATE_TIME'] = "" # M13
                localUploadAddConfirmForm.initial['KEN_ADD_FLAG'] = "" # M14
                localUploadAddConfirmForm.initial['KEN_DELETE_DATE'] = "" # M15
                localUploadAddConfirmForm.initial['KEN_DELETE_DATE_TIME'] = "" # M16
                localUploadAddConfirmForm.initial['KEN_DELETE_FLAG'] = "" # M17
                localUploadAddConfirmForm.initial['KEN_QUESTION_BODY'] = "" # M18
                localUploadAddConfirmForm.initial['KEN_QUESTION_TO_HON_OPE_FLAG'] = "" # M19
                localUploadAddConfirmForm.initial['HON_UPLOAD_ID'] = "" # M1
                localUploadAddConfirmForm.initial['HON_KEN_HON_OPE_FLAG'] = "" # M2
                localUploadAddConfirmForm.initial['HON_OPERATION_YEAR'] = "" # M3
                localUploadAddConfirmForm.initial['HON_FLOOD_YEAR'] = "" # M4
                localUploadAddConfirmForm.initial['HON_ORG_CODE'] = "" # M6
                localUploadAddConfirmForm.initial['HON_ORG_NAME'] = "" # M7
                localUploadAddConfirmForm.initial['HON_DEPT_CODE'] = "" # M8
                localUploadAddConfirmForm.initial['HON_DEPT_NAME'] = "" # M9
                localUploadAddConfirmForm.initial['HON_ACCOUNT_ID'] = "" # M10
                localUploadAddConfirmForm.initial['HON_ACCOUNT_NAME'] = "" # M11
                localUploadAddConfirmForm.initial['HON_ADD_DATE'] = "" # M12
                localUploadAddConfirmForm.initial['HON_ADD_DATE_TIME'] = "" # M13
                localUploadAddConfirmForm.initial['HON_ADD_FLAG'] = "" # M14
                localUploadAddConfirmForm.initial['HON_DELETE_DATE'] = "" # M15
                localUploadAddConfirmForm.initial['HON_DELETE_DATE_TIME'] = "" # M16
                localUploadAddConfirmForm.initial['HON_DELETE_FLAG'] = "" # M17
                localUploadAddConfirmForm.initial['HON_QUESTION_BODY'] = "" # M18
                localUploadAddConfirmForm.initial['HON_QUESTION_TO_HON_OPE_FLAG'] = "" # M19
            # アップロードデータファイル項目に初期値をセットする。
            if localUploadFileModel != None:
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_NAME'] = "" # M1
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_ID'] = "" # M1
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_PATH'] = "" # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_NAME'] = localUploadFileModel.HON_UPLOAD_FILE_NAME # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_ID'] = localUploadFileModel.HON_UPLOAD_FILE_ID # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_PATH'] = localUploadFileModel.HON_UPLOAD_FILE_PATH # M1
            else:
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_NAME'] = "" # M1
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_ID'] = "" # M1
                localUploadAddConfirmForm.initial['KEN_UPLOAD_FILE_PATH'] = "" # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_NAME'] = "" # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_ID'] = "" # M1
                localUploadAddConfirmForm.initial['HON_UPLOAD_FILE_PATH'] = "" # M1
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P13.UploadAddConfirmView関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmView関数が異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P13.UploadAddConfirmView関数でエラーが発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmView関数が異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################            
        # フォームセット処理（Ｐ１３Ａ５２）
        # （１）フォームのウィジェットの属性に値をセットする。（都道府県項目）
        # （２）フォームのウィジェットの属性に値をセットする。（本省項目）
        # ヒント：利用者が編集できない項目は、disabled、readonlyのいずれかとする。
        # ヒント：フォームを使用した場合、ブラウザでタグが自動生成されるため、ブラウザのstyle、cssでdisable、readonlyをセットしにくい。
        # ヒント：そのため。ビュー関数でdisable、readonly等をセットする。
        # ヒント：フォームのフィールドは、非表示の項目もセットすることを推奨する。
        # ヒント：ステートレスなウェブアプリにおいて、ブラウザに送ったデータをPOST時にサーバ側のビュー関数で参照可能とするため。
        ##########################################            
        # （１）フォームのウィジェットの属性に値をセットする。（都道府県項目）
        localUploadAddConfirmForm.fields['KEN_UPLOAD_ID'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_KEN_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_OPERATION_YEAR'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_FLOOD_YEAR'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_ORG_CODE'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_ORG_NAME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_DEPT_CODE'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_DEPT_NAME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_ACCOUNT_ID'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_ACCOUNT_NAME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_ADD_DATE'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_ADD_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_ADD_FLAG'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_DELETE_DATE'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_DELETE_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_DELETE_FLAG'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_QUESTION_BODY'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_QUESTION_TO_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_UPLOAD_FILE_NAME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_UPLOAD_FILE_ID'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['KEN_UPLOAD_FILE_PATH'].widget.attrs['readonly'] = True
        # （２）フォームのウィジェットの属性に値をセットする。（本省項目）
        localUploadAddConfirmForm.fields['HON_UPLOAD_ID'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_KEN_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_OPERATION_YEAR'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_FLOOD_YEAR'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_ORG_CODE'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_ORG_NAME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_DEPT_CODE'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_DEPT_NAME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_ACCOUNT_ID'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_ACCOUNT_NAME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_ADD_DATE'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_ADD_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_ADD_FLAG'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_DELETE_DATE'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_DELETE_DATE_TIME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_DELETE_FLAG'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_QUESTION_BODY'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_QUESTION_TO_HON_OPE_FLAG'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_UPLOAD_FILE_NAME'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_UPLOAD_FILE_ID'].widget.attrs['readonly'] = True
        localUploadAddConfirmForm.fields['HON_UPLOAD_FILE_PATH'].widget.attrs['readonly'] = True
        ##########################################
        # レスポンスセット処理（Ｐ１３Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        # ヒント：登録済フラグがTrueの場合、テンプレートでは、登録結果を表示する処理を想定する。
        # ヒント：登録済フラグがFalseの場合、テンプレートでは、これから登録するデータを表示し、利用者が編集を加えると想定する。
        # ヒント：必須項目の未入力等に対応するため、１画面で新規登録用の画面と、結果表示用の画面の両方が処理できたほうが効率が良いため。
        # ヒント：また、テンプレートファイルの記述は、それほど複雑にはならないためこのように実装する。
        ##########################################
        print_log('[INFO] P13.UploadAddConfirmView関数 P13A60', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            response = {
                'accountType': 1,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。     
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': True,                             # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'wasAdded': False,                         # 登録済フラグをFalseにセットする。テンプレートで画面表示処理を分岐するために使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'uploadAddConfirmForm': localUploadAddConfirmForm, # アップロードデータ登録確認画面用のフォーム
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'wasAdded': False,                         # 登録済フラグをFalseにセットする。テンプレートで画面表示処理を分岐するために使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'uploadAddConfirmForm': localUploadAddConfirmForm, # アップロードデータ登録確認画面用のフォーム
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P13.UploadAddConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P13.UploadAddConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P13.UploadAddConfirmView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１３Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P13.UploadAddConfirmView関数 P13A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P13UploadAddConfirmTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P13UploadAddConfirmTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、 
            print_log('[ERROR] P13.UploadAddConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P13.UploadAddConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ１３Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P13.UploadAddConfirmView関数 P13A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P13.UploadAddConfirmView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P13.UploadAddConfirmView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１３Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P13.UploadAddConfirmView関数 P13A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
#####################################################################################
# 関数名：P13.UploadAddConfirmDoView（Ｐ１３Ｂ）
# 関数概要：都道府県用調査結果登録確認ページでセットされた値をＤＢに本登録する。（都道府県）
# 関数概要：本省用確認結果登録確認ページでセットされた値をＤＢに本登録する。（本省）
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
# FORM：UploadAddConfirmForm：都道府県用調査結果登録確認ページ（都道府県）
# FORM：UploadAddConfirmForm：本省用確認結果登録確認ページ（本省）
# FORM：UploadAddConfirmForm：運用業者用確認結果登録ページ（運用業者）：アクセスは想定せず、不正アクセスとしてエラーページを返す。
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：UploadModel：調査結果または確認結果モデル（Ｕ）
#
# ヒント：都道府県からの呼び出しの場合、kenUploadIdはNot Null、honUploadIdはNull
# ヒント：本省からの呼び出しの場合、kenUploadIdはNot Null、honUploadIdはNot Null
# ヒント：運用業者からの呼び出しの場合、：アクセスは想定せず、不正アクセスとしてエラーページを返す。
# ヒント：UploadAddConfirmDoView関数でＤＢに本登録済で、そのときにuploadIdを引き継いでいると想定する。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def UploadAddConfirmDoView(request, accountType, accountId, operationYear, kenUploadId, honUploadId, kenHonOpeFlag):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P13.UploadAddConfirmDoView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１３Ｂ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P13.UploadAddConfirmDoView関数 P13B10', 'INFO')
        print_log('[INFO] P13.UploadAddConfirmDoView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmDoView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmDoView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmDoView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmDoView.kenUploadId = {}'.format(kenUploadId), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmDoView.honUploadId = {}'.format(honUploadId), 'INFO')
        print_log('[INFO] P13.UploadAddConfirmDoView.kenHonOpeFlag = {}'.format(kenHonOpeFlag), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ１３Ｂ２０）
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
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'POST':
            pass
        else:
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2':
            pass
        elif accountType == '3':
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-3', 'WARN')
            return render(request, 'error.html')
        else:
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-5', 'WARN')
                return render(request, 'error.html')
        # （６）都道府県アップロードＩＤをチェックする。　例　1
        if kenUploadId is None:
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenUploadId) == True:
                pass
            else:    
                print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-6', 'WARN')
                return render(request, 'error.html')
        # （７）本省アップロードＩＤをチェックする。　例　1
        if honUploadId is None:
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-7', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(honUploadId) == True:
                pass
            else:
                print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B20-7', 'WARN')
                return render(request, 'error.html')
        # （８）データ種別をチェックする。　例　１：都道府県登録データ、２：本省登録データ、３：運用業者登録データ
        if kenHonOpeFlag is None:
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13A20-8', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(kenHonOpeFlag) == True:
                pass
            else:
                print_log('[WARN] P13.UploadAddConfirmDoView関数 P13A20-8', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ１３Ｂ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P13.UploadAddConfirmDoView関数 P13B30', 'INFO')
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
            print_log('[ERROR] P13.UploadAddConfirmDoView関数 P13B30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P13.UploadAddConfirmDoView関数 P13B30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # フォームセット処理（Ｐ１３Ｂ４０）
        # （１）局所変数のフォームを初期化する。
        # （２）画面からポストされた情報を取得する。
        # ヒント：運用業者の場合は、ここにはこないと想定する。return済。
        # ヒント：画面からポストされた情報をlocalFormに一時的に格納する。
        # ヒント：localFormの値をチェックしながら、格納用のlocalAddConfirmFormに値をチェットする。
        ##########################################
        print_log('[INFO] P13.UploadAddConfirmDoView関数 P13B40', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localForm = None
        localAddConfirmForm = UploadAddConfirmForm()
        # （２）画面からポストされた情報を取得する。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                localForm = UploadAddConfirmForm(request.POST, request.FILES)
                if localForm.is_valid():
                    localAddConfirmForm.KEN_UPLOAD_ID = localForm.cleaned_data['KEN_UPLOAD_ID']
                    localAddConfirmForm.KEN_KEN_HON_OPE_FLAG = '1'
                    localAddConfirmForm.KEN_OPERATION_YEAR = localForm.cleaned_data['KEN_OPERATION_YEAR']
                    localAddConfirmForm.KEN_FLOOD_YEAR = localForm.cleaned_data['KEN_FLOOD_YEAR']
                    localAddConfirmForm.KEN_ORG_CODE = localForm.cleaned_data['KEN_ORG_CODE']
                    localAddConfirmForm.KEN_ORG_NAME = localForm.cleaned_data['KEN_ORG_NAME']
                    localAddConfirmForm.KEN_DEPT_CODE = localForm.cleaned_data['KEN_DEPT_CODE']
                    localAddConfirmForm.KEN_DEPT_NAME = localForm.cleaned_data['KEN_DEPT_NAME']
                    localAddConfirmForm.KEN_ACCOUNT_ID = localForm.cleaned_data['KEN_ACCOUNT_ID']
                    localAddConfirmForm.KEN_ACCOUNT_NAME = localForm.cleaned_data['KEN_ACCOUNT_NAME']
                    localAddConfirmForm.KEN_ADD_DATE = localForm.cleaned_data['KEN_ADD_DATE']
                    localAddConfirmForm.KEN_ADD_DATE_TIME = localForm.cleaned_data['KEN_ADD_DATE_TIME']
                    localAddConfirmForm.KEN_ADD_FLAG = localForm.cleaned_data['KEN_ADD_FLAG']
                    localAddConfirmForm.KEN_DELETE_DATE = localForm.cleaned_data['KEN_DELETE_DATE']
                    localAddConfirmForm.KEN_DELETE_DATE_TIME = localForm.cleaned_data['KEN_DELETE_DATE_TIME']
                    localAddConfirmForm.KEN_DELETE_FLAG = localForm.cleaned_data['KEN_DELETE_FLAG']
                    # ヒント：./01hokkai/aaa.lzhにファイルを格納する。
                    # ヒント：事前に全アカウントＩＤについて、ディレクトリを作成しておくことを想定する。
                    # ヒント：ＤＢに登録するデータにも上記ディレクトリ、ファイル名をセットすることを想定する。
                    localAddConfirmForm.KEN_UPLOAD_FILE_NAME = localForm.cleaned_data['KEN_UPLOAD_FILE_NAME']
                    localAddConfirmForm.KEN_UPLOAD_FILE_ID = localForm.cleaned_data['KEN_UPLOAD_FILE_ID']
                    localAddConfirmForm.KEN_UPLOAD_FILE_PATH = localForm.cleaned_data['KEN_UPLOAD_FILE_PATH']
                    localAddConfirmForm.KEN_QUESTION_BODY = localForm.cleaned_data['KEN_QUESTION_BODY']
                    localAddConfirmForm.KEN_QUESTION_TO_HON_OPE_FLAG = localForm.cleaned_data['KEN_QUESTION_TO_HON_OPE_FLAG']
                else:
                    pass
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                localForm = UploadAddConfirmForm(request.POST, request.FILES)
                if localForm.is_valid():
                    localAddConfirmForm.HON_UPLOAD_ID = localForm.cleaned_data['HON_UPLOAD_ID']
                    localAddConfirmForm.HON_KEN_HON_OPE_FLAG = '2'
                    localAddConfirmForm.HON_OPERATION_YEAR = localForm.cleaned_data['HON_OPERATION_YEAR']
                    localAddConfirmForm.HON_FLOOD_YEAR = localForm.cleaned_data['HON_FLOOD_YEAR']
                    localAddConfirmForm.HON_ORG_CODE = localForm.cleaned_data['HON_ORG_CODE']
                    localAddConfirmForm.HON_ORG_NAME = localForm.cleaned_data['HON_ORG_NAME']
                    localAddConfirmForm.HON_DEPT_CODE = localForm.cleaned_data['HON_DEPT_CODE']
                    localAddConfirmForm.HON_DEPT_NAME = localForm.cleaned_data['HON_DEPT_NAME']
                    localAddConfirmForm.HON_ACCOUNT_ID = localForm.cleaned_data['HON_ACCOUNT_ID']
                    localAddConfirmForm.HON_ACCOUNT_NAME = localForm.cleaned_data['HON_ACCOUNT_NAME']
                    localAddConfirmForm.HON_ADD_DATE = localForm.cleaned_data['HON_ADD_DATE']
                    localAddConfirmForm.HON_ADD_DATE_TIME = localForm.cleaned_data['HON_ADD_DATE_TIME']
                    localAddConfirmForm.HON_ADD_FLAG = localForm.cleaned_data['HON_ADD_FLAG']
                    localAddConfirmForm.HON_DELETE_DATE = localForm.cleaned_data['HON_DELETE_DATE']
                    localAddConfirmForm.HON_DELETE_DATE_TIME = localForm.cleaned_data['HON_DELETE_DATE_TIME']
                    localAddConfirmForm.HON_DELETE_FLAG = localForm.cleaned_data['HON_DELETE_FLAG']
                    # ヒント：./keizai/aaa.lzhにファイルを格納する
                    # ヒント：事前に全アカウントＩＤについて、ディレクトリを作成しておくことを想定する。
                    # ヒント：ＤＢに登録するデータにも上記ディレクトリ、ファイル名をセットすることを想定する。
                    localAddConfirmForm.HON_UPLOAD_FILE_NAME = localForm.cleaned_data['HON_UPLOAD_FILE_NAME']
                    localAddConfirmForm.HON_UPLOAD_FILE_ID = localForm.cleaned_data['HON_UPLOAD_FILE_ID']
                    localAddConfirmForm.HON_UPLOAD_FILE_PATH = localForm.cleaned_data['HON_UPLOAD_FILE_PATH']
                    localAddConfirmForm.HON_QUESTION_BODY = localForm.cleaned_data['HON_QUESTION_BODY']
                    localAddConfirmForm.HON_QUESTION_TO_HON_OPE_FLAG = localForm.cleaned_data['HON_QUESTION_TO_HON_OPE_FLAG']
                else:
                    pass
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                print_log('[ERROR] P13.UploadAddConfirmDoView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P13.UploadAddConfirmDoView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P13.UploadAddConfirmDoView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P13.UploadAddConfirmDoView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P13.UploadAddConfirmDoView関数 P13B40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ファイル受信処理（Ｐ１３Ｂ５０）
        # （１）画面からポストされたファイルを受信し、サーバに保存する。
        ##########################################
        print_log('[INFO] P13.UploadAddConfirmDoView関数 P13B50', 'INFO')
        ##########################################
        # ＤＢアクセス処理、アップロードデータ登録処理（＝登録フラグを５にセット）（Ｐ１３Ｂ６０）
        # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
        # （２）ＳＱＬ文を実行する。
        # （３）トランザクション管理でコミットする。
        # （４）ＤＢ接続を切断＝カーソルを閉じる。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：運用業者の場合は、ここにはこないと想定する。return済。
        # ヒント：rawはUPDATE文では使えないため、カーソルを利用する。
        ##########################################
        print_log('[INFO] P13.UploadAddConfirmDoView関数 P13B60', 'INFO')
        localAddDate = datetime.now().strftime("%Y/%m/%d")
        localAddDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
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
                        UPDATE FILE_UPLOAD_UPLOAD
                            SET
                            ADD_DATE = %s,
                            ADD_DATE_TIME = %s,
                            ADD_FLAG = '5'
                        WHERE 
                            KEN_UPLOAD_ID=%s AND 
                            KEN_HON_OPE_FLAG='1' AND 
                            OPERATION_YEAR=%s
                        """, 
                        [ localAddDate, 
                          localAddDateTime, 
                          kenUploadId, 
                          operationYear, ])
                    transaction.commit()
                except:    
                    transaction.rollback()
                    print_log('[ERROR] P13.UploadAddConfirmDoView関数 P13B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P13.UploadAddConfirmDoView関数で警告が発生しました。', 'ERROR')
                # ヒント：file_upload_uploadfileテーブルのレコードを更新する。（登録フラグの状態＝本登録済＝５）
                # ヒント：本登録済とは、レコードは登録済、ＩＤも発行済、登録フラグが本登録＝５の状態をいう。
                try:
                    localCursor.execute("""
                        UPDATE FILE_UPLOAD_UPLOADFILE
                            SET
                            ADD_DATE = %s,
                            ADD_DATE_TIME = %s,
                            ADD_FLAG = '5'
                        WHERE 
                            KEN_UPLOAD_ID=%s AND 
                            KEN_HON_OPE_FLAG='1' AND 
                            OPERATION_YEAR=%s
                        """,
                        [ localAddDate, 
                          localAddDateTime, 
                          kenUploadId, 
                          operationYear, ])
                    transaction.commit()
                except:        
                    transaction.rollback()
                    print_log('[ERROR] P13.UploadAddConfirmDoView関数 P13B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P13.UploadAddConfirmDoView関数で警告が発生しました。', 'ERROR')
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                # ヒント：file_upload_uploadテーブルのレコードを更新する。（登録フラグの状態＝本登録済＝５）
                # ヒント：本登録済とは、レコードは登録済、ＩＤも発行済、登録フラグが本登録＝５の状態をいう。
                try:
                    localCursor.execute("""
                        UPDATE FILE_UPLOAD_UPLOAD
                            SET
                            ADD_DATE = %s,
                            ADD_DATE_TIME = %s,
                            ADD_FLAG = '5'
                        WHERE 
                            HON_UPLOAD_ID=%s AND 
                            KEN_HON_OPE_FLAG='2' AND 
                            OPERATION_YEAR=%s
                        """, 
                        [ localAddDate, 
                          localAddDateTime, 
                          honUploadId, 
                          operationYear ])
                    transaction.commit()
                except:    
                    transaction.rollback()
                    print_log('[ERROR] P13.UploadAddConfirmDoView関数 P13B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P13.UploadAddConfirmDoView関数で警告が発生しました。', 'ERROR')
                # file_upload_uploadfileテーブルのレコードを更新する。（登録フラグの状態＝本登録済＝５）
                # ヒント：本登録済とは、レコードは登録済、ＩＤも発行済、登録フラグが本登録＝５の状態をいう。
                try:
                    localCursor.execute("""
                        UPDATE FILE_UPLOAD_UPLOADFILE
                            SET
                            ADD_DATE = %s,
                            ADD_DATE_TIME = %s,
                            ADD_FLAG = '5'
                        WHERE 
                            HON_UPLOAD_ID=%s AND 
                            KEN_HON_OPE_FLAG='2' AND 
                            OPERATION_YEAR=%s 
                        """,
                        [ localAddDate, 
                          localAddDateTime, 
                          honUploadId, 
                          operationYear ])
                    transaction.commit()
                except:    
                    transaction.rollback()
                    print_log('[ERROR] P13.UploadAddConfirmDoView関数 P13B60', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P13.UploadAddConfirmDoView関数で警告が発生しました。', 'ERROR')
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                print_log('[ERROR] P13.UploadAddConfirmDoView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P13.UploadAddConfirmDoView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P13.UploadAddConfirmDoView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P13.UploadAddConfirmDoView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P13.UploadAddConfirmDoView関数 P13B60', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        finally:
            # （４）ＤＢ接続を切断＝カーソルを閉じる。
            localCursor.close()
        ##########################################
        # レスポンスセット処理（Ｐ１３Ｂ７０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        # ヒント：accountType：１：都道府県、２：本省、３：運用業者
        # ヒント：accountId：　例　01hokkai
        # ヒント：isKen：True：都道府県でログインしている、False：都道府県でログインしていない
        # ヒント：isHon：True：本省でログインしている、False：本省でログインしていない
        # ヒント：isOpe：True：運用業者でログインしている、False：運用業者でログインしていない
        # ヒント：wasAdded：GETとPOSTで同じテンプレートを使用し、テンプレート内で処理を分岐するために使用する。　例　True：POSTの結果、False：削除画面の表示＝GET
        # ヒント：operationYear：調査実施年
        # ヒント：message：元の削除確認画面で、このメッセージの文字列（＝ＤＢアクセス処理の結果）を表示する。
        # ヒント：DeleteConfirmForm：テンプレートで使用するフォームのデータをセットする。
        # ヒント：isKen、isHon、isOpeは１つが必ずTrue、２つが必ずFalseを想定する。
        ##########################################
        print_log('[INFO] P13.UploadAddConfirmDoView関数 P13B70', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            response = {
                'accountType': 1,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': True,                             # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'wasAdded': True,                          # 登録済フラグをTrueにセットする。テンプレートで画面表示処理を分岐するために使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': '都道府県が登録したファイルをデータベースに登録しました。', # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'AddConfirmForm': localAddConfirmForm,     # アップロード登録確認画面用のフォーム
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'wasAdded': True,                          # 
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': '本省が登録したファイルをデータベースに登録しました。', # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'AddConfirmForm': localAddConfirmForm,     # アップロード登録確認画面用のフォーム
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P13.UploadAddConfirmDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P13.UploadAddConfirmDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P13.UploadAddConfirmDoView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１３Ｂ８０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P13.UploadAddConfirmDoView関数 P13B80', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P13UploadAddConfirmTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P13UploadAddConfirmTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            print_log('[ERROR] P13.UploadAddConfirmDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P13.UploadAddConfirmDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P13.UploadAddConfirmDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ１３Ｂ９０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P13.UploadAddConfirmDoView関数 P13B90', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P13.UploadAddConfirmDoView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P13.UploadAddConfirmDoView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１３Ｂ１００）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P13.UploadAddConfirmDoView関数 P13B100', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
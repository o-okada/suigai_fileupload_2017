#####################################################################################
# QuestionReceiveListViewビューモジュール
# ファイル名：P25.QuestionReceiveListView.py（Ｐ２５）
# ユースケース：都道府県の担当者は、問合せまたは回答の受信一覧を閲覧する。
# ユースケース：本省の担当者は、問合せまたは回答の受信一覧を閲覧する。
# ユースケース：運用業者の担当者は、問合せまたは回答の受信一覧を閲覧する。
# ヒント：問合せと回答は同じテーブル、モデルを使用する。
# ヒント：種別・区分フラグで問合せと回答を識別する。
# ヒント：accountTypeはログインした人の種別・区分
# ヒント：KEN_HON_OPE_FLAGは使用しない。
# ヒント：ここにこないはずの場合、ERRORとする。また、try exceptの場合も、ERRORとする。（判断基準１）
# ヒント：ユーザが入力した値のチェック、クエリストリング等で引っかかった場合、WARNとする。（判断基準１）
# ヒント：処理継続する場合はWARN、継続しない場合はERRORとする。（判断基準２）
#####################################################################################

#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：バイソンモジュールをインポートする。
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
# AccountModule
# QuestionModule
#####################################################################################
from file_upload.CommonFunction import print_log           # ログ出力モジュール
from file_upload.models import AccountModel                # アカウントデータモデル
from file_upload.models import QuestionModel               # 問合せ回答データモデル
#####################################################################################
# 関数名：P25.QuestionReceiveListView（Ｐ２５Ａ）
# 関数概要：都道府県用問合せまたは回答の受信一覧ページをブラウザに戻す。（都道府県）
# 関数概要：本省用問合せまたは回答の受信一覧ページをブラウザに戻す。（本省）
# 関数概要：運用業者用問合せまたは回答の受信一覧ページをブラウザに戻す。（運用業者）
#
# 引数[1]：request
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
# FORM：QuestionReceiveListForm：都道府県用問合せまたは回答の受信一覧ページ（都道府県）
# FORM：QuestionReceiveListForm：本省用問合せまたは回答の受信一覧ページ（本省）
# FORM：QuestionReceiveListForm：運用業者用問合せまたは回答の受信一覧ページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：QuestionModel：問合せまたは回答モデル（Ｒ）
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def QuestionReceiveListView(request, accountType, accountId, operationYear, filterAccount, filterRead):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P25.QuestionReceiveListView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２５Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P25.QuestionReceiveListView関数 P25A10', 'INFO')
        print_log('[INFO] P25.QuestionReceiveListView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P25.QuestionReceiveListView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P25.QuestionReceiveListView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P25.QuestionReceiveListView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P25.QuestionReceiveListView.filterAccount = {}'.format(filterAccount), 'INFO')
        print_log('[INFO] P25.QuestionReceiveListView.filterRead = {}'.format(filterRead), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２５Ａ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # （６）フィルタ種別をチェックする。　例　既読 + 未読、未読のみ、既読のみ、北海道、青森、、、沖縄、、、　
        # （７）フィルタ種別をチェックする。　例　既読 + 未読、未読のみ、既読のみ、北海道、青森、、、沖縄、、、　
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        if accountId == str(request.user.username):
            pass
        else:
            print_log('[WARN] P25.QuestionReceiveListView関数 P25A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P25.QuestionReceiveListView関数 A25A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P25.QuestionReceiveListView関数 P25A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P25.QuestionReceiveListView関数 P25A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P25.QuestionReceiveListView関数 P25A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P25.QuestionReceiveListView関数 P25A20-5', 'WARN')
                return render(request, 'error.html')
        # （６）フィルタ種別をチェックする。　例　既読 ＋ 未読
        if filterAccount is None:
            print_log('[WARN] P25.QuestionReceiveListView関数 P25A20-6', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （７）フィルタ種別をチェックする。　例　既読 ＋ 未読
        if filterRead is None:
            print_log('[WARN] P25.QuestionReceiveListView関数 P25A20-7', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(filterRead) == True:
                pass
            else:
                print_log('[WARN] P25.QuestionReceiveListView関数 P25A20-7', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ２５Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # （４）局所変数に値をセットする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P25.QuestionReceiveListView関数 P25A30', 'INFO')
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
            print_log('[ERROR] P25.QuestionReceiveListView関数 P25A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P25.QuestionReceiveListView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P25.QuestionReceiveListView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P25.QuestionReceiveListView関数P25A30', 'WARN')
            print_log('[WARN] localAccountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P25.QuestionReceiveListView関数 P25A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、問合せ回答の受信一覧の取得処理（Ｐ２５Ａ４０）
        # （１）問合せデータ、回答データを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、問合せデータ、回答データの受信一覧を取得する。
        # （３）ＤＢにアクセスし、アカウントデータを取得する。
        ##########################################
        print_log('[INFO] P25.QuestionReceiveListView関数 P25A40', 'INFO')
        # （１）問合せデータ、回答データの受信一覧を格納する局所変数を初期化する。
        localQuestionArray = None
        # （２）ＤＢにアクセスし、問合せデータ、回答データの受信一覧を取得する。
        try:
            # ヒント：ＤＢの問合せ回答データテーブルは、都道府県、本省で別々のレコードとして管理している。
            # ヒント：問合せ、回答データは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
            if filterRead == '5':
                # 既読の場合、、、
                # ヒント：このウェブアプリでは、既読とは、受信者が既読のことをいう。送信者が既読の場合は扱わない。（興味なし）
                if filterAccount == '0':
                    ##########################################
                    # ケース１：既読の場合、、、and 全アカウントの場合、、、
                    # ヒント：この受信トレイでは、全アカウントとは、送信者のアカウントが全アカウントのことをいう。
                    # ヒント：受信者のアカウントは、当然絞り込み条件とする。
                    ##########################################
                    localQuestionArray = QuestionModel.objects.raw("""
                        SELECT 
                            id,
                            QUESTION_ID,
                            OPERATION_YEAR,
                            FLOOD_YEAR,
                            SEND_ORG_CODE,
                            SEND_ORG_NAME,
                            SEND_DEPT_CODE,
                            SEND_DEPT_NAME,
                            SEND_ACCOUNT_ID,
                            SEND_ACCOUNT_NAME,
                            SEND_DATE,
                            SEND_DATE_TIME,
                            SEND_FLAG,
                            SUBJECT,
                            BODY,
                            RECEIVE_ORG_CODE,
                            RECEIVE_ORG_NAME,
                            RECEIVE_DEPT_CODE,
                            RECEIVE_DEPT_NAME,
                            RECEIVE_ACCOUNT_ID,
                            RECEIVE_ACCOUNT_NAME,
                            RECEIVE_DATE,
                            RECEIVE_DATE_TIME,
                            RECEIVE_FLAG,
                            DELETE_DATE,
                            DELETE_DATE_TIME,
                            DELETE_FLAG,
                            RECEIVE_READ_FLAG  
                        FROM 
                            FILE_UPLOAD_QUESTION 
                        WHERE 
                            RECEIVE_ACCOUNT_ID=%s AND 
                            OPERATION_YEAR=%s AND 
                            RECEIVE_READ_FLAG='5' AND
                            SEND_FLAG='5'
                        ORDER BY 
                            SEND_DATE_TIME DESC   
                        """,
                        [accountId, operationYear, ])
                else:
                    ##########################################
                    # ケース２：既読の場合、、、 and 特定アカウントの場合、、、
                    # ヒント：この受信トレイでは、特定のアカウントとは、送信者のアカウントが特定のアカウントのことをいう。
                    # ヒント：受信者のアカウントは、当然絞込条件とする。
                    ##########################################
                    localQuestionArray = QuestionModel.objects.raw("""
                        SELECT 
                            id,
                            QUESTION_ID,
                            OPERATION_YEAR,
                            FLOOD_YEAR,
                            SEND_ORG_CODE,
                            SEND_ORG_NAME,
                            SEND_DEPT_CODE,
                            SEND_DEPT_NAME,
                            SEND_ACCOUNT_ID,
                            SEND_ACCOUNT_NAME,
                            SEND_DATE,
                            SEND_DATE_TIME,
                            SEND_FLAG,
                            SUBJECT,
                            BODY,
                            RECEIVE_ORG_CODE,
                            RECEIVE_ORG_NAME,
                            RECEIVE_DEPT_CODE,
                            RECEIVE_DEPT_NAME,
                            RECEIVE_ACCOUNT_ID,
                            RECEIVE_ACCOUNT_NAME,
                            RECEIVE_DATE,
                            RECEIVE_DATE_TIME,
                            RECEIVE_FLAG,
                            DELETE_DATE,
                            DELETE_DATE_TIME,
                            DELETE_FLAG,
                            RECEIVE_READ_FLAG  
                        FROM 
                            FILE_UPLOAD_QUESTION 
                        WHERE 
                            RECEIVE_ACCOUNT_ID=%s AND 
                            OPERATION_YEAR=%s AND 
                            RECEIVE_READ_FLAG='5' AND
                            SEND_ACCOUNT_ID=%s AND 
                            SEND_FLAG='5'
                        ORDER BY 
                            SEND_DATE_TIME DESC   
                        """,
                        [accountId, operationYear, filterAccount, ])
            elif filterRead == '0':
                # 未読の場合、、、
                # ヒント：このウェブアプリでは、既読とは、受信者が既読のことをいう。送信者が既読の場合は扱わない。（興味なし）
                if filterAccount == '0':
                    ##########################################
                    # ケース３：未読の場合、、、and 全アカウントの場合、、、
                    # ヒント：この受信トレイでは、全アカウントとは、送信者のアカウントが全アカウントのことをいう。
                    # ヒント：受信者のアカウントは、当然絞り込み条件とする。
                    ##########################################
                    localQuestionArray = QuestionModel.objects.raw("""
                        SELECT 
                            id,
                            QUESTION_ID,
                            OPERATION_YEAR,
                            FLOOD_YEAR,
                            SEND_ORG_CODE,
                            SEND_ORG_NAME,
                            SEND_DEPT_CODE,
                            SEND_DEPT_NAME,
                            SEND_ACCOUNT_ID,
                            SEND_ACCOUNT_NAME,
                            SEND_DATE,
                            SEND_DATE_TIME,
                            SEND_FLAG,
                            SUBJECT,
                            BODY,
                            RECEIVE_ORG_CODE,
                            RECEIVE_ORG_NAME,
                            RECEIVE_DEPT_CODE,
                            RECEIVE_DEPT_NAME,
                            RECEIVE_ACCOUNT_ID,
                            RECEIVE_ACCOUNT_NAME,
                            RECEIVE_DATE,
                            RECEIVE_DATE_TIME,
                            RECEIVE_FLAG,
                            DELETE_DATE,
                            DELETE_DATE_TIME,
                            DELETE_FLAG,
                            RECEIVE_READ_FLAG  
                        FROM 
                            FILE_UPLOAD_QUESTION 
                        WHERE 
                            RECEIVE_ACCOUNT_ID=%s AND 
                            OPERATION_YEAR=%s AND 
                            RECEIVE_READ_FLAG='0' AND
                            SEND_FLAG='5'
                        ORDER BY 
                            SEND_DATE_TIME DESC   
                        """,
                        [accountId, operationYear, ])
                else:
                    ##########################################
                    # ケース４：未読の場合、、、 and 特定アカウントの場合、、、
                    # ヒント：この受信トレイでは、特定のアカウントとは、送信者のアカウントが特定のアカウントのことをいう。
                    # ヒント：受信者のアカウントは、当然絞込条件とする。
                    ##########################################
                    localQuestionArray = QuestionModel.objects.raw("""
                        SELECT 
                            id,
                            QUESTION_ID,
                            OPERATION_YEAR,
                            FLOOD_YEAR,
                            SEND_ORG_CODE,
                            SEND_ORG_NAME,
                            SEND_DEPT_CODE,
                            SEND_DEPT_NAME,
                            SEND_ACCOUNT_ID,
                            SEND_ACCOUNT_NAME,
                            SEND_DATE,
                            SEND_DATE_TIME,
                            SEND_FLAG,
                            SUBJECT,
                            BODY,
                            RECEIVE_ORG_CODE,
                            RECEIVE_ORG_NAME,
                            RECEIVE_DEPT_CODE,
                            RECEIVE_DEPT_NAME,
                            RECEIVE_ACCOUNT_ID,
                            RECEIVE_ACCOUNT_NAME,
                            RECEIVE_DATE,
                            RECEIVE_DATE_TIME,
                            RECEIVE_FLAG,
                            DELETE_DATE,
                            DELETE_DATE_TIME,
                            DELETE_FLAG,
                            RECEIVE_READ_FLAG  
                        FROM 
                            FILE_UPLOAD_QUESTION 
                        WHERE 
                            RECEIVE_ACCOUNT_ID=%s AND 
                            OPERATION_YEAR=%s AND 
                            RECEIVE_READ_FLAG='0' AND
                            SEND_ACCOUNT_ID=%s AND
                            SEND_FLAG='5'
                        ORDER BY 
                            SEND_DATE_TIME DESC   
                        """,
                        [accountId, operationYear, filterAccount, ])
            else:
                # 既読＋未読の場合、、、
                # ヒント：このウェブアプリでは、未読とは、受信者が未読のことをいう。送信者が未読の場合は扱わない。（興味なし）
                if filterAccount == '0':
                    ##########################################
                    # ケース５：既読＋未読の場合、、、 and 全アカウントの場合、、、
                    # ヒント：この受信トレイでは、全アカウントとは、送信者のアカウントが全アカウントのことをいう。
                    # ヒント：受信者のアカウントは、当然絞り込み条件とする。
                    ##########################################
                    localQuestionArray = QuestionModel.objects.raw("""
                        SELECT 
                            id,
                            QUESTION_ID,
                            OPERATION_YEAR,
                            FLOOD_YEAR,
                            SEND_ORG_CODE,
                            SEND_ORG_NAME,
                            SEND_DEPT_CODE,
                            SEND_DEPT_NAME,
                            SEND_ACCOUNT_ID,
                            SEND_ACCOUNT_NAME,
                            SEND_DATE,
                            SEND_DATE_TIME,
                            SEND_FLAG,
                            SUBJECT,
                            BODY,
                            RECEIVE_ORG_CODE,
                            RECEIVE_ORG_NAME,
                            RECEIVE_DEPT_CODE,
                            RECEIVE_DEPT_NAME,
                            RECEIVE_ACCOUNT_ID,
                            RECEIVE_ACCOUNT_NAME,
                            RECEIVE_DATE,
                            RECEIVE_DATE_TIME,
                            RECEIVE_FLAG,
                            DELETE_DATE,
                            DELETE_DATE_TIME,
                            DELETE_FLAG,
                            RECEIVE_READ_FLAG  
                        FROM 
                            FILE_UPLOAD_QUESTION 
                        WHERE 
                            RECEIVE_ACCOUNT_ID=%s AND 
                            OPERATION_YEAR=%s AND
                            SEND_FLAG='5' 
                        ORDER BY 
                            SEND_DATE_TIME DESC   
                        """,
                        [accountId, operationYear, ])
                else:
                    ##########################################
                    # ケース６：既読＋未読の場合、、、 and 特定アカウントの場合、、、
                    # ヒント：この受信トレイでは、特定のアカウントとは、送信者のアカウントが特定のアカウントのことをいう。
                    # ヒント：受信者のアカウントは、当然絞込条件とする。
                    ##########################################
                    localQuestionArray = QuestionModel.objects.raw("""
                        SELECT 
                            id,
                            QUESTION_ID,
                            OPERATION_YEAR,
                            FLOOD_YEAR,
                            SEND_ORG_CODE,
                            SEND_ORG_NAME,
                            SEND_DEPT_CODE,
                            SEND_DEPT_NAME,
                            SEND_ACCOUNT_ID,
                            SEND_ACCOUNT_NAME,
                            SEND_DATE,
                            SEND_DATE_TIME,
                            SEND_FLAG,
                            SUBJECT,
                            BODY,
                            RECEIVE_ORG_CODE,
                            RECEIVE_ORG_NAME,
                            RECEIVE_DEPT_CODE,
                            RECEIVE_DEPT_NAME,
                            RECEIVE_ACCOUNT_ID,
                            RECEIVE_ACCOUNT_NAME,
                            RECEIVE_DATE,
                            RECEIVE_DATE_TIME,
                            RECEIVE_FLAG,
                            DELETE_DATE,
                            DELETE_DATE_TIME,
                            DELETE_FLAG,
                            RECEIVE_READ_FLAG  
                        FROM 
                            FILE_UPLOAD_QUESTION 
                        WHERE 
                            RECEIVE_ACCOUNT_ID=%s AND 
                            OPERATION_YEAR=%s AND 
                            SEND_ACCOUNT_ID=%s AND
                            SEND_FLAG='5'
                        ORDER BY 
                            SEND_DATE_TIME DESC   
                        """,
                        [accountId, operationYear, filterAccount, ])
        except:
            localQuestionArray = None
            print_log('[ERROR] P25.QuestionReceiveListView関数 P25A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P25.QuestionReceiveListView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P25.QuestionReceiveListView関数を警告終了しました。', 'ERROR')
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
                [operationYear, ])
        except:
            localAccountArray == None        
            print_log('[ERROR] P25.QuestionReceiveListView関数 P25A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P25.QuestionReceiveListView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P25.QuestionReceiveListView関数を警告終了しました。', 'ERROR')
        ##########################################
        # フォームセット処理（Ｐ１０Ａ５０）
        # （１）局所変数のフォームを初期化する。
        ##########################################
        print_log('[INFO] P25.QuestionReceiveListView関数 P25A50', 'INFO')
        ##########################################
        # レスポンスセット処理（Ｐ２５Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        ##########################################
        print_log('[INFO] P25.QuestionReceiveListView関数 P25A60', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            if localQuestionArray != None:
                response = {
                    'accountType': 1,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'accountId': urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': True,                         # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': False,                        # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': False,                        # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': urlquote(operationYear), # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'questionArray': localQuestionArray,   # 問合せ回答データの受信一覧
                    'questionLength': len(list(localQuestionArray)), # 問合せ回答データの受信一覧に含まれる問合せ回答データの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                    'filterRead': urlquote(filterRead),    # フィルタ種別
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
                    'questionArray': localQuestionArray,   # 問合せ回答データの受信一覧
                    'questionLength': 0,                   # 問合せ回答データの受信一覧に含まれる問合せ回答データの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                    'filterRead': urlquote(filterRead),    # フィルタ種別
                }    
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            if localQuestionArray != None:
                response = {
                    'accountType': 2,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'accountId': urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isKen': False,                        # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': True,                         # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': False,                        # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': urlquote(operationYear), # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'questionArray': localQuestionArray,   # 問合せ回答データの受信一覧
                    'questionLength': len(list(localQuestionArray)), # 問合せ回答データの受信一覧に含まれる問合せ回答データの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                    'filterRead': urlquote(filterRead),    # フィルタ種別
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
                    'questionArray': localQuestionArray,   # 問合せ回答データの受信一覧
                    'questionLength': 0,                   # 問合せ回答データの受信一覧に含まれる問合せ回答データの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                    'filterRead': urlquote(filterRead),    # フィルタ種別
                }    
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            if localQuestionArray != None:
                response = {
                    'accountType': 3,                      # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'accountId': urlquote(accountId),      #　アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。　
                    'isKen': False,                        # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isHon': False,                        # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'isOpe': True,                         # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                    'operationYear': urlquote(operationYear), # 調査実施年
                    'message': 'message',                  # ブラウザに表示するメッセージを必要に応じてここにセットする。
                    'questionArray': localQuestionArray,   # 問合せ回答データの受信一覧
                    'questionLength': len(list(localQuestionArray)), # 問合せ回答データの受信一覧に含まれる問合せ回答データの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                    'filterRead': urlquote(filterRead),    # フィルタ種別
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
                    'questionArray': localQuestionArray,   # 問合せ回答データの受信一覧
                    'questionLength': 0,                   # 問合せ回答データの受信一覧に含まれる問合せ回答データの件数
                    'accountArray': localAccountArray,     # アカウント一覧（宛先選択用）
                    'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
                    'filterAccount': urlquote(filterAccount), # フィルタ種別
                    'filterRead': urlquote(filterRead),    # フィルタ種別
                }    
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P25.QuestionReceiveListView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P25.QuestionReceiveListView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P25.QuestionReceiveListView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ１０Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P25.QuestionReceiveListView関数 P25A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P25QuestionReceiveListTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P25QuestionReceiveListTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            return render(request, 'P25QuestionReceiveListTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P25.QuestionReceiveListView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P25.QuestionReceiveListView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ２５Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P25.QuestionReceiveListView関数 P25A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P25.QuestionReceiveListView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P25.QuestionReceiveListView関数が異常終了しました。', 'ERROR')
        ##########################################
        # 戻り値セット処理（Ｐ２５Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P25.QuestionReceiveListView関数 P25A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
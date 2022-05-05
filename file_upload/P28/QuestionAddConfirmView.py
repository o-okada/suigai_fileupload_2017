#####################################################################################
# QuestionAddConfirmViewビューモジュール
# ファイル名：P28.QuestionAddConfirmView.py（Ｐ２８）
# ユースケース：都道府県は、問合せを本登録する。
# ユースケース：本省は、回答を本登録する。
# ユースケース：運用業者は、回答を本登録する。
# ヒント：問合せと回答は同じテーブル、モデルを使用する。
# ヒント：種別・区分フラグで問合せと回答を識別する。
# ヒント：ここにこないはずの場合、ERRORとする。また、try exceptの場合も、ERRORとする。（判断基準１）
# ヒント：ユーザが入力した値のチェック、クエリストリング等で引っかかった場合、WARNとする。（判断基準１）
# ヒント：処理継続する場合はWARN、継続しない場合はERRORとする。（判断基準２）
# ヒント：KEN_HON_OPE_FLAGは使用しない。
#####################################################################################

#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：パイソンモジュールをインポートする。
# io
# os
# sys
# namedtuple
# datetime
#####################################################################################
import io                                                  # ioモジュール
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
from file_upload.forms import QuestionAddConfirmForm       # 問合せ回答登録確認フォーム
from file_upload.models import AccountModel                # アカウントデータモデル
from file_upload.models import QuestionFileModel           # 問合せ回答ファイルデータモデル
from file_upload.models import QuestionModel               # 問合せ回答データモデル
#####################################################################################
# 処理名：大域変数定義（０００）
# 処理概要：大域変数を定義する。
#####################################################################################
def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
#####################################################################################
# 関数名：P28.QuestionAddConfirmView（Ｐ２８Ａ）
# 関数概要：都道府県用問合せ登録確認ページをブラウザに戻す。（都道府県）
# 関数概要：本省用回答登録確認ページをブラウザに戻す。（本省）
# 関数概要：運用業者用問合せ登録確認ページをブラウザに戻す。（運用業者）
#
# 引数[1]：request
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから運用業者名、運用業者部署名、運用業者名を取得するために使用する。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）
# 引数[5]：kenQuestionId：都道府県用問合せＩＤ※ＤＢから都道府県用問合せを取得し、本登録するために使用する。（都道府県）
# 引数[5]：honOpeQuestionId：本省用問合せＩＤ※ＤＢから本省用回答を取得し、本登録するために使用する。（本省）
# 引数[5]：honOpeQuestionId：運用業者用問合せＩＤ※ＤＢから運用業者用回答を取得し、本登録するために使用する。（運用業者）
#
# 戻り値[1]：response
#
# FORM：QuestionAddConfirmForm：都道府県用問合せ登録確認ページ（都道府県）
# FORM：QuestionAddConfirmForm：本省用回答登録確認ページ（本省）
# FORM：QuestionAddConfirmForm：運用業者用回答登録確認ページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：QuestionModel：問合せまたは回答モデル（Ｒ）
# ヒント：都道府県からの呼び出しの場合、kenQuestionIdはNot Null、honOpeQuestionIdはNull
# ヒント：本省からの呼び出しの場合、kenQuestionIdはNot Null、honOpeQuestionIdはNot Null
# ヒント：運用業者からの呼び出しの場合、kenQuestionIdはNot Null、honOpeQuestionIdはNot Null
# ヒント：QuestionAddDoView関数でＤＢに仮登録済で、そのときにquestionIdを生成済と想定する。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/login/')
def QuestionAddConfirmView(request, accountType, accountId, operationYear, questionId, fromAccountId, toAccountId):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２８Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P28.QuestionAddConfirmView関数 P28A10', 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmView.questionId = {}'.format(questionId), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmView.fromAccountId = {}'.format(fromAccountId), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmView.toAccountId = {}'.format(toAccountId), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２８Ａ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # （６）問合せ回答ＩＤをチェックする。　例　1
        # （７）送信者のアカウントＩＤをチェックする。　例　1
        # （８）受信者のアカウントＩＤをチェックする。　例　1
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        if accountId == str(request.user.username):
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-5', 'WARN')
                return render(request, 'error.html')
        # （６）問合せ回答ＩＤをチェックする。　例　1
        # ヒント：複数受信アカウントＩＤに対応するため、カンマが含まれると想定する。
        if questionId is None:
            print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-6', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        localQuestionIdList = questionId.split(",")
        if len(list(localQuestionIdList)) >= 1:
            for i in range(0, len(list(localQuestionIdList)) - 1):
                if str.isdigit(localQuestionIdList[i]) == True:
                    pass
                else:
                    print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-6', 'WARN')
                    return render(request, 'error.html')
        else:
            print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-6', 'WARN')
            return render(request, 'error.html')
        # （７）送信者のアカウントＩＤをチェックする。　例　1
        if fromAccountId is None:
            print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-7', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （８）受信者のアカウントＩＤをチェックする。　例　1　ヒント：カンマで複数指定可能とする。
        # ヒント：複数受信アカウントＩＤに対応するため、カンマが含まれると想定する。
        if toAccountId is None:
            print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-8', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        localToAccountIdList = toAccountId.split(",")
        if len(list(localToAccountIdList)) >= 1:
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmView関数 P28A20-8', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ２８Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P28.QuestionAddConfirmView関数 P28A30', 'INFO')
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
                    OPERATION_YEAR=%s LIMIT 1
                """, 
                [accountId, operationYear, ])[0]
        except:
            localAccountModel = None
            print_log('[ERROR] P28.QuestionAddConfirmView関数 P28A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        # ヒント：ＤＢアクセス前にlocalAccountModelをNoneに初期化することで、ここで、ＤＢからのデータ取得に成功したか否かを判定できる。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmView関数P28A30', 'WARN')
            print_log('[WARN] localAccountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P28.QuestiondAddConfirmView関数 P28A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、問合せ回答データの取得処理（Ｐ２８Ａ４０）
        # （１）問合せ回答データ、問合せ回答ファイルデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、問合せ回答データ、問合せ回答ファイルデータを取得する。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：rawでＤＢにアクセスした場合、検索結果が０件の場合、エクセプションが発生する。
        # ヒント：後々の拡張等を考慮し、場合分けをベタで記述し、明示されていないロジックを含まないコードとするため、
        # ヒント：あえて冗長な場合分けをしている。
        # ヒント：ＤＢのアップロードテーブル、アップロードファイルテーブルには、KEN_QUESTION_ID、HON_QUESTION_ID、OPE_QUESTION_IDの項目がある。
        # ヒント：調査結果（親）と確認結果（子）を紐付けるために使用している。
        # ヒント：このため、都道府県（親）については、KEN_QUESTION_ID（親問合せ回答データのＩＤ）がセット、HON_QUESTION_ID（子問合せ回答データのＩＤ）が未セット、
        # ヒント：本省（子）については、KEN_QUESTION_ID（親問合せ回答データのＩＤ）がセット、HON_QUESTION_ID（子問合せ回答データのＩＤ）がセットされることを想定している。
        # ヒント：また、後々の拡張等を考慮し、都道府県（親）についても、KEN_QUESTION_IDがセット、HON_QUESTION_IDがセットされることも想定している。
        # ヒント：KEN_HON_OPE_FLAGは使用しない。
        ##########################################
        print_log('[INFO] P28.QuestionAddConfirmView関数 P28A40', 'INFO')
        # （１）問合せ回答データ、問合せ回答ファイルデータ、を格納する局所変数を初期化する。
        localQuestionModel = None
        localQuestionFileModel = None
        # （２）ＤＢにアクセスし、問合せ回答データ、問合せ回答ファイルデータを取得する。
        # ヒント：確認画面では、問合せ回答データは０件はあり得ないとして、ＳＱＬ文でエラーが発生した場合、処理を中止する。
        # ヒント：作成画面とは異なる。作成画面の場合、０件も可とし、処理を継続する。
        # ヒント：受信者アカウントＩＤは複数と想定する。
        # ヒント：送信確認画面が１画面のため、代表１問合せ回答データのみ取得する。
        try:
            localQuestionModel = QuestionModel.objects.raw("""
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
                    QUESTION_ID=%s AND 
                    OPERATION_YEAR=%s LIMIT 1 
                """, 
                [localQuestionIdList[0], operationYear, ])[0]
        except:
            localQuestionModel = None
            print_log('[ERROR] P28.QuestionAddConfirmView関数 P28A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # ヒント：問合せ回答ファイルデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
        # ヒント：問合せ回答ファイルデータは１問合せ回答データにつき、１件と想定している。
        # ヒント：問合せ回答ファイルデータのみ削除する機能、問合せ回答ファイルデータ、問合せ回答データを更新する機能を提供していないためこの想定は破綻しない。
        # TO-DO：必要に応じ、上記制限を緩和することを検討すること。ただし、この場合、以下のＳＱＬ文は使用できなくなり、修正が必要である。
        # ヒント：問合せ回答データを登録するというよりも、問為替回答ファイルデータを登録し、その付随として、その他の情報を登録するというユースケースを想定する。
        try:    
            localQuestionFileModel = QuestionFileModel.objects.raw("""
                SELECT 
                    id,
                    QUESTION_FILE_ID,
                    QUESTION_ID,
                    OPERATION_YEAR,
                    FLOOD_YEAR,
                    FILE_ID,
                    FILE_NAME,
                    FILE_PATH,
                    SEND_DATE,
                    SEND_DATE_TIME,
                    SEND_FLAG,
                    DELETE_DATE,
                    DELETE_DATE_TIME,
                    DELETE_FLAG 
                FROM 
                    FILE_UPLOAD_QUESTIONFILE
                WHERE 
                    QUESTION_ID=%s AND 
                    OPERATION_YEAR=%s LIMIT 1
                """,
                [localQuestionIdList[0], operationYear, ])[0]
        except:
            localQuestionFileModel = None            
            print_log('[ERROR] P28.QuestionAddConfirmView関数 P28A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmView関数を警告終了しました。', 'ERROR')
        ##########################################            
        # フォームセット処理（Ｐ２８Ａ５０）
        # （１）局所変数のフォームを初期化する。
        # ヒント：ブラウザとのデータのやりとり、特にブラウザからPOSTデータがある場合、フォームを使用する。
        # ヒント：モデルはブラウザで参照用、かつタグをコーディングする場合等に使用する。
        # ヒント：フォームはブラウザで編集用、POSTでサーバにリクエストされる項目、かつタグを自動生成する場合等に使用する。
        # ヒント：表示画面の場合、URL+QUERY STRING、VIEW関数、GET、renderでテンプレートとレスポンスで目的の画面を表示する。
        # ヒント：追加、削除の場合、URL+QUERY STRING+フォーム値、DoVIEW関数、POST、redirect（URL+QUERY STRING）で次の画面に遷移する。
        # ヒント：または、追加、削除の場合、URL+QUERY STRING+フォーム値、DoVIEW関数、POST、renderでテンプレートとレスポンスで元の同じ画面を表示する。
        # ヒント：ただし、この場合、レスポンスに、追加、削除結果のフラグを返し、ブラウザ側（正確にはサーバでのレンダリング時＝HTML生成時）で通常画面と結果画面をフラグを見て分岐処理するようにテンプレートを記述する。
        ##########################################            
        print_log('[INFO] P28.QuestionAddConfirmView関数 P28A50', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localAddDate = datetime.now().strftime("%Y/%m/%d")
        localAddDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        localQuestionAddConfirmForm = QuestionAddConfirmForm()
        ##########################################            
        # フォームセット処理（Ｐ２８Ａ５１）
        # （１）局所変数のフォームに初期値をセットする。
        ##########################################            
        # （１）局所変数のフォームに初期値をセットする。
        if localQuestionModel != None:
            localQuestionAddConfirmForm.initial['QUESTION_ID'] = localQuestionModel.QUESTION_ID                   # P28-1   
            localQuestionAddConfirmForm.initial['OPERATION_YEAR'] = localQuestionModel.OPERATION_YEAR             # P28-3
            localQuestionAddConfirmForm.initial['FLOOD_YEAR'] = localQuestionModel.FLOOD_YEAR                     # P28-4
            localQuestionAddConfirmForm.initial['SEND_ORG_CODE'] = localQuestionModel.SEND_ORG_CODE               # P28-5
            localQuestionAddConfirmForm.initial['SEND_ORG_NAME'] = localQuestionModel.SEND_ORG_NAME               # P28-6
            localQuestionAddConfirmForm.initial['SEND_DEPT_CODE'] = localQuestionModel.SEND_DEPT_CODE             # P28-7
            localQuestionAddConfirmForm.initial['SEND_DEPT_NAME'] = localQuestionModel.SEND_DEPT_NAME             # P28-8
            localQuestionAddConfirmForm.initial['SEND_ACCOUNT_ID'] = localQuestionModel.SEND_ACCOUNT_ID           # P28-9
            localQuestionAddConfirmForm.initial['SEND_ACCOUNT_NAME'] = localQuestionModel.SEND_ACCOUNT_NAME       # P28-10  
            localQuestionAddConfirmForm.initial['SEND_DATE'] = localQuestionModel.SEND_DATE                       # P28-11
            localQuestionAddConfirmForm.initial['SEND_DATE_TIME'] = localQuestionModel.SEND_DATE_TIME             # P28-12
            localQuestionAddConfirmForm.initial['SEND_FLAG'] = localQuestionModel.SEND_FLAG                       # P28-13
            localQuestionAddConfirmForm.initial['SUBJECT'] = localQuestionModel.SUBJECT                           # P28-14
            localQuestionAddConfirmForm.initial['BODY'] = localQuestionModel.BODY                                 # P28-15
            localQuestionAddConfirmForm.initial['RECEIVE_ORG_CODE'] = localQuestionModel.RECEIVE_ORG_CODE         # P28-20
            localQuestionAddConfirmForm.initial['RECEIVE_ORG_NAME'] = localQuestionModel.RECEIVE_ORG_NAME         # P28-21
            localQuestionAddConfirmForm.initial['RECEIVE_DEPT_CODE'] = localQuestionModel.RECEIVE_DEPT_CODE       # P28-22
            localQuestionAddConfirmForm.initial['RECEIVE_DEPT_NAME'] = localQuestionModel.RECEIVE_DEPT_NAME       # P28-23
            localQuestionAddConfirmForm.initial['RECEIVE_ACCOUNT_ID'] = toAccountId                               # P28-24
            localQuestionAddConfirmForm.initial['RECEIVE_ACCOUNT_NAME'] = localQuestionModel.RECEIVE_ACCOUNT_NAME # P28-25
            localQuestionAddConfirmForm.initial['RECEIVE_DATE'] = localQuestionModel.RECEIVE_DATE                 # P28-26
            localQuestionAddConfirmForm.initial['RECEIVE_DATE_TIME'] = localQuestionModel.RECEIVE_DATE_TIME       # P28-27
            localQuestionAddConfirmForm.initial['RECEIVE_FLAG'] = localQuestionModel.RECEIVE_FLAG                 # P28-28
            localQuestionAddConfirmForm.initial['DELETE_DATE'] = localQuestionModel.DELETE_DATE                   # P28-29
            localQuestionAddConfirmForm.initial['DELETE_DATE_TIME'] = localQuestionModel.DELETE_DATE_TIME         # P28-30
            localQuestionAddConfirmForm.initial['DELETE_FLAG'] = localQuestionModel.DELETE_FLAG                   # P28-31
            localQuestionAddConfirmForm.initial['RECEIVE_READ_FLAG'] = localQuestionModel.RECEIVE_READ_FLAG       # P28-32 
        else:    
            localQuestionAddConfirmForm.initial['QUESTION_ID'] = "0"                                              # P28-1
            localQuestionAddConfirmForm.initial['OPERATION_YEAR'] = "0"                                           # P28-3
            localQuestionAddConfirmForm.initial['FLOOD_YEAR'] = "0"                                               # P28-4
            localQuestionAddConfirmForm.initial['SEND_ORG_CODE'] = "0"                                            # P28-5
            localQuestionAddConfirmForm.initial['SEND_ORG_NAME'] = "0"                                            # P28-6
            localQuestionAddConfirmForm.initial['SEND_DEPT_CODE'] = "0"                                           # P28-7 
            localQuestionAddConfirmForm.initial['SEND_DEPT_NAME'] = "0"                                           # P28-8
            localQuestionAddConfirmForm.initial['SEND_ACCOUNT_ID'] = "0"                                          # P28-9
            localQuestionAddConfirmForm.initial['SEND_ACCOUNT_NAME'] = "0"                                        # P28-10
            localQuestionAddConfirmForm.initial['SEND_DATE'] = "0"                                                # P28-11
            localQuestionAddConfirmForm.initial['SEND_DATE_TIME'] = "0"                                           # P28-12
            localQuestionAddConfirmForm.initial['SEND_FLAG'] = "0"                                                # P28-13
            localQuestionAddConfirmForm.initial['SUBJECT'] = "0"                                                  # P28-14 
            localQuestionAddConfirmForm.initial['BODY'] = "0"                                                     # P28-15
            localQuestionAddConfirmForm.initial['RECEIVE_ORG_CODE'] = "0"                                         # P28-20 
            localQuestionAddConfirmForm.initial['RECEIVE_ORG_NAME'] = "0"                                         # P28-21 
            localQuestionAddConfirmForm.initial['RECEIVE_DEPT_CODE'] = "0"                                        # P28-22
            localQuestionAddConfirmForm.initial['RECEIVE_DEPT_NAME'] = "0"                                        # P28-23
            localQuestionAddConfirmForm.initial['RECEIVE_ACCOUNT_ID'] = "0"                                       # P28-24
            localQuestionAddConfirmForm.initial['RECEIVE_ACCOUNT_NAME'] = "0"                                     # P28-25
            localQuestionAddConfirmForm.initial['RECEIVE_DATE'] = "0"                                             # P28-26
            localQuestionAddConfirmForm.initial['RECEIVE_DATE_TIME'] = "0"                                        # P28-27 
            localQuestionAddConfirmForm.initial['RECEIVE_FLAG'] = "0"                                             # P28-28
            localQuestionAddConfirmForm.initial['DELETE_DATE'] = "0"                                              # P28-29
            localQuestionAddConfirmForm.initial['DELETE_DATE_TIME'] = "0"                                         # P28-30
            localQuestionAddConfirmForm.initial['DELETE_FLAG'] = "0"                                              # P28-31
            localQuestionAddConfirmForm.initial['RECEIVE_READ_FLAG'] = "0"                                        # P28-32
        # 問合せ回答ファイルデータ項目に初期値をセットする。
        if localQuestionFileModel != None:
            localQuestionAddConfirmForm.initial['FILE_ID'] = localQuestionFileModel.FILE_ID                       # P28-17
            localQuestionAddConfirmForm.initial['FILE_NAME'] = localQuestionFileModel.FILE_NAME                   # P28-18
            localQuestionAddConfirmForm.initial['FILE_PATH'] = localQuestionFileModel.FILE_PATH                   # P28-19
        else:
            localQuestionAddConfirmForm.initial['FILE_ID'] = "0"                                                  # P28-17
            localQuestionAddConfirmForm.initial['FILE_NAME'] = "0"                                                # P28-18 
            localQuestionAddConfirmForm.initial['FILE_PATH'] = "0"                                                # P28-19
        ##########################################            
        # フォームセット処理（Ｐ２８Ａ５４）
        # （１）フォームのウィジェットの属性に値をセットする。
        # ヒント：利用者が編集できない項目は、disabled、readonlyのいずれかとする。
        # ヒント：フォームを使用した場合、ブラウザでタグが自動生成されるため、ブラウザのstyle、cssでdisable、readonlyをセットしにくい。
        # ヒント：そのため。ビュー関数でdisable、readonly等をセットする。
        # ヒント：フォームのフィールドは、非表示の項目もセットすることを推奨する。
        # ヒント：ステートレスなウェブアプリにおいて、ブラウザに送ったデータをPOST時にサーバ側のビュー関数で参照可能とするため。
        ##########################################            
        # （１）フォームのウィジェットの属性に値をセットする。
        localQuestionAddConfirmForm.fields['QUESTION_ID'].widget.attrs['readonly'] = True                         # P28-1
        localQuestionAddConfirmForm.fields['OPERATION_YEAR'].widget.attrs['readonly'] = True                      # P28-3
        localQuestionAddConfirmForm.fields['FLOOD_YEAR'].widget.attrs['readonly'] = True                          # P28-4
        localQuestionAddConfirmForm.fields['SEND_ORG_CODE'].widget.attrs['readonly'] = True                       # P28-5
        localQuestionAddConfirmForm.fields['SEND_ORG_NAME'].widget.attrs['readonly'] = True                       # P28-6
        localQuestionAddConfirmForm.fields['SEND_DEPT_CODE'].widget.attrs['readonly'] = True                      # P28-7
        localQuestionAddConfirmForm.fields['SEND_DEPT_NAME'].widget.attrs['readonly'] = True                      # P28-8
        localQuestionAddConfirmForm.fields['SEND_ACCOUNT_ID'].widget.attrs['readonly'] = True                     # P28-9
        localQuestionAddConfirmForm.fields['SEND_ACCOUNT_NAME'].widget.attrs['readonly'] = True                   # P28-10
        localQuestionAddConfirmForm.fields['SEND_DATE'].widget.attrs['readonly'] = True                           # P28-11
        localQuestionAddConfirmForm.fields['SEND_DATE_TIME'].widget.attrs['readonly'] = True                      # P28-12
        localQuestionAddConfirmForm.fields['SEND_FLAG'].widget.attrs['readonly'] = True                           # P28-13
        localQuestionAddConfirmForm.fields['SUBJECT'].widget.attrs['readonly'] = True                             # P28-14
        localQuestionAddConfirmForm.fields['BODY'].widget.attrs['readonly'] = True                                # P28-15
        localQuestionAddConfirmForm.fields['FILE_ID'].widget.attrs['readonly'] = True                             # P28-17
        localQuestionAddConfirmForm.fields['FILE_NAME'].widget.attrs['readonly'] = True                           # P28-18
        localQuestionAddConfirmForm.fields['FILE_PATH'].widget.attrs['readonly'] = True                           # P28-19
        localQuestionAddConfirmForm.fields['RECEIVE_ORG_CODE'].widget.attrs['readonly'] = True                    # P28-20
        localQuestionAddConfirmForm.fields['RECEIVE_ORG_NAME'].widget.attrs['readonly'] = True                    # P28-21
        localQuestionAddConfirmForm.fields['RECEIVE_DEPT_CODE'].widget.attrs['readonly'] = True                   # P28-22
        localQuestionAddConfirmForm.fields['RECEIVE_DEPT_NAME'].widget.attrs['readonly'] = True                   # P28-23
        localQuestionAddConfirmForm.fields['RECEIVE_ACCOUNT_ID'].widget.attrs['readonly'] = True                  # P28-24
        localQuestionAddConfirmForm.fields['RECEIVE_ACCOUNT_NAME'].widget.attrs['readonly'] = True                # P28-25 
        localQuestionAddConfirmForm.fields['RECEIVE_DATE'].widget.attrs['readonly'] = True                        # P28-26
        localQuestionAddConfirmForm.fields['RECEIVE_DATE_TIME'].widget.attrs['readonly'] = True                   # P28-27
        localQuestionAddConfirmForm.fields['RECEIVE_FLAG'].widget.attrs['readonly'] = True                        # P28-28
        localQuestionAddConfirmForm.fields['DELETE_DATE'].widget.attrs['readonly'] = True                         # P28-29
        localQuestionAddConfirmForm.fields['DELETE_DATE_TIME'].widget.attrs['readonly'] = True                    # P28-30
        localQuestionAddConfirmForm.fields['DELETE_FLAG'].widget.attrs['readonly'] = True                         # P28-31
        localQuestionAddConfirmForm.fields['RECEIVE_READ_FLAG'].widget.attrs['readonly'] = True                   # P28-32
        ##########################################
        # レスポンスセット処理（Ｐ２８Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        # ヒント：登録済フラグがTrueの場合、テンプレートでは、登録結果を表示する処理を想定する。
        # ヒント：登録済フラグがFalseの場合、テンプレートでは、これから登録するデータを表示し、利用者が編集を加えると想定する。
        # ヒント：必須項目の未入力等に対応するため、１画面で新規登録用の画面と、結果表示用の画面の両方が処理できたほうが効率が良いため。
        # ヒント：また、テンプレートファイルの記述は、それほど複雑にはならないためこのように実装する。
        ##########################################
        print_log('[INFO] P28.QuestionAddConfirmView関数 P28A60', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            # ヒント：toAccountId、questionId等、クエリストリングをそのままセットしているため、セキュリティについてチェックすること。
            # ヒント：カンマをurlquoteすると「%2C」となり、現行のビュー関数では、URLがマッチしないため、上記とする。
            response = {
                'accountType': 1,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': True,                             # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'questionAddConfirmForm': localQuestionAddConfirmForm, # 問合せ回答データ登録確認画面用フォーム
                'questionLength': 1,                       # 問合せ回答データの件数
                'questionId': questionId,                  # 問合せ回答ＩＤのリスト（複数件を想定する。カンマ付き）
                'fromAccountId': fromAccountId,            # 送信者アカウントＩＤ（１件を想定する。カンマなし。）
                'toAccountId': toAccountId,                # 受信者アカウントＩＤのリスト（複数件を想定する。カンマ付き）
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            # ヒント：toAccountId、questionId等、クエリストリングをそのままセットしているため、セキュリティについてチェックすること。
            # ヒント：カンマをurlquoteすると「%2C」となり、現行のビュー関数では、URLがマッチしないため、上記とする。
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'questionAddConfirmForm': localQuestionAddConfirmForm, # 問合せ回答データ登録確認画面用フォーム
                'questionLength': 1,                       # 問合せ回答データの件数
                'questionId': questionId,                  # 問合せ回答ＩＤのリスト（複数件を想定する。カンマ付き）
                'fromAccountId': fromAccountId,            # 送信者アカウントＩＤ（１件を想定する。カンマなし。）
                'toAccountId': toAccountId,                # 受信者アカウントＩＤのリスト（複数件を想定する。カンマ付き）
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            # ヒント：toAccountId、questionId等、クエリストリングをそのままセットしているため、セキュリティについてチェックすること。
            # ヒント：カンマをurlquoteすると「%2C」となり、現行のビュー関数では、URLがマッチしないため、上記とする。
            response = {
                'accountType': 3,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': True,                             # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'questionAddConfirmForm': localQuestionAddConfirmForm, # 問合せ回答データ登録確認画面用フォーム
                'questionLength': 1,                       # 問合せ回答データの件数
                'questionId': questionId,                  # 問合せ回答ＩＤのリスト（複数件を想定する。カンマ付き）
                'fromAccountId': fromAccountId,            # 送信者アカウントＩＤ（１件を想定する。カンマなし。）
                'toAccountId': toAccountId,                # 受信者アカウントＩＤのリスト（複数件を想定する。カンマ付き）
            }
        else:    
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P28.QuestionAddConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P28.QuestionAddConfirmView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ２８Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P28.QuestionAddConfirmView関数 P28A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P28QuestionAddConfirmTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者がアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P28QuestionAddConfirmTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            return render(request, 'P28QuestionAddConfirmTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P28.QuestionAddConfirmView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 例外処理（Ｐ２８Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P28.QuestionAddConfirmView関数 P28A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P28.QuestionAddConfirmView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P28.QuestionAddConfirmView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ２８Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P28.QuestionAddConfirmView関数 P28A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
#####################################################################################
# 関数名：P28.QuestionAddConfirmDoView（Ｐ２８Ｂ）
# 関数概要：都道府県用問合せ登録確認ページでセットされた値をＤＢに本登録する。（都道府県）
# 関数概要：本省用回答登録確認ページをでセットされた値をＤＢに本登録する。（本省）
# 関数概要：運用業者用回答登録確認ページでセットされた値をＤＢに本登録する。（運用業者）
#
# 引数[1]：request
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから運用業者名、確認部署名、確認者名を取得するために使用する。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）
# 引数[5]：kenQuestionId：都道府県用問合せＩＤ※ＤＢから都道府県用問合せを取得し、本登録するために使用する。（都道府県）
# 引数[5]：honOpeQuestionId：本省用問合せＩＤ※ＤＢから本省用回答を取得し、本登録するために使用する。（本省）
# 引数[5]：honOpeQuestionId：運用業者用用問合せＩＤ※ＤＢから運用業者用回答を取得し、本登録するために使用する。（運用業者）
#
# 戻り値[1]：response
# 
# FORM：QuestionAddConfirmForm：都道府県用問合せ登録確認ページ（都道府県）
# FORM：QuestionAddConfirmForm：本省用回答登録確認ページ（本省）
# FORM：QuestionAddConfirmForm：運用業者用回答登録確認ページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：QuestionModel：問合せまたは回答モデル（Ｕ）
#
# ヒント：都道府県からの呼び出しの場合、kenQuestionIdはNot Null、honOpeQuestionIdはNull
# ヒント：本省からの呼び出しの場合、kenQuestionIdはNot Null、honOpeQuestionIdはNot Null
# ヒント：運用業者からの呼び出しの場合、kenQuestionIdはNot Null、honOpeQuestionIdはNot Null
# ヒント：QuestionAddConfirmDoView関数でＤＢに本登録済で、そのときにquestionIdを引き継いでいると想定する。
# ヒント：複数受信アカウントＩＤへの送信を利用者が１回で行うことが出来るようにするため、以下を行う。
# ヒント：問合せ回答ＩＤのリストを確認画面のURLへのクエリストリングにセットする。
# ヒント：受信者アカウントＩＤのリストを確認画面のURLへのクエリストリングにセットする。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/login/')
def QuestionAddConfirmDoView(request, accountType, accountId, operationYear, questionId, fromAccountId, toAccountId):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmDoView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２８Ｂ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P28.QuestionAddConfirmDoView関数 P28B10', 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmDoView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmDoView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmDoView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmDoView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmDoView.questionId = {}'.format(questionId), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmDoView.fromAccountId = {}'.format(fromAccountId), 'INFO')
        print_log('[INFO] P28.QuestionAddConfirmDoView.toAccountId = {}'.format(toAccountId), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２８Ｂ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # （６）問合せ回答ＩＤをチェックする。　例　1
        # （７）問合せ回答ＩＤを「,」で分離し、局所変数の問合せ回答ＩＤリストにセットする。
        # （８）送信者のアカウントＩＤをチェックする。　例　1
        # （９）受信者のアカウントＩＤをチェックする。　例　1
        # （１０）受信者のアカウントＩＤを「,」で分離し、局所変数の受信者アカウントＩＤリストにセットする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        if accountId == str(request.user.username):
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P283B20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'POST':
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B20-5', 'WARN')
                return render(request, 'error.html')
        # （６）問合せ回答ＩＤをチェックする。　例　1
        # ヒント：複数受信アカウントＩＤに対応するため、カンマが含まれると想定するが、このPOSTでは、本物のＩＤがセットされると想定する。
        if questionId is None:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B20-6', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （７）問合せ回答ＩＤを「,」で分離し、局所変数の問合せ回答ＩＤリストにセットする。
        localQuestionIdList = questionId.split(",")
        if len(list(localQuestionIdList)) >= 1:
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B20-7', 'WARN')
            return render(request, 'error.html')
        # （８）送信者のアカウントＩＤをチェックする。　例　1
        if fromAccountId is None:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B20-8', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （９）受信者のアカウントＩＤをチェックする。　例　1　ヒント：カンマで複数指定可能とする。
        if toAccountId is None:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B20-9', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （１０）受信者のアカウントＩＤを「,」で分離し、局所変数の受信者アカウントＩＤリストにセットする。
        localToAccountIdList = toAccountId.split(",")
        if len(list(localToAccountIdList)) >= 1:
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B20-10', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ２８Ｂ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P28.QuestionAddConfirmDoView関数 P28B30', 'INFO')
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
                    OPERATION_YEAR=%s LIMIT 1
                """, 
                [accountId, operationYear, ])[0]
        except:
            localAccountModel = None    
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数 P28B30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P28.QuestionAddConfirmDoView関数 P28B30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # フォームセット処理（Ｐ２８Ｂ４０）
        # （１）局所変数のフォームを初期化する。
        # （２）画面からポストされた情報を取得する。
        ##########################################
        print_log('[INFO] P28.QuestionAddConfirmDoView関数 P28B40', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localForm = None
        localAddConfirmForm = QuestionAddConfirmForm()
        # （２）画面からポストされた情報を取得する。
        try:
            localForm = QuestionAddConfirmForm(request.POST, request.FILES)
            if localForm.is_valid():
                localAddConfirmForm.QUESTION_ID = localForm.cleaned_data['QUESTION_ID']                           # P28-1
                localAddConfirmForm.OPERATION_YEAR = localForm.cleaned_data['OPERATION_YEAR']                     # P28-3
                localAddConfirmForm.FLOOD_YEAR = localForm.cleaned_data['FLOOD_YEAR']                             # P28-4
                localAddConfirmForm.SEND_ORG_CODE = localForm.cleaned_data['SEND_ORG_CODE']                       # P28-5
                localAddConfirmForm.SEND_ORG_NAME = localForm.cleaned_data['SEND_ORG_NAME']                       # P28-6
                localAddConfirmForm.SEND_DEPT_CODE = localForm.cleaned_data['SEND_DEPT_CODE']                     # P28-7
                localAddConfirmForm.SEND_DEPT_NAME = localForm.cleaned_data['SEND_DEPT_NAME']                     # P28-8
                localAddConfirmForm.SEND_ACCOUNT_ID = localForm.cleaned_data['SEND_ACCOUNT_ID']                   # P28-9
                localAddConfirmForm.SEND_ACCOUNT_NAME = localForm.cleaned_data['SEND_ACCOUNT_NAME']               # P28-10
                localAddConfirmForm.SEND_DATE = localForm.cleaned_data['SEND_DATE']                               # P28-11
                localAddConfirmForm.SEND_DATE_TIME = localForm.cleaned_data['SEND_DATE_TIME']                     # P28-12
                localAddConfirmForm.SEND_FLAG = localForm.cleaned_data['SEND_FLAG']                               # P28-13
                localAddConfirmForm.SUBJECT = localForm.cleaned_data['SUBJECT']                                   # P28-14
                localAddConfirmForm.BODY = localForm.cleaned_data['BODY']                                         # P28-15
                # ヒント：./01hokkai/aaa.lzhにファイルを格納する。
                # ヒント：事前に全アカウントＩＤについて、ディレクトリを作成しておくことを想定する。
                # ヒント：ＤＢに登録するデータにも上記ディレクトリ、ファイル名をセットすることを想定する。
                localAddConfirmForm.FILE_ID = localForm.cleaned_data['FILE_ID']                                   # P28-17
                localAddConfirmForm.FILE_NAME = localForm.cleaned_data['FILE_NAME']                               # P28-18
                localAddConfirmForm.FILE_PATH = localForm.cleaned_data['FILE_PATH']                               # P28-19
                localAddConfirmForm.RECEIVE_ORG_CODE = localForm.cleaned_data['RECEIVE_ORG_CODE']                 # P28-20
                localAddConfirmForm.RECEIVE_ORG_NAME = localForm.cleaned_data['RECEIVE_ORG_NAME']                 # P28-21
                localAddConfirmForm.RECEIVE_DEPT_CODE = localForm.cleaned_data['RECEIVE_DEPT_CODE']               # P28-22
                localAddConfirmForm.RECEIVE_DEPT_NAME = localForm.cleaned_data['RECEIVE_DEPT_NAME']               # P28-23
                localAddConfirmForm.RECEIVE_ACCOUNT_ID = localForm.cleaned_data['RECEIVE_ACCOUNT_ID']             # P28-24
                localAddConfirmForm.RECEIVE_ACCOUNT_NAME = localForm.cleaned_data['RECEIVE_ACCOUNT_NAME']         # P28-25
                localAddConfirmForm.RECEIVE_DATE = localForm.cleaned_data['RECEIVE_DATE']                         # P28-26
                localAddConfirmForm.RECEIVE_DATE_TIME = localForm.cleaned_data['RECEIVE_DATE_TIME']               # P28-27
                localAddConfirmForm.RECEIVE_FLAG = localForm.cleaned_data['RECEIVE_FLAG']                         # P28-28
                localAddConfirmForm.DELETE_DATE = localForm.cleaned_data['DELETE_DATE']                           # P28-29
                localAddConfirmForm.DELETE_DATE_TIME = localForm.cleaned_data['DELETE_DATE_TIME']                 # P28-30
                localAddConfirmForm.DELETE_FLAG = localForm.cleaned_data['DELETE_FLAG']                           # P28-31
                localAddConfirmForm.RECEIVE_READ_FLAG = localForm.cleaned_data['RECEIVE_READ_FLAG']               # P28-32
            else:
                pass
        except:
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数 P28B40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ファイル受信処理（Ｐ２８Ｂ５０）
        # （１）画面からポストされたファイルを受信し、サーバに保存する。
        ##########################################
        print_log('[INFO] P28.QuestionAddConfirmDoView関数 P28B50', 'INFO')
        ##########################################
        # ＤＢアクセス処理、アップロードデータ登録処理（＝登録フラグを５にセット（Ｐ２８Ｂ６０）
        # （１）問合せ回答データの局所変数に初期値をセットする。
        ##########################################
        print_log('[INFO] P28.QuestionAddConfirmDoView関数 P28B60', 'INFO')
        # （１）問合せ回答データの局所変数に初期値をセットする。
        localAddDate = datetime.now().strftime("%Y/%m/%d")
        localAddDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        ##########################################
        # ＤＢアクセス処理、アップロードデータ登録処理（＝登録フラグを５にセット（Ｐ２８Ｂ６１）
        # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
        # （２）受信者アカウントＩＤの件数分ループする。
        # （３）ＳＱＬ文を実行する。
        # （４）トランザクション管理でコミットする。
        # （５）ＤＢ接続を切断＝カーソルを閉じる。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：運用業者の場合は、ここにはこないと想定する。return済。
        # ヒント：rawはUPDATE文では使えないため、カーソルを利用する。
        ##########################################
        print_log('[INFO] P28.QuestionAddConfirmDoView関数 P28B61', 'INFO')
        try:
            # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
            localCursor = connection.cursor()
            # （２）受信者アカウントＩＤの件数分ループする。
            # ヒント：最後に「,」が入っていないため、lenの結果は、受信者アカウントＩＤの件数＋０件となっている。
            # ヒント：そのため、>= 2とする。
            if len(list(localToAccountIdList)) >= 1:
                for i in range(0, len(list(localToAccountIdList))):
                    # （３）ＳＱＬ文を実行する。
                    # （４）トランザクション管理でコミットする。
                    # ヒント：file_upload_questionテーブルにレコードを追加する。（登録フラグの状態＝仮登録済＝1）
                    # ヒント：仮登録済とは、レコードは登録済、ＩＤも付与済、登録フラグが仮登録済＝1の状態をいう。
                    # ヒント：ＩＤにＤＢから取得した最大値＋１をセットする。
                    # ヒント：SELECT MAX(KEN_QUESTION_ID + 0)としているが、KEN_QUESTION_IDは文字列のため、0を足すことで、
                    # ヒント：暗黙の型変換がＤＢ内で実行され、最大値を取得可能となる。
                    # ヒント：+0しないと、暗黙の型変換が実行されず、エラーとなるので注意すること。                
                    try:
                        localCursor.execute("""
                            UPDATE 
                                FILE_UPLOAD_QUESTION 
                            SET 
                                SEND_DATE = %s,
                                SEND_DATE_TIME = %s,
                                SEND_FLAG = '5'
                            WHERE 
                                QUESTION_ID=%s AND 
                                OPERATION_YEAR=%s 
                            """, 
                            [localAddDate, localAddDateTime, localQuestionIdList[i], operationYear, ])
                        transaction.commit()
                    except:
                        transaction.rollback()
                        print_log('[ERROR] P28.QuestionAddConfirmDoView関数 P28B61', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P28.QuestionAddConfirmDoView関数で警告が発生しました。', 'ERROR')
                    # ヒント：file_upload_questionfileテーブルのレコードを更新する。（登録フラグの状態＝本登録済＝５）
                    # ヒント：本登録済とは、レコードは登録済、ＩＤも発行済、登録フラグが本登録＝５の状態をいう。
                    try:
                        localCursor.execute("""
                            UPDATE 
                                FILE_UPLOAD_QUESTIONFILE
                            SET
                                SEND_DATE = %s,
                                SEND_DATE_TIME = %s,
                                SEND_FLAG = '5'
                            WHERE 
                                QUESTION_ID=%s AND 
                                OPERATION_YEAR=%s    
                            """,
                            [localAddDate, localAddDateTime, localQuestionIdList[i], operationYear, ])
                        transaction.commit()
                    except:
                        transaction.rollback()
                        print_log('[ERROR] P28.QuestionAddConfirmDoView関数 P28B61', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P28.QuestionAddConfirmDoView関数で警告が発生しました。', 'ERROR')
            else:
                pass            
        except:
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数 P28B61', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html', 'ERROR')
        finally:
            # （４）ＤＢ接続を切断＝カーソルを閉じる。
            localCursor.close()
        ##########################################
        # レスポンスセット処理（Ｐ２８Ｂ７０）
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
        print_log('[INFO] P28.QuestionAddConfirmDoView関数 P28B70', 'INFO')
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
                'message': '都道府県が送信したデータをデータベースに登録しました。', # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'AddConfirmForm': localAddConfirmForm,     # 問合せ回答データ登録確認画面用のフォーム
                'questionLength': 1,                       # 問合せ回答データの件数
                'questionId': questionId,                  # 問合せ回答ＩＤのリスト（複数件を想定する。カンマ付き）
                'fromAccountId': fromAccountId,            # 送信者アカウントＩＤ（１件を想定する。カンマなし。）
                'toAccountId': toAccountId,                # 受信者アカウントＩＤのリスト（複数件を想定する。カンマ付き）
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'wasAdded': True,                          # 登録済フラグをTrueにセットする。テンプレートで画面表示処理を分岐するために使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': '本省が送信したデータをデータベースに登録しました。', # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'AddConfirmForm': localAddConfirmForm,     # 問合せ回答データ登録確認画面用のフォーム  
                'questionLength': 1,                       # 問合せ回答データの件数
                'questionId': questionId,                  # 問合せ回答ＩＤのリスト（複数件を想定する。カンマ付き）
                'fromAccountId': fromAccountId,            # 送信者アカウントＩＤ（１件を想定する。カンマなし。）
                'toAccountId': toAccountId,                # 受信者アカウントＩＤのリスト（複数件を想定する。カンマ付き）
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            response = {
                'accountType': 3,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': True,                             # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'wasAdded': True,                          # 登録済フラグをTrueにセットする。テンプレートで画面表示処理を分岐するために使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': '運用業者が送信したデータをデータベースに登録しました。', # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'AddConfirmForm': localAddConfirmForm,     # 問合せ回答データ登録確認画面用のフォーム
                'questionLength': 1,                       # 問合せ回答データの件数
                'questionId': questionId,                  # 問合せ回答ＩＤのリスト（複数件を想定する。カンマ付き）
                'fromAccountId': fromAccountId,            # 送信者アカウントＩＤ（１件を想定する。カンマなし。）
                'toAccountId': toAccountId,                # 受信者アカウントＩＤのリスト（複数件を想定する。カンマ付き）
            }
        else:    
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P28.QuestionAddConfirmDoView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ２８Ｂ８０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P28.QuestionAddConfirmDoView関数 P28B80', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P28QuestionAddConfirmTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P28QuestionAddConfirmTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            return render(request, 'P28QuestionAddConfirmTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P28.QuestionAddConfirmDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 戻り値セット処理（Ｐ２８Ｂ９０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P28.QuestionAddConfirmDoView関数 P28B90', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P28.QuestionAddConfirmDoView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P28.QuestionAddConfirmDoView関数が異常終了しました。', 'ERROR')
        ##########################################
        # 戻り値セット処理（Ｐ２８Ｂ１００）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P28.QuestionAddConfirmDoView関数 P28B100', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
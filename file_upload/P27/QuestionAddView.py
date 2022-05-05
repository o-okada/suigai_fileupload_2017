#####################################################################################
# QuestionAddViewビューモジュール
# ファイル名：P27.QuestionAddView.py（Ｐ２７）
# ユースケース：都道府県は、本省または運用業者に問合せする。
# ユースケース：本省は、都道府県宛に回答する。
# ユースケース：運用業者は、都道府県宛に回答する。
# ヒント：調査結果と確認結果は同じテーブル、モデルを使用する。
# ヒント：種別・区分フラグで調査結果と確認結果を識別する。
# ヒント：accountTypeはログインした人の種別・区分
# TO-DO：引数チェックに引っかかった場合、ビュー関数でエラーが発生した場合、テンプレートでレンダリングでエラーが発生した場合に応じ、
# TO-DO：異なるエラー画面を表示することがＵＩ上好ましいと思われる。リリース後の課題として、TO-DO（保留）とする。
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
# HpptResponse
# get_object_or_404
# render
# redirect
# method_decorator
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
#####################################################################################
from file_upload.CommonFunction import print_log           # ログ出力モジュール
from file_upload.forms import QuestionAddForm              # 問合せ回答データ登録画面用フォーム
from file_upload.models import AccountModel                # アカウントデータ・モデル
from file_upload.models import QuestionFileModel           # 問合せ回答ファイルデータ・モデル
from file_upload.models import QuestionModel               # 問合せ回答データ・モデル
#####################################################################################
# 処理名：大域変数定義（０００）
# 処理概要：大域変数を定義する。
#####################################################################################
def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
#####################################################################################
# 関数名：P27.QuestionAddView（Ｐ２７Ａ）
# 関数概要：都道府県問合せ登録ページをブラウザに戻す。（都道府県）
# 関数概要：本省用回答登録ページをブラウザに戻す。（本省）
# 関数概要：運用業者用回答登録ページをブラウザに戻す。（運用業者用）
#
# 引数[1]：request
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから運用業者名、運用業者部署名、運用業者名を取得するために使用する。（本省）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）
# 引数[5]：kenQuestionId：問合せまたは回答：問合せＩＤ（都道府県）
# 引数[6]：honOpeQuestionId：問合せまたは回答：回答ＩＤ（本省）
# 引数[7]：honOpeQuestionId：問合せまたは回答：回答ＩＤ（運用業者）
#
# 戻り値[1]：response
#
# FORM：QuestionAddForm：都道府県用問合せページ（都道府県）
# FORM：QuestionAddForm：本省用回答ページ（本省）
# FORM：QuestionAddForm：運用業者用回答ページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：QuestionModel：問合せまたは回答モデル（Ｒ）
# ヒント：accountTypeが都道府県の場合、新規に問合せデータを生成し、都道府県名等をセットし、ページに表示する。
# ヒント：accountTypeが本省の場合、引数のquestionIdをキーに、ＤＢから問合せまたは回答データを取得し、ページに表示する。
# ヒント：accountTypeが運用業者の場合、引数のquestionIdをキーに、ＤＢから問合せまたは回答データを取得し、ページに表示する。
# ヒント：都道府県からの呼び出しの場合、kenQuestionIdはNull、honOpeQuestionIdはNull
# ヒント：本省からの呼び出しの場合、kenQuestionIdはNot Null、honOpeQuestionIdはNull
# ヒント：運用業者からの呼び出しの場合、kenQuestionIdはNot Null、honOpeQuestionIdはNull
# ヒント：理由
# ヒント：都道府県からの呼び出しの場合、新規に問合せを生成するので、また、questionIDはテーブルのユニークキーのため、サーバ側でセットする。
# ヒント：都道府県からの問合せに対して本省が回答するため、本省からの呼び出しの場合、どの問合せに対する回答かを示すkenQuestionIdがセットされていると想定する。
# ヒント：都道府県からの問合せに対して運用業者が回答するため、運用業者からの呼び出しの場合、どの問合せに対する回答かを示すkenQuestionIdがセットされていると想定する。
# ヒント：問合せと回答は同じテーブルを用いる。
# ヒント：問合せと回答はペアになるが、レコードは別々のレコードとする。
# ヒント：１件の問合せに対して、回答は１件とする。後で拡張する可能性あり。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/login/')
def QuestionAddView(request, accountType, accountId, operationYear, questionId, fromAccountId, toAccountId):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P27.QuestionAddView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２７Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P27.QuestionAddView関数 P27A10', 'INFO')
        print_log('[INFO] P27.QuestionAddView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P27.QuestionAddView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P27.QuestionAddView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P27.QuestionAddView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P27.QuestionAddView.questionId = {}'.format(questionId), 'INFO')
        print_log('[INFO] P27.QuestionAddView.fromAccountId = {}'.format(fromAccountId), 'INFO')
        print_log('[INFO] P27.QuestionAddView.toAccountId = {}'.format(toAccountId), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２７Ａ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # （６）問合せ回答ＩＤをチェックする。　例　1
        # （７）送信者のアカウントＩＤをチェックする。　例　1
        # （８）受信者のアカウントＩＤをチェックする。　例　1
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
            print_log('[WARN] P27.QuestionAddView関数 P27A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P27.QuestionAddView関数 P27A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P27.QuestionAddView関数 P27A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P27.QuestionAddView関数 P27A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P27.QuestionAddView関数 P27A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P27.QuestionAddView関数 P27A20-5', 'WARN')
                return render(request, 'error.html')
        # （６）問合せ回答ＩＤをチェックする。　例　1
        if questionId is None:
            print_log('[WARN] P27.QuestionAddView関数 P27A20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(questionId) == True:
                pass
            else:
                print_log('[WARN] P27.QuestionAddView関数 P27A20-6', 'WARN')
                return render(request, 'error.html')
        # （７）送信者のアカウントＩＤをチェックする。　例　1
        if fromAccountId is None:
            print_log('[WARN] P27.QuestionAddView関数 P27A20-8', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （８）受信者のアカウントＩＤをチェックする。　例　1　ヒント：カンマで複数指定可能とする。
        if toAccountId is None:
            print_log('[WARN] P27.QuestionAddView関数 P27A20-9', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        ##########################################
        # ＤＢアクセス処理（Ｐ２７Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P27.QuestionAddView関数 P27A30', 'INFO')
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
            print_log('[ERROR] P27.QuestionAddView関数 P27A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P27.QuestionAddView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。         
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P27.QuestionAddView関数 P27A30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P27.QuestionAddView関数 P27A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、問合せ回答データ取得処理（Ｐ２７Ａ４０）
        # （１）問合せデータ、回答データ、問合せファイルデータ、回答ファイルデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、問合せデータ、回答データ、問合せファイルデータ、回答ファイルデータを取得する。
        # （３）ＤＢにアクセスし、問合せファイルデータ、回答ファイルデータを取得する。
        # （４）ＤＢにアクセスし、アカウントデータを取得する。
        # ヒント：都道府県の場合は、問合せデータを生成する。
        # ヒント：本省の場合は、既に問合せデータが登録済と想定し、画面表示用に、ＤＢからこのデータを取得する。
        # ヒント：運用業者の場合は、既に問合せデータが登録済と想定し、画面表示用に、ＤＢからこのデータを取得する。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：KEN_UPLOAD_ID、HON_UPLOAD_IDが親子関係を示すものとしてＤＢに格納されているため、
        # ヒント：KEN_HON_OPE_FLAGは使用しない。
        ##########################################
        print_log('[INFO] P27.QuestionAddView関数 P27A40', 'INFO')
        # （１）問合せデータ、回答データ、問合せファイルデータ、回答ファイルデータを格納する局所変数を初期化する。
        localQuestionModel = None
        localQuestionFileModel = None
        # （２）ＤＢにアクセスし、問合せデータ、回答データ、問合せファイルデータ、回答ファイルデータを取得する。
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
                    OPERATION_YEAR=%s 
                LIMIT 1
                """, 
                [ questionId, 
                  operationYear, 
                ])[0]
        except:
            localQuestionModel = None
            print_log('[ERROR] P27.QuestionAddView関数 P27A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P27.QuestionAddView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddView関数を警告終了しました。', 'ERROR')
        # （３）ＤＢにアクセスし、問合せファイルデータ、回答ファイルデータを取得する。
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
                    OPERATION_YEAR=%s 
                LIMIT 1
                """, 
                [ questionId, 
                  operationYear, 
                ])[0]
        except:
            localQuestionFileModel == None        
            print_log('[ERROR] P27.QuestionAddView関数 P27A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P27.QuestionAddView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddView関数を警告終了しました。', 'ERROR')
        # （４）ＤＢにアクセスし、アカウントデータを取得する。
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
                [ operationYear, 
                ])
        except:
            localAccountArray == None        
            print_log('[ERROR] P27.QuestionAddView関数 P27A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P27.QuestionAddView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddView関数を警告終了しました。', 'ERROR')
        ##########################################
        # フォームセット処理（Ｐ２７Ａ５０）
        # （１）局所変数のフォームを初期化する。
        # ヒント：ブラウザとのデータのやりとり、特にブラウザからPOSTデータがある場合、フォームを使用する。
        # ヒント：モデルはブラウザで参照用、かつタグをコーディングする場合等に使用する。
        # ヒント：フォームはブラウザで編集用、POSTでサーバにリクエストされる項目、かつタグを自動生成する場合等に使用する。
        ##########################################
        print_log('[INFO] P27.QuestionAddView関数 P27A50', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localAddDate = datetime.now().strftime("%Y/%m/%d")
        localAddDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        localQuestionAddForm = QuestionAddForm()
        ##########################################
        # フォームセット処理（Ｐ２７Ａ５１）
        # （１）局所変数のフォームに初期値をセットする。
        ##########################################
        # （１）局所変数のフォームに初期値をセットする。
        localQuestionAddForm.initial['QUESTION_ID'] = "0"                                          # P27-1
        localQuestionAddForm.initial['OPERATION_YEAR'] = urlquote(operationYear)                   # P27-3
        localQuestionAddForm.initial['FLOOD_YEAR'] = urlquote(operationYear)                       # P27-4

        if localAccountModel != None:
            localQuestionAddForm.initial['SEND_ORG_CODE'] = localAccountModel.ORG_CODE             # P27-5
            localQuestionAddForm.initial['SEND_ORG_NAME'] = localAccountModel.ORG_NAME             # P27-6 
            localQuestionAddForm.initial['SEND_DEPT_CODE'] = localAccountModel.DEPT_CODE           # P27-7
            localQuestionAddForm.initial['SEND_DEPT_NAME'] = localAccountModel.DEPT_NAME           # P27-8
            localQuestionAddForm.initial['SEND_ACCOUNT_ID'] = localAccountModel.ACCOUNT_ID         # P27-9
            localQuestionAddForm.initial['SEND_ACCOUNT_NAME'] = localAccountModel.ACCOUNT_NAME     # P27-10
        else:
            localQuestionAddForm.initial['SEND_ORG_CODE'] = "0"                                    # P27-5
            localQuestionAddForm.initial['SEND_ORG_NAME'] = "0"                                    # P27-6
            localQuestionAddForm.initial['SEND_DEPT_CODE'] = "0"                                   # P27-7
            localQuestionAddForm.initial['SEND_DEPT_NAME'] = "0"                                   # P27-8
            localQuestionAddForm.initial['SEND_ACCOUNT_ID'] = "0"                                  # P27-9
            localQuestionAddForm.initial['SEND_ACCOUNT_NAME'] = "0"                                # P27-10

        localQuestionAddForm.initial['SEND_DATE'] = localAddDate                                   # P27-11
        localQuestionAddForm.initial['SEND_DATE_TIME'] = localAddDateTime                          # P27-12
        localQuestionAddForm.initial['SEND_FLAG'] = "0"                                            # P27-13
        localQuestionAddForm.initial['SUBJECT'] = "0"                                              # P27-14
        localQuestionAddForm.initial['BODY'] = "0"                                                 # P27-15 
        localQuestionAddForm.initial['FILE_ID'] = "0"                                              # P27-17
        localQuestionAddForm.initial['FILE_NAME'] = "0"                                            # P27-18
        localQuestionAddForm.initial['FILE_PATH'] = "0"                                            # P27-19
        localQuestionAddForm.initial['RECEIVE_ORG_CODE'] = "0"                                     # P27-20
        localQuestionAddForm.initial['RECEIVE_ORG_NAME'] = "0"                                     # P27-21
        localQuestionAddForm.initial['RECEIVE_DEPT_CODE'] = "0"                                    # P27-22 
        localQuestionAddForm.initial['RECEIVE_DEPT_NAME'] = "0"                                    # P27-23
        localQuestionAddForm.initial['RECEIVE_ACCOUNT_ID'] = "0"                                   # P27-24
        localQuestionAddForm.initial['RECEIVE_ACCOUNT_NAME'] = "0"                                 # P27-25
        localQuestionAddForm.initial['RECEIVE_DATE'] = "0"                                         # P27-26
        localQuestionAddForm.initial['RECEIVE_DATE_TIME'] = "0"                                    # P27-27
        localQuestionAddForm.initial['RECEIVE_FLAG'] = "0"                                         # P27-28
        localQuestionAddForm.initial['DELETE_DATE'] = "0"                                          # P27-29
        localQuestionAddForm.initial['DELETE_DATE_TIME'] = "0"                                     # P27-30
        localQuestionAddForm.initial['DELETE_FLAG'] = "0"                                          # P27-31
        localQuestionAddForm.initial['RECEIVE_READ_FLAG'] = "0"                                    # P27-32
        ##########################################            
        # フォームセット処理（Ｐ２７Ａ５４）
        # （１）フォームのウィジェットの属性に値をセットする。
        # ヒント：利用者が編集できない項目は、disabled、readonlyのいずれかとする。
        # ヒント：フォームを使用した場合、ブラウザでタグが自動生成されるため、ブラウザのstyle、cssでdisable、readonlyをセットしにくい。
        # ヒント：そのため。ビュー関数でdisable、readonly等をセットする。
        # ヒント：フォームのフィールドは、非表示の項目もセットすることを推奨する。
        # ヒント：ステートレスなウェブアプリにおいて、ブラウザに送ったデータをPOST時にサーバ側のビュー関数で参照可能とするため。
        ##########################################            
        # （１）フォームのウィジェットの属性に値をセットする。
        localQuestionAddForm.fields['QUESTION_ID'].widget.attrs['readonly'] = True                 # P27-1
        localQuestionAddForm.fields['OPERATION_YEAR'].widget.attrs['readonly'] = True              # P27-3
        localQuestionAddForm.fields['FLOOD_YEAR'].widget.attrs['readonly'] = True                  # P27-4
        localQuestionAddForm.fields['SEND_ORG_CODE'].widget.attrs['readonly'] = True               # P27-5
        localQuestionAddForm.fields['SEND_ORG_NAME'].widget.attrs['readonly'] = True               # P27-6
        localQuestionAddForm.fields['SEND_DEPT_CODE'].widget.attrs['readonly'] = True              # P27-7
        localQuestionAddForm.fields['SEND_DEPT_NAME'].widget.attrs['readonly'] = True              # P27-8
        localQuestionAddForm.fields['SEND_ACCOUNT_ID'].widget.attrs['readonly'] = True             # P27-9
        localQuestionAddForm.fields['SEND_ACCOUNT_NAME'].widget.attrs['readonly'] = True           # P27-10
        localQuestionAddForm.fields['SEND_DATE'].widget.attrs['readonly'] = True                   # P27-11
        localQuestionAddForm.fields['SEND_DATE_TIME'].widget.attrs['readonly'] = True              # P27-12
        localQuestionAddForm.fields['SEND_FLAG'].widget.attrs['readonly'] = True                   # P27-13
        localQuestionAddForm.fields['SUBJECT'].widget.attrs['readonly'] = False                    # P27-14
        localQuestionAddForm.fields['BODY'].widget.attrs['readonly'] = False                       # P27-15
        localQuestionAddForm.fields['FILE_ID'].widget.attrs['readonly'] = True                     # P27-17
        localQuestionAddForm.fields['FILE_NAME'].widget.attrs['readonly'] = True                   # P27-18
        localQuestionAddForm.fields['FILE_PATH'].widget.attrs['readonly'] = True                   # P27-19   
        localQuestionAddForm.fields['RECEIVE_ORG_CODE'].widget.attrs['readonly'] = True            # P27-20
        localQuestionAddForm.fields['RECEIVE_ORG_NAME'].widget.attrs['readonly'] = True            # P27-21
        localQuestionAddForm.fields['RECEIVE_DEPT_CODE'].widget.attrs['readonly'] = True           # P27-22
        localQuestionAddForm.fields['RECEIVE_DEPT_NAME'].widget.attrs['readonly'] = True           # P27-23
        localQuestionAddForm.fields['RECEIVE_ACCOUNT_ID'].widget.attrs['readonly'] = True          # P27-24
        localQuestionAddForm.fields['RECEIVE_ACCOUNT_NAME'].widget.attrs['readonly'] = True        # P27-25
        localQuestionAddForm.fields['RECEIVE_DATE'].widget.attrs['readonly'] = True                # P27-26
        localQuestionAddForm.fields['RECEIVE_DATE_TIME'].widget.attrs['readonly'] = True           # P27-27
        localQuestionAddForm.fields['RECEIVE_FLAG'].widget.attrs['readonly'] = True                # P27-28
        localQuestionAddForm.fields['DELETE_DATE'].widget.attrs['readonly'] = True                 # P27-29
        localQuestionAddForm.fields['DELETE_DATE_TIME'].widget.attrs['readonly'] = True            # P27-30
        localQuestionAddForm.fields['DELETE_FLAG'].widget.attrs['readonly'] = True                 # P27-31
        localQuestionAddForm.fields['RECEIVE_READ_FLAG'].widget.attrs['readonly'] = True           # P27-32
        ##########################################
        # レスポンスセット処理（Ｐ２７Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        # ヒント：登録済フラグがTrueの場合、テンプレートでは、登録結果を表示する処理を想定する。
        # ヒント：登録済フラグがFalseの場合、テンプレートでは、これから登録するデータを表示し、利用者が編集を加えると想定する。
        # ヒント：必須項目の未入力等に対応するため、１画面で新規登録用の画面と、結果表示用の画面の両方が処理できたほうが効率が良いため。
        # ヒント：また、テンプレートファイルの記述は、それほど複雑にはならないためこのように実装する。
        ##########################################
        print_log('[INFO] P27.QuestionAddView関数 P27A60', 'INFO')
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝都道府県の場合、、、
            response = {
                'accountType': 1,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。 
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': True,                             # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'questionAddForm': localQuestionAddForm,   # 問合せ回答データ登録画面用のフォーム
                'questionLength': 0,                       # 問合せ回答データの件数
                'accountArray': localAccountArray,         # アカウント一覧（宛先選択用）
                'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
            }
        elif accountType == 2:
            # ログインした利用者のアカウント種別・区分＝本省の場合、、、
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'questionAddForm': localQuestionAddForm,   # 問合せ回答データ登録画面用のフォーム
                'questionLength': 0,                       # 問合せ回答データの件数
                'accountArray': localAccountArray,         # アカウント一覧（宛先選択用）
                'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝運用業者の場合、、、
            response = {
                'accountType': 3,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': True,                             # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'questionAddForm': localQuestionAddForm,   # 問合せ回答データ登録画面用のフォーム
                'questionLength': 0,                       # 問合せ回答データの件数 
                'accountArray': localAccountArray,         # アカウント一覧（宛先選択用）
                'accountLength': len(list(localAccountArray)), # アカウント一覧のアカウントデータの件数
            }
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P27.QuestionAddView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P27.QuestionAddView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ２７Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P27.QuestionAddView関数 P27A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P27QuestionAddTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P27QuestionAddTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            return render(request, 'P27QuestionAddTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P27.QuestionAddView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ２７Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P27.QuestionAddView関数 P27A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P27.QuestionAddView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P27.QuestionAddView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ２７Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P27.QuestionAddView関数 P27A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
#####################################################################################
# 関数名：P27.QuestionAddDoView（Ｐ２７Ｂ）
# 関数概要：都道府県用問合せ登録ページでセットされた値をＤＢに仮登録する。（都道府県）
# 関数概要：本省用回答登録ページでセットされた値をＤＢに仮登録する。（本省）
# 関数概要：運用業者用回答登録ページでセットされた値をＤＢに仮登録する。（運用業者）
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
# 引数[5]：honQuestionId：本省用回答ＩＤ※ＤＢから本省用回答を取得し、本登録するために使用する。（本省）
# 引数[5]：opeQuestionId：運用業者用回答ＩＤ※ＤＢから運用業者用回答を取得し、本登録するために使用する。（運用業者）
#
# 戻り値[1]：response
#
# FORM：QuestionAddForm：都道府県用問合せ登録ページ（都道府県）
# FORM：QuestionAddForm：本省用回答登録ページ（本省）
# FORM：QuestionAddForm：運用業者用回答登録ページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：QuestionModel：問合せまたは回答モデル（Ｃ）
# ヒント：都道府県からの呼び出しの場合、kenQuestionIdはNull、honOpeQuestionIdはNull
# ヒント：本省からの呼び出しの場合、kenQuestionIdはNot Null、honOpeQuestionIdはNull
# ヒント：運用業者からの呼び出しの場合、kenQuestionIdはNot Null、honOpeQuestionIdはNull
# ヒント：理由
# ヒント：都道府県からの呼び出しの場合、新規に問合せを生成するので、また、questionIDはテーブルのユニークキーのため、サーバ側、つまりこの関数内でシーケンス番号等でセットする。
# ヒント：都道府県からの問合せに対して本省が回答するため、本省からの呼び出しの場合、どの問合せに対する回答かを示すkenQuestionIdがセットされていると想定する。
# ヒント：都道府県からの問合せに対して運用業者が回答するため、運用業者からの呼び出しの場合、どの問合せに対する回答かを示すkenQuestionIdがセットされていると想定する。
# ヒント：複数受信アカウントＩＤへの送信を利用者が１回で行うことが出来るようにするため、以下を行う。
# ヒント：問合せ回答ＩＤのリストを確認画面のURLへのクエリストリングにセットする。
# ヒント：受信者アカウントＩＤのリストを確認画面のURLへのクエリストリングにセットする。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/login/')
def QuestionAddDoView(request, accountType, accountId, operationYear, questionId, fromAccountId, toAccountId):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P27.QuestionAddDoView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２７Ｂ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P27.QuestionAddDoView関数 P27B10', 'INFO')
        print_log('[INFO] P27.QuestionAddDoView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P27.QuestionAddDoView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P27.QuestionAddDoView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P27.QuestionAddDoView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P27.QuestionAddDoView.questionId = {}'.format(questionId), 'INFO')
        print_log('[INFO] P27.QuestionAddDoView.fromAccountId = {}'.format(fromAccountId), 'INFO')
        print_log('[INFO] P27.QuestionAddDoView.toAccountId = {}'.format(toAccountId), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２７Ｂ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # （６）問合せ回答ＩＤをチェックする。　例　1
        # （７）送信者のアカウントＩＤをチェックする。　例　1
        # （８）受信者のアカウントＩＤをチェックする。　例　1
        # （９）受信者のアカウントＩＤを「,」で分離し、局所変数の受信者アカウントＩＤリストにセットする。
        # チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        if accountId == str(request.user.username):
            pass
        else:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'POST':
            pass
        else:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P27.QuestionAddDoView関数 P27B20-5', 'WARN')
                return render(request, 'error.html')
        # （６）問合せ回答ＩＤをチェックする。　例　1
        # ヒント：複数受信アカウントＩＤに対応するため、カンマが含まれると想定するが、このPOSTでは、ダミーの「0」がセットされると想定する。
        if questionId is None:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(questionId) == True:
                pass
            else:
                print_log('[WARN] P27.QuestionAddDoView関数 P27B20-6', 'WARN')
                return render(request, 'error.html')
        # （７）送信者のアカウントＩＤをチェックする。　例　1
        if fromAccountId is None:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B20-7', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （８）受信者のアカウントＩＤをチェックする。　例　1　ヒント：カンマで複数指定可能とする。
        # ヒント：複数受信アカウントＩＤに対応するため、カンマが含まれると想定する。
        if toAccountId is None:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B20-8', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （９）受信者のアカウントＩＤを「,」で分離し、局所変数の受信者アカウントＩＤリストにセットする。
        localToAccountIdList = toAccountId.split(",")
        if len(list(localToAccountIdList)) >= 1:
            pass
        else:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B20-9', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ２７Ｂ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P27.QuestionAddDoView関数 P27B30', 'INFO')
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
            print_log('[ERROR] P27.QuestionAddDoView関数 P27B30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P27.QuestionAddDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P27.QuestionAddDoView関数 P27B30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # フォームセット処理（Ｐ２７Ｂ４０）
        # （１）局所変数のフォームを初期化する。
        # （２）画面からポストされた情報を取得する。
        # ヒント：運用業者の場合は、ここにはこないと想定する。return済。
        # ヒント：画面からポストされた情報をlocalFormに一時的に格納する。
        # ヒント：localFormの値をチェックしながら、格納用のlocalAddConfirmFormに値をチェットする。
        ##########################################
        print_log('[INFO] P27.QuestionAddDoView関数 P27B40', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localForm = None
        localAddForm = QuestionAddForm()
        # （２）画面からポストされた情報を取得する。
        try:
            localForm = QuestionAddForm(request.POST, request.FILES)
            if localForm.is_valid():
                localAddForm.QUESTION_ID = localForm.cleaned_data['QUESTION_ID']                   # P27-1
                localAddForm.OPERATION_YEAR = localForm.cleaned_data['OPERATION_YEAR']             # P27-3 
                localAddForm.FLOOD_YEAR = localForm.cleaned_data['FLOOD_YEAR']                     # P27-4
                localAddForm.SEND_ORG_CODE = localForm.cleaned_data['SEND_ORG_CODE']               # P27-5
                localAddForm.SEND_ORG_NAME = localForm.cleaned_data['SEND_ORG_NAME']               # P27-6
                localAddForm.SEND_DEPT_CODE = localForm.cleaned_data['SEND_DEPT_CODE']             # P27-7
                localAddForm.SEND_DEPT_NAME = localForm.cleaned_data['SEND_DEPT_NAME']             # P27-8
                localAddForm.SEND_ACCOUNT_ID = localForm.cleaned_data['SEND_ACCOUNT_ID']           # P27-9
                localAddForm.SEND_ACCOUNT_NAME = localForm.cleaned_data['SEND_ACCOUNT_NAME']       # P27-10
                localAddForm.SEND_DATE = localForm.cleaned_data['SEND_DATE']                       # P27-11
                localAddForm.SEND_DATE_TIME = localForm.cleaned_data['SEND_DATE_TIME']             # P27-12
                localAddForm.SEND_FLAG = localForm.cleaned_data['SEND_FLAG']                       # P27-13
                localAddForm.SUBJECT = localForm.cleaned_data['SUBJECT']                           # P27-14
                localAddForm.BODY = localForm.cleaned_data['BODY']                                 # P27-15
                # ヒント：./01hokkai/aaa.lzhにファイルを格納する。
                # ヒント：事前に全アカウントＩＤについて、ディレクトリを作成しておくことを想定する。
                # ヒント：ＤＢに登録するデータにも上記ディレクトリ、ファイル名をセットすることを想定する。
                localAddForm.FILE_ID = localForm.cleaned_data['FILE_ID']                           # P27-17
                localAddForm.FILE_NAME = localForm.cleaned_data['FILE_NAME']                       # P27-18 
                localAddForm.FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId) # P27-19
                localAddForm.RECEIVE_ORG_CODE = localForm.cleaned_data['RECEIVE_ORG_CODE']         # P27-20
                localAddForm.RECEIVE_ORG_NAME = localForm.cleaned_data['RECEIVE_ORG_NAME']         # P27-21
                localAddForm.RECEIVE_DEPT_CODE = localForm.cleaned_data['RECEIVE_DEPT_CODE']       # P27-22
                localAddForm.RECEIVE_DEPT_NAME = localForm.cleaned_data['RECEIVE_DEPT_NAME']       # P27-23
                localAddForm.RECEIVE_ACCOUNT_ID = localForm.cleaned_data['RECEIVE_ACCOUNT_ID']     # P27-24
                localAddForm.RECEIVE_ACCOUNT_NAME = localForm.cleaned_data['RECEIVE_ACCOUNT_NAME'] # P27-25
                localAddForm.RECEIVE_DATE = localForm.cleaned_data['RECEIVE_DATE']                 # P27-26
                localAddForm.RECEIVE_DATE_TIME = localForm.cleaned_data['RECEIVE_DATE_TIME']       # P27-27
                localAddForm.RECEIVE_FLAG = localForm.cleaned_data['RECEIVE_FLAG']                 # P27-28
                localAddForm.DELETE_DATE = localForm.cleaned_data['DELETE_DATE']                   # P27-29
                localAddForm.DELETE_DATE_TIME = localForm.cleaned_data['DELETE_DATE_TIME']         # P27-30
                localAddForm.DELETE_FLAG = localForm.cleaned_data['DELETE_FLAG']                   # P27-31
                localAddForm.RECEIVE_READ_FLAG = localForm.cleaned_data['RECEIVE_READ_FLAG']       # P27-32
            else:
                pass
        except:
            print_log('[ERROR] P27.QuestionAddDoView関数 P27B40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P27.QuestionAddDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、問合せ回答データ登録処理（Ｐ２７Ａ５０）
        # （１）問合せ回答データの局所変数に初期値をセットする。
        ##########################################
        print_log('[INFO] P27.QuestionAddDoView関数 P27B50', 'INFO')
        # （１）問合せ回答データの局所変数に初期値をセットする。
        localAddDate = datetime.now().strftime("%Y/%m/%d")
        localAddDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        localQuestionIdString = ""
        localQuestionIdList = ""
        ##########################################
        # ファイル受信処理（Ｐ２７Ｂ６０）
        # （１）画面からポストされたファイルを受信し、サーバに保存する。
        ##########################################
        print_log('[INFO] P27.QuestionAddDoView関数 P27B60', 'INFO')
        try:
            # ヒント：./01hokkai/aaa.lzhにファイルを格納する。
            # ヒント：事前に全アカウントＩＤについて、ディレクトリを作成しておくことを想定する。
            # ヒント：ＤＢに登録するデータにも上記ディレクトリ、ファイル名をセットすることを想定する。
            if localAddForm.FILE_NAME == None:
                # 添付ファイルがない場合、、、
                pass
            else:
                # 添付ファイルがある場合、、、
                localTempDir = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId, (((localAddDateTime.replace(' ', '')).replace('/', '')).replace(':', '') + localAddForm.FILE_NAME.name)), 'wb+')
                for localChunk in request.FILES['FILE_NAME'].chunks():
                    localTempDir.write(localChunk)
                localTempDir.close()
        except:    
            print_log('[ERROR] P27.QuestionAddDoView関数 P27B60', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P27.QuestionAddDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、問合せ回答データ登録処理（Ｐ２７Ａ６１）
        # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
        # （２）受信者アカウントＩＤの件数分ループする。
        # （３）ＳＱＬ文を実行する。
        # （４）トランザクション管理でコミットする。
        # （５）ＤＢ接続を切断＝カーソルを閉じる。
        ##########################################
        print_log('[INFO] P27.QuestionAddDoView関数 P27B61', 'INFO')
        try:
            # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
            localCursor = connection.cursor()
            # （２）受信者アカウントＩＤの件数分ループする。
            # ヒント：最後に「,」が入っていないため、lenの結果は、受信者アカウントＩＤの件数＋０件となっている。
            # ヒント：そのため、>= 1 とする。
            if len(list(localToAccountIdList)) >= 1:
                for i in range(0, len(list(localToAccountIdList))):
                    # （３）ＳＱＬ文を実行する。
                    # 問合せ回答データをＤＢに登録する。
                    # ヒント：file_upload_questionテーブルにレコードを追加する。（登録フラグの状態＝仮登録済＝1）
                    # ヒント：仮登録済とは、レコードは登録済、ＩＤも付与済、登録フラグが仮登録済＝1の状態をいう。
                    # ヒント：ＩＤにＤＢから取得した最大値＋１をセットする。
                    # ヒント：SELECT MAX(KEN_QUESTION_ID + 1)としているが、KEN_QUESTION_IDは文字列のため、1を足すことで、
                    # ヒント：暗黙の型変換がＤＢ内で実行され、最大値を取得可能となる。
                    # ヒント：+1しないと、暗黙の型変換が実行されず、エラーとなるので注意すること。                
                    try:
                        localCursor.execute("""
                            INSERT INTO FILE_UPLOAD_QUESTION (
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
                            ) VALUES (
                                (SELECT MAX(id + 1) FROM FILE_UPLOAD_QUESTION), 
                                (SELECT MAX(QUESTION_ID + 1) FROM FILE_UPLOAD_QUESTION), 
                                %s, 
                                %s, 
                                %s, 
                                (SELECT ORG_NAME FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s),
                                %s, 
                                (SELECT DEPT_NAME FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s),
                                %s, 
                                (SELECT ACCOUNT_NAME FROM FILE_UPLOAD_ACCOUNT WHERE ACCOUNT_ID=%s),
                                %s, 
                                %s, 
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
                                %s
                            )
                            """, 
                            [ localAddForm.OPERATION_YEAR, 
                              localAddForm.FLOOD_YEAR,
                              localAddForm.SEND_ORG_CODE, 
                              localAddForm.SEND_ACCOUNT_ID,
                              localAddForm.SEND_DEPT_CODE, 
                              localAddForm.SEND_ACCOUNT_ID,
                              localAddForm.SEND_ACCOUNT_ID, 
                              localAddForm.SEND_ACCOUNT_ID,
                              localAddDate, 
                              localAddDateTime, 
                              '0', 
                              localAddForm.SUBJECT, 
                              localAddForm.BODY,
                              localToAccountIdList[i], 
                              localToAccountIdList[i],
                              localToAccountIdList[i], 
                              localToAccountIdList[i],
                              localToAccountIdList[i], 
                              localToAccountIdList[i],
                              localAddForm.RECEIVE_DATE, 
                              localAddForm.RECEIVE_DATE_TIME, 
                              '0',
                              localAddForm.DELETE_DATE, 
                              localAddForm.DELETE_DATE_TIME, 
                              '0',
                              '0'
                            ])
                        # （４）トランザクション管理でコミットする。
                        transaction.commit()
                    except:
                        transaction.rollback()
                        print_log('[ERROR] P27.QuestionAddDoView関数 P27B61', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P27.QuestionAddDoView関数で警告が発生しました。', 'ERROR')
                    # 上記で登録した問合せ回答データのQUESTION_IDを取得する。
                    # ヒント：問合せ回答ファイルデータの登録で使用するため。
                    # ヒント：cursorオープン中のため？cursorで検索しないとエラーが出力されます。    
                    # ヒント：SELECT MAX(QUESTION_ID + 0)としているが、QUESTION_IDは文字列のため、0を足すことで、
                    # ヒント：暗黙の型変換がＤＢ内で実行され、最大値を取得可能となる。
                    # ヒント：+0しないと、暗黙の型変換が実行されず、エラーとなるので注意すること。
                    try:    
                        localCursor.execute("""
                            SELECT 
                                MAX(QUESTION_ID + 0) AS QUESTION_ID 
                            FROM 
                                FILE_UPLOAD_QUESTION 
                            WHERE 
                                SEND_ACCOUNT_ID=%s AND 
                                OPERATION_YEAR=%s 
                            LIMIT 1
                            """,
                            [ accountId, 
                              operationYear, 
                            ])
                        localResults = namedtuplefetchall(localCursor)
                        localQuestionIdString = str(localResults[0].QUESTION_ID)
                        if len(list(localQuestionIdList)) == 0:
                            localQuestionIdList = localQuestionIdList + str(localResults[0].QUESTION_ID)
                        else:     
                            localQuestionIdList = localQuestionIdList + "," + str(localResults[0].QUESTION_ID)
                    except:
                        print_log('[ERROR] P27.QuestionAddDoView関数 P27B61', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P27.QuestionAddDoView関数で警告が発生しました。', 'ERROR')
                    # 問合せ回答ファイルデータをＤＢに登録する。    
                    # ヒント：file_upload_questionfileテーブルの登録フラグを更新する。ファイルアップロードボタンでレコードは仮登録済と想定する。
                    # ヒント：仮登録済とは、レコードは登録済、IDも付与済、登録フラグが仮登録済をいう。
                    # ヒント：file_upload_questionfileテーブルの登録スラグの状態＝仮登録済
                    # ヒント：SELECT MAX(KEN_QUESTION_FILE_ID + 1)としているが、KEN_QUESTION_FILE_IDは文字列のため、1を足すことで、
                    # ヒント：暗黙の型変換がＤＢ内で実行され、最大値を取得可能となる。
                    # ヒント：+1しないと、暗黙の型変換が実行されず、エラーとなるので注意すること。                
                    try:        
                        if localAddForm.FILE_NAME == None:
                            # 添付ファイルがない場合、、、
                            pass
                        else:
                            # 添付ファイルがある場合、、、
                            localCursor.execute("""
                                INSERT INTO FILE_UPLOAD_QUESTIONFILE (
                                    id, 
                                    QUESTION_FILE_ID, 
                                    QUESTION_ID,
                                    OPERATION_YEAR, 
                                    FLOOD_YEAR,
                                    SEND_DATE, 
                                    SEND_DATE_TIME, 
                                    SEND_FLAG,
                                    DELETE_DATE, 
                                    DELETE_DATE_TIME, 
                                    DELETE_FLAG,
                                    FILE_ID, 
                                    FILE_NAME, 
                                    FILE_PATH
                                ) VALUES (
                                    (SELECT MAX(id + 1) FROM FILE_UPLOAD_QUESTIONFILE), 
                                    (SELECT MAX(QUESTION_FILE_ID + 1) FROM FILE_UPLOAD_QUESTIONFILE), 
                                    %s,
                                    %s, 
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
                                [ localQuestionIdString,
                                  localAddForm.OPERATION_YEAR, 
                                  localAddForm.FLOOD_YEAR,
                                  localAddDate, 
                                  localAddDateTime, 
                                  '0',
                                  localAddForm.DELETE_DATE, 
                                  localAddForm.DELETE_DATE_TIME, 
                                  '0', 
                                  '0', 
                                  localAddForm.FILE_NAME.name, 
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), accountId, (((localAddDateTime.replace(' ', '')).replace('/', '')).replace(':', '') + localAddForm.FILE_NAME.name)),
                                ])
                            # （４）トランザクション管理でコミットする。
                            transaction.commit()
                    except:    
                        transaction.rollback()
                        print_log('[ERROR] P27.QuestionAddDoView関数 P27B61', 'ERROR')
                        print_log(sys.exc_info()[0], 'ERROR')
                        print_log('[ERROR] P27.QuestionAddDoView関数で警告が発生しました。', 'ERROR')
            else:
                pass            
        except:
            transaction.rollback()
            print_log('[ERROR] P27.QuestionAddDoView関数 P27B61', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P27.QuestionAddDoView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddDoView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （５）ＤＢ接続を切断＝カーソルを閉じる。
        finally:
            localCursor.close()
        ##########################################
        # 変数セット処理（Ｐ２７Ｂ７０）
        # （１）局所変数のレスポンスにメッセージとフォームをセットする。
        ##########################################
        print_log('[INFO] P27.QuestionAddDoView関数 P27B70', 'INFO')
        # （１）局所変数のレスポンスにメッセージとフォームをセットする。
        print_log('[INFO] P27.QuestionAddDoView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ２７Ｂ８０）
        # （１）リダイレクト関数をコールする。
        # （２）レンダリング関数をコールする。
        # （３）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        # ヒント：複数受信アカウントＩＤへの送信を利用者が１回で行うことが出来るようにするため、以下を行う。
        # ヒント：問合せ回答ＩＤのリストを確認画面のURLへのクエリストリングにセットする。
        # ヒント：受信者アカウントＩＤのリストを確認画面のURLへのクエリストリングにセットする。
        ##########################################
        print_log('[INFO] P27.QuestionAddDoView関数 P27B80', 'INFO')
        # （１）リダイレクト関数をコールする。
        # （２）レンダリング関数をコールする。
        # （３）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return HttpResponseRedirect('/file_upload/P28/QuestionAddConfirm/'+urlquote(str(localAccountModel.ACCOUNT_TYPE))+'/'+urlquote(str(localAccountModel.ACCOUNT_ID))+'/'+urlquote(str(localAccountModel.OPERATION_YEAR))+'/'+str(localQuestionIdList)+'/'+urlquote(str(fromAccountId))+'/'+str(toAccountId))
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return HttpResponseRedirect('/file_upload/P28/QuestionAddConfirm/'+urlquote(str(localAccountModel.ACCOUNT_TYPE))+'/'+urlquote(str(localAccountModel.ACCOUNT_ID))+'/'+urlquote(str(localAccountModel.OPERATION_YEAR))+'/'+str(localQuestionIdList)+'/'+urlquote(str(fromAccountId))+'/'+str(toAccountId))
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            return HttpResponseRedirect('/file_upload/P28/QuestionAddConfirm/'+urlquote(str(localAccountModel.ACCOUNT_TYPE))+'/'+urlquote(str(localAccountModel.ACCOUNT_ID))+'/'+urlquote(str(localAccountModel.OPERATION_YEAR))+'/'+str(localQuestionIdList)+'/'+urlquote(str(fromAccountId))+'/'+str(toAccountId))
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P27.QuestionAddDoView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P27.QuestionAddDoView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ２７Ｂ９０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P27.QuestionAddDoView関数 P27B90', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P27.QuestionAddDoView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P27.QuestionAddDoView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ２７Ｂ１００）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P27.QuestionAddDoView関数 P27B100', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
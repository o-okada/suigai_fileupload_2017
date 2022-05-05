#####################################################################################
# QuestionDetailViewビューモジュール
# ファイル名：P26.QuestionDetailView.py（Ｐ２６）
# ユースケース：都道府県は、本省または運用業者に問合せする。
# ユースケース：本省は、都道府県に回答する。
# ユースケース：運用業者は、都道府県に回答する。
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
# os
# shutil:ファイルコピー関数のshutil.copy2()を使用するためにインポートする。
# sys
#####################################################################################
import os                                                  # osモジュール
import shutil                                              # shutilモジュール
import sys                                                 # sysモジュール
from datetime import datetime                              # datetimeモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：ジャンゴモジュールをインポートする。
# login_required
# HttpResponse
# render
# smart_str
# urlquote 
#####################################################################################
from django.contrib.auth.decorators import login_required  # ログイン制御モジュール
from django.db import connection                           # ＤＢ接続モジュール
from django.db import transaction                          # トランザクション管理モジュール
from django.http import HttpResponse                       # レスポンスモジュール
from django.shortcuts import render                        # レンダリングモジュール
from django.utils.encoding import smart_str                # URLエスケープモジュール
from django.utils.http import urlquote                     # URLエスケープモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# print_log
# QuestionDetailForm
# QuestionFileForm
# AccountModel
# QuestionFileModel
# QuestionModel
#####################################################################################
from file_upload.CommonFunction import print_log           # ログ出力モジュール
from file_upload.forms import QuestionDetailForm           # 問合せ回答詳細画面用のフォーム
from file_upload.models import AccountModel                # アカウントデータモデル
from file_upload.models import QuestionFileModel           # 問合せ回答ファイルデータモデル
from file_upload.models import QuestionModel               # 問合せ回答データモデル
#####################################################################################
# 関数名：P26.QuestionDetailView（Ｐ２６Ａ）
# 関数概要：都道府県用問合せまたは回答詳細ページをブラウザに戻す。（都道府県）
# 関数概要：本省用問合せまたは回答詳細ページをブラウザに戻す。（本省）
# 関数概要：運用業者用問合せまたは回答詳細ページをブラウザに戻す。（運用業者）
#
# 引数[1]：request：
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから運用業者名、運用業者部署名、運用業者名を取得するために使用する。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）
# 引数[5]：questionId：都道府県用問合せまたは回答詳細ＩＤ※ＤＢから都道府県用問合せまたは回答を取得するために使用する。（都道府県）
# 引数[5]：questionId：本省用問合せまたは回答詳細ＩＤ※ＤＢから本省用問合せまたは回答を取得するために使用する。（本省）
# 引数[5]：questionId：運用業者用問合せまたは回答詳細ＩＤ※ＤＢから運用業者用問合せまたは回答を取得するために使用する。（運用業者）
#
# 戻り値[1]：response：
#
# FORM：QuestionDetailForm：都道府県用問合せまたは回答詳細ページ（都道府県）
# FORM：QuestionDetailForm：本省用問合せまたは回答詳細ページ（本省）
# FORM：QuestionDetailForm：運用業者用問合せまたは回答詳細ページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：QuestionModel：問合せまたは回答モデル（Ｒ）
# ヒント：複数の受信者をセットした場合、レコードは受信者数分ＤＢに登録されると想定する。
# ヒント：したがって、toAccountIdには１アカウントのみが入っていると想定する。
# ヒント：既読、未読をＤＢで管理したいため、受信者数分のレコードをＤＢに登録する必要がある。
# ヒント：この場合、本省が全都道府県に送信した問合せ回答データは、４７行も出力されないように、表示に工夫する必要がある。
# ヒント：また、添付ファイルについては、受信者数分登録するか、１送信について１ファイル、１レコードとする選択肢があるが、
# ヒント：効率化のため、１送信について１ファイル、１レコードとする。
# ヒント：questionIdは受信者数分生成する。
#####################################################################################
@login_required(None, login_url='/file_upload/P01/login/')
def QuestionDetailView(request, accountType, accountId, operationYear, questionId, fromAccountId, toAccountId):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P26.QuestionDetailView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２６Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P26.QuestionDetailView関数 P26A10', 'INFO')
        print_log('[INFO] P26.QuestionDetailView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P26.QuestionDetailView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P26.QuestionDetailView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P26.QuestionDetailView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P26.QuestionDetailView.questionId = {}'.format(questionId), 'INFO')
        print_log('[INFO] P26.QuestionDetailView.fromAccountId = {}'.format(fromAccountId), 'INFO')
        print_log('[INFO] P26.QuestionDetailView.toAccountId = {}'.format(toAccountId), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２６Ａ２０）
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
            print_log('[WARN] P26.QuestionDetailView関数 P26A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P26.QuestionDetailView関数 P26A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P26.QuestionDetailView関数 P26A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P26.QuestionDetailView関数 P26A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P26.QuestionDetailView関数 P26A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P26.QuestionDetailView関数 P26A20-5', 'WARN')
                return render(request, 'error.html')
        # （６）問合せ回答ＩＤをチェックする。　例　1
        if questionId is None:
            print_log('[WARN] P26.QuestionDetailView関数 P26A20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(questionId) == True:
                pass
            else:
                print_log('[WARN] P26.QuestionDetailView関数 P26A20-6', 'WARN')
                return render(request, 'error.html')
        # （７）送信者のアカウントＩＤをチェックする。　例　1
        if fromAccountId is None:
            print_log('[WARN] P26.QuestionDetailView関数 P26A20-7', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （８）受信者のアカウントＩＤをチェックする。　例　1　ヒント：カンマで複数指定可能とする。
        if toAccountId is None:
            print_log('[WARN] P26.QuestionDetailView関数 P26A20-8', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ２６Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P26.QuestionDetailView関数 P26A30', 'INFO')
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        localAccountModel = None
        try:
            localAccountModel = AccountModel.objects.raw("""
                SELECT 
                   * 
                FROM 
                    file_upload_account 
                WHERE 
                    ACCOUNT_ID=%s AND 
                    OPERATION_YEAR=%s 
                LIMIT 1
                """, 
                [accountId, operationYear, ])[0]
        except:
            localAccountModel = None
            print_log('[ERROR] P26.QuestionDetailView関数 P26A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P26.QuestionDetailView関数 P26A30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P26.QuestionDetailView関数 P26A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html', 'WARN')
        ##########################################
        # ＤＢアクセス処理、問合せ回答データ取得処理（Ｐ２６Ａ４０）
        # （１）問合せ回答データを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、問合せ回答データを取得する。
        # （３）ＤＢにアクセスし、問合せ回答ファイルデータを取得する。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：rawでＤＢにアクセスした場合、検索結果が０件の場合、エクセプションが発生する。
        # ヒント：後々の拡張等を考慮し、場合分けをベタで記述し、明示されていないロジックを含まないコードとするため、
        # ヒント：あえて冗長な場合分けをしている。
        # ヒント：ＤＢの問合せ回答テーブルには、KEN_QUESTION_ID、HON_QUESTION_ID、OPE_QUESTION_IDの項目がある。
        # ヒント：問合せ（親）と回答（子）を紐付けるために使用している。
        # ヒント：このため、問合せ（親）については、KEN_QUESTION_ID（親問合せ回答データのＩＤ）がセット、HON_QUESTION_ID（子問合せ回答データのＩＤ）が未セット、
        # ヒント：回答（子）については、KEN_QUESTION_ID（親問合せ回答データのＩＤ）がセット、HON_QUESTION_ID（子問合せ回答データのＩＤ）がセットされることを想定している。
        # ヒント：また、後々の拡張等を考慮し、問合せ（親）についても、KEN_QUESTION_IDがセット、HON_QUESTION_IDがセットされることも想定している。
        # ヒント：KEN_HON_OPE_FLAGは使用しない。
        ##########################################
        print_log('[INFO] P26.QuestionDetailView関数 P26A40', 'INFO')
        # （１）問合せ回答データを格納する局所変数を初期化する。
        localQuestionModel = None
        localQuestionFileModel = None
        # （２）ＤＢにアクセスし、問合せ回答データを取得する。
        # ヒント：問合せ回答データは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
        # ヒント：exceptが発生した場合でもreturnしない。
        try:
            localQuestionModel = QuestionModel.objects.raw("""
                SELECT 
                    * 
                FROM 
                    file_upload_question 
                WHERE 
                    QUESTION_ID=%s AND 
                    OPERATION_YEAR=%s 
                LIMIT 1
                """, 
                [questionId, operationYear, ])[0]
        except:
            localQuestionModel = None
            print_log('[ERROR] P26.QuestionDetailView関数 P26A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数を警告終了しました。', 'ERROR')
        # （３）ＤＢにアクセスし、問合せ回答ファイルデータを取得する。
        # ヒント：問合せ回答ファイルデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
        # ヒント：exceptが発生した場合でもreturnしない。
        try:
            localQuestionFileModel = QuestionFileModel.objects.raw("""
                SELECT 
                    * 
                FROM 
                    file_upload_questionfile 
                WHERE 
                    QUESTION_ID=%s AND 
                    OPERATION_YEAR=%s 
                LIMIT 1
                """, 
                [questionId, operationYear, ])[0]
        except:
            localQuestionFileModel = None    
            print_log('[ERROR] P26.QuestionDetailView関数 P26A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数を警告終了しました。', 'ERROR')
        # （４）ＤＢにアクセスし、既読未読フラグを更新する。
        # ヒント：問合せ回答データの受信アカウントＩＤがクエリストリングのアカウントＩＤと同じ場合、つまり、受信者が詳細画面をリクエストしたとき、既読未読フラグを既読に更新する。
        # ヒント：問合せ回答データの受信アカウントＩＤがクエリストリングのアカウントＩＤと異なる場合、つまり、送信者が詳細画面をリクエストしたとき、既読未読フラグを既読に更新しない。
        try:
            localCursor = connection.cursor()
            localCursor.execute("""
                UPDATE FILE_UPLOAD_QUESTION
                SET
                    RECEIVE_READ_FLAG = '5'
                WHERE
                    QUESTION_ID=%s AND 
                    OPERATION_YEAR=%s
            """,
            [questionId, operationYear, ])
        except:
            print_log('[ERROR] P26.QuestionDetailView関数 P26A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数を警告終了しました。', 'ERROR')
        finally:
            localCursor.close()
        ##########################################
        # ＤＢアクセス処理、お知らせデータ取得処理（Ｐ２６Ａ４５）
        # （１）ＤＢ接続のためのセッション＝カーソルを作成する。
        # （２）ＳＱＬ文を実行する。
        # （３）トランザクション管理でコミットする。
        # （４）ＤＢ接続を切断＝カーソルを閉じる。
        ##########################################
        print_log('[INFO] P26.QuestionDetailView関数 P26A45', 'INFO')
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
                    QUESTION_ID
                ) VALUES (
                    (SELECT MAX(id + 1) FROM FILE_UPLOAD_LOG),
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                [operationYear, 
                 operationYear,
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 'QuestionDetailView',
                 questionId, 
                 ])
            # （３）トランザクション管理でコミットする。
            transaction.commit()
        except:
            transaction.rollback()
            print_log('[ERROR] P26.QuestionDetailView関数 P26A45', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        finally:
            # （４）ＤＢ接続を切断＝カーソルを閉じる。
            localCursor.close()
        ##########################################
        # フォームセット処理（Ｐ２６Ａ５０）
        # （１）局所変数のフォームを初期化する。
        # （２）局所変数のフォームにＤＢの問合せ回答テーブルから取得した値をセットする。
        # （３）局所変数のフォームにＤＢの問合せ回答ファイルテーブルから取得した値をセットする。
        # ヒント：ブラウザとのデータのやりとり、特にブラウザからPOSTデータがある場合、フォームを使用する。
        # ヒント：モデルはブラウザで参照用、かつタグをコーディングする場合等に使用する。
        # ヒント：フォームはブラウザで編集用、POSTでサーバにリクエストされる項目、かつタグを自動生成する場合等に使用する。
        # ヒント：表示画面の場合、URL+QUERY STRING、VIEW関数、GET、renderでテンプレートとレスポンスで目的の画面を表示する。
        # ヒント：追加、削除の場合、URL+QUERY STRING+フォーム値、DoVIEW関数、POST、redirect（URL+QUERY STRING）で次の画面に遷移する。
        # ヒント：または、追加、削除の場合、URL+QUERY STRING+フォーム値、DoVIEW関数、POST、renderでテンプレートとレスポンスで元の同じ画面を表示する。
        # ヒント：ただし、この場合、レスポンスに、追加、削除結果のフラグを返し、ブラウザ側（正確にはサーバでのレンダリング時＝HTML生成時）で通常画面と結果画面をフラグを見て分岐処理するようにテンプレートを記述する。
        # ヒント：「!= None」でオブジェクトのインスタンスが生成済み＝存在していることを確認する。
        # ヒント：上記チェック処理を行い、実行時エラーの発生を防止する。
        # ヒント：これを実現するために、変数を初期化し、ＤＢアクセス時のエクセプション発生時にも、変数の初期化を確実に行う。
        ##########################################
        print_log('[INFO] P26.QuestionDetailView関数 P26A50', 'INFO')
        # （１）局所変数のフォームを初期化する。
        localQuestionDetailForm = QuestionDetailForm()
        # （２）局所変数のフォームにＤＢの問合せ回答テーブルから取得した値をセットする。
        if localQuestionModel != None:
            localQuestionDetailForm.initial['QUESTION_ID'] = localQuestionModel.QUESTION_ID
            localQuestionDetailForm.initial['OPERATION_YEAR'] = localQuestionModel.OPERATION_YEAR
            localQuestionDetailForm.initial['FLOOD_YEAR'] = localQuestionModel.FLOOD_YEAR
            localQuestionDetailForm.initial['SEND_ORG_CODE'] = localQuestionModel.SEND_ORG_CODE
            localQuestionDetailForm.initial['SEND_ORG_NAME'] = localQuestionModel.SEND_ORG_NAME
            localQuestionDetailForm.initial['SEND_DEPT_CODE'] = localQuestionModel.SEND_DEPT_CODE
            localQuestionDetailForm.initial['SEND_DEPT_NAME'] = localQuestionModel.SEND_DEPT_NAME
            localQuestionDetailForm.initial['SEND_ACCOUNT_ID'] = localQuestionModel.SEND_ACCOUNT_ID
            localQuestionDetailForm.initial['SEND_ACCOUNT_NAME'] = localQuestionModel.SEND_ACCOUNT_NAME
            localQuestionDetailForm.initial['SEND_DATE'] = localQuestionModel.SEND_DATE
            localQuestionDetailForm.initial['SEND_DATE_TIME'] = localQuestionModel.SEND_DATE_TIME
            localQuestionDetailForm.initial['SEND_FLAG'] = localQuestionModel.SEND_FLAG
            localQuestionDetailForm.initial['SUBJECT'] = localQuestionModel.SUBJECT
            localQuestionDetailForm.initial['BODY'] = localQuestionModel.BODY
            localQuestionDetailForm.initial['RECEIVE_ORG_CODE'] = localQuestionModel.RECEIVE_ORG_CODE
            localQuestionDetailForm.initial['RECEIVE_ORG_NAME'] = localQuestionModel.RECEIVE_ORG_NAME
            localQuestionDetailForm.initial['RECEIVE_DEPT_CODE'] = localQuestionModel.RECEIVE_DEPT_CODE
            localQuestionDetailForm.initial['RECEIVE_DEPT_NAME'] = localQuestionModel.RECEIVE_DEPT_NAME
            localQuestionDetailForm.initial['RECEIVE_ACCOUNT_ID'] = localQuestionModel.RECEIVE_ACCOUNT_ID
            localQuestionDetailForm.initial['RECEIVE_ACCOUNT_NAME'] = localQuestionModel.RECEIVE_ACCOUNT_NAME
            localQuestionDetailForm.initial['RECEIVE_DATE'] = localQuestionModel.RECEIVE_DATE
            localQuestionDetailForm.initial['RECEIVE_DATE_TIME'] = localQuestionModel.RECEIVE_DATE_TIME
            localQuestionDetailForm.initial['RECEIVE_FLAG'] = localQuestionModel.RECEIVE_FLAG
            localQuestionDetailForm.initial['DELETE_DATE'] = localQuestionModel.DELETE_DATE
            localQuestionDetailForm.initial['DELETE_DATE_TIME'] = localQuestionModel.DELETE_DATE_TIME
            localQuestionDetailForm.initial['DELETE_FLAG'] = localQuestionModel.DELETE_FLAG
            localQuestionDetailForm.initial['RECEIVE_READ_FLAG'] = localQuestionModel.RECEIVE_READ_FLAG
        else:
            localQuestionDetailForm.initial['QUESTION_ID'] = "0"
            localQuestionDetailForm.initial['OPERATION_YEAR'] = "0"
            localQuestionDetailForm.initial['FLOOD_YEAR'] = "0"
            localQuestionDetailForm.initial['SEND_ORG_CODE'] = "0"
            localQuestionDetailForm.initial['SEND_ORG_NAME'] = "0"
            localQuestionDetailForm.initial['SEND_DEPT_CODE'] = "0"
            localQuestionDetailForm.initial['SEND_DEPT_NAME'] = "0"
            localQuestionDetailForm.initial['SEND_ACCOUNT_ID'] = "0"
            localQuestionDetailForm.initial['SEND_ACCOUNT_NAME'] = "0"
            localQuestionDetailForm.initial['SEND_DATE'] = "0"
            localQuestionDetailForm.initial['SEND_DATE_TIME'] = "0"
            localQuestionDetailForm.initial['SEND_FLAG'] = "0"
            localQuestionDetailForm.initial['SUBJECT'] = "0"
            localQuestionDetailForm.initial['BODY'] = "0"
            localQuestionDetailForm.initial['RECEIVE_ORG_CODE'] = "0"
            localQuestionDetailForm.initial['RECEIVE_ORG_NAME'] = "0"
            localQuestionDetailForm.initial['RECEIVE_DEPT_CODE'] = "0"
            localQuestionDetailForm.initial['RECEIVE_DEPT_NAME'] = "0"
            localQuestionDetailForm.initial['RECEIVE_ACCOUNT_ID'] = "0"
            localQuestionDetailForm.initial['RECEIVE_ACCOUNT_NAME'] = "0"
            localQuestionDetailForm.initial['RECEIVE_DATE'] = "0"
            localQuestionDetailForm.initial['RECEIVE_DATE_TIME'] = "0"
            localQuestionDetailForm.initial['RECEIVE_FLAG'] = "0"
            localQuestionDetailForm.initial['DELETE_DATE'] = "0"
            localQuestionDetailForm.initial['DELETE_DATE_TIME'] = "0"
            localQuestionDetailForm.initial['DELETE_FLAG'] = "0"
            localQuestionDetailForm.initial['RECEIVE_READ_FLAG'] = "0"
        # （３）局所変数のフォームにＤＢの問合せ回答ファイルテーブルから取得した値をセットする。
        if localQuestionFileModel != None:
            localQuestionDetailForm.initial['FILE_ID'] = localQuestionFileModel.FILE_ID
            localQuestionDetailForm.initial['FILE_NAME'] = localQuestionFileModel.FILE_NAME
            localQuestionDetailForm.initial['FILE_PATH'] = localQuestionFileModel.FILE_PATH
        else:    
            localQuestionDetailForm.initial['FILE_ID'] = "0"
            localQuestionDetailForm.initial['FILE_NAME'] = "0"
            localQuestionDetailForm.initial['FILE_PATH'] = "0"
        ##########################################            
        # フォームセット処理（Ｐ２６Ａ５２）
        # （１）フォームのウィジェットの属性に値をセットする。
        ##########################################            
        # （１）フォームのウィジェットの属性に値をセットする。
        localQuestionDetailForm.fields['QUESTION_ID'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['OPERATION_YEAR'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['FLOOD_YEAR'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['SEND_ORG_CODE'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['SEND_ORG_NAME'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['SEND_DEPT_CODE'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['SEND_DEPT_NAME'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['SEND_ACCOUNT_ID'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['SEND_ACCOUNT_NAME'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['SEND_DATE'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['SEND_DATE_TIME'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['SEND_FLAG'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['SUBJECT'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['BODY'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['FILE_ID'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['FILE_NAME'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['FILE_PATH'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['RECEIVE_ORG_CODE'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['RECEIVE_ORG_NAME'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['RECEIVE_DEPT_CODE'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['RECEIVE_DEPT_NAME'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['RECEIVE_ACCOUNT_ID'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['RECEIVE_ACCOUNT_NAME'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['RECEIVE_DATE'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['RECEIVE_DATE_TIME'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['RECEIVE_FLAG'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['DELETE_DATE'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['DELETE_DATE_TIME'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['DELETE_FLAG'].widget.attrs['readonly'] = True
        localQuestionDetailForm.fields['RECEIVE_READ_FLAG'].widget.attrs['readonly'] = True
        ##########################################
        # レスポンスセット処理（Ｐ２６Ａ６０）
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
        print_log('[INFO] P26.QuestionDetailView関数 P26A60', 'INFO')
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
                'questionDetailForm': localQuestionDetailForm, # 問合せ回答詳細画面用のフォーム
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'questionDetailForm': localQuestionDetailForm, # 問合せ回答詳細画面用のフォーム
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            response = {
                'accountType': 3,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': urlquote(accountId),          # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': True,                             # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'questionDetailForm': localQuestionDetailForm, # 問合せ回答詳細画面用のフォーム
            }
        else:   
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P26.QuestionDetailView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P26.QuestionDetailView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ２６Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P26.QuestionDetailView関数 P26A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P26QuestionDetailTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P26QuestionDetailTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            return render(request, 'P26QuestionDetailTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P26.QuestionDetailView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P26.QuestionDetailView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ２６Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P26.QuestionDetailView関数 P26A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P26.QuestionDetailView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P26.QuestionDetailView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング、戻り値セット処理（Ｐ２６Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P26.QuestionDetailView関数 P26A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
#####################################################################################
# 関数名：P26.QuestionDownloadView（Ｐ２６Ｂ）
# 関数概要：都道府県用問合せまたは回答ファイルをブラウザに戻す。（都道府県）
# 関数概要：本省用問合せまたは回答ファイルをブラウザに戻す。（本省）
# 関数概要：運用業者用問合せまたは回答ファイルをブラウザに戻す。（運用業者）
#
# 引数[1]：request
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[3]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから運用業者名、運用業者部署名、運用業者名を取得するために使用する。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）
# 引数[5]：questionId：都道府県用問合せまたは回答ファイルＩＤ※ＤＢから都道府県用問合せまたは回答ファイルを取得するために使用する。（都道府県）
# 引数[5]：questionId：本省用問合せまたは回答ファイルＩＤ※ＤＢから本省用問合せまたは回答ファイルを取得するために使用する。（本省）
# 引数[5]：questionId：運用業者用問合せまたは回答ファイルＩＤ※ＤＢから運用業者用問合せまたは回答ファイルを取得するために使用する。（運用業者）
# 引数[6]：fileKenHonOpeFlag：
#
# 戻り値[1]：response
#
# FORM：QuestionDownloadForm：都道府県用問合せまたは回答ダウンロードページ（都道府県）
# FORM：QuestionDownloadForm：本省用問合せまたは回答ダウンロードページ（本省）
# FORM：QuestionDownloadForm：運用業者用問合せまたは回答ダウンロードページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：QuestionModel：問合せまたは回答（Ｒ）
#####################################################################################
@login_required(None, login_url='/file_upload/P01/login/')
def QuestionDownloadView(request, accountType, accountId, operationYear, questionId, fromAccountId, toAccountId):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P26.QuestionDownloadView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２６Ｂ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P26.QuestionDownloadView関数 P26B10', 'INFO')
        print_log('[INFO] P26.QuestionDownloadView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P26.QuestionDownloadView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P26.QuestionDownloadView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P26.QuestionDownloadView.operationYear = {}'.format(operationYear), 'INFO')
        print_log('[INFO] P26.QuestionDownloadView.questionId = {}'.format(questionId), 'INFO')
        print_log('[INFO] P26.QuestionDownloadView.fromAccountId = {}'.format(fromAccountId), 'INFO')
        print_log('[INFO] P26.QuestionDownloadView.toAccountIdId = {}'.format(toAccountId), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ２６Ｂ２０）
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
            print_log('[WARN] P26.QuestionDownloadView関数 P26B20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P26.QuestionDownloadView関数 P26B20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P26.QuestionDownloadView関数 P26B20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P26.QuestionDownloadView関数 P26B20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P26.QuestionDownloadView関数 P26B20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P26.QuestionDownloadView関数 P26B20-5', 'WARN')
                return render(request, 'error.html')
        # （６）問合せ回答ＩＤをチェックする。　例　1
        if questionId is None:
            print_log('[WARN] P26.QuestionDownloadView関数 P26B20-6', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(questionId) == True:
                pass
            else:
                print_log('[WARN] P26.QuestionDownloadView関数 P26B20-6', 'WARN')
                return render(request, 'error.html')
        # （７）送信者のアカウントＩＤをチェックする。　例　1
        if fromAccountId is None:
            print_log('[WARN] P26.QuestionDownloadView関数 P26B20-7', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （８）受信者のアカウントＩＤをチェックする。　例　1　ヒント：カンマで複数指定可能とする。
        if toAccountId is None:
            print_log('[WARN] P26.QuestionDownloadView関数 P26B20-8', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ２６Ｂ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P26.QuestionDownloadView関数 P26B30', 'INFO')
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        localAccountModel = None
        try:
            localAccountModel = AccountModel.objects.raw("""
                SELECT 
                    * 
                FROM 
                    file_upload_account 
                WHERE 
                    ACCOUNT_ID=%s AND 
                    OPERATION_YEAR=%s 
                LIMIT 1
                """, 
                [accountId, operationYear, ])[0]
        except:
            localAccountModel = None
            print_log('[ERROR] P26.QuestionDownloadView関数 P26B30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P26.QuestionDownloadView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P26.QuestionDownloadView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P26.QuestionDownloadView関数 P26B30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P26.QuestionDownloadView関数 P26B30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、問合せ回答ファイルデータ取得処理（Ｐ２６Ｂ４０）
        # （１）ファイルデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、ファイルデータを取得する。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：rawでＤＢにアクセスした場合、検索結果が０件の場合、エクセプションが発生する。
        # ヒント：後々の拡張等を考慮し、場合分けをベタで記述し、明示されていないロジックを含まないコードとするため、
        # ヒント：あえて冗長な場合分けをしている。
        ##########################################
        print_log('[INFO] P26.QuestionDownloadView関数 P26B40', 'INFO')
        # （１）ファイルデータを格納する局所変数を初期化する。
        localQuestionFileModel = None
        # （２）ＤＢにアクセスし、ファイルデータを取得する。
        try:
            # ヒント：アップロードデータは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
            # ヒント：exceptが発生した場合でもreturnしない。
            localQuestionFileModel = QuestionFileModel.objects.raw("""
                SELECT 
                    * 
                FROM 
                    file_upload_questionfile 
                WHERE 
                    QUESTION_ID=%s AND 
                    OPERATION_YEAR=%s 
                LIMIT 1
                """, 
                [questionId, operationYear, ])[0]
        except:
            localQuestionFileModel = None
            print_log('[ERROR] P26.QuestionDownloadView関数 P26B40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P26.QuestionDownloadView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P26.QuestionDownloadView関数を警告終了しました。', 'ERROR')
        ##########################################
        # 変数セット処理（Ｐ２６Ｂ５０）
        # （１）局所変数に初期値をセットする。
        # （２）局所変数に値をセットする。
        ##########################################
        print_log('[INFO] P26.QuestionDownloadView関数 P26B50', 'INFO')
        # （１）局所変数に初期値をセットする。
        # ヒント：FILE_NAMEはユーザがブラウザでセットしたファイル名である。つまり、年月日時分は追加されていない。
        # ヒント：サーバに格納されているファイル名は重複防止のため、ファイル名の前に年月日時分の文字列が追加されている。
        # ヒント：FILE_PATHはサーバに格納されているファイルのフルパスである。ファイル名の前に年月日時分の文字列が追加されている。
        localQuestionFileName = ""
        localQuestionFilePath = ""
        # （２）局所変数に値をセットする。
        if localQuestionFileModel != None:
            localQuestionFileName = localQuestionFileModel.FILE_NAME
            localQuestionFilePath = localQuestionFileModel.FILE_PATH
        else:
            pass    
        ##########################################
        # レスポンスセット処理（Ｐ２６Ｂ６０）
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
        print_log('[INFO] P26.QuestionDownloadView関数 P26B60', 'INFO')
        # （１）ファイルを格納しているディレクトリからダウンロード用のディレクトリにコピーする。
        # （２）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        # データの種別・区分＝１：都道府県の場合、、、
        # ヒント：./01hokkai/aaa.lzhを./download/aaa.lzhにコピーする。
        # ヒント：./download/aaa.lzhブラウザに戻す。
        try:
            shutil.copy2(os.path.join(localQuestionFilePath), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download', localQuestionFileName))
            response = HttpResponse(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download', localQuestionFileName), 'rb').read(), content_type="application/x-zip-compressed")
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(localQuestionFileName)
        except:
            print_log('[ERROR] P26.QuestionDownloadView関数 P26B60', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P26.QuestionDownloadView関数で警告が発生しました。', 'ERROR')
        print_log('[INFO] P26.QuestionDownloadView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ２６Ｂ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P26.QuestionDownloadView関数 P26B70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return response
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ２６Ｂ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P26.QuestionDownloadView関数 P26B80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P26.QuestionDownloadView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P26.QuestionDownloadView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ２６Ｂ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P26.QuestionDownloadView関数 P26B90', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')

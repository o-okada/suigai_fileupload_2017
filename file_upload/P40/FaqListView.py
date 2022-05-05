#####################################################################################
# FaqListViewビューモジュール【ほぼ完成】
# ファイル名：P40.FaqListView.py（Ｐ４０）
# ユースケース：都道府県は、FAQの一覧を閲覧する。
# ユースケース：本省は、FAQの一覧を閲覧する。
# ユースケース：運用業者は、FAQの一覧を閲覧する。
# ヒント：調査結果と確認結果は同じテーブル、モデルを使用する。
# ヒント：種別・区分フラグで調査結果と確認結果を識別する。
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
# AccountModel
# P40FaqModel
# print_log
#####################################################################################
from file_upload.models import AccountModel                # アカウントモデル 
from file_upload.models import P40FaqModel                 # FAQ一覧画面専用データモデル
from file_upload.CommonFunction import print_log           # ログ出力モジュール   
#####################################################################################
# 関数名：P40.FaqListView（Ｐ４０Ａ）
# 関数概要：FAQ一覧ページをブラウザに戻す。（都道府県）
# 関数概要：FAQ一覧ページをブラウザに戻す。（本省）
# 関数概要：FAQ一覧ページをブラウザに戻す。（運用業者）
#
# 引数[1]：request
# 引数[2]：accountType：アカウント種別・区分：1：都道府県、2：本省、3：運用業者※アカウント種別・区分に応じて処理を分岐させるために使用する。
# 引数[2]：accountId：アカウントＩＤ※ＤＢから都道府県名、登録部署名、登録者名を取得するために使用する。（都道府県）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから本省名、確認部署名、確認者名を取得するために使用する。（本省）
# 引数[3]：accountId：アカウントＩＤ※ＤＢから運用業者名、運用部署名、運用業者名を取得するために使用する。（運用業者）
# 引数[4]：operationYear：調査実施年（都道府県）
# 引数[4]：operationYear：調査実施年（本省）
# 引数[4]：operationYear：調査実施年（運用業者）
#
# 戻り値[]：response
#
# FORM：FaqListForm：FAQ一覧ページ（都道府県）
# FORM：FaqListForm：FAQ一覧ページ（本省）
# FORM：FaqListForm：FAQ一覧ページ（運用業者）
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：FaqModel：FAQモデル（Ｒ）
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def FaqListView(request, accountType, accountId, operationYear):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P40.FaqListView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ４０Ａ１０）
        # ブラウザからのリクエストと引数をチェックする。
        ##########################################
        print_log('[INFO] P40.FaqListView関数 P40A10', 'INFO')
        print_log('[INFO] P40.FaqListView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P40.FaqListView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P40.FaqListView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P40.FaqListView.operationYear = {}'.format(operationYear), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ４０Ａ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        if accountId == str(request.user.username):
            pass
        else:
            print_log('[WARN] P40.FaqListView関数 P40A20-0', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P40.FaqListView関数 P40A20-0', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P40.FaqListView関数 P40A20-1', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P40.FaqListView関数 P40A20-2', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P40.FaqListView関数 P40A20-3', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P40.FaqListView関数 P40A20-3', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理（Ｐ４０Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P40.FaqListView.method関数 P40A30', 'INFO')
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
            print_log('[ERROR] P40.FaqListView関数 P40A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P40FaqListView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P40FaqListView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P40.FaqListView関数 P40A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P40.FaqListView関数 P40A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理,FAQデータ（Ｐ４０Ａ４０）
        # （１）FAQデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、FAQデータを取得する。
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
        print_log('[INFO] P40.FaqListView関数 P40A40', 'INFO')
        # （１）FAQデータを格納する局所変数を初期化する。
        localCodeChousaGuideArray = ['1000', '1010', '1020', '1030', '1040', '1050', '1060', '1070', '1080', '1090', '1100', ]
        localCodeInputSystemArray = ['2000', '2010', '2020', '2030', '2040',]
        localNameChousaGuideArray = ['一般資産水害統計調査','被害区分の判断基準','水害発生年月日','水系・沿岸名、河川・海岸名','被害建物の延床面積','事業所従業者数','農作物被害額','水害区域図','公共土木施設水害統計調査','公益事業等水害統計調査','その他',]
        localNameInputSystemArray = ['起動方法','共通入力シート','提出用データの読み込み','提出用データの作成','入力システム等のダウンロード',]    
        localFaqRecentArray = None
        localFaqChousaGuideArray = []
        localFaqInputSystemArray = []
        for i in range(0, 11):
            localFaqChousaGuideArray.append([])
        for i in range(0, 5):
            localFaqInputSystemArray.append([])
        # （２）ＤＢにアクセスし、FAQデータを取得する。
        try:
            localFaqRecentArray = P40FaqModel.objects.raw("""
                SELECT 
                    T1.id As id,
                    T1.OPERATION_YEAR AS OPERATION_YEAR,
                    T1.FLOOD_YEAR AS FLOOD_YEAR,
                    T1.FAQ_NUMBER AS FAQ_NUMBER,
                    T1.CATEGORY_1_CODE AS CATEGORY_1_CODE,
                    T1.CATEGORY_2_CODE AS CATEGORY_2_CODE,
                    T2.CATEGORY_NAME AS CATEGORY_2_NAME,
                    T1.QUESTION_SUMMARY AS QUESTION_SUMMARY,
                    T1.QUESTION_BODY AS QUESTION_BODY,
                    T1.ANSWER_SUMMARY AS ANSWER_SUMMARY,
                    T1.ANSWER_BODY_1 AS ANSWER_BODY_1,
                    T1.ANSWER_BODY_2 AS ANSWER_BODY_2,
                    T1.ANSWER_BODY_3 AS ANSWER_BODY_3,
                    T1.ANSWER_BODY_4 AS ANSWER_BODY_4,
                    T1.ANSWER_BODY_5 AS ANSWER_BODY_5,
                    T1.ANSWER_BODY_6 AS ANSWER_BODY_6,
                    T1.ANSWER_BODY_7 AS ANSWER_BODY_7,
                    T1.ANSWER_BODY_8 AS ANSWER_BODY_8,
                    T1.ANSWER_BODY_9 AS ANSWER_BODY_9,
                    T1.ANSWER_BODY_10 AS ANSWER_BODY_10,
                    T1.ANSWER_BODY_11 AS ANSWER_BODY_11,
                    T1.ANSWER_BODY_12 AS ANSWER_BODY_12,
                    T1.ANSWER_BODY_13 AS ANSWER_BODY_13,
                    T1.MANUAL_PAGE AS MANUAL_PAGE,
                    T1.HTML_FILE_NAME AS HTML_FILE_NAME,
                    T1.DISPLAY_ORDER AS DISPLAY_ORDER,
                    T1.DELETE_FLAG AS DELETE_FLAG 
                FROM 
                    (SELECT * FROM FILE_UPLOAD_FAQ WHERE OPERATION_YEAR=%s AND CATEGORY_1_CODE=%s) T1 
                    LEFT OUTER JOIN 
                    (SELECT * FROM FILE_UPLOAD_FAQCATEGORY) T2
                    ON T1.CATEGORY_2_CODE=T2.CATEGORY_CODE 
                ORDER BY 
                    T1.CATEGORY_2_CODE, 
                    T1.DISPLAY_ORDER
                """,
                [operationYear, '0', ])
        except:
            localFaqRecentArray = None
            print_log('[ERROR] P40.FaqListView関数 P40A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P40.FaqListView関数で警告が発生しました。', 'ERROR')
        try:    
            for i in range(0, 11):
                localFaqChousaGuideArray[i] = P40FaqModel.objects.raw("""
                    SELECT 
                        T1.id As id,
                        T1.OPERATION_YEAR AS OPERATION_YEAR,
                        T1.FLOOD_YEAR AS FLOOD_YEAR,
                        T1.FAQ_NUMBER AS FAQ_NUMBER,
                        T1.CATEGORY_1_CODE AS CATEGORY_1_CODE,
                        T1.CATEGORY_2_CODE AS CATEGORY_2_CODE,
                        T2.CATEGORY_NAME AS CATEGORY_2_NAME,
                        T1.QUESTION_SUMMARY AS QUESTION_SUMMARY,
                        T1.QUESTION_BODY AS QUESTION_BODY,
                        T1.ANSWER_SUMMARY AS ANSWER_SUMMARY,
                        T1.ANSWER_BODY_1 AS ANSWER_BODY_1,
                        T1.ANSWER_BODY_2 AS ANSWER_BODY_2,
                        T1.ANSWER_BODY_3 AS ANSWER_BODY_3,
                        T1.ANSWER_BODY_4 AS ANSWER_BODY_4,
                        T1.ANSWER_BODY_5 AS ANSWER_BODY_5,
                        T1.ANSWER_BODY_6 AS ANSWER_BODY_6,
                        T1.ANSWER_BODY_7 AS ANSWER_BODY_7,
                        T1.ANSWER_BODY_8 AS ANSWER_BODY_8,
                        T1.ANSWER_BODY_9 AS ANSWER_BODY_9,
                        T1.ANSWER_BODY_10 AS ANSWER_BODY_10,
                        T1.ANSWER_BODY_11 AS ANSWER_BODY_11,
                        T1.ANSWER_BODY_12 AS ANSWER_BODY_12,
                        T1.ANSWER_BODY_13 AS ANSWER_BODY_13,
                        T1.MANUAL_PAGE AS MANUAL_PAGE,
                        T1.HTML_FILE_NAME AS HTML_FILE_NAME,
                        T1.DISPLAY_ORDER AS DISPLAY_ORDER,
                        T1.DELETE_FLAG AS DELETE_FLAG 
                    FROM 
                        (SELECT * FROM FILE_UPLOAD_FAQ WHERE OPERATION_YEAR=%s AND CATEGORY_1_CODE=%s AND CATEGORY_2_CODE=%s) T1 
                        LEFT OUTER JOIN 
                        (SELECT * FROM FILE_UPLOAD_FAQCATEGORY) T2
                        ON T1.CATEGORY_2_CODE=T2.CATEGORY_CODE 
                    ORDER BY 
                        T1.CATEGORY_2_CODE, 
                        T1.DISPLAY_ORDER
                    """,
                    [operationYear, '1', localCodeChousaGuideArray[i], ])
        except:
            for i in range(0, 11):
                localFaqChousaGuideArray[i] = None
            print_log('[ERROR] P40.FaqListView関数 P40A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P40.FaqListView関数で警告が発生しました。', 'ERROR')
        try:        
            for i in range(0, 5):        
                localFaqInputSystemArray[i] = P40FaqModel.objects.raw("""
                    SELECT 
                        T1.id As id,
                        T1.OPERATION_YEAR AS OPERATION_YEAR,
                        T1.FLOOD_YEAR AS FLOOD_YEAR,
                        T1.FAQ_NUMBER AS FAQ_NUMBER,
                        T1.CATEGORY_1_CODE AS CATEGORY_1_CODE,
                        T1.CATEGORY_2_CODE AS CATEGORY_2_CODE,
                        T2.CATEGORY_NAME AS CATEGORY_2_NAME,
                        T1.QUESTION_SUMMARY AS QUESTION_SUMMARY,
                        T1.QUESTION_BODY AS QUESTION_BODY,
                        T1.ANSWER_SUMMARY AS ANSWER_SUMMARY,
                        T1.ANSWER_BODY_1 AS ANSWER_BODY_1,
                        T1.ANSWER_BODY_2 AS ANSWER_BODY_2,
                        T1.ANSWER_BODY_3 AS ANSWER_BODY_3,
                        T1.ANSWER_BODY_4 AS ANSWER_BODY_4,
                        T1.ANSWER_BODY_5 AS ANSWER_BODY_5,
                        T1.ANSWER_BODY_6 AS ANSWER_BODY_6,
                        T1.ANSWER_BODY_7 AS ANSWER_BODY_7,
                        T1.ANSWER_BODY_8 AS ANSWER_BODY_8,
                        T1.ANSWER_BODY_9 AS ANSWER_BODY_9,
                        T1.ANSWER_BODY_10 AS ANSWER_BODY_10,
                        T1.ANSWER_BODY_11 AS ANSWER_BODY_11,
                        T1.ANSWER_BODY_12 AS ANSWER_BODY_12,
                        T1.ANSWER_BODY_13 AS ANSWER_BODY_13,
                        T1.MANUAL_PAGE AS MANUAL_PAGE,
                        T1.HTML_FILE_NAME AS HTML_FILE_NAME,
                        T1.DISPLAY_ORDER AS DISPLAY_ORDER,
                        T1.DELETE_FLAG AS DELETE_FLAG 
                    FROM 
                        (SELECT * FROM FILE_UPLOAD_FAQ WHERE OPERATION_YEAR=%s AND CATEGORY_1_CODE=%s AND CATEGORY_2_CODE=%s) T1 
                        LEFT OUTER JOIN 
                        (SELECT * FROM FILE_UPLOAD_FAQCATEGORY) T2
                        ON T1.CATEGORY_2_CODE=T2.CATEGORY_CODE 
                    ORDER BY 
                        T1.CATEGORY_2_CODE, 
                        T1.DISPLAY_ORDER
                    """,
                    [operationYear, '2', localCodeInputSystemArray[i], ])
        except:
            for i in range(0, 5):
                localFaqInputSystemArray[i] = None
            print_log('[ERROR] P40.FaqListView関数 P10A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P40.FaqListView関数で警告が発生しました。', 'ERROR')
        ##########################################
        # フォームセット処理（Ｐ４０Ａ５０）
        # （１）局所変数のフォームを初期化する。
        ##########################################
        print_log('[INFO] P40.FaqListView関数 P40A50', 'INFO')
        ##########################################
        # レスポンスセット処理（Ｐ４０Ａ６０）
        # （１）アレイの件数を計算する。
        # （２）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        ##########################################
        print_log('[INFO] P40.FaqListView関数 P40A60', 'INFO')
        # （１）アレイの件数を計算する。
        if localNameChousaGuideArray != None:
            localNameChousaGuideLength = len(list(localNameChousaGuideArray))
        else:
            localNameChousaGuideLength = 0    
        if localNameInputSystemArray != None:
            localNameInputSystemLength = len(list(localNameInputSystemArray))
        else:
            localNameInputSystemLength = 0
        if localFaqRecentArray != None:    
            localFaqRecentLength = len(list(localFaqRecentArray))
        else:
            localFaqRecentLength = 0
        if localFaqChousaGuideArray != None:        
            localFaqChousaGuideLength = len(list(localFaqChousaGuideArray))
        else:
            localFaqChousaGuideLength = 0
        if localFaqInputSystemArray != None:        
            localFaqInputSystemLength = len(list(localFaqInputSystemArray))
        else:
            localFaqInputSystemLength = 0    
        # （２）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝都道府県の場合、、、
            response = {
                'accountType': 1,                                        # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': accountId,                                  # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': True,                                           # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                                          # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                                          # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': operationYear,                          # 調査実施年
                'message': 'message',                                    # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'categoryChousaGuideArray': localNameChousaGuideArray,   # 調査ガイド、種別名一覧
                'categoryChousaGuideLength': localNameChousaGuideLength, # 調査ガイド、種別名一覧の件数 
                'categoryInputSystemArray': localNameInputSystemArray,   # 入力システムガイド、種別名一覧
                'categoryInputSystemLength': localNameInputSystemLength, # 入力システムガイド、種別名一覧の件数
                'faqRecentArray': localFaqRecentArray,                   # 最近の問合せ一覧
                'faqRecentLength': localFaqRecentLength,                 # 最近の問合せ一覧の件数
                'faqChousaGuideArray': localFaqChousaGuideArray,         # 調査ガイド問合せ一覧
                'faqChousaGuideLength': localFaqChousaGuideLength,       # 調査ガイド問合せ一覧の件数
                'faqInputSystemArray': localFaqInputSystemArray,         # 入力システムガイド問合せ一覧
                'faqInputSystemLength': localFaqInputSystemLength,       # 入力システムガイド問合せ一覧の件数
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝本省の場合、、、
            response = {
                'accountType': 2,                                        # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': accountId,                                  # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                                          # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                                           # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                                          # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': operationYear,                          # 調査実施年
                'message': 'message',                                    # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'categoryChousaGuideArray': localNameChousaGuideArray,   # 調査ガイド、種別名一覧
                'categoryChousaGuideLength': localNameChousaGuideLength, # 調査ガイド、種別名一覧の件数 
                'categoryInputSystemArray': localNameInputSystemArray,   # 入力システムガイド、種別名一覧
                'categoryInputSystemLength': localNameInputSystemLength, # 入力システムガイド、種別名一覧の件数
                'faqRecentArray': localFaqRecentArray,                   # 最近の問合せ一覧
                'faqRecentLength': localFaqRecentLength,                 # 最近の問合せ一覧の件数
                'faqChousaGuideArray': localFaqChousaGuideArray,         # 調査ガイド問合せ一覧
                'faqChousaGuideLength': localFaqChousaGuideLength,       # 調査ガイド問合せ一覧の件数
                'faqInputSystemArray': localFaqInputSystemArray,         # 入力システムガイド問合せ一覧
                'faqInputSystemLength': localFaqInputSystemLength,       # 入力システムガイド問合せ一覧の件数
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝運用業者の場合、、、
            response = {
                'accountType': 3,                                        # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': accountId,                                  # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                                          # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                                          # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': True,                                           # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': operationYear,                          # 調査実施年
                'message': 'message',                                    # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'categoryChousaGuideArray': localNameChousaGuideArray,   # 調査ガイド、種別名一覧
                'categoryChousaGuideLength': localNameChousaGuideLength, # 調査ガイド、種別名一覧の件数 
                'categoryInputSystemArray': localNameInputSystemArray,   # 入力システムガイド、種別名一覧
                'categoryInputSystemLength': localNameInputSystemLength, # 入力システムガイド、種別名一覧の件数
                'faqRecentArray': localFaqRecentArray,                   # 最近の問合せ一覧
                'faqRecentLength': localFaqRecentLength,                 # 最近の問合せ一覧の件数
                'faqChousaGuideArray': localFaqChousaGuideArray,         # 調査ガイド問合せ一覧
                'faqChousaGuideLength': localFaqChousaGuideLength,       # 調査ガイド問合せ一覧の件数
                'faqInputSystemArray': localFaqInputSystemArray,         # 入力システムガイド問合せ一覧
                'faqInputSystemLength': localFaqInputSystemLength,       # 入力システムガイド問合せ一覧の件数
            }
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P40.FaqListView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P40.FaqListView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P40.FaqListView関数が正常終了しました。', 'INFO')
        ##########################################
        # 戻り値セット処理（Ｐ４０Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P40.FaqListView関数 P40A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝都道府県の場合、、、
            return render(request, 'P40FaqListTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝本省の場合、、、
            return render(request, 'P40FaqListTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝運用業者の場合、、、
            return render(request, 'P40FaqListTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P40.FaqListView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P40.FaqListView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ４０Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P40.FaqListView関数 P40A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P40.FaqListView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P40.FaqListView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ４０Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P40.FaqListView関数 P40A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
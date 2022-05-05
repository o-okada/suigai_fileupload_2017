#####################################################################################
# TopViewビューモジュール【ほぼ完成】
# ファイル ：P02.TopView.py（Ｐ０２）
# ユースケース：都道府県の担当者は、お知らせを閲覧する。
# ユースケース：本省の担当者は、お知らせを閲覧する。
# ユースケース：運用業者の担当者は、お知らせを閲覧する。
# ユースケース：都道府県の担当者は、メニューから都道府県用水害統計オンライン登録サイト、都道府県用水害統計問合せ対応サイト、FAQサイトのいずれかを選択する。
# ユースケース：本省のの担当者は、メニューから本省用水害統計オンライン登録サイト、本省用水害統計問合せ対応サイト、FAQサイトのいずれかを選択する。
# ユースケース：運用業者の担当者は、メニューから運用業者用水害統計オンライン登録サイト、運用業者用水害統計問合せ対応サイト、FAQサイトのいずれかを選択する。
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
#####################################################################################
import sys                                                 # sysモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：ジャンゴモジュールをインポートする。
# login_required：VIEW関数毎に、ログインの有無でフィルタリングするために使用する。
# render：VIEW関数の戻り値をブラウザに戻すために使用する。
# urlquote：
#####################################################################################
from django.contrib.auth.decorators import login_required  # ログイン制御モジュール
from django.shortcuts import render                        # レンダリングモジュール
from django.utils.http import urlquote                     # URLエスケープモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# AccountModel：
# InfoModel：
# print_log：
#####################################################################################
from file_upload.models import AccountModel                # アカウントモデル
from file_upload.models import InfoModel                   # お知らせモデル
from file_upload.CommonFunction import print_log           # ログ出力モジュール
#####################################################################################
# 関数名：P02.TopView（Ｐ０２Ａ）
# 関数概要：都道府県用トップページをブラウザに戻す。
#
# 引数[1]：request：
# 引数[2]：accountType：ログインした人の区分・種別に応じてDBから取得するデータ、ブラウザに戻すデータを制御するために使用する。
# ※１：都道府県担当者、２：本省担当者、３：運用業者担当者
# 引数[3]：accountId：
# 引数[4]：operationYear：複数年度の情報を消去せずに処理可能とするために使用する。
#
# 戻り値[1]：response：
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def TopView(request, accountType, accountId, operationYear):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P02.TopView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ０２Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P02.TopView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P02.TopView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P02.TopView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P02.TopView.operationYear = {}'.format(operationYear), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ０２Ａ２０）
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
            print_log('[WARN] P02.TopView関数 P02A20-0', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P02.TopView関数 P02A20-0', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P02.TopView関数 P02A20-1', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P02.TopView関数 P02A20-2', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P02.TopView関数 P02A20-3', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P02.TopView関数 P02A20-3', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ０２Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P02.TopView関数 P02A30', 'INFO')
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # ヒント：ＳＱＬ文でエラーが発生した場合、戻り値のアカウントモデルの局所変数をNoneにセットする。
        # ヒント：理由は、ＳＱＬ文でエラーが発生し、正しく処理を継続できないことを以降の処理に対して示すためである。
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
            print_log('[ERROR] P02.TopView関数 P02A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P02.TopView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P02.TopView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウントデータが存在することをチェックする。         
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P02.TopView関数 P02A30', 'WARN')
            print_log('[WARN] localAcountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P02.TopView関数 P02A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、お知らせ一覧取得処理（Ｐ０２Ａ４０）
        # （１）お知らせ一覧を格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、お知らせの一覧を取得する。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        # ヒント：rawでＤＢにアクセスした場合、検索結果が０件の場合、エクセプションが発生する。
        # ヒント：後々の拡張等を考慮し、場合分けをベタで記述し、明示されていないロジックを含まないコードとするため、
        # ヒント：あえて冗長な場合分けをしている。
        ##########################################
        print('[INFO] P02.TopView関数P02A40', 'INFO')
        # （１）お知らせ一覧を格納する局所変数を初期化する。
        localInfoArray = None
        # （２）ＤＢにアクセスし、お知らせの一覧を取得する。
        try:
            if accountType == '1':
                # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
                # ヒント：お知らせは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                try:
                    localInfoArray = InfoModel.objects.raw("""
                        SELECT 
                            * 
                        FROM 
                            FILE_UPLOAD_INFO 
                        WHERE 
                            OPERATION_YEAR=%s 
                        ORDER BY 
                            CAST(DISPLAY_ORDER AS INTEGER) 
                        """,
                        [ operationYear, ])
                except:
                    localInfoArray = None
                    print_log('[ERROR] P02.TopView関数 P02A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P02.TopView関数で警告が発生しました。', 'ERROR')
            elif accountType == '2':
                # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
                # ヒント：お知らせは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                try:
                    localInfoArray = InfoModel.objects.raw("""
                        SELECT 
                            * 
                        FROM 
                            FILE_UPLOAD_INFO 
                        WHERE 
                            OPERATION_YEAR=%s 
                        ORDER BY 
                            CAST(DISPLAY_ORDER AS INTEGER) 
                        """,
                        [ operationYear, ])
                except:
                    localInfoArray = None
                    print_log('[ERROR] P02.TopView関数 P02A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P02.TopView関数で警告が発生しました。', 'ERROR')
            elif accountType == '3':
                # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
                # ヒント：お知らせは０件もあり得るとして、ＳＱＬ文でエラーが発生した場合でも、処理を継続させると想定する。
                try:
                    localInfoArray = InfoModel.objects.raw("""
                        SELECT 
                            * 
                        FROM 
                            FILE_UPLOAD_INFO 
                        WHERE 
                            OPERATION_YEAR=%s 
                        ORDER BY 
                            CAST(DISPLAY_ORDER AS INTEGER) 
                        """,
                        [ operationYear, ])
                except:
                    localInfoArray = None    
                    print_log('[ERROR] P02.TopView関数 P02A40', 'ERROR')
                    print_log(sys.exc_info()[0], 'ERROR')
                    print_log('[ERROR] P02.TopView関数で警告が発生しました。', 'ERROR')
            else:
                # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
                print_log('[ERROR] P02.TopView関数で異常が発生しました。', 'ERROR')
                print_log('[ERROR] P02.TopView関数を異常終了しました。', 'ERROR')
                return render(request, 'error.html')
        except:
            print_log('[ERROR] P02.TopView関数 P02A40', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P02.TopView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P02.TopView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # フォームセット処理（Ｐ０２Ａ５０）
        # （１）局所変数のフォームを初期化する。
        # ヒント：ブラウザとのデータのやりとり、特にブラウザからPOSTデータがある場合、フォームを使用する。
        # ヒント：モデルはブラウザで参照用、かつタグをコーディングする場合等に使用する。
        # ヒント：フォームはブラウザで編集用、POSTでサーバにリクエストされる項目、かつタグを自動生成する場合等に使用する。
        ##########################################
        print_log('[INFO] P02.TopView関数 P02A50', 'INFO')
        # （１）局所変数のフォームを初期化する。
        ##########################################
        # レスポンスセット処理（Ｐ０２Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        ##########################################
        print_log('[INFO] P02.TopView関数 P02A60', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        # ヒント：お知らせ一覧が０件の場合でも、正しくトップページが表示されると想定する。
        # ヒント：０件でも正常とする。テンプレートで０件の場合でも正しく処理できること。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            response = {
                'accountType'  : 1,                        # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId'    : urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen'        : True,                     # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。                    
                'isHon'        : False,                    # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe'        : False,                    # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message'      : 'message',                # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'infoArray'    : localInfoArray,           # お知らせ一覧
                'infoLength'   : len(list(localInfoArray)),# お知らせ一覧の件数
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            response = {
                'accountType'  : 2,                        # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId'    : urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen'        : False,                    # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。     
                'isHon'        : True,                     # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe'        : False,                    # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message'      : 'message',                # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'infoArray'    : localInfoArray,           # お知らせ一覧
                'infoLength'   : len(list(localInfoArray)),# お知らせ一覧の件数
            }
        elif accountType == '3':    
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            response = {
                'accountType'  : 3,                        # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId'    : urlquote(accountId),      # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen'        : False,                    # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。     
                'isHon'        : False,                    # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe'        : True,                     # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': urlquote(operationYear),  # 調査実施年
                'message'      : 'message',                # ブラウザに表示するメッセージを必要に応じてここにセットする。
                'infoArray'    : localInfoArray,           # お知らせ一覧
                'infoLength'   : len(list(localInfoArray)),# お知らせ一覧の件数
            }
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P02.TopView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P02.TopView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P02.TopView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ０２Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P02.TopView関数 P02A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝１：都道府県の場合、、、
            return render(request, 'P02TopTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝２：本省の場合、、、
            return render(request, 'P02TopTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝３：運用業者の場合、、、
            return render(request, 'P02TopTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P02.TopView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P02.TopView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ０２Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P02.TopView関数 P02A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P02.TopView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P02.TopView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング、戻り値セット処理（Ｐ０２Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P02.TopView関数 P02A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
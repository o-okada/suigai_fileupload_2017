#####################################################################################
# RdfViewビューモジュール【ほぼ完成】
# ファイル名：P42.RdfView.py（Ｐ４２）
# ユースケース：都道府県は、RSSの一覧を閲覧する。
# ユースケース：本省は、RSSの一覧を閲覧する。
# ユースケース：運用業者は、RSSの一覧を閲覧する。
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
# HttpResponse
# render
# urlquote
#####################################################################################
from django.contrib.auth.decorators import login_required  # ログイン制御モジュール
###from django.http.response import HttpResponse           # HTTPレスポンスモジュール
from django.shortcuts import render                        # レンダリングモジュール
from django.utils.http import urlquote                     # URLエスケープモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# AccountModel
# RssModel
# print_log
#####################################################################################
from file_upload.models import AccountModel                # アカウントデータモデル
from file_upload.models import RssModel                    # RSSデータ・モデル
from file_upload.CommonFunction import print_log           # ログ出力モジュール
#####################################################################################
# 関数名：P42.RdfView（Ｐ４２Ａ）
# 関数概要：RSS購読、RSS一覧ページをブラウザに戻す。（都道府県）
# 関数概要：RSS購読、RSS一覧ページをブラウザに戻す。（本省）
# 関数概要：RSS購読、RSS一覧ページをブラウザに戻す。（運用業者）
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
# MODEL：AccountModel：アカウントモデル（Ｒ）
# MODEL：RssModel：RSSモデル（Ｒ）
# ヒント：FireFox　Live Bookmark等からアクセスされるため、ビュー関数へのアクセスは未ログインでも可能とする。
# ヒント：ただし、アカウントＩＤ毎に異なるコンテンツを提供するため、クエリストリングは必要です。
#####################################################################################
###@login_required(None, login_url='/file_upload/P01/Login/')
def RdfView(request, accountType, accountId, operationYear):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P42.RdfView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ４２Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P42.RdfView関数 P42A10', 'INFO')
        print_log('[INFO] P42.RdfView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P42.RdfView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P42.RdfView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P42.RdfView.operationYear = {}'.format(operationYear), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ４２Ａ２０）
        # （１）アカウントＩＤをチェックする。　例　01hokkai
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        # （５）調査実施年をチェックする。　例　2016
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        # ヒント：FireFox　Live Bookmark等からアクセスされるため、ビュー関数へのアクセスは未ログインでも可能とする。
        # ヒント：ただし、アカウントＩＤ毎に異なるコンテンツを提供するため、クエリストリングは必要です。
        ##########################################
        #### （１）アカウントＩＤをチェックする。　例　01hokkai
        ###if accountId == str(request.user.username):
        ###    pass
        ###else:
        ###    print_log('[WARN] P42.RdfView関数 P42A20-1', 'WARN')
        ###    return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P42.RdfView関数 P42A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P42.RdfView関数 P42A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P42.RdfView関数 P42A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P42.RdfView関数 P42A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P42.RdfView関数 P42A20-5', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ４２Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P42.RdfView.method関数 P42A30', 'INFO')
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
            print_log('[ERROR] P42.RdfView関数 P42A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P42RdfView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P42RdfView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
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
            print_log('[WARN] P42.RdfView関数 P42A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、RSSデータ取得処理（Ｐ４２Ａ４０）
        # （１）RSSデータを格納する局所変数を初期化する。
        # （２）ＤＢにアクセスし、RSSデータを取得する。
        # ヒント：ＤＢアクセスは別途try～exceptする。
        ##########################################
        print_log('[INFO] P42.RdfView関数 P42A40', 'INFO')
        # （１）RSSデータを格納する局所変数を初期化する。
        localRssArray = None
        # （２）ＤＢにアクセスし、RSSデータを取得する。
        try:
            localRssArray = RssModel.objects.raw("""
                SELECT 
                    * 
                FROM 
                    FILE_UPLOAD_RSS 
                WHERE 
                    OPERATION_YEAR=%s AND 
                    TO_ACCOUNT_ID=%s 
                ORDER BY 
                    ADD_DATE 
                LIMIT 5
                """, 
                [operationYear, accountId, ])
        except:
            localRssArray = None
            print_log('[ERROR] P42.RdfView関数 P42A40', 'ERROR')
            print_log(sys.exc_info()[0],'ERROR')
            print_log('[ERROR] P42.RdfView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P42.RdfView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # フォームセット処理（Ｐ４２Ａ５０）
        # （１）局所変数のフォームを初期化する。
        ##########################################
        print_log('[INFO] P42.RdfView関数 P42A50', 'INFO')
        ##########################################
        # レスポンスセットト処理（Ｐ４２Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        ##########################################
        print_log('[INFO] P42.RdfView関数P42A60', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝都道府県の場合、、、
            if localRssArray != None:
                response = {
                    'accountType': 1,
                    'accountId': accountId,
                    'isKen': True,
                    'isHon': False,
                    'isOpe': False,
                    'operationYear': operationYear,
                    'message': 'message',
                    'rssArray': localRssArray,
                    'rssLength': len(list(localRssArray)),
                }
            else:
                response = {
                    'accountType': 1,
                    'accountId': accountId,
                    'isKen': True,
                    'isHon': False,
                    'isOpe': False,
                    'operationYear': operationYear,
                    'message': 'message',
                    'rssArray': localRssArray,
                    'rssLength': 0,
                }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝本省の場合、、、
            if localRssArray != None:
                response = {
                    'accountType': 2,
                    'accountId': accountId,
                    'isKen': False,
                    'isHon': True,
                    'isOpe': False,
                    'operationYear': operationYear,
                    'message': 'message',
                    'rssArray': localRssArray,
                    'rssLength': len(list(localRssArray)),
                }
            else:
                response = {
                    'accountType': 2,
                    'accountId': accountId,
                    'isKen': False,
                    'isHon': True,
                    'isOpe': False,
                    'operationYear': operationYear,
                    'message': 'message',
                    'rssArray': localRssArray,
                    'rssLength': 0,
                }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝運用業者の場合、、、
            if localRssArray != None:
                response = {
                    'accountType': 3,
                    'accountId': accountId,
                    'isKen': False,
                    'isHon': False,
                    'isOpe': True,
                    'operationYear': operationYear,
                    'message': 'message',
                    'rssArray': localRssArray,
                    'rssLength': len(list(localRssArray)),
                }
            else:    
                response = {
                    'accountType': 3,
                    'accountId': accountId,
                    'isKen': False,
                    'isHon': False,
                    'isOpe': True,
                    'operationYear': operationYear,
                    'message': 'message',
                    'rssArray': localRssArray,
                    'rssLength': 0,
                }
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P42.RdfView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P42.RdfView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P42.RdfView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ４２Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P42.RdfView関数 P42A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝都道府県の場合、、、
            return render(request, 'P42RdfTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝本省の場合、、、
            return render(request, 'P42RdfTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝運用業者の場合、、、
            return render(request, 'P42RdfTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P42.RdfView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P42.RdfView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ４２Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P42.RdfView関数 P42A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P42.RdfView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P42.RdfView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ４２Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P42.RdfView関数 P42A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
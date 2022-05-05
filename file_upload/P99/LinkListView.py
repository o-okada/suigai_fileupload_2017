#####################################################################################
# LinkListViewビューモジュール【ほぼ完成】
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
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# AccountModel
# print_log
#####################################################################################
from file_upload.models import AccountModel                # アカウントデータ・モデル
from file_upload.CommonFunction import print_log           # ログ出力モジュール
#####################################################################################
# 関数名：P99.LinkListView（Ｐ９９Ａ）
# 関数概要：リンク一覧ページをブラウザに戻す。（都道府県）
# 関数概要：リンク一覧ページをブラウザに戻す。（本省）
# 関数概要：リンク一覧ページをブラウザに戻す。（運用業者）
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
# FORM：LinkListForm：リンク一覧ページ（都道府県）
# FORM：LinkListForm：リンク一覧ページ（本省）
# FORM：LinkListForm：リンク一覧ページ（運用業者）
#####################################################################################
@login_required(None, login_url='/file_upload/P01/Login/')
def LinkListView(request, accountType, accountId, operationYear):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P99.LinkListView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ９９Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        # （１）ブラウザからのリクエストと引数をチェックする。
        print_log('[INFO] P99.LinkListView関数 P99A10', 'INFO')
        print_log('[INFO] P99.LinkListView.method = {}'.format(request.method), 'INFO')
        print_log('[INFO] P99.LinkListView.accountType = {}'.format(accountType), 'INFO')
        print_log('[INFO] P99.LinkListView.accountId = {}'.format(accountId), 'INFO')
        print_log('[INFO] P99.LinkListView.operationYear = {}'.format(operationYear), 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ９９Ａ２０）
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
            print_log('[WARN] P99.LinkListView関数 P99A20-1', 'WARN')
            return render(request, 'error.html')
        # （２）リクエストメソッドをチェックする。　例　GET、POST
        if request.method == 'GET':
            pass
        else:
            print_log('[WARN] P99.LinkListView関数 P99A20-2', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別をチェックする。　例　１：都道府県、２：本省、３：運用業者
        if accountType == '1' or accountType == '2' or accountType == '3':
            pass
        else:
            print_log('[WARN] P99.LinkListView関数 P99A20-3', 'WARN')
            return render(request, 'error.html')
        # （４）アカウントＩＤをチェックする。　例　01hokkai
        if accountId is None:
            print_log('[WARN] P99.LinkListView関数 P99A20-4', 'WARN')
            return render(request, 'error.html')
        else:
            pass
        # （５）調査実施年をチェックする。　例　2016
        if operationYear is None:
            print_log('[WARN] P99.LinkListView関数 P99A20-5', 'WARN')
            return render(request, 'error.html')
        else:
            if str.isdigit(operationYear) == True:
                pass
            else:
                print_log('[WARN] P99.LinkListView関数 P99A20-5', 'WARN')
                return render(request, 'error.html')
        ##########################################
        # 引数チェック処理、ＤＢアクセス処理（Ｐ９９Ａ３０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値をチェックする。
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P99.LinkListView.method関数 P99A30', 'INFO')
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        localAccountModel = None
        try:
            localAccountModel = AccountModel.objects.raw("""
                SELECT * FROM file_upload_account 
                WHERE ACCOUNT_ID=%s AND OPERATION_YEAR=%s LIMIT 1
                """, 
                [accountId, operationYear, ])[0]
        except:
            localAccountModel = None
            print_log('[ERROR] P99.LinkListView関数 P99A30', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P99.LinkListView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P99.LinkListView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        # （２）ＤＢからの戻り値をチェックする。
        # ヒント：アカウント情報が存在することをチェックする。
        if localAccountModel != None:
            pass
        else:
            print_log('[WARN] P99.LinkListView関数P99A30', 'WARN')
            print_log('[WARN] localAccountModel is NULL', 'WARN')
            return render(request, 'error.html')
        # （３）アカウント種別がアカウントデータのアカウント種別と同じことをチェックする。
        if accountType == localAccountModel.ACCOUNT_TYPE:
            pass
        else:
            print_log('[WARN] P99.LinkListView関数 P99A30', 'WARN')
            print_log('[WARN] accountType != localAcountModel.ACCOUNT_TYPE', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # レスポンスセット処理（Ｐ９９Ａ６０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        ##########################################
        print_log('[INFO] P99.LinkListView関数 P99A60', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝都道府県の場合、、、
            response = {
                'accountType': 1,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': accountId,                    # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': True,                             # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': operationYear,            # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
            }
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝本省の場合、、、
            response = {
                'accountType': 2,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': accountId,                    # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': True,                             # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': False,                            # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': operationYear,            # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
            }
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝運用業者の場合、、、
            response = {
                'accountType': 3,                          # アカウント種別、レンダリング時の分岐、URLのクエリストリングに使用する。
                'accountId': accountId,                    # アカウントＩＤ、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isKen': False,                            # アカウント種別、都道府県、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isHon': False,                            # アカウント種別、本省、レンダリング時の分岐、URLのクエリストリングに使用する。
                'isOpe': True,                             # アカウント種別、運用業者、レンダリング時の分岐、URLのクエリストリングに使用する。
                'operationYear': operationYear,            # 調査実施年
                'message': 'message',                      # ブラウザに表示するメッセージを必要に応じてここにセットする。
            }
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P99.LinkListView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P99.LinkListView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
        print_log('[INFO] P99.LinkListView関数が正常終了しました。', 'INFO')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ９９Ａ７０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[INFO] P99.LinkListView関数 P99A70', 'INFO')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        if accountType == '1':
            # ログインした利用者のアカウント種別・区分＝都道府県の場合、、、
            return render(request, 'P99LinkListTemplate.html', response)
        elif accountType == '2':
            # ログインした利用者のアカウント種別・区分＝本省の場合、、、
            return render(request, 'P99LinkListTemplate.html', response)
        elif accountType == '3':
            # ログインした利用者のアカウント種別・区分＝運用業者の場合、、、
            return render(request, 'P99LinkListTemplate.html', response)
        else:
            # ログインした利用者のアカウント種別・区分＝上記以外の場合、、、
            print_log('[ERROR] P99.LinkListView関数で異常が発生しました。', 'ERROR')
            print_log('[ERROR] P99.LinkListView関数を異常終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ９９Ａ８０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P99.LinkListView関数 P99A80', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P99.LinkListView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P99.LinkListView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ９９Ａ９０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P99.LinkListView関数 P99A90', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
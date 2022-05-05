#####################################################################################
# LoginViewビューモジュール【ほぼ完成】
# ファイル：P01.LoginView.py（Ｐ０１）
# ユースケース：都道府県の担当者は、ユーザID、パスワードを入力してログインする。
# ユースケース：本省の担当者は、ユーザID、パスワードを入力してログインする。
# ユースケース：運用業者の担当者は、ユーザID、パスワードを入力してログインする。
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
# authenticate
# login
# logout
# HttpResponseRedirect
# render
# urlquote
#####################################################################################
from django.contrib.auth import authenticate               # 認証モジュール
from django.contrib.auth import login                      # ログインもジール
from django.contrib.auth import logout                     # ログアウトモジュール
from django.http import HttpResponseRedirect               # URLリダイレクトモジュール
from django.shortcuts import render                        # レンダリングモジュール
from django.utils.http import urlquote                     # URLエスケープモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
# AccountModel
# print_log
#####################################################################################
from file_upload.models import AccountModel                # アカウントモデル
from file_upload.CommonFunction import print_log           # ログ出力モジュール
#####################################################################################
# 関数名：P01.LoginView（Ｐ０１Ａ）
# 関数概要：都道府県用ログインページをブラウザに戻す。（都道府県）
# 関数概要：本省用ログインページをブラウザに戻す。（本省）
# 関数概要：運用業者用ログインページをブラウザに戻す。（運用業者）
#
# 引数[1]：request：
#
# 戻り値[1]：response：
#####################################################################################
def LoginView(request):
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] P01.LoginView関数が開始しました。', 'INFO')
        ##########################################
        # 引数チェック処理（Ｐ０１Ａ１０）
        # （１）ブラウザからのリクエストと引数をチェックする。
        ##########################################
        print_log('[INFO] P01.LoginView関数 P01A10', 'INFO')
        print_log('[INFO] P01.LoginView.method = {}'.format(request.method), 'INFO')
        ##########################################
        # ログインログアウト処理（Ｐ０１Ａ２０）
        # （１）ログイン中、ログアウト中によらず、ログアウトする。
        # ヒント：ログアウトに失敗した場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）ログイン中、ログアウト中によらず、ログアウトする。
        try:
            logout(request)
        except:
            print_log('[ERROR] P01.LoginView関数 P01A20', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P01.LoginView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P01.LoginView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # 引数チェック処理（Ｐ０１Ａ３０）
        # （１）リクエストメソッドをチェックする。
        # ヒント：チェックに引っかかった場合、エラー画面をブラウザに戻す。
        ##########################################
        # （１）リクエストメソッドをチェックする。
        if request.method == 'GET':
            print_log('[INFO] P01.LoginView関数 P01A30-0', 'INFO')
            return render(request, 'P01LoginTemplate.html')
        elif request.method == 'POST':
            pass
        else:
            print_log('[WARN] P01.LoginView関数 P01A30-0', 'WARN')
            return render(request, 'error.html')
        ##########################################
        # 変数初期化処理（Ｐ０１Ａ４０）
        # （１）局所変数に初期値をセットする。
        ##########################################
        print_log('[INFO] P01.LoginView関数P01A40', 'INFO')
        # （１）局所変数に初期値をセットする。
        localUserName = ''                                 # ユーザ名＝ログインＩＤ＝アカウント名＝ＩＤ＝アカウントID
        localPassword = ''                                 # ユーザパスワード＝ログインパスワード＝パスワード＝アカウントパスワード
        ##########################################
        # ポスト文字列取得、変数セット処理（Ｐ０１Ａ５０）
        # （１）POSTされたユーザ名、ユーザパスワードを局所変数にセットする。
        # ヒント：ポスト文字列取得に失敗した場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P01.LoginView関数P01A50', 'INFO')
        # （１）POSTされたユーザ名、ユーザパスワードを局所変数にセットする。
        try:
            localUserName = request.POST['username']
            localPassword = request.POST['password']
        except:
            print_log('[ERROR] P01.LoginView関数 P01A50', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P01.LoginView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P01.LoginView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ログインログアウト処理（Ｐ０１Ａ６０）
        # （１）ユーザ名、ユーザパスワードを引数に認証関数をコールする。
        # ヒント：認証関数コールに失敗した場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P01.LoginView関数 P01A60', 'INFO')
        # （１）ユーザ名、ユーザパスワードを引数に認証関数をコールする。
        try:
            localUser = authenticate(username=localUserName, password=localPassword)
        except:
            print_log('[ERROR] P01.LoginView関数 P01A60', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P01.LoginView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P01.LoginView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ログインログアウト処理（Ｐ０１Ａ７０）
        # （１）ユーザ、パスワードが正常、つまり認証に成功、かつ活性（有効）の場合、ログイン関数をコールする。
        # （２）ユーザ、パスワードが異常、つまり認証に失敗、または非活性（無効）の場合、何もしない。
        # ヒント：ログイン関数コールに失敗した場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P01.LoginView関数 P01A70', 'INFO')
        # （１）ユーザ、パスワードが正常、つまり認証に成功、かつ活性（有効）の場合、ログイン関数をコールする。
        # （２）ユーザ、パスワードが異常、つまり認証に失敗、または非活性（無効）の場合、何もしない。
        try:
            if localUser is not None:
                # 認証に成功した場合、、、
                if localUser.is_active:
                    # ユーザが活性（有効）の場合、、、
                    login(request, localUser)
                else:
                    # ユーザが非活性（無効）の場合、、、
                    pass
            else:
                # 認証に失敗した場合、、、
                pass
        except:
            print_log('[ERROR] P01.LoginView関数 P01A70', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P01.LoginView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P01.LoginView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # ＤＢアクセス処理、変数セット処理（Ｐ０１Ａ８０）
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値を局所変数にセットする。
        # ヒント：処理中二エラーが発生した場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P01.LoginView関数 P01A80', 'INFO')
        # （１）ＤＢにアクセスし、アカウントデータを取得する。
        # （２）ＤＢからの戻り値を局所変数にセットする。
        localAccountModel = None
        try:
            if localUser is not None:
                # 認証に成功した場合、、、
                if localUser.is_active:
                    # ユーザが活性（有効）の場合、、、
                    localAccountModel = AccountModel.objects.raw("""
                        SELECT 
                            * 
                        FROM 
                            FILE_UPLOAD_ACCOUNT 
                        WHERE 
                            ACCOUNT_ID=%s 
                        LIMIT 1
                        """, 
                        [ localUserName, ])[0]
                else:
                    # ユーザが非活性（無効）の場合、、、
                    pass
            else:
                #　認証に失敗した場合、、、
                pass
        except:
            print_log('[ERROR] P01.LoginView関数 P01A80', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P01.LoginView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P01.LoginView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
        ##########################################
        # レスポンスセット処理（Ｐ０１Ａ９０）
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        ##########################################
        print_log('[INFO] P01.LoginView関数 P01A90', 'INFO')
        # （１）局所変数のレスポンス変数にブラウザに送付するデータをセットする。
        if localUser is not None:
            # 認証に成功した場合、、、
            if localUser.is_active:
                # ユーザが活性（有効）の場合、、、
                pass
            else:
                # ユーザが非活性（無効）の場合、、、
                response = {
                    'message': 'ログインに失敗しました。',
                }
        else:
            # 認証に失敗した場合、、、
            response = {
                'message': 'ログインに失敗しました。',
            }
        print_log('[INFO] P01.LoginView関数が正常終了しました。', 'INFO')
        ##########################################
        # HTTPリダイレクト処理、戻り値セット処理（Ｐ０１Ａ１００）
        # （１）ユーザ、パスワードが正常、つまり認証に成功、かつ活性（有効）の場合、トップページにリダイレクトする。
        # （２）ユーザ、パスワードが異常、つまり認証に失敗、または非活性（無効）の場合、ログインページをレンダリングする。
        # （３）ユーザ、パスワードが異常、つまり認証に失敗、または非活性（無効）の場合、レンダリング関数の戻り値を当該関数の戻り値にセットする。
        # （４）ユーザ、パスワードが異常、つまり認証に失敗、または非活性（無効）の場合、ブラウザにレスポンスを返す。
        # ヒント：処理中にエラーが発生した場合、エラー画面をブラウザに戻す。
        ##########################################
        print_log('[INFO] P01.LoginView関数P01A100', 'INFO')
        # （１）ユーザ、パスワードが正常、つまり認証に成功、かつ活性（有効）の場合、トップページにリダイレクトする。
        # （２）ユーザ、パスワードが異常、つまり認証に失敗、または非活性（無効）の場合、ログインページをレンダリングする。
        # （３）ユーザ、パスワードが異常、つまり認証に失敗、または非活性（無効）の場合、レンダリング関数の戻り値を当該関数の戻り値にセットする。
        # （４）ユーザ、パスワードが異常、つまり認証に失敗、または非活性（無効）の場合、ブラウザにレスポンスを返す。
        try:
            if localUser is not None:
                # 認証に成功した場合、、、
                if localUser.is_active:
                    # ユーザが活性（有効）の場合、、、
                    return HttpResponseRedirect('/file_upload/P02/Top/' + urlquote(str(localAccountModel.ACCOUNT_TYPE)) + '/' + urlquote(str(localAccountModel.ACCOUNT_ID)) + '/' + urlquote(str(localAccountModel.OPERATION_YEAR)))
                else:
                    # ユーザが非活性（無効）の場合、、、
                    return render(request, 'P01LoginTemplate.html', response)
            else:
                # 認証に失敗した場合、、、
                return render(request, 'P01LoginTemplate.html', response)
        except:
            print_log('[ERROR] P01.LoginView関数 P01A100', 'ERROR')
            print_log(sys.exc_info()[0], 'ERROR')
            print_log('[ERROR] P01.LoginView関数で警告が発生しました。', 'ERROR')
            print_log('[ERROR] P01.LoginView関数を警告終了しました。', 'ERROR')
            return render(request, 'error.html')
    except:
        ##########################################
        # 関数全体の例外処理（Ｐ０１Ａ１１０）
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        ##########################################
        # （１）ログ出力関数をコールし、ログファイルにエラーメッセージを出力する。
        print_log('[ERROR] P01.LoginView関数 P01A110', 'ERROR')
        print_log(sys.exc_info()[0], 'ERROR')
        print_log('[ERROR] P01.LoginView関数でエラーが発生しました。', 'ERROR')
        print_log('[ERROR] P01.LoginView関数が異常終了しました。', 'ERROR')
        ##########################################
        # レンダリング処理、戻り値セット処理（Ｐ０１Ａ１２０）
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        ##########################################
        print_log('[ERROR] P01.LoginView関数 P01A120', 'ERROR')
        # （１）レンダリング関数をコールする。
        # （２）レンダリング関数の戻り値をブラウザへの戻り値にセットする。
        return render(request, 'error.html')
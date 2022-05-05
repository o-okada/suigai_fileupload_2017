#####################################################################################
# ファイル名：urls.py
#####################################################################################

#####################################################################################
# 処理名：インポート処理（０２０）
# 処理概要：ジャンゴモジュールをインポートする。
#####################################################################################
from django.conf.urls import url
#####################################################################################
# 処理名：インポート処理（０３０）
# 処理概要：file_uploadモジュールをインポートする。
# Eclipseに該当するViewファイルを開いていない場合、エラーが表示されることがある。
# この場合、Eclipseで該当するViewファイルを開き、エラーが再現しない（消える）ことを確認すること。
#####################################################################################
from file_upload.P01.LoginView import *                    # ログインページ
from file_upload.P02.TopView import *                      # トップページ
from file_upload.P03.InfoDetailView import *               # お知らせ詳細ページ
from file_upload.P10.UploadListView import *               # 調査結果一覧または確認結果一覧ページ
from file_upload.P11.UploadDetailView import *             # 調査結果詳細または確認結果詳細ページ
from file_upload.P12.UploadAddView import *                # 調査結果登録または確認結果登録ページ
from file_upload.P13.UploadAddConfirmView import *         # 調査結果登録確認または確認結果登録確認ページ
from file_upload.P15.UploadDeleteConfirmView import *      # 調査結果削除確認または確認結果削除確認ページ
from file_upload.P25.QuestionReceiveListView import *      # 問合せ受信一覧または回答受信一覧ページ
from file_upload.P25.QuestionSendListView import *         # 問合せ送信一覧または回答送信一覧ページ
from file_upload.P26.QuestionDetailView import *           # 問合せまたは回答詳細ページ
from file_upload.P27.QuestionAddView import *              # 問合せまたは回答送信ページ
from file_upload.P28.QuestionAddConfirmView import *       # 問合せまたは回答送信確認ページ
from file_upload.P40.FaqListView import *                  # FAQ一覧ページ
from file_upload.P41.FaqDetailView import *                # FAQ詳細ページ
from file_upload.P42.RdfView import *                      # RDFページ
###from file_upload.P42.RssListView import *               # RSS一覧ページ
###from file_upload.P42.RssDetailView import *             # RSS詳細ページ
from file_upload.P99.LinkListView import *                 # リンク一覧ページ
from file_upload.pageNotFound import pageNotFound          # ページが存在しない場合に表示するページ 
#####################################################################################
# 処理名：変数セット処理
# 変数概要：URL、VIEW関数、URL名前空間内でのURL名前との対応関係をグローバル変数にセットする。
# ※http://127.0.0.1:8000/file_upload
# 第1要素：URL Pattern
# 第2要素：View関数
# 第3要素：URL名前空間内でのURL名前
# 例：テンプレートではfile_upload:UploadListUrlでURLパターンを参照できる。
#####################################################################################

##########################################
# ログイン画面（Ｐ０１）
##########################################
urlpatterns = []
urlpatterns = urlpatterns + [url(r'^'                           + '$', LoginView, name='LoginUrl'), ]                                                                                                                                                                                                              # ログインページ
urlpatterns = urlpatterns + [url(r'^'                           + '/$', LoginView, name='LoginUrl'), ]                                                                                                                                                                                                             # ログインページ
urlpatterns = urlpatterns + [url(r'^P01/Login'                  + '$', LoginView, name='LoginUrl'), ]                                                                                                                                                                                                              # ログインページ
urlpatterns = urlpatterns + [url(r'^P01/Login'                  + '/$', LoginView, name='LoginUrl'), ]                                                                                                                                                                                                             # ログインページ
##########################################
# トップページ、お知らせ画面（Ｐ０２）
##########################################
urlpatterns = urlpatterns + [url(r'^P02/Top'                    + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)$', TopView, name='TopUrl'), ]                                                                                                                                                   # トップページ
urlpatterns = urlpatterns + [url(r'^P03/InfoDetail'             + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<infoId>\d+)$', InfoDetailView, name='InfoDetailUrl'), ]                                                                                                                     # お知らせ詳細ページ
##########################################
# アップロードデータ、アップロードファイルデータ関連画面（Ｐ１０）
##########################################
urlpatterns = urlpatterns + [url(r'^P10/UploadList'             + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<filterAccount>\w+)$', UploadListView, name='UploadListUrl'), ]                                                                                                              # 調査結果一覧または確認結果一覧ページ
urlpatterns = urlpatterns + [url(r'^P11/UploadDetail'           + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<kenUploadId>\d+)/(?P<honUploadId>\d+)/(?P<kenHonOpeFlag>\d+)$', UploadDetailView, name='UploadDetailUrl'), ]                                                                # 調査結果詳細または確認結果詳細ページ
urlpatterns = urlpatterns + [url(r'^P11/UploadDownload'         + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<kenUploadFileId>\d+)/(?P<honUploadFileId>\d+)/(?P<kenHonOpeFlag>\d+)$', UploadDownloadView, name='UploadDownloadUrl'), ]                                                    # 調査結果詳細または確認結果詳細ページ
urlpatterns = urlpatterns + [url(r'^P12/UploadAdd'              + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<kenUploadId>\d+)/(?P<honUploadId>\d+)/(?P<kenHonOpeFlag>\d+)$', UploadAddView, name='UploadAddUrl'), ]                                                                      # 調査結果登録または確認結果登録ページ
urlpatterns = urlpatterns + [url(r'^P12/UploadAdd.do'           + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<kenUploadId>\d+)/(?P<honUploadId>\d+)/(?P<kenHonOpeFlag>\d+)$', UploadAddDoView, name='UploadAddDoUrl'), ]                                                                  # 調査結果登録または確認結果登録ページ
urlpatterns = urlpatterns + [url(r'^P13/UploadAddConfirm'       + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<kenUploadId>\d+)/(?P<honUploadId>\d+)/(?P<kenHonOpeFlag>\d+)$', UploadAddConfirmView, name='UploadAddConfirmUrl'), ]                                                        # 調査結果登録確認または確認結果登録確認ページ
urlpatterns = urlpatterns + [url(r'^P13/UploadAddConfirm.do'    + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<kenUploadId>\d+)/(?P<honUploadId>\d+)/(?P<kenHonOpeFlag>\d+)$', UploadAddConfirmDoView, name='UploadAddConfirmDoUrl'), ]                                                    # 調査結果登録確認または確認結果登録確認ページ
urlpatterns = urlpatterns + [url(r'^P15/UploadDeleteConfirm'    + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<kenUploadId>\d+)/(?P<honUploadId>\d+)/(?P<kenHonOpeFlag>\d+)$', UploadDeleteConfirmView, name='UploadDeleteConfirmUrl'), ]                                                  # 調査結果削除確認または確認結果削除確認ページ
urlpatterns = urlpatterns + [url(r'^P15/UploadDeleteConfirm.do' + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<kenUploadId>\d+)/(?P<honUploadId>\d+)/(?P<kenHonOpeFlag>\d+)$', UploadDeleteConfirmDoView, name='UploadDeleteConfirmDoUrl'), ]                                              # 調査結果削除確認または確認結果削除確認ページ
##########################################
# 問合せデータ、回答データ関連画面（Ｐ２０）
##########################################
urlpatterns = urlpatterns + [url(r'^P25/QuestionSendList'       + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<filterAccount>\w+)/(?P<filterRead>\d+)$', QuestionSendListView, name='QuestionSendListUrl'), ]                                                                              # 問合せ回答送信トレイ
urlpatterns = urlpatterns + [url(r'^P25/QuestionReceiveList'    + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<filterAccount>\w+)/(?P<filterRead>\d+)$', QuestionReceiveListView, name='QuestionReceiveListUrl'), ]                                                                        # 問合せ回答受信トレイ
urlpatterns = urlpatterns + [url(r'^P26/QuestionDetail'         + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<questionId>\d+)/(?P<fromAccountId>\w+)/(?P<toAccountId>[a-zA-Z0-9_,]+)$', QuestionDetailView, name='QuestionDetailUrl'), ]                                                  # 問合せ回答詳細ページ
urlpatterns = urlpatterns + [url(r'^P26/QuestionDownload'       + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<questionId>\d+)/(?P<fromAccountId>\w+)/(?P<toAccountId>[a-zA-Z0-9_,]+)$', QuestionDownloadView, name='QuestionDownloadUrl'), ]                                              # 問合せ回答ファイルダウンロードページ
urlpatterns = urlpatterns + [url(r'^P27/QuestionAdd'            + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<questionId>\d+)/(?P<fromAccountId>\w+)/(?P<toAccountId>[a-zA-Z0-9_,]+)$', QuestionAddView, name='QuestionAddUrl'), ]                                                        # 問合せ回答登録ページ
urlpatterns = urlpatterns + [url(r'^P27/QuestionAdd.do'         + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<questionId>\d+)/(?P<fromAccountId>\w+)/(?P<toAccountId>[a-zA-Z0-9_,]+)$', QuestionAddDoView, name='QuestionAddDoUrl'), ]                                                    # 問合せ回答登録ページ
urlpatterns = urlpatterns + [url(r'^P28/QuestionAddConfirm'     + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<questionId>[a-zA-Z0-9_,]+)/(?P<fromAccountId>\w+)/(?P<toAccountId>[a-zA-Z0-9_,]+)$', QuestionAddConfirmView, name='QuestionAddConfirmUrl'), ]                               # 問合せ回答登録確認ページ
urlpatterns = urlpatterns + [url(r'^P28/QuestionAddConfirm.do'  + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<questionId>[a-zA-Z0-9_,]+)/(?P<fromAccountId>\w+)/(?P<toAccountId>[a-zA-Z0-9_,]+)$', QuestionAddConfirmDoView, name='QuestionAddConfirmDoUrl'), ]                           # 問合せ回答登録確認ページ
##########################################
# ＦＡＱ画面（Ｐ４０）
##########################################
urlpatterns = urlpatterns + [url(r'^P40/FaqList'                + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)$', FaqListView, name='FaqListUrl'), ]                                                                                                                                           # Faq一覧ページ
urlpatterns = urlpatterns + [url(r'^P41/FaqDetail'              + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)/(?P<faqId>\d+)$', FaqDetailView, name='FaqDetailUrl'), ]                                                                                                                        # Faq詳細ページ
##########################################
# ＲＳＳ画面（Ｐ４２）
# ＲＳＳ：Rich Site Summaryの略
# ＲＤＦ：Resource Description Frameworkの略
# ヒント：rss/Rdfのページでは、購読、RDFのitemの一覧を表示する。
# ヒント：これはLivebookmark等に表示されるメニューの一覧になる。
# ヒント：このページはLivebookmark等からアクセスされるため、ログインなしで閲覧可能とする。
# ヒント：個々の記事は、ログイン済ページへの直接リンクとする。
# ヒント：つまり、ブラウザでURLを指定しても、一度、ログイン画面にリダイレクトされ、ログイン後、目的のページが表示されるものとする。
##########################################
urlpatterns = urlpatterns + [url(r'^rss/Rdf'                    + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)$', RdfView, name='RdfUrl'), ]                                                                                                                                                   # RDFのページ
###urlpatterns = urlpatterns + [url(r'^rss/feed.xml'            + '$', RssListView, name='RssListUrl'), ]                                                                                                                                                                                                          # RSS一覧のページ
###urlpatterns = urlpatterns + [url(r'^rss/feed'                + '/(?P<rssId>\d+)$', RssDetailView, name='RssDetailUrl'), ]                                                                                                                                                                                       # RSS詳細のページ
##########################################
# リンク画面（Ｐ９９）
##########################################
urlpatterns = urlpatterns + [url(r'^P99/LinkList'               + '/(?P<accountType>\d+)/(?P<accountId>\w+)/(?P<operationYear>\d+)$', LinkListView, name='LinkListlUrl'), ]                                                                                                                                        # リンク一覧ページ
##########################################
# 共通画面
##########################################
urlpatterns = urlpatterns + [url(''                             + '', pageNotFound, name='pageNotFound'), ]                                                                                                                                                                                                        # ページが存在しない場合に表示するページ

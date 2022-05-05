#####################################################################################
# JOB_ADD_RSS
# ファイル名：JOB_ADD_RSS.py
# ユースケース：アクセスログテーブルからお知らせの登録、調査結果または確認結果の登録、問合せまたは回答の登録を検索し、
# ユースケース：ＲＳＳテーブルに追加する。
# ヒント：sqlite3版
# ヒント：postgresql版は別途作成する。
# ヒント：アカウントＩＤ毎の日毎、データ種別毎の集計結果を計算しRSSテーブルに登録する。
# ヒント：P42RdfView関数では、ログインした担当者が閲覧すべきか否かを判別可能とするために、その担当者が閲覧すべき日毎、データ種別毎のデータの件数をRSSとして表示する。
#####################################################################################

#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：パイソンモジュールをインポートする。
# sys
#####################################################################################
import os
import sys                                                 # sysモジュール     
from collections import namedtuple                         # namedtupleモジュール
from datetime import datetime                              # datetimeモジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：ジャンゴモジュールをインポートする。
#####################################################################################
from django.contrib.auth.decorators import login_required  # ログイン制御モジュール
from django.db import connection                           # ＤＢ接続モジュール
from django.db import transaction                          # ＤＢトランザクション管理モジュール
#####################################################################################
# 処理名：インポート処理（０００）
# 処理概要：file_uploadモジュールをインポートする。
#####################################################################################
from file_upload.CommonFunction import print_log           # ログ出力モジュール
from file_upload.models import AccountModel                # アカウントデータモデル
from file_upload.models import RssModel                    # RSSデータモデル
from _pydecimal import local
#####################################################################################
# 処理名：大域変数定義（０００）
# 処理概要：大域変数を定義する。
#####################################################################################
def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
#####################################################################################
# 処理名：各種初期化処理（０００）
# ベースディレクトリ、データベースの接続情報をセットする。 
#####################################################################################
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#####################################################################################
# 処理名：グローバル変数セット処理（１０）
#####################################################################################
globalAccountArray = None                                  # アカウント一覧を格納するためのＤＢアクセス用のデータオブジェクト
globalOperationYear = None                                 # 業務実施年　例　2016
globalCountDate = None                                     # お知らせ、調査結果、問合せカウント対象年月日（＝今日） 
globalAddDate = None                                       # ＲＳＳ登録年月日（＝今日）
#####################################################################################
# 処理名：ＡＡＡ処理（１０）
# 業務実施年を計算し、グローバル変数のglobalOperationYearにセットする。
# （１）局所変数の業務実施年等に初期値をセットする。
# （２）ＤＢにアクセスし、業務実施年の最大値を取得する。
# （３）グローバル変数の業務実施年に値をセットする。
#####################################################################################
def GetOperationYearFromDB():
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] GetOperationYearFromDB関数が開始しました。', 'INFO')
        ##########################################
        # （１）局所変数の業務実施年等に初期値をセットする。
        ##########################################
        localAccountModel = None                           # 業務実施年を計算するためのＤＢアクセス用のデータオブジェクト
        ##########################################
        # （２）ＤＢにアクセスし、業務実施年の最大値を取得する。
        ##########################################
        try:
            localAccountModel = AccountModel.objects.raw("""
                SELECT
                    MAX(OPERATION_YEAR) AS OPERATION_YEAR
                FROM
                    FILE_UPLOAD_ACCOUNT
                LIMIT 1    
                """,
                )[0]
        except:
            localAccountModel = None
        finally:
            pass
        ##########################################
        # （３）局所変数のカレントの業務実施年に値をセットする。
        ##########################################
        if localAccountModel != None:
            # アカウントモデルに値がセットされている場合、、、
            globalOperationYear = localAccountModel.OPERATION_YEAR
        else:
            # アカウントモデルに値がセットされていない場合、、、
            globalOperationYear = "2016"
        ##########################################    
        # （４）関数を抜け、呼び出し元に戻り値を戻す。
        ##########################################    
        return True
    except:
        return False   
#####################################################################################
# 処理名：ＢＢＢ処理（２０）
# アカウントＩＤの一覧を取得し、グローバル変数のglobalAccountArrayにセットする。
# （１）アカウントＩＤの一覧を格納するための大域変数のglobalAccountArrayに初期値をセットする。
# （２）ＤＢにアクセスし、アカウントＩＤの一覧を取得し、大域変数のglobalAccountArrayにセットする。    
# （３）関数を抜け、呼び出し元に戻り値を戻す。
# ヒント：これは、アカウントＩＤで最も外側のループを形成するため。
#####################################################################################
def GetAccountArrayFromDB():
    try: 
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] GetAccountArrayFromDB関数が開始しました。', 'INFO')
        ##########################################    
        # （１）アカウントＩＤの一覧を格納するための大域変数のglobalAccountArrayに初期値をセットする。
        ##########################################    
        globalAccountArray = None                          # アカウント一覧を格納するためのＤＢアクセス用のデータオブジェクト
        ##########################################    
        # （２）ＤＢにアクセスし、アカウントＩＤの一覧を取得し、大域変数のglobalAccountArrayにセットする。    
        ##########################################    
        try:
            globalAccountArray = AccountModel.objects.raw("""
                SELECT 
                    ACCOUNT_ID, 
                    ACCOUNT_TYPE 
                FROM
                    FILE_UPLOAD_ACCOUNT
                WHERE
                    OPERATION_YEAR=%s    
                ORDER BY 
                    ACCOUNT_TYPE,
                    ACCOUNT_ID    
                """,
                [ globalOperationYear, ])
        except:
            globalAccountArray = None    
        finally:
            pass
        ##########################################    
        # （３）関数を抜け、呼び出し元に戻り値を戻す。
        ##########################################    
        return True
    except:
        return False
#####################################################################################
# 処理名：ＣＣＣ処理（３０）
# （１）データ件数を集計する年月日（今日）を局所変数にセットする。
# （２）ＲＳＳ登録年月日を局所変数にセットする。
# （３）関数を抜け、呼び出し元に戻り値を戻す。
#####################################################################################
def SetDate():
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] SetDate関数が開始しました。', 'INFO')
        ##########################################    
        # （１）データ件数をカウントする年月日（＝今日）を大域変数にセットする。
        ##########################################    
        globalCountDate = datetime.now().strftime("%Y/%m/%d")
        ##########################################    
        # （２）ＲＳＳ登録年月日（＝今日）を大域変数にセットする。
        ##########################################    
        globalAddDate = datetime.now().strftime("%Y/%m/%d")
        ##########################################    
        # （３）関数を抜け、呼び出し元に戻り値を戻す。
        ##########################################    
        return True
    except:
        ##########################################    
        # （４）エラーが発生した場合、関数を抜け、呼び出し元に戻り値を戻す。
        ##########################################    
        return False
#####################################################################################
# 処理名：ＤＤＤ処理（４０）
# お知らせテーブルから、今日登録されたデータの件数を取得する。
# （１）局所変数のＤＢアクセス用カーソルに値をセットする。（＝ＤＢに接続する）
# （２）お知らせテーブルからカウント対象年月日のデータの件数を取得する。
# （３）ＲＳＳテーブルにInsert、またはUpdateするかの判定を行う。
# （４）ＲＳＳテーブルにカウント対象年月日（＝今日）のお知らせの登録件数を登録する。
# （５）処理が正常に終了したため、コミットする。
# （６）エラーが発生した場合、ロールバックする。
# （７）正常終了、エラー発生のいずれの場合でも、以降の処理に影響を与えないため、カーソルを閉じる。
# ヒント：このままだとRSSに膨大なデータが蓄積され、ライブブックマークも閲覧できなくなる。
# ヒント：RSSにデータは蓄積するが、定期的に過去データを削除する。
# ヒント：また、RSSには過去７日分のみ表示するなどとすることにより問題を回避する。
# ヒント：お知らせは全アカウント共通のため、アカウントＩＤでループしないで処理する。
#####################################################################################
def SetInfoCountToDB():
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] SetInfoCountToDB関数が開始しました。', 'INFO')
        ##########################################
        # （１）局所変数のＤＢアクセス用カーソルに値をセットする。（＝ＤＢに接続する）
        ##########################################
        localCursor = connection.cursor()
        ##########################################
        # （２）お知らせテーブルからカウント対象年月日（＝今日）のデータの件数を取得する。
        ##########################################
        localCursor.execute("""
            SELECT 
                COUNT(1) AS INFO_DATA_COUNT
            FROM
                FILE_UPLOAD_INFO
            WHERE 
                ADD_DATE_TIME=%s AND
                OPERATION_YEAR=%s   
            """,
            [ globalCountDate, 
              globalOperationYear, 
            ])
        localInfoResults = namedtuplefetchall(localCursor)
        localInfoCount = str(localInfoResults[0].INFO_DATA_COUNT)
        ##########################################
        # （３）ＲＳＳテーブルにInsert、またはUpdateするかの判定を行う。
        # ヒント：カウント対象年月日（＝今日）のお知らせのＲＳＳの件数をカウントする。
        ##########################################
        localCursor.execute("""
            SELECT
                COUNT(1) AS RSS_DATA_COUNT
            FROM
                FILE_UPLOAD_RSS
            WHERE
                ADD_DATE_TIME=%s AND
                OPERATION_YEAR=%s AND
                VIEW_NAME=%s    
            """,
            [ globalCountDate,
              globalOperationYear,
              'InfoDetailView', ])
        localRssResults = namedtuplefetchall(localCursor)
        localRssCount = str(localRssResults[0].RSS_DATA_COUNT)
        ##########################################
        # （４）ＲＳＳテーブルにカウント対象年月日（＝今日）のお知らせの登録件数を登録する。
        ##########################################
        if localRssCount == "0":
            # カウント対象年月日（＝今日）のお知らせの登録件数が０件の場合、、、
            # ヒント：INSERTする。
            for i in range(0, len(list(globalAccountArray)) - 1):
                localCursor.execute("""
                    INSERT INTO FILE_UPLOAD_RSS (
                        id,
                        OPERATION_YEAR,
                        FLOOD_YEAR,
                        ABOUT,
                        TITLE,
                        DESCRIPTION,
                        ADD_DATE,
                        COUNT_DATE,
                        VIEW_NAME,
                        ACCOUNT_ID,
                        DATA_COUNT
                    ) VALUES (
                        (SELECT MAX(id + 1) FROM FILE_UPLOAD_RSS),
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
                    [ globalOperationYear,
                      globalOperationYear,
                      'http://127.0.0.1:8000/file_upload/P02/TopPage/',
                      '新規お知らせ登録のお知らせ',
                      '新規お知らせ登録のお知らせ',
                      globalAddDate,
                      globalCountDate,
                      'InfoDetailView',
                      globalAccountArray[i].ACCOUNT_ID,
                      localInfoCount, 
                    ])
        else:
            # カウント対象年月日（＝今日）のお知らせの登録件数が１件以上の場合、、、
            # ヒント：UPDATEする。
            # ヒント：全アカウントで同じ値をセットするため、WHERE句にACCOUNT_IDをセットしない。（ACCOUNT_IDで対象レコードを絞り込まない）
            localCursor.execute("""
                UPDATE FILE_UPLOAD_RSS 
                SET
                    DATA_COUNT=%s
                WHERE
                    OPERATION_YEAR=%s AND
                    ADD_DATE=%s AND
                    COUNT_DATE=%s AND
                    VIEW_NAME=%s
                """,
                [ localInfoCount,
                  globalOperationYear,
                  globalAddDate,
                  globalCountDate,
                  'InfoDetailView',
                ])
        ##########################################    
        # （５）処理が正常に終了したため、コミットする。
        ##########################################
        localCursor.commit()
        localReturn = True
    except:
        ##########################################
        # （６）エラーが発生した場合、ロールバックする。
        ##########################################
        localCursor.rollback()
        localReturn = False
    finally:
        ##########################################
        # （７）正常終了、エラー発生のいずれの場合でも、以降の処理に影響を与えないため、カーソルを閉じる。
        ##########################################
        localCursor.close()
        return localReturn   
#####################################################################################
# 処理名：ＥＥＥ処理（５０）
# 調査結果または確認結果テーブルから、今日登録されたデータの件数を取得する。
# （１）局所変数のＤＢアクセス用カーソルに値をセットする。（＝ＤＢに接続する）
# （２）ＲＳＳテーブルにInsert、またはUpdateするかの判定を行う。
# （３）アカウント数分ループする。
# （４）調査結果または確認結果テーブルから、アカウントＩＤ宛にカウント対象年月日（＝今日）のデータの件数を取得する。
# （５）ＲＳＳテーブルにカウント対象年月日（＝今日）の調査結果または確認結果の登録件数を登録する。
# （６）処理が正常に終了したため、コミットする。
# （７）エラーが発生した場合、、ロールバックする。
# （８）正常終了、エラー発生のいずれの場合でも、以降の処理に影響を与えないため、カーソルを閉じる。
#####################################################################################
def SetUploadCountToDB():
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] SetUploadCountToDB関数が開始しました。', 'INFO')
        ##########################################
        # （１）局所変数のＤＢアクセス用カーソルに値をセットする。（＝ＤＢに接続する）
        ##########################################
        localCursor = connection.cursor()
        ##########################################
        # （２）ＲＳＳテーブルにInsert、またはUpdateするかの判定を行う。
        # ヒント：カウント対象年月日（＝今日）のお知らせのＲＳＳの件数をカウントする。
        ##########################################
        localCursor.execute("""
            SELECT
                COUNT(1) AS RSS_DATA_COUNT
            FROM
                FILE_UPLOAD_RSS
            WHERE
                ADD_DATE_TIME=%s AND
                OPERATION_YEAR=%s AND
                VIEW_NAME=%s    
            """,
            [ globalCountDate,
              globalOperationYear,
              'UploadDetailView', ])
        localRssResults = namedtuplefetchall(localCursor)
        localRssCount = str(localRssResults[0].RSS_DATA_COUNT)
        ##########################################
        # （３）アカウント数分ループする。
        ##########################################
        if globalAccountArray != None:
            for i in range(0, len(list(globalAccountArray)) - 1):
                ##########################################
                # （４）調査結果または確認結果テーブルから、アカウントＩＤ毎にカウント対象年月日（＝今日）のデータの件数を取得する。 
                ##########################################
                localCursor.execute("""
                    SELECT 
                        COUNT(1) AS UPLOAD_DATA_COUNT
                    FROM
                        FILE_UPLOAD_UPLOAD
                    WHERE
                        ADD_DATE=%s AND
                        OPERATION_YEAR=%s AND
                        ACCOUNT_ID=%s
                    """,
                    [ globalCountDate,
                      globalOperationYear,
                      globalAccountArray[i].ACCOUNT_ID, 
                    ])
                localUploadResults = namedtuplefetchall(localCursor)
                localUploadCount = str(localUploadResults[0].UPLOAD_DATA_COUNT)
                ##########################################
                # （５）ＲＳＳテーブルにカウント対象年月日（＝今日）の調査結果または確認結果の登録件数を登録する。 
                ##########################################
                if localRssCount == "0":
                    # カウント対象年月日（＝今日）のお知らせの登録件数が０件の場合、、、
                    # ヒント：INSERTする。
                    localCursor.execute("""
                        INSERT INTO FILE_UPLOAD_RSS (
                            id,
                            OPERATION_YEAR,
                            FLOOD_YEAR,
                            ABOUT,
                            TITLE,
                            DESCRIPTION,
                            ADD_DATE,
                            COUNT_DATE,
                            VIEW_NAME,
                            ACCOUNT_ID,
                            DATA_COUNT
                        ) VALUES (
                            (SELECT MAX(id + 1) FROM FILE_UPLOAD_RSS),
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
                        [ globalOperationYear,
                          globalOperationYear,
                          'http://127.0.0.1:8000/file_upload/P10/UploadList/',
                          '新規の調査結果または確認結果登録のお知らせ',
                          '新規の調査結果または確認結果登録のお知らせ',
                          globalAddDate,
                          globalCountDate,
                          'UploadDetailView',
                          globalAccountArray[i].ACCOUNT_ID,
                          localUploadCount,
                        ])
                else:
                    # カウント対象年月日（＝今日）のお知らせの登録件数が１件以上の場合、、、
                    # ヒント：UPDATEする。
                    localCursor.execute("""
                        UPDATE FILE_UPLOAD_RSS
                        SET
                            DATA_COUNT=%s
                        WHERE
                            OPERATION_YEAR=%s AND   
                            ADD_DATE=%s AND
                            COUNT_DATE=%s AND
                            VIEW_NAME=%s 
                        """,
                        [ localUploadCount,
                          globalOperationYear,
                          globalAddDate,
                          globalCountDate,
                          'UploadDetailView',
                        ])
        else:
            pass            
        ##########################################    
        # （６）処理が正常に終了したため、コミットする。
        ##########################################
        localCursor.commit()
        localReturn = True
    except:
        ##########################################
        # （７）エラーが発生した場合、、ロールバックする。
        ##########################################
        localCursor.rollback()
        localReturn = False
    finally:
        ##########################################
        # （８）正常終了、エラー発生のいずれの場合でも、以降の処理に影響を与えないため、カーソルを閉じる。
        ##########################################
        localCursor.close()
        return localReturn
#####################################################################################
# 処理名：ＦＦＦ処理（６０）
# 問合せまたは回答テーブルから、今日登録されたデータの件数を取得する。
# （１）局所変数のＤＢアクセス用カーソルに値をセットする。（＝ＤＢに接続する）
# （２）ＲＳＳテーブルにInsert、またはUpdateするかの判定を行う。
# （３）アカウント数分ループする。
# （４）調査結果または確認結果テーブルから、アカウントＩＤ宛にカウント対象年月日（＝今日）のデータの件数を取得する。
# （５）ＲＳＳテーブルにカウント対象年月日（＝今日）の調査結果または確認結果の登録件数を登録する。
# （６）処理が正常に終了したため、コミットする。
# （７）エラーが発生した場合、、ロールバックする。
# （８）正常終了、エラー発生のいずれの場合でも、以降の処理に影響を与えないため、カーソルを閉じる。
#####################################################################################
def SetQuestionCountToDB():
    try:
        print_log('[INFO] ##########################################', 'INFO')
        print_log('[INFO] SetQuestionCountToDB関数が開始しました。', 'INFO')
        ##########################################
        # （１）局所変数のＤＢアクセス用カーソルに値をセットする。（＝ＤＢに接続する）
        ##########################################
        localCursor = connection.cursor()
        ##########################################
        # （２）ＲＳＳテーブルにInsert、またはUpdateするかの判定を行う。
        # ヒント：カウント対象年月日（＝今日）のお知らせのＲＳＳの件数をカウントする。
        ##########################################
        localCursor.execute("""
            SELECT
                COUNT(1) AS RSS_DATA_COUNT
            FROM
                FILE_UPLOAD_RSS
            WHERE
                ADD_DATE_TIME=%s AND
                OPERATION_YEAR=%s AND
                VIEW_NAME=%s    
            """,
            [ globalCountDate,
              globalOperationYear,
              'QuestionDetailView', ])
        localRssResults = namedtuplefetchall(localCursor)
        localRssCount = str(localRssResults[0].RSS_DATA_COUNT)
        ##########################################
        # （３）アカウント数分ループする。
        ##########################################
        if globalAccountArray != None:
            for i in range(0, len(list(globalAccountArray)) - 1):
                ##########################################
                # （４）問合せまたは回答テーブルから、アカウントＩＤ毎にカウント対象年月日（＝今日）のデータの件数を取得する。 
                ##########################################
                localCursor.execute("""
                    SELECT 
                        COUNT(1) AS QUESTION_DATA_COUNT
                    FROM
                        FILE_UPLOAD_QUESTION
                    WHERE
                        ADD_DATE=%s AND
                        OPERATION_YEAR=%s AND
                        ACCOUNT_ID=%s
                    """,
                    [ globalCountDate,
                      globalOperationYear,
                      globalAccountArray[i].ACCOUNT_ID, 
                    ])
                localQuestionResults = namedtuplefetchall(localCursor)
                localQuestionCount = str(localQuestionResults[0].QUESTION_DATA_COUNT)
                ##########################################
                # （５）ＲＳＳテーブルにカウント対象年月日（＝今日）の調査結果または確認結果の登録件数を登録する。 
                ##########################################
                if localRssCount == "0":
                    # カウント対象年月日（＝今日）のお知らせの登録件数が０件の場合、、、
                    # ヒント：INSERTする。
                    localCursor.execute("""
                        INSERT INTO FILE_UPLOAD_RSS (
                            id,
                            OPERATION_YEAR,
                            FLOOD_YEAR,
                            ABOUT,
                            TITLE,
                            DESCRIPTION,
                            ADD_DATE,
                            COUNT_DATE,
                            VIEW_NAME,
                            ACCOUNT_ID,
                            DATA_COUNT
                        ) VALUES (
                            (SELECT MAX(id + 1) FROM FILE_UPLOAD_RSS),
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
                        [ globalOperationYear,
                          globalOperationYear,
                          'http://127.0.0.1:8000/file_upload/P25/QuestionList/',
                          '新規の問合せまたは回答登録のお知らせ',
                          '新規の問合せまたは回答登録のお知らせ',
                          globalAddDate,
                          globalCountDate,
                          'QuestionDetailView',
                          globalAccountArray[i].ACCOUNT_ID,
                          localQuestionCount,
                        ])
                else:
                    # カウント対象年月日（＝今日）のお知らせの登録件数が１件以上の場合、、、
                    # ヒント：UPDATEする。
                    localCursor.execute("""
                        UPDATE FILE_UPLOAD_RSS
                        SET
                            DATA_COUNT=%s
                        WHERE
                            OPERATION_YEAR=%s AND   
                            ADD_DATE=%s AND
                            COUNT_DATE=%s AND
                            VIEW_NAME=%s 
                        """,
                        [ localQuestionCount,
                          globalOperationYear,
                          globalAddDate,
                          globalCountDate,
                          'QuestionDetailView',
                        ])
        else:
            pass            
        ##########################################    
        # （６）処理が正常に終了したため、コミットする。
        ##########################################
        localCursor.commit()
        localReturn = True
    except:
        ##########################################
        # （７）エラーが発生した場合、、ロールバックする。
        ##########################################
        localCursor.rollback()
        localReturn = False
    finally:
        ##########################################
        # （８）正常終了、エラー発生のいずれの場合でも、以降の処理に影響を与えないため、カーソルを閉じる。
        ##########################################
        localCursor.close()
        return localReturn
#####################################################################################
# 処理名：メイン処理（７０）
#####################################################################################
print_log('[INFO] ##########################################', 'INFO')
print_log('[INFO] Main関数が開始しました。', 'INFO')
localReturn = True
##########################################
# （１）業務実施年　例　２０１６　をＤＢから取得し、グローバル変数のglobalOperationYearにセットする。
##########################################
print_log('[INFO] GetOperationYearFromDB関数をコールします。', 'INFO')
localReturn = GetOperationYearFromDB()
if localReturn == True:
    # 関数の戻り値が正常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[INFO] GetOperationYearFromDB関数が正常終了し、制御がメインに戻りました。', 'INFO')
else:
    # 関数の戻り値が異常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[ERROR] GetOperationYearFromDB関数が異常終了し、制御がメインに戻りました。', 'ERROR')
##########################################
# （２）アカウントＩＤとアカウント種別の一覧をＤＢから取得し、グローバル変数のglobalAccountArrayにセットする。
##########################################
print_log('[INFO] GetAccountArrayFromDB関数をコールします。', 'INFO')
localReturn = GetAccountArrayFromDB()
if localReturn == True:
    # 関数の戻り値が正常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[INFO] GetAccountArrayFromDB関数が正常終了し、制御がメインに戻りました。', 'INFO')
else:
    # 関数の戻り値が異常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[ERROR] GetAccountArrayFromDB関数が異常終了し、制御がメインに戻りました。', 'ERROR')
##########################################
# （３）カウント対象年月日（＝今日）、ＲＳＳテーブル登録日（＝今日）を計算し、グローバル変数のglobalCountDate、globalAddDateにセットする。
##########################################
print_log('[INFO] SetDate関数をコールします。', 'INFO')
localReturn = SetDate()
if localReturn == True:
    # 関数の戻り値が正常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[INFO] SetDate関数が正常終了し、制御がメインに戻りました。', 'INFO')
else:
    # 関数の戻り値が異常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[ERROR] SetDate関数が異常終了し、制御がメインに戻りました。', 'ERROR')
##########################################
# （４）お知らせの件数のうち、カウント対象年月日（＝今日）ＤＢに登録された件数を計算し、ＤＢのＲＳＳテーブルに登録する。
##########################################
print_log('[INFO] SetInfoCountToDB関数をコールします。', 'INFO')
localReturn = SetInfoCountToDB()
if localReturn == True:
    # 関数の戻り値が正常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[INFO] SetInfoCountToDB関数が正常終了し、制御がメインに戻りました。', 'INFO')
else:
    # 関数の戻り値が異常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[ERROR] SetInfoCountToDB関数が異常終了し、制御がメインに戻りました。', 'ERROR')
##########################################
# （５）調査結果または確認結果の件数のうち、カウント対象年月日（＝今日）ＤＢに登録された件数を計算し、ＤＢのＲＳＳテーブルに登録する。
##########################################
print_log('[INFO] SetUploadCountToDB関数をコールします。', 'INFO')
localReturn = SetUploadCountToDB()
if localReturn == True:
    # 関数の戻り値が正常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[INFO] SetUploadCountToDB関数が正常終了し、制御がメインに戻りました。', 'INFO')
else:
    # 関数の戻り値が異常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[ERROR] SetUploadCountToDB関数が異常終了し、制御がメインに戻りました。', 'ERROR')
##########################################
# （６）問合せまたは回答の件数のうち、カウント対象年月日（＝今日）ＤＢに登録された件数を計算し、ＤＢのＲＳＳテーブルに登録する。
##########################################
print_log('[INFO] SetQuestionCountToDB関数をコールします。', 'INFO')
localReturn = SetQuestionCountToDB()
if localReturn == True:
    # 関数の戻り値が正常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[INFO] SetQuestionCountToDB関数が正常終了し、制御がメインに戻りました。', 'INFO')
else:
    # 関数の戻り値が異常の場合、、、
    # 初版では、ここでは何もしない。本来はログに出力し、ログもローテートさせる。
    print_log('[ERROR] SetQuestionCountToDB関数が異常終了し、制御がメインに戻りました。', 'ERROR')

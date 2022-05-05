#####################################################################################
# formsモジュール
# ファイル名：forms.py
# ヒント：フォームは、画面毎に定義するものとした。
# ヒント：同じ項目でも画面毎に異なる制限、ウィジェットを使用するケースを想定した。
# ヒント：P01等は画面のコード番号である。
# ヒント：以下では、画面のコード番号順（昇順）に定義した。
# ヒント：初版では制限はほぼ無し、つまりrequired=false等としたが、必要に応じてセットすることを第２版以降で検討する。
#####################################################################################
from django import forms
#####################################################################################
# フォーム名：P11.UploadDetailForm
# 処理概要：調査結果詳細ページまたは確認結果詳細ページ用のフォームを定義する。
# ヒント：UPLOAD_FILE_NAMEのフィールドは、UploadAddFormのときはFileField、それ以外のときはCharFieldである。
# ヒント：これは、ブラウザのファイル選択画面を使用するために、ダミーのボタンを持たせ、Javascriptで処理するようにした苦肉の策を反映したものである。
# ヒント：オンラインファイル登録サイトでは、データをデータ登録者の所属組織の種別毎に分けた。
# ヒント：第２版以降でリファクタリングし、すっきりとさせても良い。
# ヒント：問合せ回答対応サイトでは、データをデータ登録者の所属組織の種別毎には分けなかった。
# ヒント：これは、ビジネスロジックが希薄で、親データ子データの関係などがなくても十分実用性があり、コードもすっきりすると考えたからである。
#####################################################################################
class UploadDetailForm(forms.Form):
    # P11-1
    KEN_UPLOAD_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-2
    KEN_KEN_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-3
    KEN_OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-4
    KEN_FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-6
    KEN_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-7
    KEN_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-8
    KEN_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-9
    KEN_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-10
    KEN_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-11
    KEN_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-12
    KEN_ADD_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-13
    KEN_ADD_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-14
    KEN_ADD_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-15
    KEN_DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-16
    KEN_DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-17
    KEN_DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-18
    KEN_UPLOAD_FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-18
    KEN_UPLOAD_FILE_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-18
    KEN_UPLOAD_FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-19
    KEN_QUESTION_BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5})
    )
    # P11-20
    KEN_QUESTION_TO_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-1
    HON_UPLOAD_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-2
    HON_KEN_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-3
    HON_OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-4
    HON_FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-6
    HON_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-7
    HON_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-8
    HON_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-9
    HON_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-10
    HON_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-11
    HON_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-12
    HON_ADD_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-13
    HON_ADD_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-14
    HON_ADD_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-15
    HON_DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-16
    HON_DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-17
    HON_DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-18
    HON_UPLOAD_FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-18
    HON_UPLOAD_FILE_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-18
    HON_UPLOAD_FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P11-19
    HON_QUESTION_BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5})
    )
    # P11-20
    HON_QUESTION_TO_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )    
#####################################################################################
# フォーム名：P12.UploadAddForm
# 処理概要：調査結果登録ページまたは確認結果登録ページ用のフォームを定義する。
# ヒント：UPLOAD_FILE_NAMEのフィールドは、UploadAddFormのときはFileField、それ以外のときはCharFieldである。
# ヒント：これは、ブラウザのファイル選択画面を使用するために、ダミーのボタンを持たせ、Javascriptで処理するようにした苦肉の策を反映したものである。
#####################################################################################
class UploadAddForm(forms.Form):
    # P12-1
    KEN_UPLOAD_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-2
    KEN_KEN_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-3
    KEN_OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-4
    KEN_FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-6
    KEN_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-7
    KEN_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-8
    KEN_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-9
    KEN_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-10
    KEN_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-11
    KEN_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-12
    KEN_ADD_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-13
    KEN_ADD_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-14
    KEN_ADD_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-15
    KEN_DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-16
    KEN_DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-17
    KEN_DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-18
    KEN_UPLOAD_FILE_NAME = forms.FileField(
        required=False
    )
    # P12-18
    KEN_UPLOAD_FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-18
    KEN_UPLOAD_FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-19
    KEN_QUESTION_BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5})
    )
    # P12-20
    KEN_QUESTION_TO_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-1
    HON_UPLOAD_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-2
    HON_KEN_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-3
    HON_OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-4
    HON_FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-6
    HON_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-7
    HON_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-8
    HON_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-9
    HON_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-10
    HON_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-11
    HON_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-12
    HON_ADD_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-13
    HON_ADD_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-14
    HON_ADD_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-15
    HON_DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-16
    HON_DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-17
    HON_DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-18
    HON_UPLOAD_FILE_NAME = forms.FileField(
        required=False
    )
    # P12-19
    HON_UPLOAD_FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-20
    HON_UPLOAD_FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P12-21
    HON_QUESTION_BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5})
    )
    # P12-12
    HON_QUESTION_TO_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
#####################################################################################
# フォーム名：P13.UploadAddConfirmForm
# 処理概要：調査結果登録確認ページまたは確認結果登録確認ページ用のフォームを定義する。
#####################################################################################
class UploadAddConfirmForm(forms.Form):
    # P13-1
    KEN_UPLOAD_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-2
    KEN_KEN_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-3
    KEN_OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-4
    KEN_FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-6
    KEN_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-7
    KEN_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-8
    KEN_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-9
    KEN_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-10
    KEN_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-11
    KEN_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-12
    KEN_ADD_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-13
    KEN_ADD_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-14
    KEN_ADD_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-15
    KEN_DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-16
    KEN_DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-17
    KEN_DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-18
    KEN_UPLOAD_FILE_NAME = forms.CharField(
        required=False
    )
    # P13-18
    KEN_UPLOAD_FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-18
    KEN_UPLOAD_FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-19
    KEN_QUESTION_BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5})
    )
    # P13-20
    KEN_QUESTION_TO_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-1
    HON_UPLOAD_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-2
    HON_KEN_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-3
    HON_OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-4
    HON_FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-6
    HON_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-7
    HON_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-8
    HON_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-9
    HON_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-10
    HON_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-11
    HON_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-12
    HON_ADD_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-13
    HON_ADD_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-14
    HON_ADD_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-15
    HON_DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-16
    HON_DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-17
    HON_DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-18
    HON_UPLOAD_FILE_NAME = forms.CharField(
        required=False,
    )
    # P13-18
    HON_UPLOAD_FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-18
    HON_UPLOAD_FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P13-19
    HON_QUESTION_BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5})
    )
    # P13-20
    HON_QUESTION_TO_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
#####################################################################################
# フォーム名：P15.UploadDeleteConfirmForm
# 処理概要：調査結果削除確認ページまたは確認結果削除確認ページ用のフォームを定義する。
#####################################################################################
class UploadDeleteConfirmForm(forms.Form):
    # P15-1
    KEN_UPLOAD_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-2
    KEN_KEN_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-3
    KEN_OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-4
    KEN_FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-6
    KEN_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-7
    KEN_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-8
    KEN_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-9
    KEN_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-10
    KEN_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-11
    KEN_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-12
    KEN_ADD_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-13
    KEN_ADD_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-14
    KEN_ADD_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-15
    KEN_DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-16
    KEN_DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-17
    KEN_DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-18
    KEN_UPLOAD_FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-18
    KEN_UPLOAD_FILE_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-18
    KEN_UPLOAD_FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-19
    KEN_QUESTION_BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5})
    )
    # P15-20
    KEN_QUESTION_TO_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-1
    HON_UPLOAD_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-2
    HON_KEN_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-3
    HON_OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-4
    HON_FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-6
    HON_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-7
    HON_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-8
    HON_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-9
    HON_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-10
    HON_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-11
    HON_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-12
    HON_ADD_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-13
    HON_ADD_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-14
    HON_ADD_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-15
    HON_DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-16
    HON_DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-17
    HON_DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-18
    HON_UPLOAD_FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-18
    HON_UPLOAD_FILE_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-18
    HON_UPLOAD_FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P15-19
    HON_QUESTION_BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5})
    )
    # P15-20
    HON_QUESTION_TO_HON_OPE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
#####################################################################################
# フォーム名：P26.QuestionDetailForm
# 処理概要：問合せ回答詳細ページ用のフォームを定義する。
# ヒント：問合せ回答では、データの登録者の組織の種別を示すKEN_HON_OPE_FLAGを使用しない。
# ヒント：メールと同じ扱いとし、誰が登録したデータに誰が確認することができる等のビジネスロジックは実装しない。
#####################################################################################
class QuestionDetailForm(forms.Form):
    # P26-1
    QUESTION_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-3
    OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-4
    FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-5
    SEND_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-6
    SEND_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-7
    SEND_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-8
    SEND_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-9
    SEND_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-10
    SEND_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-11
    SEND_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-12
    SEND_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-13
    SEND_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-14
    SUBJECT = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-15
    BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 10})
    )
    # P26-17
    FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-18
    FILE_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-19
    FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-20
    RECEIVE_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-21
    RECEIVE_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-22
    RECEIVE_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-23
    RECEIVE_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-24
    RECEIVE_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-25
    RECEIVE_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-26
    RECEIVE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-27
    RECEIVE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-28
    RECEIVE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-29
    DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-30
    DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-31
    DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P26-32
    RECEIVE_READ_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
#####################################################################################
# フォーム名：P27.QuestionAddForm
# 処理概要：問合せ回答送信文作成ページ用のフォームを定義する。
# ヒント：問合せ回答では、データの登録者の組織の種別を示すKEN_HON_OPE_FLAGを使用しない。
# ヒント：メールと同じ扱いとし、誰が登録したデータに誰が確認することができる等のビジネスロジックは実装しない。
#####################################################################################
class QuestionAddForm(forms.Form):
    # P27-1
    QUESTION_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-3
    OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-4
    FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-5
    SEND_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-6
    SEND_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-7
    SEND_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-8
    SEND_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-9
    SEND_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-10
    SEND_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-11
    SEND_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-12
    SEND_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-13
    SEND_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-14
    SUBJECT = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-15
    BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 10})
    )
    # P27-17
    FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-18
    FILE_NAME = forms.FileField(
        required=False,
    )
    # P27-19
    FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-20
    RECEIVE_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-21
    RECEIVE_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-22
    RECEIVE_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-23
    RECEIVE_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-24
    RECEIVE_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-25
    RECEIVE_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-26
    RECEIVE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-27
    RECEIVE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-28
    RECEIVE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-29
    DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-30
    DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-31
    DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P27-32
    RECEIVE_READ_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
#####################################################################################
# フォーム名：P28.QuestionAddConfirmForm
# 処理概要：問合せ回答送信確認ページ用のフォームを定義する。
# ヒント：問合せ回答では、データの登録者の組織の種別を示すKEN_HON_OPE_FLAGを使用しない。
# ヒント：メールと同じ扱いとし、誰が登録したデータに誰が確認することができる等のビジネスロジックは実装しない。
#####################################################################################
class QuestionAddConfirmForm(forms.Form):
    # P28-1
    QUESTION_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-3
    OPERATION_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-4
    FLOOD_YEAR = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-5
    SEND_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-6
    SEND_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-7
    SEND_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-8
    SEND_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-9
    SEND_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-10
    SEND_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-11
    SEND_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-12
    SEND_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-13
    SEND_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-14
    SUBJECT = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-15
    BODY = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 10})
    )
    # P28-17
    FILE_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-18
    FILE_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-19
    FILE_PATH = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-20
    RECEIVE_ORG_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-21
    RECEIVE_ORG_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-22
    RECEIVE_DEPT_CODE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-23
    RECEIVE_DEPT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-24
    RECEIVE_ACCOUNT_ID = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-25
    RECEIVE_ACCOUNT_NAME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-26
    RECEIVE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-27
    RECEIVE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-28
    RECEIVE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-29
    DELETE_DATE = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-30
    DELETE_DATE_TIME = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-31
    DELETE_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )
    # P28-32
    RECEIVE_READ_FLAG = forms.CharField(
        required=False,
        widget=forms.TextInput()
    )

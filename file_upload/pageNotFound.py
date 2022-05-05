import logging

from django.shortcuts import render # 追加する
from django.http.response import HttpResponse

def pageNotFound(request):
    return render(request, 'pageNotFound.html')
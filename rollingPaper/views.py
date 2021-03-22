from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, DetailView
from .models import Board, Post
import hashlib
import os

def main(request) :
    if request.session.get('sign_complete', False):
        del request.session['sign_complete']
    return render(request, 'rollingPaper/main.html', {'view':"main"})

class signView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'rollingPaper/formBoard.html', {'view':"sign"})

    def post(self, request):
        _salt = os.urandom(16)
        hashedPw = hashlib.pbkdf2_hmac('sha256', request.POST['pwBoard'].encode(),_salt, 100000)
        data = Board.objects.create(board_name=request.POST['txtName'], hashed_pw=hashedPw, salt=_salt)
        data.save()
        request.session['sign_complete'] = data.pk
        return redirect('/'+str(data.pk))

class listView(View):
    def get(self, request, *args, **kwargs):
        sql = Board.objects.filter(id=self.kwargs['pk'])
        try:
            sql.get()
        except:
            return redirect("/?msg=방번호를 확인해주세요.")

        if request.session.get('sign_complete', False) != self.kwargs['pk']:
            return render(request, "rollingPaper/sign.html", {'view':"list"})
        else:
            post = Post.objects.filter(board_id=self.kwargs['pk'])
            return render(request, "rollingPaper/list.html", {'view':"list", 'board_name':sql.first().board_name, 'post':post})

    def post(self, request, *args, **kwargs):

        sql = Board.objects.filter(id=self.kwargs['pk'])
        try:
            sql.get()
            infoBoard = sql.first()
            _salt = infoBoard.salt
            hashedPw = hashlib.pbkdf2_hmac('sha256', request.POST['pwBoard'].encode(), _salt, 100000)
            if infoBoard.hashed_pw == hashedPw :
                request.session['sign_complete'] = self.kwargs['pk']
            else :
                raise Exception('비밀번호가 틀렸습니다.')
        except:
            print("error")
            return render(request, "rollingPaper/sign.html", {'view':"sign", 'msg':"비밀번호가 틀렸습니다."})
        return redirect('./')

def createBoard(request) :
    # return redirect('../sign')
    return redirect('rollingPaper:sign')
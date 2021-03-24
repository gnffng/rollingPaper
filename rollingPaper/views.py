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
        if request.session.get('master', False):
            del request.session['master']
        del request.session['board_name']
    return render(request, 'rollingPaper/main.html', {'view':"main"})

class signView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'rollingPaper/formBoard.html', {'view':"sign"})

    def post(self, request):
        _salt = os.urandom(16)
        hashedPw = hashlib.pbkdf2_hmac('sha256', request.POST['pwBoard'].encode(),_salt, 100000)
        masterPw = hashlib.pbkdf2_hmac('sha256', request.POST['masterPw'].encode(), _salt, 100000)

        data = Board.objects.create(
            board_name=request.POST['txtName'],
            hashed_pw=hashedPw,
            master_pw=masterPw,
            salt=_salt
        )
        data.save()

        request.session['sign_complete'] = data.pk
        request.session['board_name'] = data.board_name

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
            return render(request, "rollingPaper/list.html", {'view':"list", 'board_name':request.session.get('board_name', False), 'post':post})

    def post(self, request, *args, **kwargs):

        sql = Board.objects.filter(id=self.kwargs['pk'])
        try:
            sql.get()
            infoBoard = sql.first()
            _salt = infoBoard.salt
            hashedPw = hashlib.pbkdf2_hmac('sha256', request.POST['pwBoard'].encode(), _salt, 100000)

            if infoBoard.master_pw == hashedPw :
                request.session['sign_complete'] = self.kwargs['pk']
                request.session['master'] = True
                request.session['board_name'] = infoBoard.board_name
            elif infoBoard.hashed_pw == hashedPw :
                request.session['sign_complete'] = self.kwargs['pk']
                request.session['board_name'] = infoBoard.board_name
            else :
                raise Exception('비밀번호가 틀렸습니다.')
        except:
            print("error")
            return render(request, "rollingPaper/sign.html", {'view':"sign", 'msg':"비밀번호가 틀렸습니다."})
        return redirect('./')


class writeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "rollingPaper/write.html", {'view': "write", 'board_name':request.session.get('board_name', False)})

    def post(self, request, *args, **kwargs):
        _salt = os.urandom(16)
        hashedPw = hashlib.pbkdf2_hmac('sha256', request.POST['pwPost'].encode(), _salt, 100000)

        data = Post.objects.create(
            board_id=Board.objects.filter(id=self.kwargs['pk'])[0],
            hashed_pw=hashedPw, salt=_salt,
            contents=request.POST['contents'],
            nickname=request.POST['nickname']
        )

        return redirect('./')

class detailView(View):

    def get(self, request, *args, **kwargs):
        return redirect("./")

    def post(self, request, *args, **kwargs):
        post = Post.objects.filter(board_id=self.kwargs['pk'])
        return render(request, "rollingPaper/detail.html", {'view': "detail", 'post': post, 'goto': request.POST["goto"]})

class deleteView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "rollingPaper/delete.html", {})

    def post(self, request, *args, **kwargs):
        sql = Post.objects.filter(board_id=self.kwargs['fk'], id=self.kwargs['pk'])

        try:
            obj = sql.get()
            infoPost = sql.first()
            _salt = infoPost.salt
            hashedPw = hashlib.pbkdf2_hmac('sha256', request.POST['pwBoard'].encode(), _salt, 100000)

            if infoPost.master_pw == hashedPw :
                obj.delete()
            elif infoPost.hashed_pw == hashedPw :
                obj.delete()
            else :
                raise Exception('비밀번호가 틀렸습니다.')
        except:
            print("error")
            return render(request, ".../", {'view':"sign", 'msg':"비밀번호가 틀렸습니다."})


        return render(request, "rollingPaper/detail.html", {'view': "detail", 'post': post, 'goto': request.POST["goto"]})
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, DetailView
from .models import Board, Post

def main(request) :
    if request.session.get('sign_complete', False):
        del request.session['sign_complete']
    return render(request, 'rollingPaper/main.html', {'view':"main"})

class signView(View):
    def get(self, request):
        return render(request, 'rollingPaper/formBoard.html', {'view':"sign"})

    def post(self, request):
        data = Board.objects.create(board_name=request.POST['txtName'], board_pw=request.POST['pwBoard'])
        data.save()
        request.session['sign_complete'] = data.pk
        return redirect('/'+str(data.pk))

class listView(View):
    def get(self, request, *args, **kwargs):
        if request.session.get('sign_complete', False) != self.kwargs['pk']:
            return render(request, "rollingPaper/sign.html", {'view':"list"})
        else:
            return render(request, "rollingPaper/list.html", {'view':"list"})
        # return render(request, 'rollingPaper/formBoard.html', {})

    def post(self, request, *args, **kwargs):
        sql = Board.objects.filter(id=self.kwargs['pk'], board_pw=request.POST['pwBoard'])
        try:
            sql.get()
            userInfo = sql.first()
            request.session['sign_complete'] = self.kwargs['pk']
        except:
            print("error")
            return render(request, "rollingPaper/sign.html", {'msg':"비밀번호가 틀렸습니다."})
        return redirect('./')

def createBoard(request) :
    # return redirect('../sign')
    return redirect('rollingPaper:sign')
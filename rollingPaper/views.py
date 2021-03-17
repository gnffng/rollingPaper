from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Board, Post

def main(request) :
    return render(request, 'rollingPaper/main.html', {})

class signView(View):
    def post(self, request):
        return render(request, 'rollingPaper/sign.html', {'idBoard' : request.POST['idBoard']})
    def get(self, request):
        return render(request, 'rollingPaper/create.html', {})
from django.db import models
from django import forms

class Board(models.Model):
    board_name = models.CharField(max_length=40)
    board_pw = models.CharField(max_length=40)
    pub_date = models.DateTimeField(auto_now=True)

class Post(models.Model):
    question = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    contents = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now=True)
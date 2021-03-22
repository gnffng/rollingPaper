from django.db import models
from django import forms


class Board(models.Model):
    board_name = models.CharField(max_length=40)
    hashed_pw = models.BinaryField(max_length=32)
    salt = models.BinaryField(max_length=16)
    pub_date = models.DateTimeField(auto_now=True)

class Post(models.Model):
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40, blank=True)
    contents = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now=True)
from django.db import models

class Board(models.Model):
    board_name = models.CharField(max_length=40)
    pub_date = models.DateTimeField('board published')

class Post(models.Model):
    question = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    contents = models.CharField(max_length=300)
    pub_date = models.DateTimeField('board published')
from django.contrib import admin
from rollingPaper.models import *

class BoardAdmin(admin.ModelAdmin):
    list_display=('board_name','hashed_pw','master_pw','salt','pub_date')
    fields=('board_name',)

class PostAdmin(admin.ModelAdmin):
    list_display=('board_id','hashed_pw','nickname','salt','contents','pub_date')
    fields=('board_id','nickname','contents')

admin.site.register(Board, BoardAdmin)
admin.site.register(Post, PostAdmin)

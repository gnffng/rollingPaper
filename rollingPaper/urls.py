from django.urls import path
from . import views

app_name = 'rollingPaper'
urlpatterns = [
    path('', views.main, name='main'),
    path('<int:pk>/', views.listView.as_view(), name='list'),
    path('sign/', views.signView.as_view(), name='sign'),
    path('createBoard/', views.createBoard, name='createBoard'),
]
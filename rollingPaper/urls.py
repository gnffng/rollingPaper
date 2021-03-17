from django.urls import path
from . import views

app_name = 'rollingPaper'
urlpatterns = [
    path('', views.main, name='main'),
    path('sign/', views.signView.as_view(), name='sign'),
]
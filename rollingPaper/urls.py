from django.urls import path
from . import views

app_name = 'rollingPaper'
urlpatterns = [
    path('', views.main, name='main'),
    path('<int:pk>/', views.listView.as_view(), name='list'),
    path('<int:pk>/write/', views.writeView.as_view(), name='write'),
    path('<int:pk>/detail/', views.detailView.as_view(), name='detail'),
    path('<int:fk>/delete/<int:pk>/', views.deleteView.as_view(), name='delete'),
    path('sign/', views.signView.as_view(), name='sign'),
]

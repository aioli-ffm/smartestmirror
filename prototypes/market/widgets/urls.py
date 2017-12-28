from django.urls import path

from . import views

urlpatterns = [
    #path('', WidgetsListView.as_view(), name='widgets-list'),
    path('', views.index, name='index'),
    path('<widget_id>/', views.detail, name='detail'),
    path('download/<widget_id>/', views.download, name='download'),
]
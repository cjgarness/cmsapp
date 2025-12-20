from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('pages/', views.PageListView.as_view(), name='page_list'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
]

from django.urls import path
from . import views

app_name = 'media'

urlpatterns = [
    path('library/', views.MediaLibraryView.as_view(), name='library'),
    path('library/<int:pk>/', views.MediaFileDetailView.as_view(), name='detail'),
]

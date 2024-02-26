from django.urls import path
from .views import PostListView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:id>/', PostListView.as_view(), name='post-detail')
]
from django.urls import path
from .views import (
    SchoolInfoView,
    NewsListView,
    NewsDetailView,
    SchoolStatsView
)

app_name = 'public_info'

urlpatterns = [
    path('school-info/', SchoolInfoView.as_view(), name='school_info'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('stats/', SchoolStatsView.as_view(), name='school_stats'),
]
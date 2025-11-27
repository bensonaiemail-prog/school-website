from django.urls import path
from .views import (
    AnnouncementListView,
    AnnouncementDetailView,
    AnnouncementCreateView,
    AnnouncementUpdateView,
    AnnouncementDeleteView,
    AllAnnouncementsView,
)

app_name = 'announcements'

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='announcement_list'),
    path('all/', AllAnnouncementsView.as_view(), name='all_announcements'),
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement_detail'),
    path('create/', AnnouncementCreateView.as_view(), name='announcement_create'),
    path('<int:pk>/update/', AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement_delete'),
]
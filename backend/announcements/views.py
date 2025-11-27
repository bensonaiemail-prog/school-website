from rest_framework import generics, permissions
from django.utils import timezone
from .models import Announcement
from .serializers import (
    AnnouncementSerializer,
    AnnouncementCreateSerializer,
    AnnouncementListSerializer
)

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class AnnouncementListView(generics.ListAPIView):
    """
    List announcements based on user role
    """
    serializer_class = AnnouncementListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        
        # Base queryset: published and not expired
        queryset = Announcement.objects.filter(
            is_published=True,
            publish_date__lte=now
        )
        
        # Exclude expired announcements
        queryset = queryset.exclude(
            expiry_date__lt=now
        )
        
        # Filter by audience based on user role
        if user.is_admin:
            # Admin sees all announcements
            pass
        elif user.is_teacher:
            queryset = queryset.filter(audience__in=['ALL', 'TEACHERS'])
        elif user.is_parent:
            queryset = queryset.filter(audience__in=['ALL', 'PARENTS'])
        else:
            queryset = queryset.filter(audience='ALL')
        
        return queryset.order_by('-publish_date')


class AnnouncementDetailView(generics.RetrieveAPIView):
    """
    Get single announcement detail
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnnouncementCreateView(generics.CreateAPIView):
    """
    Create announcement (Admin only)
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementCreateSerializer
    permission_classes = [IsAdminUser]


class AnnouncementUpdateView(generics.UpdateAPIView):
    """
    Update announcement (Admin only)
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementCreateSerializer
    permission_classes = [IsAdminUser]


class AnnouncementDeleteView(generics.DestroyAPIView):
    """
    Delete announcement (Admin only)
    """
    queryset = Announcement.objects.all()
    permission_classes = [IsAdminUser]


class AllAnnouncementsView(generics.ListAPIView):
    """
    List all announcements for admin management
    """
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementListSerializer
    permission_classes = [IsAdminUser]
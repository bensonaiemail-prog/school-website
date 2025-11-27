from rest_framework import generics, permissions
from .models import GalleryCategory, GalleryImage
from .serializers import (
    GalleryCategorySerializer,
    GalleryImageSerializer,
    GalleryImageCreateSerializer,
    GalleryImageListSerializer
)

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


# Category Views
class CategoryListView(generics.ListAPIView):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryCreateView(generics.CreateAPIView):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [IsAdminUser]


class CategoryUpdateView(generics.UpdateAPIView):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [IsAdminUser]


class CategoryDeleteView(generics.DestroyAPIView):
    queryset = GalleryCategory.objects.all()
    permission_classes = [IsAdminUser]


# Gallery Image Views
class GalleryListView(generics.ListAPIView):
    """Public gallery view - only published images"""
    serializer_class = GalleryImageListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = GalleryImage.objects.filter(is_published=True)
        
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        
        return queryset.order_by('-event_date', '-created_at')


class GalleryDetailView(generics.RetrieveAPIView):
    queryset = GalleryImage.objects.filter(is_published=True)
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.AllowAny]


class GalleryCreateView(generics.CreateAPIView):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageCreateSerializer
    permission_classes = [IsAdminUser]


class GalleryUpdateView(generics.UpdateAPIView):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageCreateSerializer
    permission_classes = [IsAdminUser]


class GalleryDeleteView(generics.DestroyAPIView):
    queryset = GalleryImage.objects.all()
    permission_classes = [IsAdminUser]


class AllGalleryImagesView(generics.ListAPIView):
    """Admin view - all images including unpublished"""
    queryset = GalleryImage.objects.all().order_by('-created_at')
    serializer_class = GalleryImageListSerializer
    permission_classes = [IsAdminUser]
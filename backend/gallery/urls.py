from django.urls import path
from .views import (
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    GalleryListView,
    GalleryDetailView,
    GalleryCreateView,
    GalleryUpdateView,
    GalleryDeleteView,
    AllGalleryImagesView,
)

app_name = 'gallery'

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # Gallery Images
    path('', GalleryListView.as_view(), name='gallery_list'),
    path('all/', AllGalleryImagesView.as_view(), name='all_gallery'),
    path('<int:pk>/', GalleryDetailView.as_view(), name='gallery_detail'),
    path('create/', GalleryCreateView.as_view(), name='gallery_create'),
    path('<int:pk>/update/', GalleryUpdateView.as_view(), name='gallery_update'),
    path('<int:pk>/delete/', GalleryDeleteView.as_view(), name='gallery_delete'),
]
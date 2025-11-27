from rest_framework import serializers
from .models import GalleryCategory, GalleryImage

class GalleryCategorySerializer(serializers.ModelSerializer):
    image_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryCategory
        fields = '__all__'
    
    def get_image_count(self, obj):
        return obj.images.filter(is_published=True).count()


class GalleryImageSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = GalleryImage
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'created_at']


class GalleryImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        exclude = ['uploaded_by', 'created_at']
    
    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class GalleryImageListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = GalleryImage
        fields = ['id', 'title', 'image', 'category', 'category_name', 
                  'event_date', 'is_published', 'created_at']
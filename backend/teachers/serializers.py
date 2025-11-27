from rest_framework import serializers
from .models import Teacher
from accounts.serializers import UserSerializer

class TeacherPublicSerializer(serializers.ModelSerializer):
    """
    Public teacher information (no sensitive data)
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'full_name', 
                  'qualification', 'specialization', 'experience_years', 
                  'bio', 'profile_image']


class TeacherDetailSerializer(serializers.ModelSerializer):
    """
    Full teacher information (admin only)
    """
    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherCreateSerializer(serializers.ModelSerializer):
    """
    Create teacher profile
    """
    class Meta:
        model = Teacher
        exclude = ['user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Link to the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
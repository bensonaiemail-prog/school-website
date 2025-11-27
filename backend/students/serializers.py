from rest_framework import serializers
from .models import Student

class StudentListSerializer(serializers.ModelSerializer):
    """
    Student list serializer (basic info)
    """
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    parent_name = serializers.CharField(source='parent.get_full_name', read_only=True)
    class_name = serializers.CharField(source='current_class.name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'full_name', 'age', 'gender', 
                  'current_class', 'class_name', 'parent', 'parent_name', 
                  'profile_image', 'is_active']


class StudentDetailSerializer(serializers.ModelSerializer):
    """
    Full student details (parent can see own children, admin/teachers see all)
    """
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    parent_name = serializers.CharField(source='parent.get_full_name', read_only=True)
    class_name = serializers.CharField(source='current_class.name', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'


class StudentCreateSerializer(serializers.ModelSerializer):
    """
    Create student (Parents and Admins)
    """
    class Meta:
        model = Student
        exclude = ['parent', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        request = self.context['request']
        
        # If parent creates, auto-assign to them
        if request.user.role == 'PARENT':
            validated_data['parent'] = request.user
        
        return super().create(validated_data)
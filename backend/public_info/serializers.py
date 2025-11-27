from rest_framework import serializers
from .models import SchoolInfo, News
from students.models import Student
from teachers.models import Teacher

class SchoolInfoSerializer(serializers.ModelSerializer):
    """
    School information serializer
    """
    class Meta:
        model = SchoolInfo
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    """
    News serializer
    """
    class Meta:
        model = News
        fields = '__all__'


class SchoolStatsSerializer(serializers.Serializer):
    """
    School statistics for public view
    """
    total_students = serializers.IntegerField()
    total_teachers = serializers.IntegerField()
    total_classes = serializers.IntegerField()
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SchoolInfo, News
from .serializers import SchoolInfoSerializer, NewsSerializer, SchoolStatsSerializer
from students.models import Student
from teachers.models import Teacher
from classes.models import Class

class SchoolInfoView(generics.RetrieveAPIView):
    """
    Get school information (public)
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = SchoolInfoSerializer
    
    def get_object(self):
        return SchoolInfo.load()


class NewsListView(generics.ListAPIView):
    """
    List published news (public)
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = NewsSerializer
    
    def get_queryset(self):
        return News.objects.filter(is_published=True)


class NewsDetailView(generics.RetrieveAPIView):
    """
    Get single news item (public)
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_published=True)


class SchoolStatsView(APIView):
    """
    Get school statistics (public)
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        stats = {
            'total_students': Student.objects.filter(is_active=True).count(),
            'total_teachers': Teacher.objects.filter(is_active=True).count(),
            'total_classes': Class.objects.count(),
        }
        
        serializer = SchoolStatsSerializer(stats)
        return Response(serializer.data)